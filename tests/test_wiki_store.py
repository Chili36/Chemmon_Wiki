from __future__ import annotations

from pathlib import Path

from wiki_api.wiki_store import WikiStore


def _store() -> WikiStore:
    return WikiStore(Path(__file__).resolve().parents[1])


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


def test_orientation_pages_are_readable_but_not_selector_evidence():
    store = _store()
    for name in ("README.md", "PROJECT_CONTEXT.md", "SCHEMA.md", "INGEST_WORKFLOW.md"):
        assert store.read_page(name).page_type == "orientation"
        assert name not in store.list_pages()
        assert name not in store.selector_catalog()


def test_model_evidence_preserves_source_locators():
    store = _store()
    page = store.read_page("ssd2-result-units-and-limits.md")
    content = store.clean_content_for_model(page)
    assert "Source: ChemMon 2026 pp. 65-66" in content
    assert "(ChemMon 2026 p65)" in content
    assert "<!--" not in content
    assert page.source_pages


def test_backlinks_include_inline_and_related_links():
    store = _store()
    names = store.backlinks("ssd2-matrix-vmpr-coding.md")
    assert "vmpr-reporting.md" in names
    assert "ssd2-matrix-vmpr-coding.md" not in names


def test_index_summary_refreshes_without_service_restart(tmp_path):
    (tmp_path / "index.md").write_text("- [Topic](wiki/chemmon-guidance/topic.md): Before\n")
    store = WikiStore(tmp_path)
    assert store._summaries["topic.md"] == "Before"
    (tmp_path / "index.md").write_text("- [Topic](wiki/chemmon-guidance/topic.md): After\n")
    assert store._summaries["topic.md"] == "After"
