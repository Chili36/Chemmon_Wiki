from __future__ import annotations

import json
import logging
import os
import re
from pathlib import Path
import time
from typing import Any, Literal

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel, Field
from openai import APIError

from .answerer import AnswerResult, WikiAnswerer
from .page_selector import WikiPageSelector
from .jev_selector import make_selector
from .wiki_store import WikiStore
from .evidence import selected_names, full_evidence, bounded_pack
from .source_review import source_review_status, rule_inventory_status


_WIKI_LINK_RE = re.compile(r"\[\[([a-zA-Z0-9_\-]+)(?:\|[^\]]+)?\]\]")


REPO_ROOT = Path(__file__).resolve().parent.parent
store = WikiStore(REPO_ROOT)
selector_runner: WikiPageSelector | None = None
answerer_runner: WikiAnswerer | None = None
logger = logging.getLogger("wiki_api")
if not logging.getLogger().handlers:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")


def get_selector_runner() -> WikiPageSelector:
    """Return a page-selector instance using the unified WikiPageSelector."""
    global selector_runner
    if selector_runner is None:
        selector_runner = make_selector(store=store)
    return selector_runner


def get_answerer_runner() -> WikiAnswerer:
    global answerer_runner
    if answerer_runner is None:
        answerer_runner = WikiAnswerer()
    return answerer_runner


class SelectionRequest(BaseModel):
    question: str = Field(min_length=1, pattern=r"\S", max_length=20000, description="Question about ChemMon reporting.")
    max_pages: int = Field(default=6, ge=1, le=10)
    selector_model: str | None = Field(default=None, min_length=1, max_length=200, pattern=r"^\S+$")


class ContextPackRequest(SelectionRequest):
    max_chars: int = Field(default=60000, ge=2000, le=120000)


class AskRequest(SelectionRequest):
    answerer_model: str | None = Field(default=None, min_length=1, max_length=200, pattern=r"^\S+$")
    stream: bool = Field(
        default=False,
        description=(
            "If true, stream the answer back as Server-Sent Events (SSE). "
            "The final event contains the full AskResponse object. "
            "Only supported for /wiki/ask."
        ),
    )
    use_graph_expansion: bool = Field(
        default=False,
        description=(
            "Opt in to related-page summaries within max_pages. Summaries are "
            "navigation hints, not citable evidence. Full selected pages take priority."
        ),
    )


class PageSummary(BaseModel):
    page_name: str
    title: str
    summary: str
    sources: list[str] = Field(default_factory=list)
    related: list[str] = Field(default_factory=list)
    content: str | None = None
    source_pages: list[str] = Field(default_factory=list)
    evidence_kind: Literal["full", "summary"] = "full"


class AskResponse(BaseModel):
    answer: str
    citations: list[str]
    pages_used: list[str]
    pages: list[PageSummary]
    trace: dict[str, Any]


