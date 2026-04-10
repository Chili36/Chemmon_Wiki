from __future__ import annotations

import json
import logging
import re
from pathlib import Path
import time
from typing import Any

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from .answerer import AnthropicChemMonAnswerer
from .page_selector import AnthropicWikiPageSelector, build_fast_path_result
from .wiki_store import WikiStore


REPO_ROOT = Path(__file__).resolve().parent.parent
store = WikiStore(REPO_ROOT)
selector_runner: AnthropicWikiPageSelector | Any | None = None
answerer_runner: AnthropicChemMonAnswerer | Any | None = None
logger = logging.getLogger("wiki_api")
if not logging.getLogger().handlers:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")


def get_selector_runner() -> AnthropicWikiPageSelector | Any:
    global selector_runner
    if selector_runner is None:
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


# -------------------------------------------------------------------------
# Deterministic page-selection fast-path
#
# For stable, repetitive queries (e.g. rule-ID lookups or domain-keyword
# questions), the LLM page-selector is unnecessary overhead. This fast-path
# short-circuits the selector call when a question matches a known pattern.
# Each hit returns the minimal page set the answerer needs.
#
# The rule-ID → slice map is the inverse of the canonical allocation in
# wiki/chemmon-guidance/business-rules-*.md; a CHEMMON number can map to
# more than one slice when the source guidance uses letter-suffixed variants
# (e.g. CHEMMON43 is cross-cutting, CHEMMON43_b is in additives).
#
# Returns None for non-matching questions, falling through to the LLM selector.
# -------------------------------------------------------------------------

_SLICE_RULES: dict[str, list[int]] = {
    "business-rules-cross-cutting.md": [
        1, 3, 4, 5, 6, 7, 8, 22, 23, 24, 26, 27, 30, 33, 34, 35, 37, 40, 41,
        42, 43, 44, 45, 46, 48, 50, 51, 57, 58, 62, 65, 66, 67, 68, 77, 78,
        79, 82, 85, 94, 97, 99, 103,
    ],
    "business-rules-vmpr.md": [28, 31, 32, 73, 76, 91, 92, 93, 96, 100, 102],
    "business-rules-pesticide.md": [
        2, 3, 52, 56, 59, 60, 61, 70, 72, 90, 95, 101, 104,
    ],
    "business-rules-contaminant.md": [
        9, 10, 11, 12, 14, 15, 17, 18, 19, 20, 21, 54, 69, 71, 80, 83, 84,
        98, 105,
    ],
    "business-rules-additives.md": [
        36, 39, 43, 84, 86, 87, 88, 89, 106, 107, 108, 109,
    ],
    "business-rules-baby-food.md": [55, 63],
}

_CHEMMON_RULE_TO_SLICES: dict[int, list[str]] = {}
for _slice_name, _rule_ids in _SLICE_RULES.items():
    for _rid in _rule_ids:
        _CHEMMON_RULE_TO_SLICES.setdefault(_rid, []).append(_slice_name)

_CHEMMON_RULE_REGEX = re.compile(r"\bCHEMMON\s*0*(\d+)", re.IGNORECASE)

_KEYWORD_PATTERNS: list[tuple[re.Pattern[str], list[str]]] = [
    (
        re.compile(
            r"\b(?:vmpr|wild\s+game|insects?|novel\s+food|veterinary\s+(?:drug|residues?))\b",
            re.IGNORECASE,
        ),
        [
            "business-rules-vmpr.md",
            "business-rules-cross-cutting.md",
            "vmpr-reporting.md",
        ],
    ),
    (
        re.compile(
            r"\b(?:pesticide|mrl|ppp|plant\s+protection|copper)\b",
            re.IGNORECASE,
        ),
        [
            "business-rules-pesticide.md",
            "business-rules-cross-cutting.md",
            "pesticide-reporting.md",
        ],
    ),
    (
        re.compile(r"\b(?:baby\s+food|infant|follow-on)\b", re.IGNORECASE),
        [
            "business-rules-baby-food.md",
            "baby-food-reporting.md",
        ],
    ),
    (
        re.compile(
            r"\b(?:food\s+additive|flavouring|sweetener|F33)\b",
            re.IGNORECASE,
        ),
        [
            "business-rules-additives.md",
            "business-rules-cross-cutting.md",
            "food-additives-reporting.md",
        ],
    ),
    (
        re.compile(
            r"\b(?:contaminant|acrylamide|dioxin|pcb|bfr|mycotoxin|pah|arsenic|mineral\s+oil|bisphenol|chlorate|3-mcpd|nitrate)\b",
            re.IGNORECASE,
        ),
        [
            "business-rules-contaminant.md",
            "business-rules-cross-cutting.md",
            "contaminant-reporting.md",
        ],
    ),
    (
        re.compile(
            r"\b(?:legal\s+limit|maximum\s+level|maximum\s+permitted\s+level|\bmpl\b)\b",
            re.IGNORECASE,
        ),
        ["business-rules-legal-limits.md"],
    ),
]


def _try_deterministic_selection(question: str) -> list[str] | None:
    """Return a minimal page set for known question patterns, or None."""
    # Rule-ID lookup takes priority over keyword matching. The regex only
    # captures \d+, so int() cannot fail.
    rule_matches = _CHEMMON_RULE_REGEX.findall(question)
    if rule_matches:
        pages: list[str] = []
        for match in rule_matches:
            slices = _CHEMMON_RULE_TO_SLICES.get(int(match))
            if slices:
                pages.extend(slices)
        if pages:
            if "business-rules-cross-cutting.md" not in pages:
                pages.append("business-rules-cross-cutting.md")
            return list(dict.fromkeys(pages))

    for pattern, slices in _KEYWORD_PATTERNS:
        if pattern.search(question):
            return list(slices)

    return None


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

    fast_path_pages = _try_deterministic_selection(request.question)
    if fast_path_pages is not None:
        selection_result = build_fast_path_result(fast_path_pages)
        selector_model_for_trace = "fast-path"
        selection_method = "deterministic fast-path (heuristic) + llm answerer"
    else:
        selector = get_selector_runner()
        if request.max_pages != selector.max_pages:
            selector.max_pages = request.max_pages
        try:
            selection_result = selector.run({"question": request.question})
        except (RuntimeError, ValueError) as exc:
            raise HTTPException(status_code=503, detail=str(exc)) from exc
        selector_model_for_trace = selector.model
        selection_method = "service-owned llm page selector + answerer"

    pages_raw = [store.read_page(page_name) for page_name in selection_result.pages_used]
    page_contents = [
        {"page_name": page.name, "content": store.clean_content_for_model(page)}
        for page in pages_raw
    ]

    answerer = get_answerer_runner()
    try:
        answer_result = answerer.run(question=request.question, pages=page_contents)
    except (RuntimeError, ValueError) as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    pages = [
        PageSummary(
            page_name=page.name,
            title=page.title,
            summary=page.summary,
            sources=page.sources,
            related=page.related,
            content=store.clean_content_for_model(page),
        )
        for page in pages_raw
    ]

    response = AskResponse(
        answer=answer_result.answer,
        citations=answer_result.citations,
        pages_used=selection_result.pages_used,
        pages=pages,
        trace={
            "selection_method": selection_method,
            "selector": {
                "model": selector_model_for_trace,
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
