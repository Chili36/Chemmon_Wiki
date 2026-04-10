"""Pytest wrapper around tools/health_check.py so CI exercises it."""

from __future__ import annotations

from tools.health_check import run_health_check


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
