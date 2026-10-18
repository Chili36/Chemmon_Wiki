"""The MCP endpoint at /mcp on the API: exact path, Host allowlist, REST API untouched."""
from __future__ import annotations

import pytest
from starlette.testclient import TestClient

import wiki_api.app as app_module
from wiki_api import mcp_server

HEADERS = {"Content-Type": "application/json", "Accept": "application/json, text/event-stream"}
TOOLS_LIST = {"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}}


@pytest.fixture(scope="module")
def client():
    # One lifespan per module: a session manager can only be run once.
    with TestClient(app_module.app, base_url="http://localhost:8005") as test_client:
        yield test_client


def test_post_to_exact_path_is_not_redirected(client):
    response = client.post("/mcp", json=TOOLS_LIST, headers=HEADERS, follow_redirects=False)
    assert response.status_code == 200
    assert {t["name"] for t in response.json()["result"]["tools"]} == {
        "search_guidance", "get_guidance_page", "get_reporting_context", "ask_guidance"}


def test_host_allowlist(client):
    docker = client.post("/mcp", json=TOOLS_LIST, headers={**HEADERS, "Host": "host.docker.internal:8005"})
    assert docker.status_code == 200
    assert client.post("/mcp", json=TOOLS_LIST, headers={**HEADERS, "Host": "evil.example"}).status_code == 421


def test_extra_hosts_from_env(monkeypatch):
    monkeypatch.setenv("WIKI_MCP_ALLOWED_HOSTS", "wiki.lan, ")
    assert {"wiki.lan", "wiki.lan:*", "host.docker.internal:*", "localhost"} <= set(mcp_server.allowed_hosts())
    assert "" not in mcp_server.allowed_hosts()


def test_rest_api_is_unaffected_by_the_allowlist(client):
    assert client.get("/health", headers={"Host": "evil.example"}).status_code == 200
