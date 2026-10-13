from __future__ import annotations

import json
import os
import re
import time
from dataclasses import dataclass
from typing import Any, Iterator, Literal, TypedDict

from .providers import (
    aggregate_timing as _aggregate_timing,
    aggregate_usage as _aggregate_usage,
    client_for_model,
    extract_json_payload,
    normalize_usage as _normalize_usage,
)


ANSWERER_SYSTEM_PROMPT = """You are the ChemMon wiki assistant.

Your job is to answer questions about EFSA Chemical Monitoring reporting using only the provided wiki pages.

Rules:
- Answer based solely on the provided wiki page content.
- Cite which page each claim comes from using the page filename.
- Only pages marked evidence_kind=full support claims or citations. Related summaries are navigation hints, not evidence.
- Preserve domain scope, exceptions and the distinction between requirements and recommendations. Include source section/page locators when supplied.
- If the wiki pages do not contain enough information to answer the question, say so clearly.
- Do not make up rules or guidance that is not in the provided pages.
- Be concise and direct.

Write the answer as plain text (Markdown lists and code formatting are fine).
After each claim, cite its page filename in parentheses, for example
(page-name.md). Do not wrap the answer in JSON or repeat it.

If you cannot answer from the provided pages, say "The wiki does not cover this topic." and cite nothing.
"""

# Page filenames cited inline, e.g. "(pesticide-reporting.md; other-page.md)".
INLINE_CITATION_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.-]*\.md\b")


def inline_citations(answer: str) -> list[str]:
    """Page filenames mentioned in the answer, in first-mention order.

    The API keeps only those that were supplied as evidence.
    """
    return list(dict.fromkeys(INLINE_CITATION_RE.findall(answer)))


@dataclass(frozen=True)
class AnswerResult:
    answer: str
    citations: list[str]
    token_summary: dict[str, Any]
    timing_summary: dict[str, Any]


class AnswerStreamDelta(TypedDict):
    type: Literal["delta"]
    text: str


class AnswerStreamFinal(TypedDict):
    type: Literal["final"]
    result: AnswerResult


AnswerStreamEvent = AnswerStreamDelta | AnswerStreamFinal




class WikiAnswerer:
    def __init__(
        self,
        *,
        client: Any | None = None,
        model_id: str | None = None,
        model_str: str | None = None,
        max_tokens: int | None = None,
    ):
        if client and model_id:
            self.client = client
            self.model_id = model_id
        else:
            resolved_str = model_str or os.getenv("WIKI_ANSWERER_MODEL", "anthropic/claude-sonnet-5-5")
            self.client, self.model_id = client_for_model(resolved_str)
        self._sonnet55 = self.model_id.split("/")[-1] == "claude-sonnet-5-5"
        # Sonnet 5.5 shares this allowance between adaptive thinking and text.
        self.max_tokens = max_tokens if max_tokens is not None else (8192 if self._sonnet55 else 2000)

    def _retry_budget(self, budget: int) -> int:
        return max(budget, min(budget * 2, 16384)) if self._sonnet55 else budget

    def _build_messages(self, question: str, pages: list[dict[str, Any]]) -> list[dict[str, str]]:
        return [
            {"role": "system", "content": ANSWERER_SYSTEM_PROMPT},
            {
                "role": "user",
                "content": json.dumps(
                    {"question": question, "pages": pages},
                    ensure_ascii=False,
                ),
            },
        ]

    def _parse_answer(self, text: str) -> tuple[str, list[str]]:
        if not text.strip():
            raise RuntimeError("The answer model returned no answer. Please try a narrower question.")
        # Answers are plain text with inline citations. A JSON object with an
        # "answer" field (older prompt, other models, or a trailing copy) wins.
        data = extract_json_payload(text)
        if data and isinstance(data.get("answer"), str):
            answer = data["answer"]
            listed = [c for c in data.get("citations") or [] if isinstance(c, str)]
            return answer, list(dict.fromkeys(listed + inline_citations(answer)))
        answer = text.strip()
        return answer, inline_citations(answer)

    def _build_result(self, answer: str, citations: list[str], usages: list[dict], timings: list[dict], wall_start: float) -> AnswerResult:
        return AnswerResult(
            answer=answer,
            citations=citations,
            token_summary=_aggregate_usage(usages, self.model_id),
            timing_summary={
                **_aggregate_timing(timings),
                "answerer_wall_time_ms": int((time.perf_counter() - wall_start) * 1000),
            },
        )

    def run(self, question: str, pages: list[dict[str, Any]]) -> AnswerResult:
        started = time.perf_counter()
        usages, timings = [], []
        budget = self.max_tokens
        for attempt in range(2):
            call_started = time.perf_counter()
            response = self.client.chat.completions.create(
                model=self.model_id,
                max_tokens=budget,
                messages=self._build_messages(question, pages),
                stream=False,
            )
            finish_reason = response.choices[0].finish_reason if response.choices else None
            usages.append(_normalize_usage(response.usage, finish_reason))
            timings.append({"call_number": attempt + 1, "duration_ms": int((time.perf_counter() - call_started) * 1000), "stop_reason": finish_reason})
            if finish_reason not in {"length", "max_tokens"}:
                break
            retry_budget = self._retry_budget(budget)
            if attempt or retry_budget <= budget:
                raise RuntimeError("The answer exceeded its output limit. Please try a narrower question.")
            budget = retry_budget

        text = response.choices[0].message.content or "" if response.choices else ""
        answer, citations = self._parse_answer(text)
        return self._build_result(answer, citations, usages, timings, started)

    def stream(
        self,
        question: str,
        pages: list[dict[str, Any]],
    ) -> Iterator[AnswerStreamEvent]:
        started = time.perf_counter()
        usages, timings = [], []
        budget = self.max_tokens
        for attempt in range(2):
            accumulated_text = ""
            usage_data: Any = None
            finish_reason: str | None = None
            any_deltas_sent = False
            call_started = time.perf_counter()
            try:
                response_stream = self.client.chat.completions.create(
                    model=self.model_id,
                    max_tokens=budget,
                    messages=self._build_messages(question, pages),
                    stream=True,
                    stream_options={"include_usage": True},
                )
                for chunk in response_stream:
                    if chunk.choices:
                        delta = chunk.choices[0].delta
                        if delta and delta.content:
                            accumulated_text += delta.content
                            any_deltas_sent = True
                            yield {"type": "delta", "text": delta.content}
                        if chunk.choices[0].finish_reason:
                            finish_reason = chunk.choices[0].finish_reason
                    if chunk.usage:
                        usage_data = chunk.usage
            except Exception:
                if any_deltas_sent or usages:
                    raise
                result = self.run(question, pages)
                yield {"type": "delta", "text": result.answer}
                yield {"type": "final", "result": result}
                return

            usages.append(_normalize_usage(usage_data, finish_reason))
            timings.append({"call_number": attempt + 1, "duration_ms": int((time.perf_counter() - call_started) * 1000), "stop_reason": finish_reason})
            if finish_reason not in {"length", "max_tokens"}:
                break
            retry_budget = self._retry_budget(budget)
            # Once visible text has been sent, retrying would concatenate two
            # different answers. Let the endpoint send an SSE error, never done.
            if any_deltas_sent or attempt or retry_budget <= budget:
                raise RuntimeError("The answer exceeded its output limit. Please try a narrower question.")
            budget = retry_budget

        if finish_reason is None:
            raise RuntimeError("The answer stream ended without a completion status.")
        answer, citations = self._parse_answer(accumulated_text)
        yield {"type": "final", "result": self._build_result(answer, citations, usages, timings, started)}
