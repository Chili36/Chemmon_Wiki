from __future__ import annotations

import json
import os
import re
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

from .providers import client_for_model, normalize_usage as _normalize_usage
from .wiki_store import WikiStore


REPO_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(REPO_ROOT / ".env")


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


@dataclass(frozen=True)
class PageSelectionResult:
    pages_used: list[str]
    tool_trace: list[dict[str, Any]]
    token_summary: dict[str, Any]
    timing_summary: dict[str, Any]


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


class WikiPageSelector:
    def __init__(
        self,
        *,
        store: WikiStore,
        client: Any | None = None,
        model_id: str | None = None,
        model_str: str | None = None,
        max_pages: int = 6,
    ):
        self.store = store
        self.max_pages = max_pages
        if client and model_id:
            self.client = client
            self.model_id = model_id
        else:
            resolved_str = model_str or os.getenv("WIKI_SELECTOR_MODEL", "openai/gpt-5.4-mini")
            self.client, self.model_id = client_for_model(resolved_str)

    def run(self, payload: dict[str, Any]) -> PageSelectionResult:
        selector_started = time.perf_counter()
        index_content = self.store.read_page("index.md").content
        llm_started = time.perf_counter()

        response = self.client.chat.completions.create(
            model=self.model_id,
            messages=[
                {"role": "system", "content": SELECTION_SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": json.dumps(
                        {"question": payload["question"], "wiki_index": index_content},
                        ensure_ascii=False,
                    ),
                },
            ],
            response_format={"type": "json_object"},
        )

        llm_duration_ms = int((time.perf_counter() - llm_started) * 1000)
        finish_reason = response.choices[0].finish_reason if response.choices else None
        usage = _normalize_usage(response.usage, finish_reason)
        timing_trace = [{"call_number": 1, "duration_ms": llm_duration_ms, "stop_reason": finish_reason}]

        output_text = response.choices[0].message.content or "" if response.choices else ""
        try:
            data = _extract_json_payload(output_text)
            raw = data.get("page_names", []) if isinstance(data, dict) else []
            if not isinstance(raw, list):
                raw = [raw]
            selected_page_names = [str(name) for name in raw]
        except (ValueError, json.JSONDecodeError, AttributeError):
            selected_page_names = []

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
            token_summary=_aggregate_usage([usage], self.model_id),
            timing_summary={
                **_aggregate_timing(timing_trace),
                "selector_wall_time_ms": int((time.perf_counter() - selector_started) * 1000),
            },
        )