app = FastAPI(
    title="ChemMon Wiki API",
    version="0.3.0",
    description="Wiki-owned Q&A API for EFSA Chemical Monitoring reporting guidance.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

STATIC_DIR = Path(__file__).resolve().parent / "static"


# Per-million-token pricing for cost attribution in the trace.
# Configured estimates only; unknown model pricing is explicitly unavailable.
_MODEL_PRICING_USD_PER_MTOK: dict[str, tuple[float, float]] = {
    # (input_price_per_mtok, output_price_per_mtok)
    "claude-haiku-4-5-20251001": (1.0, 5.0),
    "claude-haiku-5-5": (0.10, 0.50),  # prompts up to 100K tokens
    "claude-sonnet-4-6": (3.0, 15.0),
    "claude-sonnet-5-5": (2.0, 10.0),
    "claude-opus-4-6": (15.0, 75.0),
    "claude-3-7-sonnet-latest": (3.0, 15.0),
    "gpt-5.4-mini": (0.75, 4.50),
    "jev-1.13.0": (0.042, 0.0),  # TypeSafe; output tokens free (docs.typesafe.ai/models, 2026-10-18)
    "gpt-5.4-mini-2026-03-17": (0.75, 4.50),
}


def _compute_call_cost(token_summary: dict[str, Any]) -> float | None:
    """Compute USD cost for a single LLM call's token summary.

    Returns None for unknown pricing; a skipped call costs zero.
    Prices are configured estimates, not live quotations.
    """
    if token_summary.get("calls") == 0:
        return 0.0
    model = token_summary.get("model", "")
    prices = _MODEL_PRICING_USD_PER_MTOK.get(model)
    if prices is None:
        return None
    input_price, output_price = prices
    input_tokens = int(token_summary.get("input_tokens", 0) or 0)
    output_tokens = int(token_summary.get("output_tokens", 0) or 0)
    return (input_tokens * input_price + output_tokens * output_price) / 1_000_000


def _total_cost(*summaries: dict[str, Any]) -> float | None:
    costs = [_compute_call_cost(summary) for summary in summaries]
    return None if any(c is None for c in costs) else round(sum(costs), 6)


def _select(request: SelectionRequest, limit: int | None = None):
    try:
        selector = make_selector(store=store, model_str=request.selector_model) if request.selector_model else get_selector_runner()
        result = selector.run({"question": request.question, "max_pages": limit if limit is not None else request.max_pages})
        return selector, result
    except APIError as exc:
        raise HTTPException(status_code=503, detail="Model provider request failed; check provider availability and server configuration.") from exc
    except (RuntimeError, ValueError) as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


def _selection_trace(selector, result) -> dict:
    return {"model": selector.model_id, "tool_trace": result.tool_trace,
            "token_summary": result.token_summary, "timing_summary": result.timing_summary,
            "estimated_cost_usd": _compute_call_cost(result.token_summary)}


@app.post("/wiki/select")
def select_pages(request: SelectionRequest) -> dict[str, Any]:
    selector, result = _select(request)
    names = selected_names(store, result.pages_used, request.max_pages)
    return {"pages_used": names, "pages": [dict(
                {k: v for k, v in full_evidence(store, n).items() if k not in {"content", "citable", "evidence_kind"}},
                evidence_kind="selection", citable=False) for n in names],
            "trace": _selection_trace(selector, result)}


@app.get("/wiki/review-status")
def review_status() -> dict[str, Any]:
    return {"source_review": source_review_status(store.root), "rule_inventory": rule_inventory_status(store.root)}


@app.post("/wiki/context-pack")
def context_pack(request: ContextPackRequest) -> dict[str, Any]:
    started = time.perf_counter()
    names, trace = [], {"model": None, "token_summary": {"calls": 0}, "reason": "policy consumes the sole page slot"}
    if request.max_pages > 1:
        selector, result = _select(request, request.max_pages - 1)
        names = selected_names(store, result.pages_used, request.max_pages - 1)
        trace = _selection_trace(selector, result)
    try:
        pack = bounded_pack(store, names, request.max_pages, request.max_chars, question=request.question)
    except (ValueError, OSError) as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    # Only the selector runs: callers receive evidence, never an intermediate answer.
    pack.update({"schema_version": 1, "question": request.question,
                 "review": source_review_status(store.root),
                 "trace": {"selector": trace, "answerer_calls": 0,
                           "request_wall_time_ms": int((time.perf_counter() - started) * 1000)}})
    return pack


# Related summaries are optional navigation hints. Full pages always take
# priority in the final page budget, and only those pages can support citations.


def _expand_related_summaries(
    selected_page_names: list[str],
    store: WikiStore,
    *,
    max_neighbors: int,
    max_total_tokens: int,
) -> list[dict[str, Any]]:
    """Return short summary blocks for curated neighbors of the selected pages.

    Walks each selected page's frontmatter `related:` list (depth=1, no
    transitive expansion), deduplicates against the selected set and each
    other, and emits one summary block per neighbor. Stops when either the
    neighbor count cap or the token budget is reached.
    """
    already_selected = set(selected_page_names)
    allowed = set(store.list_pages())

    candidates: list[str] = []
    seen_candidates: set[str] = set()

    for page_name in selected_page_names:
        try:
            page = store.read_page(page_name)
        except FileNotFoundError:
            continue
        for ref in page.related:
            match = _WIKI_LINK_RE.search(ref)
            if not match:
                continue
            target = f"{match.group(1)}.md"
            if target in already_selected or target in seen_candidates:
                continue
            if target not in allowed:
                continue
            seen_candidates.add(target)
            candidates.append(target)

    blocks: list[dict[str, Any]] = []
    total_tokens = 0

    for candidate in candidates:
        if len(blocks) >= max_neighbors:
            break
        try:
            neighbor = store.read_page(candidate)
        except FileNotFoundError:
            continue
        summary_text = neighbor.summary or "(no summary available — see full page for details)"
        content = (
            "[NAVIGATION ONLY — the full page is not loaded. "
            "Do not use this summary to support claims or citations.]\n"
            f"Title: {neighbor.title}\n"
            f"{summary_text}"
        )
        # Rough token estimate: ~4 chars per token
        block_tokens = max(1, len(content) // 4)
        if total_tokens + block_tokens > max_total_tokens:
            break
        blocks.append({"page_name": neighbor.name, "content": content, "expansion": True, "evidence_kind": "summary"})
        total_tokens += block_tokens

    return blocks


def _sse(payload: dict[str, Any], *, event: str | None = None) -> str:
    """Serialize a single SSE event with a compact JSON payload."""
    data = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    lines = []
    if event:
        lines.append(f"event: {event}")
    lines.append(f"data: {data}")
    return "\n".join(lines) + "\n\n"


class _JsonStringFieldExtractor:
    """Incrementally extract and decode a JSON string field from streamed text.

    Used to stream only the `answer` value while the model returns a JSON object.
    If extraction never starts (e.g. malformed JSON), callers can fall back to
    streaming raw deltas.
    """

    _START_RE = re.compile(r"\"answer\"\s*:\s*\"")

    def __init__(self) -> None:
        self._buffer = ""
        self._started = False
        self._done = False
        self._escape = False
        self._unicode_remaining = 0
        self._unicode_hex = ""

    @property
    def started(self) -> bool:
        return self._started

    @property
    def done(self) -> bool:
        return self._done

    def feed(self, chunk: str) -> str:
        if self._done or not chunk:
            return ""
        self._buffer += chunk

        if not self._started:
            match = self._START_RE.search(self._buffer)
            if not match:
                # Keep a small tail so cross-chunk `"answer":"` matches still work.
                if len(self._buffer) > 256:
                    self._buffer = self._buffer[-256:]
                return ""
            self._started = True
            self._buffer = self._buffer[match.end() :]

        out: list[str] = []
        i = 0
        while i < len(self._buffer):
            ch = self._buffer[i]

            if self._unicode_remaining:
                if ch.lower() in "0123456789abcdef":
                    self._unicode_hex += ch
                    self._unicode_remaining -= 1
                    if self._unicode_remaining == 0:
                        try:
                            out.append(chr(int(self._unicode_hex, 16)))
                        except Exception:
                            out.append("\\u" + self._unicode_hex)
                        self._unicode_hex = ""
                else:
                    out.append("\\u" + self._unicode_hex + ch)
                    self._unicode_remaining = 0
                    self._unicode_hex = ""
                i += 1
                continue

            if self._escape:
                self._escape = False
                if ch == "n":
                    out.append("\n")
                elif ch == "r":
                    out.append("\r")
                elif ch == "t":
                    out.append("\t")
                elif ch == "b":
                    out.append("\b")
                elif ch == "f":
                    out.append("\f")
                elif ch == "\\":
                    out.append("\\")
                elif ch == "/":
                    out.append("/")
                elif ch == '"':
                    out.append('"')
                elif ch == "u":
                    self._unicode_remaining = 4
                    self._unicode_hex = ""
                else:
                    out.append(ch)
                i += 1
                continue

            if ch == "\\":
                self._escape = True
                i += 1
                continue

            if ch == '"':
                self._done = True
                i += 1
                break

            out.append(ch)
            i += 1

        self._buffer = self._buffer[i:]
        return "".join(out)


@app.get("/wiki/view", include_in_schema=False)
def wiki_viewer():
    return FileResponse(STATIC_DIR / "viewer.html", media_type="text/html")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/wiki/index")
def get_index() -> dict[str, Any]:
    index = store.read_page("index.md")
    return {
        "page_name": index.name,
        "title": index.title,
        "summary": index.summary,
        "content": index.content,
    }


@app.get("/wiki/pages")
def list_pages() -> dict[str, Any]:
    pages = [
        {
            "page_name": page.name,
            "title": page.title,
            "summary": page.summary,
            "sources": page.sources,
            "related": page.related,
            "type": page.page_type,
            "domain": page.domain,
            "last_updated": page.last_updated,
            "source_pages": page.source_pages,
        }
        for page in store.catalog(include_orientation=True)
    ]
    return {"pages": pages, "count": len(pages)}


@app.get("/wiki/search")
def search_pages(q: str = Query(min_length=1), domain: str | None = None, limit: int = Query(default=20, ge=1, le=100)) -> dict[str, Any]:
    terms = re.findall(r"[\w-]+", q.casefold())
    matches = []
    for page in store.catalog():
        if domain and page.domain != domain:
            continue
        text = f"{page.name} {page.title} {page.summary} {page.body}".casefold()
        if not terms or not all(term in text for term in terms):
            continue
        heading = f"{page.name} {page.title}".casefold()
        score = sum(5 * (term in heading) + 2 * (term in page.summary.casefold()) + (term in text) for term in terms)
        matches.append({"page_name": page.name, "title": page.title, "summary": page.summary, "domain": page.domain, "score": score})
    matches.sort(key=lambda p: (-p["score"], p["page_name"]))
    return {"pages": matches[:limit], "count": len(matches)}


@app.get("/wiki/pages/{page_name}/backlinks")
def get_backlinks(page_name: str) -> dict[str, Any]:
    try:
        names = store.backlinks(page_name)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return {"page_name": store.normalize_page_name(page_name), "backlinks": names}


@app.get("/wiki/pages/{page_name}")
def get_page(page_name: str, include_content: bool = Query(default=True)) -> dict[str, Any]:
    try:
        page = store.read_page(page_name)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return {
        "page_name": page.name,
        "title": page.title,
        "summary": page.summary,
        "sources": page.sources,
        "related": page.related,
        "type": page.page_type,
        "domain": page.domain,
        "last_updated": page.last_updated,
        "source_pages": page.source_pages,
        "content": page.content if include_content else None,
    }


@app.post(
    "/wiki/ask",
    response_model=AskResponse,
    summary="Ask a question about ChemMon reporting",
    description=(
        "Send a natural language question about EFSA Chemical Monitoring reporting. "
        "The service selects relevant wiki pages and returns a grounded answer with citations."
    ),
)
def ask_question(request: AskRequest) -> AskResponse:
    request_started = time.perf_counter()
    logger.info(
        "ask_request %s",
        json.dumps({"question": request.question, "max_pages": request.max_pages}, ensure_ascii=False),
    )

    # Phase timings: capture wall time at each phase boundary so the trace
    # surfaces a clean breakdown of where time is spent. Values at the end
    # should approximately sum to request_wall_time_ms (modulo FastAPI and
    # network-to-client overhead, which is reported as 'overhead').
    selector_start = time.perf_counter()
    selector, selection_result = _select(request)
    selector_end = time.perf_counter()

    page_read_start = time.perf_counter()
    selected_page_names = selected_names(store, selection_result.pages_used, request.max_pages)
    pages_raw = [store.read_page(name) for name in selected_page_names]
    page_contents = [full_evidence(store, name, question=request.question) for name in selected_page_names]
    page_read_end = time.perf_counter()

    # Optional navigation hints use only remaining slots; never replace evidence.
    graph_expansion_start = time.perf_counter()
    expansion_blocks: list[dict[str, Any]] = []
    if request.use_graph_expansion and len(selected_page_names) < request.max_pages:
        expansion_blocks = _expand_related_summaries(
            selected_page_names,
            store,
            max_neighbors=request.max_pages - len(selected_page_names),
            max_total_tokens=2000,
        )
    graph_expansion_end = time.perf_counter()

    answerer_input_pages = page_contents + expansion_blocks
    expanded_page_names = [block["page_name"] for block in expansion_blocks]
    pages_used = [*selected_page_names, *expanded_page_names]

    expansion_content_by_page = {block["page_name"]: block["content"] for block in expansion_blocks}
    expanded_pages_raw = []
    for page_name in expanded_page_names:
        try:
            expanded_pages_raw.append(store.read_page(page_name))
        except FileNotFoundError:
            continue

    pages = []
    for page in pages_raw:
        pages.append(
            PageSummary(
                page_name=page.name,
                title=page.title,
                summary=page.summary,
                sources=page.sources,
                related=page.related,
                content=store.clean_content_for_model(page),
                source_pages=list(page.source_pages),
            )
        )
    for page in expanded_pages_raw:
        pages.append(
            PageSummary(
                page_name=page.name,
                title=page.title,
                summary=page.summary,
                sources=page.sources,
                related=page.related,
                content=expansion_content_by_page.get(page.name),
                evidence_kind="summary",
            )
        )

    allowed_citations = set(selected_page_names)
    selector_total_ms = int((selector_end - selector_start) * 1000)
    page_read_ms = int((page_read_end - page_read_start) * 1000)
    graph_expansion_ms = int((graph_expansion_end - graph_expansion_start) * 1000)

    try:
        answerer = (WikiAnswerer(model_str=request.answerer_model) if request.answerer_model else get_answerer_runner()) if pages_raw else None
    except APIError as exc:
        raise HTTPException(status_code=503, detail="Model provider request failed; check provider availability and server configuration.") from exc
    except (RuntimeError, ValueError) as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    def _normalize_citations(raw_citations: list[Any]) -> list[str]:
        citations: list[str] = []
        for raw_citation in raw_citations:
            if not isinstance(raw_citation, str):
                continue
            citation = raw_citation.strip()
            if not citation:
                continue
            if not citation.endswith(".md"):
                citation = f"{citation}.md"
            citation = store.normalize_page_name(citation)
            if citation in allowed_citations:
                citations.append(citation)
        return list(dict.fromkeys(citations))

    def _build_response(*, answer_result: Any, answerer_total_ms: int) -> AskResponse:
        citations = _normalize_citations(getattr(answer_result, "citations", []))
        request_wall_time_ms = int((time.perf_counter() - request_started) * 1000)
        overhead_ms = max(
            0,
            request_wall_time_ms - selector_total_ms - page_read_ms - graph_expansion_ms - answerer_total_ms,
        )
        response = AskResponse(
            answer=answer_result.answer,
            citations=citations,
            pages_used=pages_used,
            pages=pages,
            trace={
                "selection_method": "service-owned llm page selector + answerer",
                "graph_expansion": {
                    "enabled": request.use_graph_expansion,
                    "neighbors_added": [block["page_name"] for block in expansion_blocks],
                    "neighbors_count": len(expansion_blocks),
                },
                "selector": {
                    "model": selector.model_id,
                    "tool_trace": selection_result.tool_trace,
                    "token_summary": selection_result.token_summary,
                    "timing_summary": selection_result.timing_summary,
                },
                "answerer": {
                    "model": answerer.model_id if answerer else None,
                    "token_summary": answer_result.token_summary,
                    "timing_summary": answer_result.timing_summary,
                },
                "total": {
                    "request_wall_time_ms": request_wall_time_ms,
                    "total_llm_calls": (
                        int(selection_result.token_summary["calls"])
                        + int(answer_result.token_summary["calls"])
                    ),
                    "total_tracked_tokens": (
                        int(selection_result.token_summary["total_tracked_tokens"])
                        + int(answer_result.token_summary["total_tracked_tokens"])
                    ),
                    "total_cost_usd": _total_cost(selection_result.token_summary, answer_result.token_summary),
                    "cost_basis": "configured estimate; null when pricing is unknown",
                },
                "phase_timings_ms": {
                    "selector_total": selector_total_ms,
                    "page_read": page_read_ms,
                    "graph_expansion": graph_expansion_ms,
                    "answerer_total": answerer_total_ms,
                    "overhead": overhead_ms,
                },
            },
        )
        logger.info(
            "ask_response %s",
            json.dumps(
                {
                    "question": request.question,
                    "answer_length": len(response.answer),
                    "citations": response.citations,
                    "pages_used": response.pages_used,
                    "total_tokens": response.trace["total"]["total_tracked_tokens"],
                },
                ensure_ascii=False,
            ),
        )
        return response

    if answerer is None:
        result = AnswerResult(
            answer="No relevant wiki evidence was retrieved. Try specifying the reporting domain or SSD2 field.",
            citations=[],
            token_summary={"model": "none", "calls": 0, "input_tokens": 0, "output_tokens": 0, "total_tracked_tokens": 0},
            timing_summary={"calls": 0, "llm_time_ms": 0},
        )
        response = _build_response(answer_result=result, answerer_total_ms=0)
        if request.stream:
            return StreamingResponse(iter([
                _sse({"type": "meta", "pages_used": [], "pages": []}, event="meta"),
                _sse({"type": "done", "response": json.loads(response.model_dump_json())}, event="done"),
            ]), media_type="text/event-stream")
        return response

    if request.stream:
        def _event_stream() -> Any:
            # Small metadata burst so clients can show what context will be used.
            meta_pages = [
                {"page_name": p.page_name, "title": p.title, "summary": p.summary, "evidence_kind": p.evidence_kind}
                for p in pages
            ]
            yield _sse({"type": "meta", "pages_used": pages_used, "pages": meta_pages}, event="meta")

            extractor = _JsonStringFieldExtractor()
            raw_fallback_buffer = ""
            raw_mode = False

            answerer_start = time.perf_counter()
            final_answer_result = None
            try:
                for event in answerer.stream(question=request.question, pages=answerer_input_pages):
                    if event.get("type") == "delta":
                        raw = event.get("text", "")
                        if not isinstance(raw, str) or not raw:
                            continue

                        if raw_mode:
                            yield _sse({"type": "delta", "text": raw}, event="delta")
                            continue

                        extracted = extractor.feed(raw)
                        if extracted:
                            yield _sse({"type": "delta", "text": extracted}, event="delta")
                            continue

                        if not extractor.started:
                            raw_fallback_buffer += raw
                            if len(raw_fallback_buffer) >= 200:
                                raw_mode = True
                                yield _sse({"type": "delta", "text": raw_fallback_buffer}, event="delta")
                                raw_fallback_buffer = ""
                        continue

                    if event.get("type") == "final":
                        final_answer_result = event.get("result")
                        break
            except Exception as exc:
                if raw_fallback_buffer and (not raw_mode) and (not extractor.started):
                    yield _sse({"type": "delta", "text": raw_fallback_buffer}, event="delta")
                yield _sse({"type": "error", "message": str(exc)}, event="error")
                return

            if final_answer_result is None:
                yield _sse({"type": "error", "message": "Answer stream ended without a final result"}, event="error")
                return

            if raw_fallback_buffer and (not raw_mode) and (not extractor.started):
                yield _sse({"type": "delta", "text": raw_fallback_buffer}, event="delta")

            answerer_total_ms = int((time.perf_counter() - answerer_start) * 1000)
            response = _build_response(answer_result=final_answer_result, answerer_total_ms=answerer_total_ms)
            yield _sse(
                {"type": "done", "response": json.loads(response.model_dump_json())},
                event="done",
            )

        return StreamingResponse(
            _event_stream(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                # Nginx: prevent buffering so deltas flush immediately.
                "X-Accel-Buffering": "no",
            },
        )

    answerer_start = time.perf_counter()
    try:
        answer_result = answerer.run(question=request.question, pages=answerer_input_pages)
    except APIError as exc:
        raise HTTPException(status_code=503, detail="Model provider request failed; check provider availability and server configuration.") from exc
    except (RuntimeError, ValueError) as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    answerer_total_ms = int((time.perf_counter() - answerer_start) * 1000)
    return _build_response(answer_result=answer_result, answerer_total_ms=answerer_total_ms)
