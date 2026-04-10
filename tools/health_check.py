#!/usr/bin/env python3
"""Health check for the ChemMon wiki.

Validates:
  1. Frontmatter schema compliance for every page under wiki/chemmon-guidance/
  2. Every [[wiki-link]] resolves to an existing page
  3. Rule-ID coverage — each CHEMMON\\d+(_[a-z])? ID should appear exactly
     once across the business-rules-*.md slice files. Duplicates surface as
     warnings (the source guidance has a known CHEMMON03 duplicate).
  4. No prose reference to the old `raw/chemmon-guidance/` path remains in
     any tracked file under the repo root or the wiki directory.

Exit codes:
  0 — clean (no errors; warnings allowed)
  1 — one or more errors found
  2 — setup error (wiki directory missing, import failure, etc.)

Usage:
  python tools/health_check.py          # run normally
  python tools/health_check.py --strict # treat warnings as errors
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

try:
    from wiki_api.wiki_store import split_frontmatter
except ImportError as exc:
    print(f"ERROR: could not import wiki_api.wiki_store: {exc}")
    sys.exit(2)

WIKI_DIR = REPO_ROOT / "wiki" / "chemmon-guidance"
METADATA_FILES = [
    REPO_ROOT / "README.md",
    REPO_ROOT / "PROJECT_CONTEXT.md",
    REPO_ROOT / "SCHEMA.md",
    REPO_ROOT / "index.md",
    REPO_ROOT / "log.md",
]

ALLOWED_TYPES = {"overview", "reference", "domain-guide", "rule-reference", "hub"}
ALLOWED_DOMAINS = {
    "all",
    "vmpr",
    "pesticide",
    "contaminant",
    "additives",
    "baby-food",
    "cross-cutting",
}
REQUIRED_FIELDS = {"title", "type", "domain", "last_updated"}

OLD_PATH_LITERAL = "raw/chemmon-guidance/"

WIKI_LINK_RE = re.compile(r"\[\[([a-zA-Z0-9_\-]+)(?:\|[^\]]+)?\]\]")
# Matches a table row whose first cell is a rule ID like CHEMMON12 or CHEMMON79_a/b/c
RULE_ID_TABLE_ROW_RE = re.compile(
    r"^\|\s*(CHEMMON\s*\d+(?:_[a-z](?:/[a-z])*)?)\s*\|",
    re.MULTILINE,
)


@dataclass
class HealthReport:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def error(self, msg: str) -> None:
        self.errors.append(msg)

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)

    def is_clean(self, strict: bool = False) -> bool:
        if self.errors:
            return False
        if strict and self.warnings:
            return False
        return True

    def print_summary(self) -> None:
        for w in self.warnings:
            print(f"WARN:  {w}")
        for e in self.errors:
            print(f"ERROR: {e}")
        status = "PASS" if not self.errors else "FAIL"
        print(
            f"\nHEALTH CHECK: {status} "
            f"({len(self.errors)} error(s), {len(self.warnings)} warning(s))"
        )


def _rel(path: Path) -> str:
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def check_frontmatter(report: HealthReport, path: Path, data: dict[str, Any]) -> None:
    rel = _rel(path)
    missing = REQUIRED_FIELDS - set(data.keys())
    if missing:
        report.error(
            f"{rel}: missing required frontmatter field(s): {sorted(missing)}"
        )
        return
    page_type = data.get("type")
    if page_type not in ALLOWED_TYPES:
        report.error(
            f"{rel}: invalid type '{page_type}'; must be one of {sorted(ALLOWED_TYPES)}"
        )
    domain = data.get("domain")
    if domain not in ALLOWED_DOMAINS:
        report.error(
            f"{rel}: invalid domain '{domain}'; must be one of {sorted(ALLOWED_DOMAINS)}"
        )


def check_wiki_links(
    report: HealthReport,
    path: Path,
    body: str,
    valid_targets: set[str],
) -> None:
    rel = _rel(path)
    for match in WIKI_LINK_RE.finditer(body):
        target = match.group(1)
        if target not in valid_targets:
            report.error(f"{rel}: broken wiki-link [[{target}]] — no such page")


def collect_rule_ids(body: str) -> list[str]:
    return [m.group(1).replace(" ", "") for m in RULE_ID_TABLE_ROW_RE.finditer(body)]


def check_rule_id_uniqueness(
    report: HealthReport, rule_occurrences: dict[str, list[str]]
) -> None:
    for rule_id, files in rule_occurrences.items():
        if len(files) > 1:
            report.warn(
                f"rule {rule_id} defined in {len(files)} files: "
                f"{', '.join(sorted(files))}"
            )


def check_no_old_path_references(report: HealthReport) -> None:
    # log.md is exempt because it documents historical state (e.g. rename entries).
    exempt_files = {REPO_ROOT / "log.md"}
    targets = [
        p
        for p in list(WIKI_DIR.glob("*.md")) + METADATA_FILES
        if p.exists() and p not in exempt_files
    ]
    for path in targets:
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        if OLD_PATH_LITERAL in text:
            report.error(
                f"{_rel(path)}: contains stale reference to '{OLD_PATH_LITERAL}'"
            )


def run_health_check(strict: bool = False) -> HealthReport:
    report = HealthReport()

    if not WIKI_DIR.is_dir():
        report.error(f"wiki directory not found at {_rel(WIKI_DIR)}")
        return report

    wiki_files = sorted(WIKI_DIR.glob("*.md"))
    valid_targets = {p.stem for p in wiki_files}
    for metadata_path in METADATA_FILES:
        if metadata_path.exists():
            valid_targets.add(metadata_path.stem)

    rule_occurrences: dict[str, list[str]] = {}

    for path in wiki_files:
        try:
            raw = path.read_text(encoding="utf-8")
        except OSError as exc:
            report.error(f"{_rel(path)}: could not read: {exc}")
            continue
        try:
            data, body = split_frontmatter(raw)
        except Exception as exc:  # noqa: BLE001
            report.error(f"{_rel(path)}: frontmatter parse error: {exc}")
            continue
        check_frontmatter(report, path, data)
        check_wiki_links(report, path, body, valid_targets)

        if path.name.startswith("business-rules-"):
            for rule_id in collect_rule_ids(body):
                rule_occurrences.setdefault(rule_id, []).append(path.name)

    check_rule_id_uniqueness(report, rule_occurrences)
    check_no_old_path_references(report)

    return report


def main(argv: list[str]) -> int:
    strict = "--strict" in argv
    report = run_health_check(strict=strict)
    report.print_summary()
    return 0 if report.is_clean(strict=strict) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
