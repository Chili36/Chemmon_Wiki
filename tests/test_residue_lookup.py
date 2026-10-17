"""Lookup of pinned rd-bridge residue records for pesticides named in a question."""
from __future__ import annotations

import dataclasses

from pathlib import Path

import wiki_api.app as app_module
from tests.test_app import FakeAnswerer, FakeSelector, request
from wiki_api.datasets import claim_problems, load_rd_bridge
from wiki_api.residue_lookup import (
    LOOKUP_PAGE, MAX_RECORDS, find_records, lookup_evidence, lookup_markdown, name_keys, render_lookup_page,
)
from wiki_api.wiki_store import split_frontmatter

ROOT = Path(__file__).resolve().parents[1]


def ids(question: str) -> list[int]:
    _, index = load_rd_bridge(ROOT)
    return [r["residue_id"] for r in find_records(question, index)]


def test_single_definition_pesticide_is_found():
    assert ids("Which paramCode should we report for glyphosate in wheat?") == [120]


def test_case_punctuation_and_spelling_do_not_matter():
    assert 377 in ids("What is the residue definition for SULFUR?")  # EU writes "Sulphur"
    assert 7 in ids("paramCode for 2,4-D in lemons")


def test_whole_words_only_and_food_words_do_not_trigger():
    assert ids("pesticide residues in honey and milk") == []
    assert ids("thiabendazole in cow milk") == [210]  # "Cow Milk" is also a basic-substance record
    assert 2372 not in ids("sulphur in grapes")  # "Sulphuric acid" needs the whole name


def test_expressed_as_anchor_and_alias_names_are_keys():
    keys = name_keys("Sum of M4 and M6 (both free and conjugated), expressed as pinoxaden(R)(A)")
    assert "pinoxaden" in keys
    assert "putrescine" in name_keys("1,4-Diaminobutane  (aka Putrescine)")


def test_number_of_records_is_bounded():
    _, index = load_rd_bridge(ROOT)
    names = " ".join(r["name"].split(" (")[0] for r in list(index.values())[:40])
    assert len(find_records(names, index)) == MAX_RECORDS


def test_evidence_lists_scopes_codes_and_parts_and_passes_claim_checks():
    block = lookup_evidence(ROOT, "Acetamiprid in bovine milk: which paramCode?")
    assert block["page_name"] == LOOKUP_PAGE and block["citable"]
    content = block["content"]
    assert "| Default | Acetamiprid | `RF-0014-001-PPP` |" in content
    assert "`1000000`; **except** `1040000`" in content and "`RF-00003326-PAR`" in content
    assert "`RF-00002836-PAR`" in content  # a part, listed outside the table
    raw = lookup_markdown(ROOT, "Acetamiprid in bovine milk: which paramCode?")
    assert claim_problems(ROOT, LOOKUP_PAGE, block["sources"], raw)[0] == []


def test_unlinked_definition_says_no_code_instead_of_guessing():
    content = lookup_evidence(ROOT, "paramCode for diquat?")["content"]
    assert "Diquat" in content and "no PARAM code found" in content


def test_no_named_pesticide_means_no_evidence():
    assert lookup_evidence(ROOT, "How do I report LOQ for acrylamide?") is None


def test_repository_lookup_page_is_current():
    page = (ROOT / "wiki" / "chemmon-guidance" / LOOKUP_PAGE).read_text()
    assert page == render_lookup_page(ROOT)
    data, body = split_frontmatter(page)
    assert claim_problems(ROOT, LOOKUP_PAGE, data["sources"], body) == ([], [])


def test_ask_attaches_lookup_evidence_and_allows_its_citation():
    class CitingLookup(FakeAnswerer):
        def run(self, question, pages):
            return dataclasses.replace(super().run(question, pages),
                                       citations=["contaminant-reporting.md", LOOKUP_PAGE])

    app_module.selector_runner = FakeSelector()
    app_module.answerer_runner = CitingLookup()
    payload = request("POST", "/wiki/ask", json={"question": "Which paramCode for glyphosate?"}).json()
    pages = app_module.answerer_runner.calls[0]["pages"]
    lookup = [p for p in pages if p["page_name"] == LOOKUP_PAGE]
    assert lookup and "`RF-1020-001-PPP`" in lookup[0]["content"]
    assert LOOKUP_PAGE in payload["pages_used"] and LOOKUP_PAGE in payload["citations"]


def test_ask_without_a_named_pesticide_is_unchanged():
    app_module.selector_runner = FakeSelector()
    app_module.answerer_runner = FakeAnswerer()
    payload = request("POST", "/wiki/ask", json={"question": "Do I need F33 for acrylamide?"}).json()
    assert LOOKUP_PAGE not in payload["pages_used"]


def test_context_pack_includes_lookup_evidence():
    app_module.selector_runner = FakeSelector()
    payload = request("POST", "/wiki/context-pack", json={"question": "paramCode for glyphosate", "max_pages": 4}).json()
    assert LOOKUP_PAGE in payload["citable_pages"]
