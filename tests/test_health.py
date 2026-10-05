"""Pytest wrapper around tools/health_check.py so CI exercises it."""

from __future__ import annotations

import pytest

from tools.health_check import run_health_check
from wiki_api.wiki_store import ROOT_PAGE_PATHS


def test_health_check_has_no_errors() -> None:
    """The wiki must not have any hard errors.

    Warnings are permitted (e.g. the pre-existing CHEMMON03 duplicate in the
    source guidance surfaces as a warning, not an error).
    """
    report = run_health_check()
    assert report.errors == [], (
        f"health check errors:\n  - " + "\n  - ".join(report.errors)
    )


def test_health_check_chemmon03_duplicate_surfaces_as_warning() -> None:
    """The known CHEMMON03 duplicate in the source guidance should be
    flagged as a warning so future maintainers see it."""
    report = run_health_check()
    assert any("CHEMMON03" in w for w in report.warnings), (
        "expected a warning about the CHEMMON03 duplicate; got: " + str(report.warnings)
    )


@pytest.fixture
def small_wiki(tmp_path):
    for path in ROOT_PAGE_PATHS.values():
        target = tmp_path / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("# Orientation\n")
    (tmp_path / "index.md").write_text("- [Topic](wiki/chemmon-guidance/topic.md): Topic summary\n")
    folder = tmp_path / "wiki" / "chemmon-guidance"
    folder.mkdir(parents=True)
    (tmp_path / "chemmon_docs").mkdir()
    (tmp_path / "chemmon_docs" / "source.pdf").write_bytes(b"source placeholder")
    (folder / "topic.md").write_text('''---
title: Topic
type: reference
domain: all
last_updated: "2026-10-05"
sources: [source.pdf]
related: []
---
# Topic
Durable guidance.
''')
    return tmp_path


def test_health_checks_small_registered_wiki(small_wiki):
    assert run_health_check(small_wiki).errors == []


@pytest.mark.parametrize("fault,expected", [
    ("unregistered", "missing topic summary"),
    ("missing_source", "unresolved source"),
    ("broken_related", "broken wiki-link"),
    ("invalid_date", "ISO date"),
    ("unserved", "not served by the API"),
])
def test_health_detects_catalog_and_provenance_faults(small_wiki, fault, expected):
    page = small_wiki / "wiki" / "chemmon-guidance" / "topic.md"
    if fault == "unregistered":
        (small_wiki / "index.md").write_text("# Empty catalogue\n")
    elif fault == "missing_source":
        (small_wiki / "chemmon_docs" / "source.pdf").unlink()
    elif fault == "broken_related":
        page.write_text(page.read_text().replace("related: []", 'related: ["[[missing]]"]'))
    elif fault == "invalid_date":
        page.write_text(page.read_text().replace("2026-10-05", "not-a-date"))
    else:
        (small_wiki / "unserved.md").write_text("# Present but not registered\n")
        with (small_wiki / "index.md").open("a") as index:
            index.write("- [Unserved](unserved.md): Unserved page\n")
    assert any(expected in error for error in run_health_check(small_wiki).errors)
