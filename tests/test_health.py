"""Pytest wrapper around tools/health_check.py so CI exercises it."""

from __future__ import annotations

import pytest

from tools.health_check import run_health_check
from wiki_api.wiki_store import ROOT_PAGE_PATHS


def test_health_check_has_no_errors() -> None:
    """The wiki must not have any hard errors.

    Warnings are permitted for explicitly documented source-coverage gaps.
    """
    report = run_health_check()
    assert report.errors == [], (
        f"health check errors:\n  - " + "\n  - ".join(report.errors)
    )


def test_review_reports_real_source_gaps_not_a_source_duplicate():
    report = run_health_check()
    assert report.rule_inventory['status'] == 'current'
    assert report.rule_inventory['missing_active_ids'] == []
    assert report.rule_inventory['duplicate_wiki_ids'] == {}
    assert report.rule_inventory['unexpected_wiki_ids'] == []
    assert not any('rule CHEMMON03 defined' in w for w in report.warnings)


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


def test_strict_health_output_matches_failure_status(capsys):
    from tools.health_check import HealthReport
    report = HealthReport(warnings=['open finding'])
    report.print_summary(strict=True)
    assert 'FAIL' in capsys.readouterr().out
    assert not report.is_clean(strict=True)
