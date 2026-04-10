from __future__ import annotations

import asyncio

import httpx

import wiki_api.app as app_module
from wiki_api.page_selector import PageSelectionResult
from wiki_api.answerer import AnswerResult


async def _request(method: str, path: str, **kwargs: object) -> httpx.Response:
    transport = httpx.ASGITransport(app=app_module.app)
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        return await client.request(method, path, **kwargs)


def request(method: str, path: str, **kwargs: object) -> httpx.Response:
    return asyncio.run(_request(method, path, **kwargs))


class FakeSelector:
    def __init__(self) -> None:
        self.max_pages = 6
        self.model = "fake-claude"
        self.calls: list[dict[str, object]] = []

    def run(self, payload: dict[str, object]) -> PageSelectionResult:
        self.calls.append(payload)
        return PageSelectionResult(
            pages_used=["index.md"],
            tool_trace=[],
            token_summary={
                "model": "fake-claude",
                "calls": 1,
                "input_tokens": 90,
                "output_tokens": 20,
                "cache_creation_input_tokens": 0,
                "cache_read_input_tokens": 0,
                "total_tracked_tokens": 110,
                "per_call": [
                    {
                        "stop_reason": "end_turn",
                        "input_tokens": 90,
                        "output_tokens": 20,
                        "cache_creation_input_tokens": 0,
                        "cache_read_input_tokens": 0,
                        "total_tracked_tokens": 110,
                    }
                ],
            },
            timing_summary={
                "calls": 1,
                "llm_time_ms": 500,
                "selector_wall_time_ms": 550,
                "per_call": [{"call_number": 1, "duration_ms": 500, "stop_reason": "end_turn"}],
            },
        )


class FakeAnswerer:
    def __init__(self) -> None:
        self.model = "fake-claude"
        self.calls: list[dict[str, object]] = []

    def run(self, question: str, pages: list[dict[str, object]]) -> AnswerResult:
        self.calls.append({"question": question, "pages": pages})
        return AnswerResult(
            answer="F33 is mandatory for acrylamide per CHEMMON12.",
            citations=["index.md"],
            token_summary={
                "model": "fake-claude",
                "calls": 1,
                "input_tokens": 200,
                "output_tokens": 50,
                "cache_creation_input_tokens": 0,
                "cache_read_input_tokens": 0,
                "total_tracked_tokens": 250,
                "per_call": [
                    {
                        "stop_reason": "end_turn",
                        "input_tokens": 200,
                        "output_tokens": 50,
                        "cache_creation_input_tokens": 0,
                        "cache_read_input_tokens": 0,
                        "total_tracked_tokens": 250,
                    }
                ],
            },
            timing_summary={
                "calls": 1,
                "llm_time_ms": 600,
                "answerer_wall_time_ms": 650,
                "per_call": [{"call_number": 1, "duration_ms": 600, "stop_reason": "end_turn"}],
            },
        )


class FakeBadAnswerer:
    def __init__(self) -> None:
        self.model = "fake-claude"

    def run(self, question: str, pages: list[dict[str, object]]) -> AnswerResult:
        raise ValueError("Could not extract answer from model response")


def setup_function() -> None:
    app_module.selector_runner = FakeSelector()
    app_module.answerer_runner = FakeAnswerer()


def test_health() -> None:
    response = request("GET", "/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_get_index() -> None:
    response = request("GET", "/wiki/index")
    assert response.status_code == 200
    payload = response.json()
    assert payload["page_name"] == "index.md"
    assert "Wiki Index" in payload["title"]


def test_list_pages_returns_ingested_pages() -> None:
    response = request("GET", "/wiki/pages")
    assert response.status_code == 200
    payload = response.json()
    # After the patterns refactor: 9 original pages + 9 business-rules slice files = 18
    assert payload["count"] >= 16
    names = {p["page_name"] for p in payload["pages"]}
    assert "business-rules.md" in names  # hub
    assert any(n.startswith("business-rules-") for n in names)


def test_get_unknown_page_returns_404() -> None:
    response = request("GET", "/wiki/pages/not-a-real-page.md")
    assert response.status_code == 404


def test_ask_returns_answer_with_citations() -> None:
    response = request(
        "POST",
        "/wiki/ask",
        json={"question": "Do I need F33 for acrylamide?"},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["answer"] == "F33 is mandatory for acrylamide per CHEMMON12."
    assert payload["citations"] == ["index.md"]
    assert "index.md" in payload["pages_used"]
    assert payload["trace"]["selection_method"] == "service-owned llm page selector + answerer"
    assert payload["trace"]["selector"]["model"] == "fake-claude"
    assert payload["trace"]["answerer"]["model"] == "fake-claude"
    assert payload["trace"]["total"]["total_llm_calls"] == 2
    assert app_module.selector_runner.calls[0]["question"] == "Do I need F33 for acrylamide?"


def test_ask_requires_question() -> None:
    response = request("POST", "/wiki/ask", json={})
    assert response.status_code == 422


def test_ask_returns_503_on_answerer_error() -> None:
    app_module.answerer_runner = FakeBadAnswerer()
    response = request(
        "POST",
        "/wiki/ask",
        json={"question": "test question"},
    )
    assert response.status_code == 503


def test_openapi_exposes_ask_endpoint() -> None:
    response = request("GET", "/openapi.json")
    assert response.status_code == 200
    payload = response.json()
    assert "/wiki/ask" in payload["paths"]
    assert "AskRequest" in payload["components"]["schemas"]
    assert "AskResponse" in payload["components"]["schemas"]
