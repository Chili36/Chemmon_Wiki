from __future__ import annotations

import json
import os
import re
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol

from anthropic import Anthropic
from dotenv import load_dotenv

from .wiki_store import WikiStore


REPO_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(REPO_ROOT / ".env")


READ_WIKI_PAGES_TOOL = {
    "name": "read_wiki_pages",
    "description": (
        "Read one or more non-index pages from the local ChemMon wiki by filename. "
        "Use this to batch the page reads you need after reviewing the provided index."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "page_names": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Wiki filenames to read.",
            }
        },
        "required": ["page_names"],
    },
}

TOOLS = [READ_WIKI_PAGES_TOOL]

SELECTION_SYSTEM_PROMPT = """You are the ChemMon wiki page selector.

Your only job is to choose which wiki pages should be returned as context for the user's question about chemical monitoring reporting.

Rules:
- The full catalog from `index.md` is already provided in the user message.
- Use that catalog first to decide which pages matter.
- Do not request `index.md` again.
- Do not answer the question.
- Request the minimal set of non-index pages needed for this question.
- When possible, request all needed pages in a single `read_wiki_pages` call.
- You may request at most 5 non-index pages.
- If no additional pages are needed, return JSON only: {"page_names": []}
"""


class AnthropicMessagesClient(Protocol):
    def create(self, **kwargs: Any) -> Any: ...


class AnthropicClientProtocol(Protocol):
    @property
    def messages(self) -> AnthropicMessagesClient: ...


@dataclass(frozen=True)
class PageSelectionResult:
    pages_used: list[str]
    tool_trace: list[dict[str, Any]]
    token_summary: dict[str, Any]
    timing_summary: dict[str, Any]


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


def _extract_json_payload(text: str) -> dict[str, Any]:
    text = text.strip()
    if not text:
        raise ValueError("Empty response from page selector")
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    fenced = re.search(r"```json\s*(\{.*\})\s*```", text, flags=re.DOTALL)
    if fenced:
        return json.loads(fenced.group(1))
    brace_start = text.find("{")
    brace_end = text.rfind("}")
    if brace_start != -1 and brace_end != -1 and brace_end > brace_start:
        return json.loads(text[brace_start : brace_end + 1])
    raise ValueError("Could not extract JSON from page selector response")


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


def _aggregate_usage(usages: list[dict[str, int | str | None]], model: str) -> dict[str, Any]:
    return {
        "model": model,
        "calls": len(usages),
        "input_tokens": sum(int(u["input_tokens"]) for u in usages),
        "output_tokens": sum(int(u["output_tokens"]) for u in usages),
        "cache_creation_input_tokens": sum(int(u["cache_creation_input_tokens"]) for u in usages),
        "cache_read_input_tokens": sum(int(u["cache_read_input_tokens"]) for u in usages),
        "total_tracked_tokens": sum(int(u["total_tracked_tokens"]) for u in usages),
        "per_call": usages,
    }


def build_fast_path_result(pages: list[str]) -> PageSelectionResult:
    """Construct a PageSelectionResult for a deterministic fast-path hit.

    Zero-fills the token/timing summaries using the same aggregation
    helpers as the LLM selector path so downstream trace consumers see a
    consistent field set regardless of which path was taken.
    """
    pages_used = list(dict.fromkeys(["index.md", *pages]))
    tool_trace: list[dict[str, Any]] = [
        {"fast_path": True, "page_name": p, "order": i + 1, "synthetic": True}
        for i, p in enumerate(pages)
    ]
    return PageSelectionResult(
        pages_used=pages_used,
        tool_trace=tool_trace,
        token_summary=_aggregate_usage([], "fast-path"),
        timing_summary={**_aggregate_timing([]), "selector_wall_time_ms": 0},
    )


def _aggregate_timing(timings: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "calls": len(timings),
        "llm_time_ms": sum(int(t["duration_ms"]) for t in timings),
        "per_call": timings,
    }


