from __future__ import annotations

import json
import logging
import os
import re
from pathlib import Path
import time
from typing import Any

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from .answerer import AnthropicChemMonAnswerer
from .page_selector import AnthropicWikiPageSelector, OpenAIWikiPageSelector
from .wiki_store import WikiStore


_WIKI_LINK_RE = re.compile(r"\[\[([a-zA-Z0-9_\-]+)(?:\|[^\]]+)?\]\]")


REPO_ROOT = Path(__file__).resolve().parent.parent
store = WikiStore(REPO_ROOT)
selector_runner: AnthropicWikiPageSelector | Any | None = None
answerer_runner: AnthropicChemMonAnswerer | Any | None = None
logger = logging.getLogger("wiki_api")
if not logging.getLogger().handlers:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")


def get_selector_runner() -> AnthropicWikiPageSelector | OpenAIWikiPageSelector | Any:
    """Return a page-selector instance, dispatching by WIKI_SELECTOR_MODEL.

    Model names starting with 'gpt-' are routed to the OpenAI Responses-API
    selector; everything else goes to the Anthropic selector (which is also
    the default). This is a simple prefix match — if we ever need multi-
    provider routing beyond OpenAI/Anthropic, promote to a registry.
    """
    global selector_runner
    if selector_runner is None:
        requested_model = os.getenv("WIKI_SELECTOR_MODEL", "")
        if requested_model.startswith("gpt-"):
            selector_runner = OpenAIWikiPageSelector(store=store)
        else:
            selector_runner = AnthropicWikiPageSelector(store=store)
    return selector_runner


def get_answerer_runner() -> AnthropicChemMonAnswerer | Any:
    global answerer_runner
    if answerer_runner is None:
        answerer_runner = AnthropicChemMonAnswerer()
    return answerer_runner


class AskRequest(BaseModel):
    question: str = Field(description="The user's question about ChemMon reporting.")
    max_pages: int = Field(default=6, ge=1, le=10)
    use_graph_expansion: bool = Field(
        default=True,
        description=(
            "If true (default), the answerer also receives short summary "
            "blocks for pages listed in each selected page's `related:` "
            "frontmatter. This recovers cases where the selector picks a "
            "page adjacent to the one containing the answer."
        ),
    )


class PageSummary(BaseModel):
    page_name: str
    title: str
    summary: str
    sources: list[str] = Field(default_factory=list)
    related: list[str] = Field(default_factory=list)
    content: str | None = None


class AskResponse(BaseModel):
    answer: str
    citations: list[str]
    pages_used: list[str]
    pages: list[PageSummary]
    trace: dict[str, Any]


