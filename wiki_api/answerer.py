from __future__ import annotations

import json
import os
import re
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol, Iterator, Literal, TypedDict

from anthropic import Anthropic
from dotenv import load_dotenv


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


class AnthropicMessagesClient(Protocol):
    def create(self, **kwargs: Any) -> Any: ...
    def stream(self, **kwargs: Any) -> Any: ...


class AnthropicClientProtocol(Protocol):
    @property
    def messages(self) -> AnthropicMessagesClient: ...


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


def _get_block_value(block: Any, key: str, default: Any = None) -> Any:
    if isinstance(block, dict):
        return block.get(key, default)
    return getattr(block, key, default)


def _response_text(content_blocks: list[Any]) -> str:
    parts: list[str] = []
    for block in content_blocks:
        if _get_block_value(block, "type") == "text":
            parts.append(_get_block_value(block, "text", ""))
    return "".join(parts).strip()


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


def _usage_dict(usage: Any, *, stop_reason: str | None) -> dict[str, int | str | None]:
    input_tokens = int(_get_block_value(usage, "input_tokens", 0) or 0)
    output_tokens = int(_get_block_value(usage, "output_tokens", 0) or 0)
    cache_creation = int(_get_block_value(usage, "cache_creation_input_tokens", 0) or 0)
    cache_read = int(_get_block_value(usage, "cache_read_input_tokens", 0) or 0)
    return {
        "stop_reason": stop_reason,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "cache_creation_input_tokens": cache_creation,
        "cache_read_input_tokens": cache_read,
        "total_tracked_tokens": input_tokens + output_tokens + cache_creation + cache_read,
    }


def _resolve_model(*env_keys: str, default: str) -> str:
    for key in env_keys:
        value = os.getenv(key)
        if value:
            return value
    return default


def build_anthropic_client() -> AnthropicClientProtocol:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY is not set")
    return Anthropic(api_key=api_key)


class AnthropicChemMonAnswerer:
    def __init__(
        self,
        *,
        client: AnthropicClientProtocol | None = None,
        model: str | None = None,
        max_tokens: int = 2000,
    ):
        self.client = client or build_anthropic_client()
        self.model = model or _resolve_model("WIKI_ANSWERER_MODEL", default="claude-sonnet-4-6")
        self.max_tokens = max_tokens

    def run(
        self,
        question: str,
        pages: list[dict[str, Any]],
    ) -> AnswerResult:
        answerer_started = time.perf_counter()
        llm_started = time.perf_counter()
        response = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            system=ANSWERER_SYSTEM_PROMPT,
            messages=[
                {
                    "role": "user",
                    "content": json.dumps(
                        {"question": question, "pages": pages},
                        ensure_ascii=False,
                    ),
                }
            ],
        )
        llm_duration_ms = int((time.perf_counter() - llm_started) * 1000)
        usage = _usage_dict(
            _get_block_value(response, "usage"),
            stop_reason=_get_block_value(response, "stop_reason"),
        )
        final_text = _response_text(_get_block_value(response, "content", []))
        data = _extract_json_payload(final_text)
        if data and "answer" in data:
            answer = data["answer"]
            citations = data.get("citations", [])
        else:
            answer = final_text
            citations = []

        return AnswerResult(
            answer=answer,
            citations=citations,
            token_summary={
                "model": self.model,
                "calls": 1,
                "input_tokens": usage["input_tokens"],
                "output_tokens": usage["output_tokens"],
                "cache_creation_input_tokens": usage["cache_creation_input_tokens"],
                "cache_read_input_tokens": usage["cache_read_input_tokens"],
                "total_tracked_tokens": usage["total_tracked_tokens"],
                "per_call": [usage],
            },
            timing_summary={
                "calls": 1,
                "llm_time_ms": llm_duration_ms,
                "answerer_wall_time_ms": int((time.perf_counter() - answerer_started) * 1000),
                "per_call": [
                    {
                        "call_number": 1,
                        "duration_ms": llm_duration_ms,
                        "stop_reason": _get_block_value(response, "stop_reason"),
                    }
                ],
            },
        )

    def stream(
        self,
        question: str,
        pages: list[dict[str, Any]],
    ) -> Iterator[AnswerStreamEvent]:
        """Stream the raw model text deltas, then yield a final AnswerResult.

        The model is still instructed to return JSON only (see ANSWERER_SYSTEM_PROMPT).
        Streaming callers can extract the `answer` field progressively while the
        request is in-flight, then rely on the final AnswerResult for citations
        and token accounting.
        """
        answerer_started = time.perf_counter()
        llm_started = time.perf_counter()

        with self.client.messages.stream(
            model=self.model,
            max_tokens=self.max_tokens,
            system=ANSWERER_SYSTEM_PROMPT,
            messages=[
                {
                    "role": "user",
                    "content": json.dumps(
                        {"question": question, "pages": pages},
                        ensure_ascii=False,
                    ),
                }
            ],
        ) as stream:
            for text in stream.text_stream:
                if text:
                    yield {"type": "delta", "text": text}

            final_message = stream.get_final_message()
            try:
                final_text = stream.get_final_text()
            except Exception:
                final_text = _response_text(_get_block_value(final_message, "content", []))

        llm_duration_ms = int((time.perf_counter() - llm_started) * 1000)
        usage = _usage_dict(
            _get_block_value(final_message, "usage"),
            stop_reason=_get_block_value(final_message, "stop_reason"),
        )

        data = _extract_json_payload(final_text)
        if data and "answer" in data:
            answer = data["answer"]
            citations = data.get("citations", [])
        else:
            answer = final_text.strip()
            citations = []

        yield {
            "type": "final",
            "result": AnswerResult(
                answer=answer,
                citations=citations,
                token_summary={
                    "model": self.model,
                    "calls": 1,
                    "input_tokens": usage["input_tokens"],
                    "output_tokens": usage["output_tokens"],
                    "cache_creation_input_tokens": usage["cache_creation_input_tokens"],
                    "cache_read_input_tokens": usage["cache_read_input_tokens"],
                    "total_tracked_tokens": usage["total_tracked_tokens"],
                    "per_call": [usage],
                },
                timing_summary={
                    "calls": 1,
                    "llm_time_ms": llm_duration_ms,
                    "answerer_wall_time_ms": int((time.perf_counter() - answerer_started) * 1000),
                    "per_call": [
                        {
                            "call_number": 1,
                            "duration_ms": llm_duration_ms,
                            "stop_reason": _get_block_value(final_message, "stop_reason"),
                        }
                    ],
                },
            ),
        }
