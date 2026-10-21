#!/usr/bin/env python3
"""Health check for the ChemMon wiki.

Validates:
  1. Frontmatter schema compliance for every page under wiki/chemmon-guidance/
  2. Every [[wiki-link]] resolves to an existing page
  3. Rule-ID uniqueness — CHEMMON IDs are checked across the slice files.
     This is not a semantic-completeness check. Duplicate definitions surface as warnings.
  4. No prose reference to the old `raw/chemmon-guidance/` path remains in
     any tracked file under the repo root or the wiki directory.
  5. Index/service registration, source files, metadata dates and related links.
  6. Dataset snapshots match their manifests, codes cited from a dataset
     appear in the cited records, and generated pages match their snapshot.

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
import json
import sys
from datetime import date
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

try:
    from wiki_api.wiki_store import INDEX_ENTRY_RE, ROOT_PAGE_PATHS, WikiStore, split_frontmatter
    from wiki_api.source_review import source_review_status, rule_inventory_status
    from wiki_api.datasets import claim_problems, manifest_problems
    from tools import rd_bridge_page, ssd2_elements
except ImportError as exc:
    print(f"ERROR: could not import wiki_api.wiki_store: {exc}")
    sys.exit(2)

WIKI_DIR = REPO_ROOT / "wiki" / "chemmon-guidance"
# Pages rendered from data, with the command that rewrites them.
GENERATED_PAGES = [
    (rd_bridge_page.PAGE_NAME, rd_bridge_page.render, "its dataset snapshot", "python tools/rd_bridge_page.py"),
    (ssd2_elements.PAGE_NAME, ssd2_elements.render, "docs/ssd2-elements.json", "python tools/ssd2_elements.py page"),
]
METADATA_FILES = [
    REPO_ROOT / "README.md",
    REPO_ROOT / "PROJECT_CONTEXT.md",
    REPO_ROOT / "SCHEMA.md",
    REPO_ROOT / "INGEST_WORKFLOW.md",
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
    source_review: dict = field(default_factory=dict)
    rule_inventory: dict = field(default_factory=dict)

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

    def print_summary(self, strict: bool = False) -> None:
        for w in self.warnings:
            print(f"WARN:  {w}")
        for e in self.errors:
            print(f"ERROR: {e}")
        status = "PASS" if self.is_clean(strict) else "FAIL"
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
    if not isinstance(page_type, str) or page_type not in ALLOWED_TYPES:
        report.error(
            f"{rel}: invalid type '{page_type}'; must be one of {sorted(ALLOWED_TYPES)}"
        )
    domain = data.get("domain")
    if not isinstance(domain, str) or domain not in ALLOWED_DOMAINS:
        report.error(
            f"{rel}: invalid domain '{domain}'; must be one of {sorted(ALLOWED_DOMAINS)}"
        )
    if not isinstance(data.get("title"), str) or not data["title"].strip():
        report.error(f"{rel}: title must be a nonempty string")
    try:
        value = str(data.get("last_updated"))
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
            raise ValueError("not an ISO date")
        date.fromisoformat(value)
    except ValueError:
        report.error(f"{rel}: last_updated must be an ISO date (YYYY-MM-DD)")
    for key in ("sources", "related", "source_pages"):
        value = data.get(key, [])
        if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
            report.error(f"{rel}: {key} must be a list of strings")
    hint = data.get("select_when")
    if hint is not None and (not isinstance(hint, str) or not hint.strip() or len(hint) > 400):
        report.error(f"{rel}: select_when must be a nonempty string of at most 400 characters")


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


def check_no_old_path_references(
    report: HealthReport, file_contents: dict[Path, str]
) -> None:
    """Check cached file contents for stale references to the old wiki path.

    log.md is exempt because it documents historical state (e.g. rename entries).
    Metadata files not already in the cache are read here.
    """
    exempt_files = {REPO_ROOT / "log.md"}
    for path, text in file_contents.items():
        if path in exempt_files:
            continue
        if OLD_PATH_LITERAL in text:
            report.error(
                f"{_rel(path)}: contains stale reference to '{OLD_PATH_LITERAL}'"
            )
    for metadata_path in METADATA_FILES:
        if metadata_path in exempt_files or metadata_path in file_contents:
            continue
        if not metadata_path.exists():
            continue
        try:
            text = metadata_path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        if OLD_PATH_LITERAL in text:
            report.error(
                f"{_rel(metadata_path)}: contains stale reference to '{OLD_PATH_LITERAL}'"
            )


def run_health_check(root: Path = REPO_ROOT) -> HealthReport:
    report = HealthReport()
    wiki_dir = root / "wiki" / "chemmon-guidance"
    store = WikiStore(root)

    if not wiki_dir.is_dir():
        report.error(f"wiki directory not found at {wiki_dir}")
        return report

    wiki_files = sorted(wiki_dir.glob("*.md"))
    valid_targets = {Path(name).stem for name in store.allowed_page_names()}

    index_path = root / "index.md"
    if not index_path.is_file():
        report.error("index.md: missing catalogue")
        return report
    entries = {}
    for line in index_path.read_text(encoding="utf-8").splitlines():
        match = INDEX_ENTRY_RE.match(line)
        if not match:
            continue
        target, summary = match.groups()
        name = Path(target).name
        if not target.endswith(".md"):
            continue
        entries[name] = summary
        if not (root / target).is_file():
            report.error(f"index.md: missing local target {target}")
        if name not in store.allowed_page_names():
            report.error(f"index.md: page is not served by the API: {name}")
    for path in wiki_files:
        if not entries.get(path.name, "").strip():
            report.error(f"index.md: missing topic summary for {path.name}")
    for name, path in ROOT_PAGE_PATHS.items():
        if not (root / path).is_file():
            report.error(f"missing orientation document: {name}")

    rule_occurrences: dict[str, list[str]] = {}
    file_contents: dict[Path, str] = {}

    for path in wiki_files:
        try:
            raw = path.read_text(encoding="utf-8")
        except OSError as exc:
            report.error(f"{_rel(path)}: could not read: {exc}")
            continue
        file_contents[path] = raw
        try:
            data, body = split_frontmatter(raw)
        except Exception as exc:  # noqa: BLE001
            report.error(f"{_rel(path)}: frontmatter parse error: {exc}")
            continue
        check_frontmatter(report, path, data)
        related = data.get("related", [])
        related_text = "\n".join(item for item in related if isinstance(item, str)) if isinstance(related, list) else ""
        check_wiki_links(report, path, body + "\n" + related_text, valid_targets)
        sources = data.get("sources", [])
        if isinstance(sources, list):
            if not sources and data.get("type") != "hub":
                report.warn(f"{path.name}: no source references")
            for source in sources:
                if not isinstance(source, str):
                    continue
                if not ((root / "chemmon_docs" / source).is_file() or (root / source).is_file()):
                    report.error(f"{path.name}: unresolved source {source}")
            errors, warnings = claim_problems(root, path.name, [s for s in sources if isinstance(s, str)], body)
            for message in errors:
                report.error(message)
            for message in warnings:
                report.warn(message)

        if path.name.startswith("business-rules-"):
            for rule_id in collect_rule_ids(body):
                rule_occurrences.setdefault(rule_id, []).append(path.name)

    check_rule_id_uniqueness(report, rule_occurrences)
    for problem in manifest_problems(root):
        report.error(problem)
    for page_name, render, source, command in GENERATED_PAGES:
        generated = wiki_dir / page_name
        if not generated.is_file():
            continue
        try:
            if generated.read_text(encoding="utf-8") != render(root):
                report.error(f"{page_name}: differs from {source}; "
                             f"run {command} instead of editing it")
        except (OSError, ValueError, KeyError, TypeError) as exc:
            report.error(f"{page_name}: cannot regenerate: {exc}")
    if root == REPO_ROOT:
        check_no_old_path_references(report, file_contents)

    report.source_review = source_review_status(root)
    report.rule_inventory = rule_inventory_status(root)
    for label, status in (("source review", report.source_review), ("rule inventory", report.rule_inventory)):
        if status['status'] == 'invalid':
            report.error(f"{label}: invalid record: {status['error']}")
        elif status['status'] != 'current':
            report.warn(f"{label}: {status['status']}; reviewed coverage is not established for this corpus")
    for finding in report.source_review.get('open_findings', []):
        report.warn(f"source finding {finding['id']}: {finding['observation']}")
    for field_name in ('missing_active_ids', 'unexpected_wiki_ids', 'duplicate_wiki_ids', 'inactive_wiki_ids'):
        values = report.rule_inventory.get(field_name, [])
        if values:
            report.warn(f"rule inventory {field_name}: {len(values)}; see tools/source_review.py for IDs and locators")
    return report


def main(argv: list[str]) -> int:
    strict = "--strict" in argv
    report = run_health_check()
    if "--json" in argv:
        print(json.dumps({"errors": report.errors, "warnings": report.warnings,
            "source_review": report.source_review, "rule_inventory": report.rule_inventory,
            "structural_pass": report.is_clean(strict=strict)}, indent=2, ensure_ascii=False))
    else:
        report.print_summary(strict=strict)
    return 0 if report.is_clean(strict=strict) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
