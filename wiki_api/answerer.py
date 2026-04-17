from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass
from typing import Any, Iterator, Literal, TypedDict

from .providers import (
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
- If the wiki pages do not contain enough information to answer the question, say so clearly.
- Do not make up rules or guidance that is not in the provided pages.
- Be concise and direct.

Return JSON only with this structure:
{
  "answer": "Your grounded answer here.",
  "citations": ["page-name.md", "other-page.md"]
}

If you cannot answer from the provided pages, return:
{
  "answer": "The wiki does not cover this topic.",
  "citations": []
}
"""


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
        max_tokens: int = 2000,
    ):
        self.max_tokens = max_tokens
        if client and model_id:
            self.client = client
            self.model_id = model_id
        else:
            resolved_str = model_str or os.getenv("WIKI_ANSWERER_MODEL", "anthropic/claude-sonnet-4-6")
            self.client, self.model_id = client_for_model(resolved_str)

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
        data = extract_json_payload(text)
        if data and "answer" in data:
            return data["answer"], data.get("citations", [])
        return text.strip(), []

    def _build_result(self, answer: str, citations: list[str], usage: dict, finish_reason: str | None, llm_ms: int, wall_start: float) -> AnswerResult:
        return AnswerResult(
            answer=answer,
            citations=citations,
            token_summary=_aggregate_usage([usage], self.model_id),
            timing_summary={
                "calls": 1,
                "llm_time_ms": llm_ms,
                "answerer_wall_time_ms": int((time.perf_counter() - wall_start) * 1000),
                "per_call": [{"call_number": 1, "duration_ms": llm_ms, "stop_reason": finish_reason}],
            },
        )

    def run(self, question: str, pages: list[dict[str, Any]]) -> AnswerResult:
        started = time.perf_counter()

        response = self.client.chat.completions.create(
            model=self.model_id,
            max_tokens=self.max_tokens,
            messages=self._build_messages(question, pages),
            stream=False,
        )

        llm_ms = int((time.perf_counter() - started) * 1000)
        finish_reason = response.choices[0].finish_reason if response.choices else None
        usage = _normalize_usage(response.usage, finish_reason)
        text = response.choices[0].message.content or "" if response.choices else ""
        answer, citations = self._parse_answer(text)

        return self._build_result(answer, citations, usage, finish_reason, llm_ms, started)

    def stream(
        self,
        question: str,
        pages: list[dict[str, Any]],
    ) -> Iterator[AnswerStreamEvent]:
        started = time.perf_counter()
        accumulated_text = ""
        usage_data: Any = None
        finish_reason: str | None = None
        any_deltas_sent = False

        try:
            response_stream = self.client.chat.completions.create(
                model=self.model_id,
                max_tokens=self.max_tokens,
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
            if any_deltas_sent:
                raise
            result = self.run(question, pages)
            yield {"type": "delta", "text": result.answer}
            yield {"type": "final", "result": result}
            return

        llm_ms = int((time.perf_counter() - started) * 1000)
        usage = _normalize_usage(usage_data, finish_reason)
        answer, citations = self._parse_answer(accumulated_text)

        yield {"type": "final", "result": self._build_result(answer, citations, usage, finish_reason, llm_ms, started)}
