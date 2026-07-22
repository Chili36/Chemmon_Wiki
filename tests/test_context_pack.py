"""Tests for /wiki/context-pack and its deterministic selector.

These run against the real wiki content in the repo: context-pack makes no LLM
call, so there is nothing to stub, and asserting on real pages catches
frontmatter drift (a page losing its `domain:` tag) that a fixture would hide.
"""

from __future__ import annotations

import asyncio

import httpx

import wiki_api.app as app_module
from wiki_api.context_pack import normalize_domain, select_pages
from wiki_api.wiki_store import WikiStore


async def _request(method: str, path: str, **kwargs: object) -> httpx.Response:
    transport = httpx.ASGITransport(app=app_module.app)
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        return await client.request(method, path, **kwargs)


def request(method: str, path: str, **kwargs: object) -> httpx.Response:
    return asyncio.run(_request(method, path, **kwargs))


def _store() -> WikiStore:
    return app_module.store


# --- domain normalisation -------------------------------------------------


def test_normalize_domain_accepts_wiki_enum():
    assert normalize_domain("pesticide") == "pesticide"
    assert normalize_domain("vmpr") == "vmpr"
    assert normalize_domain("contaminant") == "contaminant"
    assert normalize_domain("additives") == "additives"
    assert normalize_domain("baby-food") == "baby-food"


def test_normalize_domain_accepts_caller_vocabularies():
    """DMT's PARAM domains and the EFSA hierarchy names both map through."""
    assert normalize_domain("PESTICIDES") == "pesticide"
    assert normalize_domain("CONTAMINANTS") == "contaminant"
    assert normalize_domain("pestParam") == "pesticide"
    assert normalize_domain("vmprParam") == "vmpr"
    assert normalize_domain("chemAnalysis") == "contaminant"


def test_flavourings_maps_to_additives():
    """SCHEMA.md folds flavourings into `additives`; callers split them."""
    assert normalize_domain("FLAVOURINGS") == "additives"
    assert normalize_domain("flavAnalysis") == "additives"
    assert normalize_domain("ADDITIVES") == "additives"


def test_normalize_domain_unknown_is_none():
    assert normalize_domain("not-a-domain") is None
    assert normalize_domain("") is None
    assert normalize_domain(None) is None


# --- store ----------------------------------------------------------------


def test_store_parses_domain_frontmatter():
    store = _store()
    assert store.read_page("pesticide-reporting.md").domain == "pesticide"
    assert store.read_page("business-rules-vmpr.md").domain == "vmpr"
    # Pages that apply everywhere declare `all`.
    assert store.read_page("reporting-flags.md").domain == "all"


def test_every_page_declares_a_known_domain():
    """Guards SCHEMA.md's required-field contract across the whole corpus."""
    known = {"all", "vmpr", "pesticide", "contaminant", "additives", "baby-food", "cross-cutting"}
    for page in _store().catalog():
        assert page.domain in known, f"{page.name} has unexpected domain {page.domain!r}"


# --- selection ------------------------------------------------------------


def test_domain_pages_are_selected_first():
    selected, trace = select_pages(
        _store(), search_term="Chlorpyrifos", domain="PESTICIDES", max_pages=6
    )
    names = [item.page.name for item in selected]
    assert "pesticide-reporting.md" in names
    assert "business-rules-pesticide.md" in names
    # Domain-tier pages precede any relevance fill.
    reasons = [item.selected_by for item in selected]
    assert reasons[0] == "domain"
    assert trace["counts"]["domain"] >= 2


def test_other_domain_pages_are_excluded():
    """A pesticide query must not pull baby-food or VMPR rules."""
    selected, _ = select_pages(
        _store(), search_term="Chlorpyrifos", domain="PESTICIDES", max_pages=10
    )
    domains = {item.page.domain for item in selected}
    assert domains <= {"pesticide", "cross-cutting", "all"}


