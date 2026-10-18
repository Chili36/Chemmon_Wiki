"""Jev page selector: request shape, score ranking and failure handling (no network)."""
from __future__ import annotations

import json
from pathlib import Path

import httpx
import pytest

from wiki_api.jev_selector import (
    DEFAULT_JEV_MODEL, JevWikiPageSelector, LEVELS, build_request, make_selector, ranked_pages,
)
from wiki_api.page_selector import WikiPageSelector
from wiki_api.wiki_store import WikiStore

ROOT = Path(__file__).resolve().parents[1]
STORE = WikiStore(ROOT)


def respond(scores: dict[str, float], usage=None, status=200):
    """A mock TypeSafe API scoring pages by filename (unlisted pages score 0)."""
    def handler(request: httpx.Request) -> httpx.Response:
        body = json.loads(request.content)
        assert request.headers["Authorization"] == "Bearer test-key"
        assert body["model"] == DEFAULT_JEV_MODEL
        answers = {key: {"type": "score", "score": scores.get(q["instructions"]["page"]["filename"], 0.0)}
                   for key, q in body["questions"].items()}
        return httpx.Response(status, json={"model": body["model"], "answers": answers,
                                            "usage": usage or {"input_tokens": 9000, "output_tokens": 0}})
    return httpx.Client(transport=httpx.MockTransport(handler))


def test_one_score_question_per_catalogue_page():
    body, mapping = build_request(STORE, "How do I report LOQ?", DEFAULT_JEV_MODEL)
    assert len(body["questions"]) == len(STORE.catalog()) == len(mapping)
    question = body["questions"]["page_0"]
    assert question["type"] == "score" and question["criteria"] == LEVELS
    assert body["state"]["question"] == "How do I report LOQ?"


def test_pages_ranked_by_score_above_threshold_and_capped(monkeypatch):
    monkeypatch.setenv("TYPESAFE_API_KEY", "test-key")
    client = respond({"pesticide-reporting.md": 3.0, "ssd2-analysis-parameter-coding.md": 2.0,
                      "contaminant-reporting.md": 1.0, "pesticide-residue-definition-by-matrix.md": 2.5})
    result = JevWikiPageSelector(store=STORE, client=client).run({"question": "q", "max_pages": 2})
    # 1.0/3 = 0.33 is below the 0.35 threshold; the cap keeps the two best.
    assert result.pages_used == ["pesticide-reporting.md", "pesticide-residue-definition-by-matrix.md"]
    assert result.token_summary["model"] == DEFAULT_JEV_MODEL
    assert result.token_summary["input_tokens"] == 9000


def test_nothing_relevant_selects_nothing(monkeypatch):
    monkeypatch.setenv("TYPESAFE_API_KEY", "test-key")
    result = JevWikiPageSelector(store=STORE, client=respond({})).run({"question": "q"})
    assert result.pages_used == []


@pytest.mark.parametrize("answers", [
    {"page_0": {"type": "score", "score": 5}},
    {"page_0": {"type": "score", "score": float("nan")}},
    {"page_0": {"type": "choice", "score": 1}},
    {},
])
def test_invalid_answers_are_rejected(answers):
    mapping = {"page_0": "a.md"}
    with pytest.raises(ValueError):
        ranked_pages({"answers": answers}, mapping)


def test_provider_failure_hides_the_upstream_body(monkeypatch):
    monkeypatch.setenv("TYPESAFE_API_KEY", "test-key")
    client = httpx.Client(transport=httpx.MockTransport(lambda r: httpx.Response(500, text="secret upstream detail")))
    with pytest.raises(RuntimeError) as info:
        JevWikiPageSelector(store=STORE, client=client).run({"question": "q"})
    assert "secret" not in str(info.value)


def test_missing_key_is_reported(monkeypatch):
    monkeypatch.delenv("TYPESAFE_API_KEY", raising=False)
    with pytest.raises(RuntimeError, match="TYPESAFE_API_KEY"):
        JevWikiPageSelector(store=STORE, client=respond({})).run({"question": "q"})


def test_factory_routes_jev_models_and_keeps_chat_default(monkeypatch):
    assert isinstance(make_selector(store=STORE, model_str="jev-1.13.0"), JevWikiPageSelector)
    monkeypatch.setenv("ANTHROPIC_API_KEY", "x")
    assert isinstance(make_selector(store=STORE, model_str="anthropic/claude-haiku-5-5"), WikiPageSelector)


def test_internal_client_is_closed_after_each_request(monkeypatch):
    monkeypatch.setenv("TYPESAFE_API_KEY", "test-key")
    created = []
    real = httpx.Client
    transport = respond({})._transport  # built before Client is patched

    class Tracking(real):
        def __init__(self, *args, **kwargs):
            kwargs["transport"] = transport
            super().__init__(*args, **kwargs)
            created.append(self)
    monkeypatch.setattr("wiki_api.jev_selector.httpx.Client", Tracking)
    selector = JevWikiPageSelector(store=STORE)
    selector.run({"question": "q"})
    selector.run({"question": "q"})
    assert len(created) == 2 and all(c.is_closed for c in created)


def test_eval_report_records_the_prompt_each_selector_used():
    import hashlib
    from tools.evaluate import run_suite
    from wiki_api.jev_selector import PROMPT_FINGERPRINT
    from wiki_api.page_selector import SELECTION_SYSTEM_PROMPT
    dataset = json.loads((ROOT / "evals" / "cases.json").read_text())
    report = run_suite(STORE, dataset, mode="select", models=["anthropic/claude-haiku-5-5", "jev-1.13.0"])
    by_model = report["prompt_sha256_by_model"]
    assert by_model["jev-1.13.0"] == hashlib.sha256(PROMPT_FINGERPRINT.encode()).hexdigest()
    assert by_model["anthropic/claude-haiku-5-5"] == hashlib.sha256(SELECTION_SYSTEM_PROMPT.encode()).hexdigest()
