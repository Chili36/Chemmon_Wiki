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
    resolve_provider,
    extract_json_payload,
    normalize_usage as _normalize_usage,
)
from .anthropic_native import json_schema_format, native_client, response_text, usage_dict
from .wiki_store import WikiStore


SELECTION_SYSTEM_PROMPT = """You are the ChemMon wiki page selector.

Your only job is to choose which wiki pages should be returned as context for the user's question about chemical monitoring reporting.

Rules:
- The topic catalog is provided with the request. It is discovery metadata, not evidence.
- Use that catalog first to decide which pages matter.
- Do not request `index.md` again.
- Do not answer the question.
- Request the minimal set of non-index pages needed for this question.
- Select only filenames in the catalog, respecting domain scope and explicit exceptions.
- Select at most max_pages pages (the request supplies this limit).
- Return JSON only: {"page_names": ["page-name.md"]}. No tools are available.
- If no topic pages can help, return {"page_names": []}.
"""

# Providers that enforce a strict json_schema response_format on the OpenAI-compatible
# endpoint. Anthropic is called natively (output_config) instead; other providers get
# no response_format and rely on the prompt and tolerant parsing.
STRUCTURED_OUTPUT_PROVIDERS = {"openai"}
NATIVE_MAX_TOKENS = 4096  # adaptive thinking and the short JSON answer share this

SELECTION_RESPONSE_FORMAT = {
    "type": "json_schema",
    "json_schema": {
        "name": "page_selection",
        "strict": True,
        "schema": {
            "type": "object",
            "additionalProperties": False,
            "required": ["page_names"],
            "properties": {"page_names": {"type": "array", "items": {"type": "string"}}},
        },
    },
}


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
        use_hints: bool = True,
        structured_output: bool | None = None,
    ):
        self.store = store
        self.max_pages = max_pages
        self.use_hints = use_hints
        self.native = False
        if client and model_id:
            self.client = client
            self.model_id = model_id
            provider = None
        else:
            resolved_str = model_str or os.getenv("WIKI_SELECTOR_MODEL", "anthropic/claude-haiku-5-5")
            provider, self.model_id = resolve_provider(resolved_str)
            if provider == "anthropic":
                # Native Messages API: prompt caching and enforced JSON.
                self.native, self.client = True, native_client()
            else:
                self.client, self.model_id = client_for_model(resolved_str)
        self.structured_output = (
            structured_output if structured_output is not None else provider in STRUCTURED_OUTPUT_PROVIDERS
        )

    def _format_kwargs(self) -> dict[str, Any]:
        return {"response_format": SELECTION_RESPONSE_FORMAT} if self.structured_output else {}

    def run(self, payload: dict[str, Any]) -> PageSelectionResult:
        selector_started = time.perf_counter()
        max_pages = int(payload.get("max_pages", self.max_pages))
        if not 1 <= max_pages <= 10:
            raise ValueError("max_pages must be between 1 and 10")
        catalog = self.store.selector_catalog(use_hints=self.use_hints)
        llm_started = time.perf_counter()
        if self.native:
            output_text, usage, finish_reason = self._run_native(payload["question"], max_pages, catalog)
        else:
            output_text, usage, finish_reason = self._run_compatible(payload["question"], max_pages, catalog)
        llm_duration_ms = int((time.perf_counter() - llm_started) * 1000)
        timing_trace = [{"call_number": 1, "duration_ms": llm_duration_ms, "stop_reason": finish_reason}]
        return self._result(output_text, usage, timing_trace, max_pages, selector_started)

    def _run_native(self, question: str, max_pages: int, catalog: str) -> tuple[str, dict, str | None]:
        # The rules and catalogue are identical for every question, so they form the cached prefix;
        # only the question follows the breakpoint.
        message = self.client.messages.create(
            model=self.model_id,
            max_tokens=NATIVE_MAX_TOKENS,
            system=[{"type": "text", "text": SELECTION_SYSTEM_PROMPT},
                    {"type": "text", "text": f"Topic catalog:\n{catalog}", "cache_control": {"type": "ephemeral"}}],
            messages=[{"role": "user", "content": json.dumps({"question": question, "max_pages": max_pages},
                                                              ensure_ascii=False)}],
            output_config=json_schema_format(SELECTION_RESPONSE_FORMAT["json_schema"]["schema"]),
        )
        return response_text(message), usage_dict(message.usage, message.stop_reason), message.stop_reason

    def _run_compatible(self, question: str, max_pages: int, catalog: str) -> tuple[str, dict, str | None]:
        response = self.client.chat.completions.create(
            model=self.model_id,
            messages=[
                {"role": "system", "content": SELECTION_SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": json.dumps(
                        {"question": question, "max_pages": max_pages, "catalog": catalog},
                        ensure_ascii=False,
                    ),
                },
            ],
            **self._format_kwargs(),
        )
        finish_reason = response.choices[0].finish_reason if response.choices else None
        output_text = response.choices[0].message.content or "" if response.choices else ""
        return output_text, _normalize_usage(response.usage, finish_reason), finish_reason

    def _result(self, output_text: str, usage: dict, timing_trace: list[dict], max_pages: int,
                selector_started: float) -> PageSelectionResult:
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
