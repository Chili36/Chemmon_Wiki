from __future__ import annotations

import json
import logging
from pathlib import Path
import time
from typing import Any

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from .answerer import AnthropicChemMonAnswerer
from .page_selector import AnthropicWikiPageSelector
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

    selector = get_selector_runner()
    if request.max_pages != selector.max_pages:
        selector.max_pages = request.max_pages

    try:
        selection_result = selector.run({"question": request.question})
    except (RuntimeError, ValueError) as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

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
            "selection_method": "service-owned llm page selector + answerer",
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