app = FastAPI(
    title="ChemMon Wiki API",
    version="0.1.0",
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
# Only covers models we actually use; unknown models fall back to zero cost.
_MODEL_PRICING_USD_PER_MTOK: dict[str, tuple[float, float]] = {
    # (input_price_per_mtok, output_price_per_mtok)
    "claude-haiku-4-5-20251001": (1.0, 5.0),
    "claude-sonnet-4-6": (3.0, 15.0),
    "claude-opus-4-6": (15.0, 75.0),
    "claude-3-7-sonnet-latest": (3.0, 15.0),
    "gpt-5.4-mini": (0.75, 4.50),
    "gpt-5.4-mini-2026-03-17": (0.75, 4.50),
}


def _compute_call_cost(token_summary: dict[str, Any]) -> float:
    """Compute USD cost for a single LLM call's token summary.

    Returns 0.0 if the model is not in the pricing table (unknown models
    contribute nothing to the aggregated cost rather than crashing).
    """
    model = token_summary.get("model", "")
    prices = _MODEL_PRICING_USD_PER_MTOK.get(model)
    if prices is None:
        return 0.0
    input_price, output_price = prices
    input_tokens = int(token_summary.get("input_tokens", 0) or 0)
    output_tokens = int(token_summary.get("output_tokens", 0) or 0)
    return (input_tokens * input_price + output_tokens * output_price) / 1_000_000


# -------------------------------------------------------------------------
# Graph expansion: summary-only injection of related neighbors
#
# The LLM page selector picks a minimal set of pages from the catalog.
# In practice, the selector sometimes picks a page *adjacent* to the one
# containing the answer — e.g., for an SSD2 question it picks the SSD2
# data-model page, while the specific rule the user asked about lives in
# chemmon-overview. Full-page graph expansion (injecting every linked
# neighbor's content) would recover these misses at the cost of ~3x more
# tokens per query, which defeats the wiki's efficiency argument vs RAG.
#
# Instead, we inject *summary-only* blocks for each selected page's
# curated `related:` frontmatter neighbors. Each block is ~50-150 tokens
# (title + the one-line summary from index.md) rather than the ~1500
# tokens of a full page. The answerer sees "there's also a page X with
# summary Y" — enough to surface the adjacent fact when the summary
# contains it, without ballooning the context window.
#
# This is "Option C" from the research-note / retrieval-architecture
# discussion: related-neighbor summaries, depth=1, curated edges only.
# -------------------------------------------------------------------------


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
    allowed = store.allowed_page_names()

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
            "[RELATED CONTEXT — brief summary of a neighbor page. "
            "Use as peripheral context; the full page is not loaded.]\n"
            f"Title: {neighbor.title}\n"
            f"{summary_text}"
        )
        # Rough token estimate: ~4 chars per token
        block_tokens = max(1, len(content) // 4)
        if total_tokens + block_tokens > max_total_tokens and blocks:
            break
        blocks.append({"page_name": neighbor.name, "content": content, "expansion": True})
        total_tokens += block_tokens

    return blocks


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
        }
        for page in store.catalog()
    ]
    return {"pages": pages, "count": len(pages)}


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
    selector = get_selector_runner()
    if request.max_pages != selector.max_pages:
        selector.max_pages = request.max_pages

    try:
        selection_result = selector.run({"question": request.question})
    except (RuntimeError, ValueError) as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    selector_end = time.perf_counter()

    page_read_start = time.perf_counter()
    pages_raw = [store.read_page(page_name) for page_name in selection_result.pages_used]
    page_contents = [
        {"page_name": page.name, "content": store.clean_content_for_model(page)}
        for page in pages_raw
    ]
    page_read_end = time.perf_counter()

    # Graph expansion: add summary-only blocks for curated neighbors of the
    # selected pages. This recovers cases where the selector picks a page
    # adjacent to the one containing the answer. Controlled by request flag;
    # default on. See _expand_related_summaries for the rationale.
    graph_expansion_start = time.perf_counter()
    expansion_blocks: list[dict[str, Any]] = []
    if request.use_graph_expansion:
        expansion_blocks = _expand_related_summaries(
            selection_result.pages_used,
            store,
            max_neighbors=8,
            max_total_tokens=2000,
        )
    graph_expansion_end = time.perf_counter()

    answerer_input_pages = page_contents + expansion_blocks
    expanded_page_names = [block["page_name"] for block in expansion_blocks]
    pages_used = list(dict.fromkeys([*selection_result.pages_used, *expanded_page_names]))

    answerer_start = time.perf_counter()
    answerer = get_answerer_runner()
    try:
        answer_result = answerer.run(question=request.question, pages=answerer_input_pages)
    except (RuntimeError, ValueError) as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    answerer_end = time.perf_counter()

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
                # Expansion pages were injected as summary-only blocks; return the
                # same short content so citations can be resolved consistently.
                content=expansion_content_by_page.get(page.name),
            )
        )

    allowed_citations = set(pages_used)
    citations: list[str] = []
    for raw_citation in answer_result.citations:
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
    citations = list(dict.fromkeys(citations))

    response = AskResponse(
        answer=answer_result.answer,
        citations=citations,
        pages_used=pages_used,
        pages=pages,
        trace={
            "selection_method": "service-owned llm page selector + answerer",
            "graph_expansion": {
                "enabled": request.use_graph_expansion,
                "neighbors_added": [
                    block["page_name"] for block in expansion_blocks
                ],
                "neighbors_count": len(expansion_blocks),
            },
            "selector": {
                "model": selector.model,
                "tool_trace": selection_result.tool_trace,
                "token_summary": selection_result.token_summary,
                "timing_summary": selection_result.timing_summary,
            },
            "answerer": {
                "model": answerer.model,
                "token_summary": answer_result.token_summary,
                "timing_summary": answer_result.timing_summary,
            },
            "total": {
                "request_wall_time_ms": int((time.perf_counter() - request_started) * 1000),
                "total_llm_calls": (
                    int(selection_result.token_summary["calls"])
                    + int(answer_result.token_summary["calls"])
                ),
                "total_tracked_tokens": (
                    int(selection_result.token_summary["total_tracked_tokens"])
                    + int(answer_result.token_summary["total_tracked_tokens"])
                ),
                "total_cost_usd": round(
                    _compute_call_cost(selection_result.token_summary)
                    + _compute_call_cost(answer_result.token_summary),
                    6,
                ),
            },
            "phase_timings_ms": {
                "selector_total": int((selector_end - selector_start) * 1000),
                "page_read": int((page_read_end - page_read_start) * 1000),
                "graph_expansion": int((graph_expansion_end - graph_expansion_start) * 1000),
                "answerer_total": int((answerer_end - answerer_start) * 1000),
                "overhead": max(
                    0,
                    int((time.perf_counter() - request_started) * 1000)
                    - int((selector_end - selector_start) * 1000)
                    - int((page_read_end - page_read_start) * 1000)
                    - int((graph_expansion_end - graph_expansion_start) * 1000)
                    - int((answerer_end - answerer_start) * 1000),
                ),
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
