"""The chat page served by the API itself at /chat (formerly an nginx container on :8080)."""
from __future__ import annotations

from tests.test_app import request


def test_chat_page_is_served():
    response = request("GET", "/chat")
    assert response.status_code == 200 and "text/html" in response.headers["content-type"]
    assert "ChemMon Wiki Chat" in response.text
    assert 'href="/chat/static/styles.css"' in response.text and 'src="/chat/static/app.js"' in response.text


def test_chat_assets_are_served():
    assert request("GET", "/chat/static/styles.css").status_code == 200
    script = request("GET", "/chat/static/app.js")
    assert script.status_code == 200


def test_chat_asks_the_same_origin_api():
    script = request("GET", "/chat/static/app.js").text
    assert "/api/wiki/ask" not in script and "127.0.0.1:8005" not in script
    assert "/wiki/ask" in script


def test_chat_cannot_be_pointed_at_another_server():
    # A crafted ?api= link must not send questions to, or render answers from, another origin.
    script = request("GET", "/chat/static/app.js").text
    assert 'params.get("api")' not in script and "fetch(\"/wiki/ask\"" in script
