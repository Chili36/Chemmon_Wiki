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
    resolve_provider,
)
from .anthropic_native import json_schema_format, native_client, response_text, usage_dict


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
- After each claim, cite its page filename in parentheses, for example (page-name.md).
- If you cannot answer from the provided pages, say "The wiki does not cover this topic." and cite nothing.
"""

PLAIN_TEXT_FORMAT = """
Write the answer as plain text (Markdown lists and code formatting are fine). Do not repeat it."""

STRUCTURED_FORMAT = """
Put the full answer, with its inline citations, in "answer". List every page you cited in "citations"."""

# Structured answers: OpenAI enforces json_schema on its endpoint; Anthropic is called natively
# with output_config, because its OpenAI-compatible endpoint ignores response_format.
# Others get the plain-text contract; citations then come from inline mentions.
STRUCTURED_OUTPUT_PROVIDERS = {"anthropic", "openai"}

ANSWER_RESPONSE_FORMAT = {
    "type": "json_schema",
    "json_schema": {
        "name": "wiki_answer",
        "strict": True,
        "schema": {
            "type": "object",
            "additionalProperties": False,
            "required": ["answer", "citations"],
            "properties": {
                "answer": {"type": "string"},
                "citations": {"type": "array", "items": {"type": "string"}},
            },
        },
    },
}

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
        structured_output: bool | None = None,
    ):
        self.native = False
        if client and model_id:
            self.client = client
            self.model_id = model_id
            provider = None
        else:
            resolved_str = model_str or os.getenv("WIKI_ANSWERER_MODEL", "anthropic/claude-sonnet-5-5")
            provider, self.model_id = resolve_provider(resolved_str)
            if provider == "anthropic":
                self.native, self.client = True, native_client()
            else:
                self.client, self.model_id = client_for_model(resolved_str)
        self.provider = provider
        self.structured_output = (
            structured_output if structured_output is not None else provider in STRUCTURED_OUTPUT_PROVIDERS
        )
        self._sonnet55 = self.model_id.split("/")[-1] == "claude-sonnet-5-5"
        # Sonnet 5.5 shares this allowance between adaptive thinking and text.
        self.max_tokens = max_tokens if max_tokens is not None else (8192 if self._sonnet55 else 2000)

    def _limit_kwargs(self, budget: int) -> dict[str, int]:
        # OpenAI's GPT-5 models reject max_tokens; reasoning counts toward this limit.
        return {"max_completion_tokens": budget} if self.provider == "openai" else {"max_tokens": budget}

    def _format_kwargs(self) -> dict[str, Any]:
        return {"response_format": ANSWER_RESPONSE_FORMAT} if self.structured_output else {}

    def _retry_budget(self, budget: int) -> int:
        return max(budget, min(budget * 2, 16384)) if self._sonnet55 else budget

    def _build_messages(self, question: str, pages: list[dict[str, Any]]) -> list[dict[str, str]]:
        return [
            {"role": "system", "content": ANSWERER_SYSTEM_PROMPT
             + (STRUCTURED_FORMAT if self.structured_output else PLAIN_TEXT_FORMAT)},
            {
                "role": "user",
                "content": json.dumps(
                    {"question": question, "pages": pages},
                    ensure_ascii=False,
                ),
            },
        ]

    def _native_kwargs(self, question: str, pages: list[dict[str, Any]], budget: int) -> dict[str, Any]:
        system, user = (m["content"] for m in self._build_messages(question, pages))
        kwargs: dict[str, Any] = {
            "model": self.model_id, "max_tokens": budget,
            # Stable instructions first, marked for caching; the question and evidence vary.
            "system": [{"type": "text", "text": system, "cache_control": {"type": "ephemeral"}}],
            "messages": [{"role": "user", "content": user}],
        }
        if self.structured_output:
            kwargs["output_config"] = json_schema_format(ANSWER_RESPONSE_FORMAT["json_schema"]["schema"])
        return kwargs

    def _call(self, question: str, pages: list[dict[str, Any]], budget: int) -> tuple[str, dict, str | None]:
        if self.native:
            message = self.client.messages.create(**self._native_kwargs(question, pages, budget))
            return response_text(message), usage_dict(message.usage, message.stop_reason), message.stop_reason
        response = self.client.chat.completions.create(
            model=self.model_id,
            **self._limit_kwargs(budget),
            messages=self._build_messages(question, pages),
            stream=False,
            **self._format_kwargs(),
        )
        finish_reason = response.choices[0].finish_reason if response.choices else None
        text = response.choices[0].message.content or "" if response.choices else ""
        return text, _normalize_usage(response.usage, finish_reason), finish_reason

    def _stream_chunks(self, question: str, pages: list[dict[str, Any]], budget: int, final: dict) -> Iterator[str]:
        """Yield answer text; on completion put usage and stop reason in `final`."""
        if self.native:
            with self.client.messages.stream(**self._native_kwargs(question, pages, budget)) as stream:
                for text in stream.text_stream:
                    yield text
                message = stream.get_final_message()
            final.update(usage=usage_dict(message.usage, message.stop_reason), stop=message.stop_reason)
            return
        usage_data = None
        response_stream = self.client.chat.completions.create(
            model=self.model_id,
            **self._limit_kwargs(budget),
            messages=self._build_messages(question, pages),
            stream=True,
            stream_options={"include_usage": True},
            **self._format_kwargs(),
        )
        for chunk in response_stream:
            if chunk.choices:
                delta = chunk.choices[0].delta
                if delta and delta.content:
                    yield delta.content
                if chunk.choices[0].finish_reason:
                    final["stop"] = chunk.choices[0].finish_reason
            if chunk.usage:
                usage_data = chunk.usage
        final["usage"] = _normalize_usage(usage_data, final.get("stop"))

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
            text, usage, finish_reason = self._call(question, pages, budget)
            usages.append(usage)
            timings.append({"call_number": attempt + 1, "duration_ms": int((time.perf_counter() - call_started) * 1000), "stop_reason": finish_reason})
            if finish_reason not in {"length", "max_tokens"}:
                break
            retry_budget = self._retry_budget(budget)
            if attempt or retry_budget <= budget:
                raise RuntimeError("The answer exceeded its output limit. Please try a narrower question.")
            budget = retry_budget

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
            final: dict[str, Any] = {}
            any_deltas_sent = False
            call_started = time.perf_counter()
            try:
                for text in self._stream_chunks(question, pages, budget, final):
                    accumulated_text += text
                    any_deltas_sent = True
                    yield {"type": "delta", "text": text}
            except Exception:
                if any_deltas_sent or usages:
                    raise
                result = self.run(question, pages)
                yield {"type": "delta", "text": result.answer}
                yield {"type": "final", "result": result}
                return

            finish_reason = final.get("stop")
            usages.append(final.get("usage") or _normalize_usage(None, finish_reason))
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