def _read_pages_payload(
    *,
    store: WikiStore,
    requested_page_names: list[str],
    max_pages: int,
    pages_read: list[str],
    tool_trace: list[dict[str, Any]],
) -> dict[str, Any]:
    pages: list[dict[str, Any]] = []
    skipped: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []
    max_followup_pages = max(max_pages - 1, 0)
    seen_in_request: set[str] = set()

    for raw_name in requested_page_names:
        page_name = str(raw_name)
        if page_name in seen_in_request:
            skipped.append({"page_name": page_name, "reason": "duplicate_in_request"})
            continue
        seen_in_request.add(page_name)

        if page_name == "index.md":
            skipped.append({"page_name": page_name, "reason": "index_already_provided"})
            continue

        if len(pages_read) >= max_followup_pages:
            skipped.append({"page_name": page_name, "reason": "page_limit_exceeded", "limit": max_pages})
            continue

        try:
            page = store.read_page(page_name)
            normalized_name = store.normalize_page_name(page_name)
            if normalized_name in pages_read:
                skipped.append({"page_name": normalized_name, "reason": "already_read_in_conversation"})
                continue
            pages_read.append(normalized_name)
            tool_trace.append({"page_name": normalized_name, "order": len(tool_trace) + 1, "chars": len(page.content), "synthetic": False})
            pages.append({"page_name": normalized_name, "content": page.content})
        except Exception as exc:
            errors.append({"page_name": page_name, "reason": "read_failed", "message": str(exc)})
            tool_trace.append({"page_name": page_name, "order": len(tool_trace) + 1, "chars": len(str(exc)), "synthetic": True})

    return {"pages": pages, "skipped": skipped, "errors": errors}


def _selection_payload_from_response(content: list[Any]) -> list[str]:
    tool_uses = [b for b in content if _get_block_value(b, "type") == "tool_use"]
    if tool_uses:
        page_names: list[str] = []
        for block in tool_uses:
            raw = _get_block_value(block, "input", {}).get("page_names", [])
            if not isinstance(raw, list):
                raw = [raw]
            page_names.extend(str(name) for name in raw)
        return page_names
    final_text = _response_text(content)
    data = _extract_json_payload(final_text)
    raw = data.get("page_names", [])
    if not isinstance(raw, list):
        raw = [raw]
    return [str(name) for name in raw]


def build_anthropic_client() -> AnthropicClientProtocol:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY is not set")
    return Anthropic(api_key=api_key)


def _resolve_model(*env_keys: str, default: str) -> str:
    for key in env_keys:
        value = os.getenv(key)
        if value:
            return value
    return default


class AnthropicWikiPageSelector:
    def __init__(
        self,
        *,
        store: WikiStore,
        client: AnthropicClientProtocol | None = None,
        model: str | None = None,
        max_pages: int = 6,
        max_tokens: int = 1500,
    ):
        self.store = store
        self.client = client or build_anthropic_client()
        self.model = model or _resolve_model("WIKI_SELECTOR_MODEL", default="claude-3-7-sonnet-latest")
        self.max_pages = max_pages
        self.max_tokens = max_tokens

    def run(self, payload: dict[str, Any]) -> PageSelectionResult:
        selector_started = time.perf_counter()
        index_content = self.store.read_page("index.md").content
        llm_started = time.perf_counter()
        response = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            system=SELECTION_SYSTEM_PROMPT,
            tools=TOOLS,
            messages=[
                {
                    "role": "user",
                    "content": json.dumps(
                        {"question": payload["question"], "wiki_index": index_content},
                        ensure_ascii=False,
                    ),
                }
            ],
        )
        llm_duration_ms = int((time.perf_counter() - llm_started) * 1000)
        timing_trace = [{"call_number": 1, "duration_ms": llm_duration_ms, "stop_reason": _get_block_value(response, "stop_reason")}]
        usage_trace = [_usage_dict(_get_block_value(response, "usage"), stop_reason=_get_block_value(response, "stop_reason"))]
        content = _get_block_value(response, "content", [])
        selected_page_names = _selection_payload_from_response(content)
        pages_read: list[str] = []
        tool_trace: list[dict[str, Any]] = []
        _read_pages_payload(
            store=self.store,
            requested_page_names=selected_page_names,
            max_pages=self.max_pages,
            pages_read=pages_read,
            tool_trace=tool_trace,
        )
        return PageSelectionResult(
            pages_used=list(dict.fromkeys(["index.md", *pages_read])),
            tool_trace=tool_trace,
            token_summary=_aggregate_usage(usage_trace, self.model),
            timing_summary={
                **_aggregate_timing(timing_trace),
                "selector_wall_time_ms": int((time.perf_counter() - selector_started) * 1000),
            },
        )
