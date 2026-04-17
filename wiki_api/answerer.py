from __future__ import annotations

import json
import os
import re
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterator, Literal, TypedDict

from dotenv import load_dotenv

from .providers import client_for_model


REPO_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(REPO_ROOT / ".env")

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


def _extract_json_payload(text: str) -> dict[str, Any] | None:
    text = text.strip()
    if not text:
        return None
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    fenced = re.search(r"```json\s*(\{.*\})\s*```", text, flags=re.DOTALL)
    if fenced:
        try:
            return json.loads(fenced.group(1))
        except json.JSONDecodeError:
            pass
    brace_start = text.find("{")
    brace_end = text.rfind("}")
    if brace_start != -1 and brace_end != -1 and brace_end > brace_start:
        try:
            return json.loads(text[brace_start : brace_end + 1])
        except json.JSONDecodeError:
            pass
    return None


def _normalize_usage(usage: Any, finish_reason: str | None) -> dict[str, int | str | None]:
    """Normalise usage from either OpenAI-style (prompt_tokens/completion_tokens)
    or Anthropic-style (input_tokens/output_tokens) usage objects.

    Duplicated from page_selector.py — will be extracted to a shared location in Task 5.
    """
    if usage is None:
        return {
            "stop_reason": finish_reason,
            "input_tokens": 0,
            "output_tokens": 0,
            "cache_creation_input_tokens": 0,
            "cache_read_input_tokens": 0,
            "total_tracked_tokens": 0,
        }
    input_tokens = int(getattr(usage, "prompt_tokens", 0) or getattr(usage, "input_tokens", 0) or 0)
    output_tokens = int(getattr(usage, "completion_tokens", 0) or getattr(usage, "output_tokens", 0) or 0)
    cache_creation = int(getattr(usage, "cache_creation_input_tokens", 0) or 0)
    cache_read = int(getattr(usage, "cache_read_input_tokens", 0) or 0)
    return {
        "stop_reason": finish_reason,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "cache_creation_input_tokens": cache_creation,
        "cache_read_input_tokens": cache_read,
        "total_tracked_tokens": input_tokens + output_tokens + cache_creation + cache_read,
    }


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
        data = _extract_json_payload(text)
        if data and "answer" in data:
            return data["answer"], data.get("citations", [])
        return text.strip(), []

    def run(self, question: str, pages: list[dict[str, Any]]) -> AnswerResult:
        answerer_started = time.perf_counter()
        llm_started = time.perf_counter()

        response = self.client.chat.completions.create(
            model=self.model_id,
            max_tokens=self.max_tokens,
            messages=self._build_messages(question, pages),
            stream=False,
        )

        llm_duration_ms = int((time.perf_counter() - llm_started) * 1000)
        finish_reason = response.choices[0].finish_reason if response.choices else None
        usage = _normalize_usage(response.usage, finish_reason)
        text = response.choices[0].message.content or "" if response.choices else ""
        answer, citations = self._parse_answer(text)

        return AnswerResult(
            answer=answer,
            citations=citations,
            token_summary={
                "model": self.model_id,
                "calls": 1,
                **{k: usage[k] for k in ("input_tokens", "output_tokens", "cache_creation_input_tokens", "cache_read_input_tokens", "total_tracked_tokens")},
                "per_call": [usage],
            },
            timing_summary={
                "calls": 1,
                "llm_time_ms": llm_duration_ms,
                "answerer_wall_time_ms": int((time.perf_counter() - answerer_started) * 1000),
                "per_call": [{"call_number": 1, "duration_ms": llm_duration_ms, "stop_reason": finish_reason}],
            },
        )
