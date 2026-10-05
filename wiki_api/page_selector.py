from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass
from typing import Any

from .providers import (
    aggregate_timing as _aggregate_timing,
    aggregate_usage as _aggregate_usage,
    client_for_model,
    extract_json_payload,
    normalize_usage as _normalize_usage,
)
from .wiki_store import WikiStore


SELECTION_SYSTEM_PROMPT = """You are the ChemMon wiki page selector.

Your only job is to choose which wiki pages should be returned as context for the user's question about chemical monitoring reporting.

Rules:
- The topic catalog is provided in the user message. It is discovery metadata, not evidence.
- Use that catalog first to decide which pages matter.
- Do not request `index.md` again.
- Do not answer the question.
- Request the minimal set of non-index pages needed for this question.
- Select only filenames in the catalog, respecting domain scope and explicit exceptions.
- Select at most max_pages pages (the request supplies this limit).
- Return JSON only: {"page_names": ["page-name.md"]}. No tools are available.
- If no topic pages can help, return {"page_names": []}.
"""


@dataclass(frozen=True)
class PageSelectionResult:
    pages_used: list[str]
    tool_trace: list[dict[str, Any]]
    token_summary: dict[str, Any]
    timing_summary: dict[str, Any]




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
    allowed = set(store.list_pages())
    seen_in_request: set[str] = set()

    for raw_name in requested_page_names:
        page_name = store.normalize_page_name(str(raw_name))
        if page_name in seen_in_request:
            skipped.append({"page_name": page_name, "reason": "duplicate_in_request"})
            continue
        seen_in_request.add(page_name)

        if page_name not in allowed:
            skipped.append({"page_name": page_name, "reason": "not_a_topic_page"})
            continue

        if len(pages_read) >= max_pages:
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
        max_pages = int(payload.get("max_pages", self.max_pages))
        if not 1 <= max_pages <= 10:
            raise ValueError("max_pages must be between 1 and 10")
        catalog = self.store.selector_catalog()
        llm_started = time.perf_counter()

        response = self.client.chat.completions.create(
            model=self.model_id,
            messages=[
                {"role": "system", "content": SELECTION_SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": json.dumps(
                        {"question": payload["question"], "max_pages": max_pages, "catalog": catalog},
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
        data = extract_json_payload(output_text)
        if not isinstance(data, dict) or not isinstance(data.get("page_names"), list):
            raise ValueError("Page selector must return a JSON object with a page_names array")
        selected_page_names = data["page_names"]
        if not all(isinstance(name, str) for name in selected_page_names):
            raise ValueError("Page selector returned invalid page names")

        pages_read: list[str] = []
        tool_trace: list[dict[str, Any]] = []
        _read_pages_payload(
            store=self.store,
            requested_page_names=selected_page_names,
            max_pages=max_pages,
            pages_read=pages_read,
            tool_trace=tool_trace,
        )

        if selected_page_names and not pages_read:
            raise ValueError("Page selector did not return any valid topic pages")

        return PageSelectionResult(
            pages_used=pages_read,
            tool_trace=tool_trace,
            token_summary=_aggregate_usage([usage], self.model_id),
            timing_summary={
                **_aggregate_timing(timing_trace),
                "selector_wall_time_ms": int((time.perf_counter() - selector_started) * 1000),
            },
        )
