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


def test_store_lists_no_pages_before_ingest() -> None:
    store = _store()
    pages = store.list_pages()
    assert pages == []


def test_store_catalog_empty_before_ingest() -> None:
    store = _store()
    catalog = store.catalog()
    assert catalog == []


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
