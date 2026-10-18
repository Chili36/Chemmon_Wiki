"""MCP tools: same results as the HTTP endpoints, errors as tool errors (no network)."""
from __future__ import annotations

import asyncio
import dataclasses
import json

import anthropic
import httpx
import pytest
from mcp import Client

import wiki_api.app as app_module
from wiki_api.mcp_server import mcp


def run(coro):
    return asyncio.run(coro)


def call(name: str, args: dict):
    async def go():
        async with Client(mcp) as client:
            return await client.call_tool(name, args)
    return run(go())


def as_json(value):
    """What an HTTP or MCP client receives (tuples become lists)."""
    return json.loads(json.dumps(value))


def tool_names() -> set[str]:
    async def go():
        async with Client(mcp) as client:
            return {tool.name for tool in (await client.list_tools()).tools}
    return run(go())


def test_tools_are_listed():
    assert {"search_guidance", "get_guidance_page"} <= tool_names()


def test_search_matches_the_http_endpoint():
    result = call("search_guidance", {"query": "acrylamide", "limit": 5})
    assert not result.is_error
    assert result.structured_content == as_json(app_module.search_pages(q="acrylamide", domain=None, limit=5))


def test_page_matches_the_http_endpoint():
    result = call("get_guidance_page", {"page_name": "contaminant-reporting.md"})
    assert not result.is_error
    assert result.structured_content == as_json(app_module.get_page("contaminant-reporting.md", include_content=True))


def test_unknown_page_is_a_tool_error():
    result = call("get_guidance_page", {"page_name": "no-such-page.md"})
    assert result.is_error and "no-such-page" in result.content[0].text


def test_limit_out_of_range_is_rejected():
    assert call("search_guidance", {"query": "x", "limit": 101}).is_error


@pytest.fixture
def fakes():
    from tests.test_app import FakeAnswerer, FakeSelector
    saved = app_module.selector_runner, app_module.answerer_runner
    app_module.selector_runner, app_module.answerer_runner = FakeSelector(), FakeAnswerer()
    yield app_module.selector_runner
    app_module.selector_runner, app_module.answerer_runner = saved


def test_all_four_tools_are_listed():
    assert tool_names() == {"search_guidance", "get_guidance_page", "get_reporting_context", "ask_guidance"}


def test_context_matches_the_http_endpoint(fakes):
    got = call("get_reporting_context", {"question": "acrylamide F33", "max_pages": 4}).structured_content
    expected = as_json(app_module.context_pack(app_module.ContextPackRequest(question="acrylamide F33", max_pages=4)))
    assert "trace" not in got and "cost_usd" in got
    assert got["pages"] == expected["pages"] and got["citable_pages"] == expected["citable_pages"]
    assert got == {**{k: v for k, v in expected.items() if k != "trace"}, "cost_usd": got["cost_usd"]}


def test_ask_returns_answer_and_citations(fakes):
    got = call("ask_guidance", {"question": "Is F33 mandatory for acrylamide?"}).structured_content
    assert got["answer"] == "F33 is mandatory for acrylamide per CHEMMON12."
    assert got["citations"] == ["contaminant-reporting.md"] and got["pages_used"] == ["contaminant-reporting.md"]
    assert set(got) == {"answer", "citations", "pages_used", "cost_usd"}


def test_ask_with_no_selected_pages(fakes):
    selected = fakes.run({"question": "q", "max_pages": 6})
    fakes.run = lambda payload: dataclasses.replace(selected, pages_used=[])
    result = call("ask_guidance", {"question": "unrelated"})
    assert not result.is_error
    assert result.structured_content["citations"] == [] and result.structured_content["pages_used"] == []


def test_provider_failure_is_a_safe_tool_error(fakes):
    def fail(payload):
        raise anthropic.APIError("secret upstream detail", httpx.Request("POST", "https://api.anthropic.com"), body=None)
    fakes.run = fail
    result = call("ask_guidance", {"question": "q"})
    assert result.is_error and "Model provider request failed" in result.content[0].text
    assert "secret" not in result.content[0].text


def test_max_pages_out_of_range_is_rejected():
    assert call("ask_guidance", {"question": "q", "max_pages": 11}).is_error
    assert call("get_reporting_context", {"question": "q", "max_pages": 0}).is_error
