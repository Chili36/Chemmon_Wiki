from __future__ import annotations

from pathlib import Path

from wiki_api.wiki_store import WikiStore


def _store() -> WikiStore:
    return WikiStore(Path("/Users/davidfoster/Dev/Chemmon_Wiki"))


def test_store_reads_index() -> None:
    store = _store()
    page = store.read_page("index.md")
    assert page.name == "index.md"
    assert page.title == "Wiki Index"
    assert page.content.startswith("---")


def test_store_lists_ingested_pages() -> None:
    store = _store()
    pages = store.list_pages()
    # After the patterns refactor: 9 original pages + 9 business-rules slice files = 18
    assert len(pages) >= 16
    assert "business-rules.md" in pages  # hub
    assert "chemmon-overview.md" in pages
    # At least one sliced rule-reference file is present
    assert any(p.startswith("business-rules-") for p in pages)


def test_store_catalog_returns_ingested_pages() -> None:
    store = _store()
    catalog = store.catalog()
    assert len(catalog) >= 16
    names = {page.name for page in catalog}
    assert "business-rules.md" in names  # hub
    assert any(n.startswith("business-rules-") for n in names)


def test_store_guiding_principles_extracted() -> None:
    store = _store()
    principles = store.guiding_principles()
    assert len(principles) >= 3
    assert any("business rule" in p.lower() for p in principles)


def test_store_unknown_page_raises() -> None:
    store = _store()
    try:
        store.read_page("nonexistent.md")
        assert False, "Expected FileNotFoundError"
    except FileNotFoundError:
        pass
