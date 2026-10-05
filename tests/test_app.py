from __future__ import annotations

import asyncio
import json

import httpx
import pytest

import wiki_api.app as app_module
from wiki_api.page_selector import PageSelectionResult
from wiki_api.answerer import AnswerResult
from wiki_api.wiki_store import WikiStore


async def _request(method: str, path: str, **kwargs: object) -> httpx.Response:
    transport = httpx.ASGITransport(app=app_module.app)
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        return await client.request(method, path, **kwargs)


def request(method: str, path: str, **kwargs: object) -> httpx.Response:
    return asyncio.run(_request(method, path, **kwargs))


class FakeSelector:
    def __init__(self) -> None:
        self.max_pages = 6
        self.model_id = "fake-claude"
        self.calls: list[dict[str, object]] = []

    def run(self, payload: dict[str, object]) -> PageSelectionResult:
        self.calls.append(payload)
        return PageSelectionResult(
            pages_used=["contaminant-reporting.md"],
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
        self.model_id = "fake-claude"
        self.calls: list[dict[str, object]] = []

    def run(self, question: str, pages: list[dict[str, object]]) -> AnswerResult:
        self.calls.append({"question": question, "pages": pages})
        return AnswerResult(
            answer="F33 is mandatory for acrylamide per CHEMMON12.",
            citations=["contaminant-reporting.md"],
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
        self.model_id = "fake-claude"

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
    assert payload["citations"] == ["contaminant-reporting.md"]
    assert "contaminant-reporting.md" in payload["pages_used"]
    assert payload["trace"]["selection_method"] == "service-owned llm page selector + answerer"
    assert payload["trace"]["selector"]["model"] == "fake-claude"
    assert payload["trace"]["answerer"]["model"] == "fake-claude"
    assert payload["trace"]["total"]["total_llm_calls"] == 2
    assert app_module.selector_runner.calls[0]["question"] == "Do I need F33 for acrylamide?"


def _parse_sse_events(body: str) -> list[dict[str, object]]:
    events: list[dict[str, object]] = []
    for block in body.strip().split("\n\n"):
        data_lines = [line for line in block.splitlines() if line.startswith("data:")]
        if not data_lines:
            continue
        data = "\n".join(line[len("data:") :].strip() for line in data_lines)
        events.append(json.loads(data))
    return events


async def _stream_body(path: str, *, payload: dict[str, object]) -> tuple[int, str, str]:
    transport = httpx.ASGITransport(app=app_module.app)
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        async with client.stream("POST", path, json=payload) as response:
            body = (await response.aread()).decode("utf-8")
            content_type = response.headers.get("content-type", "")
            return response.status_code, content_type, body


def test_ask_streams_answer_when_requested() -> None:
    class FakeStreamingAnswerer:
        def __init__(self) -> None:
            self.model_id = "fake-claude"

        def stream(self, question: str, pages: list[dict[str, object]]):  # type: ignore[no-untyped-def]
            raw_json_1 = '{"answer":"F33 is mandatory for'
            raw_json_2 = ' acrylamide per CHEMMON12.","citations":["contaminant-reporting.md"]}'
            yield {"type": "delta", "text": raw_json_1}
            yield {"type": "delta", "text": raw_json_2}
            yield {
                "type": "final",
                "result": AnswerResult(
                    answer="F33 is mandatory for acrylamide per CHEMMON12.",
                    citations=["contaminant-reporting.md"],
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
                ),
            }

    app_module.answerer_runner = FakeStreamingAnswerer()

    status, content_type, body = asyncio.run(
        _stream_body(
            "/wiki/ask",
            payload={"question": "Do I need F33 for acrylamide?", "stream": True},
        )
    )
    assert status == 200
    assert content_type.startswith("text/event-stream")

    events = _parse_sse_events(body)
    assert events[0]["type"] == "meta"
    assert "contaminant-reporting.md" in events[0]["pages_used"]

    streamed_answer = "".join(e["text"] for e in events if e["type"] == "delta")
    assert streamed_answer == "F33 is mandatory for acrylamide per CHEMMON12."

    done = [e for e in events if e["type"] == "done"][0]
    response = done["response"]
    assert response["answer"] == "F33 is mandatory for acrylamide per CHEMMON12."
    assert response["citations"] == ["contaminant-reporting.md"]


@pytest.mark.parametrize("max_pages,expected_neighbors", [(1, []), (2, ["b.md"])])
def test_ask_includes_graph_expansion_pages_in_metadata(tmp_path, monkeypatch, max_pages, expected_neighbors) -> None:
    """Graph expansion adds neighbor summaries; response metadata must reflect them."""

    (tmp_path / "wiki" / "chemmon-guidance").mkdir(parents=True, exist_ok=True)

    (tmp_path / "index.md").write_text(
        "\n".join(
            [
                "---",
                'title: "Wiki Index"',
                'last_updated: "2026-04-12"',
                "---",
                "",
                "# Index",
                "",
                "- [A](wiki/chemmon-guidance/a.md): Page A summary",
                "- [B](wiki/chemmon-guidance/b.md): Page B summary",
                "",
            ]
        ),
        encoding="utf-8",
    )
    (tmp_path / "log.md").write_text("# Log\n", encoding="utf-8")

    (tmp_path / "wiki" / "chemmon-guidance" / "a.md").write_text(
        "\n".join(
            [
                "---",
                'title: "A"',
                'type: "reference"',
                'domain: "all"',
                'last_updated: "2026-04-12"',
                "related:",
                '  - "[[b]]"',
                "---",
                "",
                "# A",
                "",
                "Body A.",
                "",
            ]
        ),
        encoding="utf-8",
    )
    (tmp_path / "wiki" / "chemmon-guidance" / "b.md").write_text(
        "\n".join(
            [
                "---",
                'title: "B"',
                'type: "reference"',
                'domain: "all"',
                'last_updated: "2026-04-12"',
                "---",
                "",
                "# B",
                "",
                "Body B.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    monkeypatch.setattr(app_module, "store", WikiStore(tmp_path))

    class SelectorWithRelated:
        def __init__(self) -> None:
            self.max_pages = 6
            self.model_id = "fake-claude"

        def run(self, payload: dict[str, object]) -> PageSelectionResult:
            return PageSelectionResult(
                pages_used=["index.md", "a.md"],
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

    class AnswererCitingExpansion:
        def __init__(self) -> None:
            self.model_id = "fake-claude"

        def run(self, question: str, pages: list[dict[str, object]]) -> AnswerResult:
            return AnswerResult(
                answer="Answer based on expansion.",
                citations=["b.md"],
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

    app_module.selector_runner = SelectorWithRelated()
    app_module.answerer_runner = AnswererCitingExpansion()

    response = request("POST", "/wiki/ask", json={"question": "test", "max_pages": max_pages, "use_graph_expansion": True})
    assert response.status_code == 200
    payload = response.json()
    assert payload["citations"] == []  # Summaries cannot be cited as evidence.
    assert payload["trace"]["graph_expansion"]["neighbors_added"] == expected_neighbors
    assert payload["pages_used"] == ["a.md", *expected_neighbors]
    assert len(payload["pages"]) <= max_pages
    assert app_module.selector_runner.max_pages == 6
    if expected_neighbors:
        assert payload["pages"][1]["evidence_kind"] == "summary"
        assert "Body B" not in payload["pages"][1]["content"]


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


@pytest.mark.parametrize("name", ["README.md", "PROJECT_CONTEXT.md", "SCHEMA.md", "INGEST_WORKFLOW.md", "2026-10-05-foodex2-parity.md"])
def test_orientation_navigation_targets_are_served(name):
    response = request("GET", "/wiki/pages/" + name)
    assert response.status_code == 200
    assert response.json()["type"] == "orientation"
    assert response.json()["content"]


def test_catalog_contains_navigation_metadata():
    pages = request("GET", "/wiki/pages").json()["pages"]
    assert any(p["type"] == "orientation" for p in pages)
    assert any(p["type"] == "domain-guide" and p["domain"] == "vmpr" for p in pages)
    assert all("type" in p and "domain" in p for p in pages)


def test_search_finds_body_terms_and_respects_domain():
    results = request("GET", "/wiki/search", params={"q": "A07VF", "domain": "vmpr"}).json()
    names = {p["page_name"] for p in results["pages"]}
    assert "ssd2-matrix-vmpr-coding.md" in names
    assert all(p["domain"] == "vmpr" for p in results["pages"])
    assert request("GET", "/wiki/search", params={"q": "nonexistent987654"}).json()["count"] == 0


def test_backlinks_route():
    result = request("GET", "/wiki/pages/ssd2-matrix-vmpr-coding.md/backlinks")
    assert result.status_code == 200
    assert "vmpr-reporting.md" in result.json()["backlinks"]
    assert request("GET", "/wiki/pages/missing.md/backlinks").status_code == 404


def test_request_budget_is_local_and_expansion_is_opt_in():
    result = request("POST", "/wiki/ask", json={"question": "test", "max_pages": 1}).json()
    assert result["pages_used"] == ["contaminant-reporting.md"]
    assert result["trace"]["graph_expansion"]["enabled"] is False
    assert app_module.selector_runner.calls[0]["max_pages"] == 1
    assert app_module.selector_runner.max_pages == 6
    assert app_module.answerer_runner.calls[0]["pages"][0]["evidence_kind"] == "full"


@pytest.mark.parametrize("stream", [False, True])
def test_no_evidence_does_not_call_answerer(stream):
    class EmptySelector(FakeSelector):
        def run(self, payload):
            result = super().run(payload)
            return PageSelectionResult([], result.tool_trace, result.token_summary, result.timing_summary)
    app_module.selector_runner = EmptySelector()
    response = request("POST", "/wiki/ask", json={"question": "test", "stream": stream})
    assert response.status_code == 200
    result = _parse_sse_events(response.text)[-1]["response"] if stream else response.json()
    assert result["pages_used"] == []
    assert result["citations"] == []
    assert "No relevant wiki evidence" in result["answer"]
    assert result["trace"]["answerer"]["token_summary"]["calls"] == 0
    assert app_module.answerer_runner.calls == []


@pytest.mark.parametrize("question", ["", "   ", "\n"])
def test_ask_rejects_blank_questions(question):
    assert request("POST", "/wiki/ask", json={"question": question}).status_code == 422


def test_select_is_inspectable_and_never_calls_answerer():
    response = request('POST', '/wiki/select', json={'question': 'test', 'max_pages': 1})
    assert response.status_code == 200
    result = response.json()
    assert result['pages_used'] == ['contaminant-reporting.md']
    assert 'source_pages' in result['pages'][0]
    assert len(result['pages'][0]['sha256']) == 64
    assert 'content' not in result['pages'][0]
    assert result['pages'][0]['citable'] is False
    assert result['pages'][0]['evidence_kind'] == 'selection'
    assert app_module.answerer_runner.calls == []


@pytest.mark.parametrize('limit', [1, 2, 6])
def test_context_pack_counts_policy_and_has_no_answer_call(limit):
    response = request('POST', '/wiki/context-pack', json={'question': 'test', 'max_pages': limit})
    assert response.status_code == 200
    result = response.json()
    assert len(result['pages']) <= limit
    assert result['pages'][0]['evidence_kind'] == 'policy'
    assert result['pages'][0]['citable'] is False
    assert result['trace']['answerer_calls'] == 0
    assert 'answer' not in result
    assert 'RUNTIME_POLICY.md' not in result['citable_pages']
    assert app_module.answerer_runner.calls == []
    if limit == 1:
        assert app_module.selector_runner.calls == []
        assert result['status'] == 'budget_exhausted'
        assert result['citable_pages'] == []
    else:
        assert app_module.selector_runner.calls[0]['max_pages'] == limit - 1
        assert result['citable_pages'] == ['contaminant-reporting.md']
        assert result['pages'][1]['evidence_kind'] == 'full'
        assert result['pages'][1]['sources']
        assert 'source_pages' in result['pages'][1]
        assert result['pages'][1]['sha256']


def test_context_pack_omits_whole_pages_that_exceed_text_budget():
    result = request('POST', '/wiki/context-pack', json={'question': 'test', 'max_chars': 2000}).json()
    assert result['status'] == 'budget_exhausted'
    assert result['budget']['used_chars'] <= 2000
    assert result['citable_pages'] == []
    assert result['omitted_pages'] == [{'page_name': 'contaminant-reporting.md', 'reason': 'character_budget'}]
    assert result['pages'][0]['content'].endswith('authoritative evidence.\n')


def test_request_model_overrides_do_not_change_defaults(monkeypatch):
    selector_default, answerer_default = app_module.selector_runner, app_module.answerer_runner
    created = []
    def selector_factory(**kwargs):
        obj = FakeSelector()
        obj.model_id = kwargs['model_str']
        created.append(obj)
        return obj
    def answerer_factory(**kwargs):
        obj = FakeAnswerer()
        obj.model_id = kwargs['model_str']
        return obj
    monkeypatch.setattr(app_module, 'WikiPageSelector', selector_factory)
    monkeypatch.setattr(app_module, 'WikiAnswerer', answerer_factory)
    result = request('POST', '/wiki/ask', json={'question': 'test', 'selector_model': 'test/selector', 'answerer_model': 'test/answer'}).json()
    assert result['trace']['selector']['model'] == 'test/selector'
    assert result['trace']['answerer']['model'] == 'test/answer'
    assert app_module.selector_runner is selector_default
    assert app_module.answerer_runner is answerer_default
    assert selector_default.calls == answerer_default.calls == []
    request('POST', '/wiki/select', json={'question': 'test'})
    assert len(selector_default.calls) == 1


def test_unknown_pricing_is_not_reported_as_free():
    result = request('POST', '/wiki/ask', json={'question': 'test'}).json()
    assert result['trace']['total']['total_cost_usd'] is None
    assert app_module._compute_call_cost({'calls': 0}) == 0
    assert app_module._compute_call_cost({'model': 'unknown', 'calls': 1}) is None


@pytest.mark.parametrize('endpoint', ['select', 'context-pack', 'ask'])
def test_invalid_selection_requests_are_rejected(endpoint):
    for payload in [{'question': ' '}, {'question': 'q', 'max_pages': 0}, {'question': 'q', 'selector_model': 'a b'}]:
        assert request('POST', '/wiki/' + endpoint, json=payload).status_code == 422


def test_review_status_exposes_scope_and_remaining_work():
    response = request('GET', '/wiki/review-status')
    assert response.status_code == 200
    status = response.json()
    assert status['source_review']['status'] == 'current'
    assert status['source_review']['scope']
    assert status['source_review']['limitations']
    # A completed review can legitimately have no open findings. The endpoint
    # must expose the manifest's actual backlog, including the empty case.
    record = json.loads((app_module.store.root/'docs/source-review.json').read_text())
    assert status['source_review']['open_findings'] == [
        finding for finding in record['findings'] if finding['status'] == 'open'
    ]
    assert status['source_review']['resolved_count'] == sum(
        finding['status'] == 'resolved' for finding in record['findings']
    )
    assert status['rule_inventory']['source_counts']['GBR'] == 92


def test_context_pack_preserves_exact_source_locators():
    class RulesSelector(FakeSelector):
        def run(self, payload):
            r = super().run(payload)
            return PageSelectionResult(['business-rules-gbr.md'], r.tool_trace, r.token_summary, r.timing_summary)
    app_module.selector_runner = RulesSelector()
    result = request('POST', '/wiki/context-pack', json={'question': 'GBR28', 'max_pages': 2}).json()
    page = result['pages'][1]
    assert page['source_pages'] == ['pp. 98-112, Table 9']
    assert 'Source:' in page['content']
    assert 'p. 103' in page['content']


def test_provider_failure_returns_service_error_without_provider_details():
    from openai import APIConnectionError
    class UnavailableSelector(FakeSelector):
        def run(self, payload):
            raise APIConnectionError(request=httpx.Request('POST', 'https://provider.example'), message='private diagnostic')
    app_module.selector_runner = UnavailableSelector()
    response = request('POST', '/wiki/context-pack', json={'question': 'test'})
    assert response.status_code == 503
    assert 'private diagnostic' not in response.text
