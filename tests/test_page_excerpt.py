"""Answer-time excerpt of the by-food list page for the pesticides a question names."""
from __future__ import annotations

from pathlib import Path

from wiki_api.evidence import full_evidence
from wiki_api.page_excerpt import BY_FOOD_PAGE, excerpt
from wiki_api.wiki_store import WikiStore

ROOT = Path(__file__).resolve().parents[1]
STORE = WikiStore(ROOT)


def content(question=None):
    return full_evidence(STORE, BY_FOOD_PAGE, question=question)


def test_named_pesticide_keeps_only_its_line_and_the_reading_guide():
    full, trimmed = content()["content"], content("Are there any special rules regarding Abamectin?")["content"]
    assert "**Abamectin**" in trimmed and "**Acetamiprid**" not in trimmed
    for section in ("## How to read this list", "## Annex I codes", "## Sources and attribution"):
        assert section in trimmed
    assert "whole-residue `paramCode`" in trimmed  # the reading guide stays complete
    assert len(trimmed) < len(full) / 5


def test_several_pesticides_and_spelling_variants():
    trimmed = content("Compare thiabendazole and 2,4-DB in milk")["content"]
    assert "**Thiabendazole**" in trimmed and "**2,4-DB**" in trimmed
    assert "**Abamectin**" not in trimmed


def test_names_with_a_qualifier_match_on_the_name():
    assert "**Pinoxaden (sum of M4 and M6)**" in content("residue definition of pinoxaden")["content"]


def test_interpreted_wording_kept_only_for_named_pesticides():
    trimmed = content("thiabendazole")["content"]
    section = trimmed.split("## Interpreted source wording", 1)[1].split("##", 1)[0]
    assert "Thiabendazole" in section and "2-phenylphenol" not in section


def test_no_listed_pesticide_sends_the_whole_page():
    assert content("Which pesticides have milk-specific definitions?")["content"] == content()["content"]
    assert content("glyphosate in wheat")["content"] == content()["content"]  # not on the list


def test_excerpt_is_marked_and_other_pages_are_untouched():
    trimmed = content("abamectin")
    assert trimmed["excerpt"] is True and trimmed["evidence_kind"] == "full" and trimmed["citable"]
    assert content()["excerpt"] is False
    other = full_evidence(STORE, "pesticide-reporting.md", question="abamectin")
    assert other == full_evidence(STORE, "pesticide-reporting.md")


def test_unrelated_text_is_returned_unchanged():
    assert excerpt("# Some page\n\nNo list here.", "abamectin") is None