def test_topics_surface_the_parameter_coding_page():
    """Topic hints are how a caller reaches reference pages tagged `all`
    without naming page files."""
    selected, _ = select_pages(
        _store(),
        search_term="Tujon (alfa- og beta-tujon, sum)",
        domain="FLAVOURINGS",
        topics=["analysis parameter coding", "controlled terminology catalogues"],
        max_pages=8,
    )
    names = [item.page.name for item in selected]
    assert "ssd2-analysis-parameter-coding.md" in names


def test_topic_hints_survive_a_crowded_domain():
    """Regression: `additives` has 4 pages, which together with the 2
    cross-cutting pages exactly filled a 6-page budget and starved the
    relevance tier -- so an explicitly requested reference page was dropped.
    Part of the budget is now reserved whenever topics are supplied."""
    selected, trace = select_pages(
        _store(),
        search_term="Kinin",
        domain="FLAVOURINGS",  # -> additives, the crowded domain
        topics=["analysis parameter coding"],
        max_pages=6,
    )
    names = [item.page.name for item in selected]
    assert "ssd2-analysis-parameter-coding.md" in names
    assert trace["counts"]["relevance"] >= 1
    assert len(selected) == 6  # budget still fully used


def test_no_reserved_slots_without_topics():
    """Without topic hints there is nothing to reserve for: the tiered pages
    should use the whole budget."""
    selected, trace = select_pages(
        _store(), search_term="Kinin", domain="FLAVOURINGS", max_pages=6
    )
    assert trace["counts"]["domain"] + trace["counts"]["cross_cutting"] == len(selected)


def test_max_pages_is_respected():
    for cap in (1, 3, 6):
        selected, _ = select_pages(
            _store(), search_term="Cadmium", domain="CONTAMINANTS", max_pages=cap
        )
        assert len(selected) <= cap


def test_unknown_domain_degrades_instead_of_failing():
    selected, trace = select_pages(
        _store(), search_term="acrylamide business rules", domain="nonsense", max_pages=5
    )
    assert trace["domain_recognized"] is False
    assert trace["normalized_domain"] is None
    # Still returns something useful via relevance ranking.
    assert selected


def test_selection_is_deterministic():
    args = dict(search_term="Glyphosate", domain="PESTICIDES", max_pages=6)
    first, _ = select_pages(_store(), **args)
    second, _ = select_pages(_store(), **args)
    assert [i.page.name for i in first] == [i.page.name for i in second]


# --- endpoint -------------------------------------------------------------


def test_endpoint_returns_pages_and_trace():
    response = request(
        "POST",
        "/wiki/context-pack",
        json={
            "search_term": "Chlorpyrifos",
            "context": {"domain": "PESTICIDES"},
            "max_pages": 5,
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["domain"] == "pesticide"
    assert payload["pages_used"]
    assert len(payload["pages"]) <= 5
    assert payload["pages"][0]["content"]
    assert payload["trace"]["pages"][0]["selected_by"] == "domain"


def test_endpoint_accepts_reporting_domain_key():
    """`reporting_domain` is the key DMT already uses for FoodEx2."""
    response = request(
        "POST",
        "/wiki/context-pack",
        json={"search_term": "Cadmium", "context": {"reporting_domain": "CONTAMINANTS"}},
    )
    assert response.status_code == 200
    assert response.json()["domain"] == "contaminant"


def test_endpoint_can_omit_content():
    response = request(
        "POST",
        "/wiki/context-pack",
        json={
            "search_term": "Cadmium",
            "context": {"domain": "CONTAMINANTS"},
            "include_page_content": False,
        },
    )
    assert response.status_code == 200
    assert all(page["content"] is None for page in response.json()["pages"])


def test_endpoint_rejects_out_of_range_max_pages():
    response = request(
        "POST",
        "/wiki/context-pack",
        json={"search_term": "Cadmium", "max_pages": 99},
    )
    assert response.status_code == 422


def test_endpoint_works_without_domain():
    response = request(
        "POST",
        "/wiki/context-pack",
        json={"search_term": "legal limits for pesticide residues"},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["domain"] is None
    assert payload["pages"]
