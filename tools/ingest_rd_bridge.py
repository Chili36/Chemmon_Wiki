#!/usr/bin/env python3
"""Pin a new rd-bridge snapshot into chemmon_docs/datasets/rd-bridge/.

This is the dataset equivalent of adding a new guidance PDF: it copies the
upstream files verbatim from one commit, records checksums and dates, and
prints which residue definitions changed and which wiki pages cite them. It
never edits wiki pages. Follow INGEST_WORKFLOW.md for the passes after it.

Usage:
  python tools/ingest_rd_bridge.py                     # latest main from GitHub
  python tools/ingest_rd_bridge.py --ref 104448e       # a specific commit
  python tools/ingest_rd_bridge.py --source ~/Dev/rd-bridge --dry-run
  python tools/ingest_rd_bridge.py --report reports/dataset-ingest/rd-bridge.md
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from wiki_api.datasets import (  # noqa: E402
    MANIFEST_NAME, RD_BRIDGE_DIR, RD_BRIDGE_GUIDANCE, RD_BRIDGE_MAP, dataset_citations, guidance_citations,
    guidance_index, read_manifest, residue_index, sha256_bytes,
)
from wiki_api.wiki_store import split_frontmatter  # noqa: E402
from tools.rd_bridge_page import ANNEX_DIR, PAGE_NAME, NamesMissing, _cell, write as write_page  # noqa: E402

DEFAULT_SOURCE = "https://github.com/Chili36/rd-bridge"
# Snapshot file name -> path in the rd-bridge repository.
FILES = {
    "residue_param_map.json": "data/residue_param_map.json",
    "DATA_SOURCES.md": "DATA_SOURCES.md",
    "interpretation_guidance.json": "data/interpretation_guidance.json",
}


def git(repo: Path, *args: str) -> bytes:
    return subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True).stdout


def fetch(source: str, ref: str, workdir: Path) -> dict[str, Any]:
    """Read the snapshot files and dates from one upstream commit."""
    clone = workdir / "rd-bridge"
    subprocess.run(["git", "clone", "--quiet", "--no-checkout", "--filter=blob:none", source, str(clone)],
                   check=True, capture_output=True)
    commit = None
    for candidate in (ref, f"origin/{ref}"):
        try:
            commit = git(clone, "rev-parse", "--verify", "--quiet", f"{candidate}^{{commit}}").decode().strip()
            break
        except subprocess.CalledProcessError:
            continue
    if not commit:
        raise SystemExit(f"ref not found in {source}: {ref}")
    repository = source
    if Path(source).expanduser().is_dir():
        try:
            repository = git(Path(source).expanduser(), "remote", "get-url", "origin").decode().strip() or source
        except subprocess.CalledProcessError:
            pass
    files = {name: git(clone, "show", f"{commit}:{path}") for name, path in FILES.items()}
    return {
        "repository": repository.removesuffix(".git"),
        "commit": commit,
        "commit_date": git(clone, "log", "-1", "--format=%cs", commit).decode().strip(),
        "dataset_changed_at": git(clone, "log", "-1", "--format=%cs", commit, "--",
                                  FILES["residue_param_map.json"]).decode().strip(),
        "files": files,
    }


def summarize(index: dict[int, dict[str, Any]]) -> dict[str, int]:
    varying = [r for r in index.values() if r.get("exceptions")]
    return {"records": len(index), "with_commodity_exceptions": len(varying),
            "exceptions": sum(len(r["exceptions"]) for r in varying)}


def _scope_view(scope: dict[str, Any]) -> dict[str, Any]:
    return {k: scope.get(k) for k in ("commodity_codes", "except_codes", "definition", "param_codes",
                                      "repairs", "issues")}


def record_view(record: dict[str, Any]) -> dict[str, Any]:
    """The parts of a record the wiki relies on; evidence-only fields are ignored."""
    return {"name": record["name"], "default": _scope_view(record["default"]),
            "exceptions": [_scope_view(e) for e in record.get("exceptions", [])]}


def compare(old: dict[int, dict[str, Any]], new: dict[int, dict[str, Any]]) -> dict[str, list[int]]:
    return {
        "added": sorted(new.keys() - old.keys()),
        "removed": sorted(old.keys() - new.keys()),
        "changed": sorted(k for k in old.keys() & new.keys() if record_view(old[k]) != record_view(new[k])),
    }


def compare_rules(old: dict[str, dict[str, Any]], new: dict[str, dict[str, Any]]) -> dict[str, list[str]]:
    return {
        "added": sorted(new.keys() - old.keys()),
        "removed": sorted(old.keys() - new.keys()),
        "changed": sorted(k for k in old.keys() & new.keys() if old[k] != new[k]),
    }


def citing_guidance_pages(root: Path) -> dict[str, set[str]]:
    """Wiki pages that cite the interpretation guidance, with the rule IDs they cite."""
    pages: dict[str, set[str]] = {}
    for path in sorted((root / "wiki" / "chemmon-guidance").glob("*.md")):
        data, body = split_frontmatter(path.read_text(encoding="utf-8"))
        rules = {r for p, _, cited, _ in guidance_citations(body) if p == RD_BRIDGE_GUIDANCE for r in cited}
        if rules or RD_BRIDGE_GUIDANCE in (data.get("sources") or []):
            pages[path.name] = rules
    return pages


def citing_pages(root: Path) -> dict[str, set[int]]:
    """Wiki pages that cite the residue map, with the residue_ids they cite."""
    pages: dict[str, set[int]] = {}
    for path in sorted((root / "wiki" / "chemmon-guidance").glob("*.md")):
        data, body = split_frontmatter(path.read_text(encoding="utf-8"))
        ids = {n for p, _, cited, _ in dataset_citations(body) if p == RD_BRIDGE_MAP for n in cited}
        if ids or RD_BRIDGE_MAP in (data.get("sources") or []):
            pages[path.name] = ids
    return pages


def render_report(previous: dict[str, Any] | None, fetched: dict[str, Any], summary: dict[str, int],
                  diff: dict[str, list[int]] | None, old: dict[int, dict[str, Any]],
                  new: dict[int, dict[str, Any]], pages: dict[str, set[int]], written: bool,
                  rule_diff: dict[str, list[str]] | None = None,
                  guidance_pages: dict[str, set[str]] | None = None) -> str:
    lines = [f"# rd-bridge ingest {date.today().isoformat()}", ""]
    before = f"{previous['commit'][:7]} ({previous['dataset_changed_at']})" if previous else "none"
    lines += [f"- Repository: {fetched['repository']}",
              f"- Snapshot: {before} -> {fetched['commit'][:7]} (map last changed {fetched['dataset_changed_at']})",
              f"- Records: {summary['records']}; food-dependent: {summary['with_commodity_exceptions']} "
              f"({summary['exceptions']} exceptions)",
              f"- Written: {'yes' if written else 'no (dry run or unchanged)'}", ""]
    if diff is not None:
        lines.append("## Residue definition changes")
        if not any(diff.values()):
            lines.append("None in the fields the wiki uses (names, scopes, definitions, PARAM codes, notes).")
        for kind, source in (("added", new), ("removed", old), ("changed", new)):
            for n in diff[kind]:
                lines.append(f"- {kind}: residue_id {n} {_cell(source[n]['name'])}")
        lines.append("")
    if rule_diff is not None:
        lines.append("## Interpretation guidance changes")
        if not any(rule_diff.values()):
            lines.append("None.")
        for kind in ("added", "removed", "changed"):
            for rule in rule_diff[kind]:
                lines.append(f"- {kind}: rule {rule}")
        lines.append("")
    changed = set(diff["removed"] + diff["changed"]) if diff else set()
    changed_rules = set(rule_diff["removed"] + rule_diff["changed"]) if rule_diff else set()
    guidance_pages = guidance_pages or {}
    lines.append("## Wiki pages to review")
    if not pages and not guidance_pages:
        lines.append("No page cites the dataset.")
    for page in sorted(pages.keys() | guidance_pages.keys()):
        if page == PAGE_NAME:
            continue  # generated from the snapshot; rewritten by the ingest
        hit = sorted(pages.get(page, set()) & changed)
        rule_hit = sorted(guidance_pages.get(page, set()) & changed_rules)
        why = [f"cites changed residue_id {', '.join(map(str, hit))}"] if hit else []
        why += [f"cites changed rule {', '.join(rule_hit)}"] if rule_hit else []
        lines.append(f"- {page}: {'; '.join(why) or 'cites the dataset; confirm and update the Source commit'}")
    lines += ["", "Next: patch pages rule-first (INGEST_WORKFLOW.md, dataset sources), run "
              "`python tools/health_check.py` and `pytest -q`, update the source review record and log.md."]
    return "\n".join(lines) + "\n"


def ingest(root: Path, source: str, ref: str, dry_run: bool = False) -> tuple[str, bool]:
    target = root / RD_BRIDGE_DIR
    with tempfile.TemporaryDirectory() as tmp:
        fetched = fetch(source, ref, Path(tmp))
    new = residue_index(json.loads(fetched["files"]["residue_param_map.json"]))
    new_rules = guidance_index(json.loads(fetched["files"]["interpretation_guidance.json"]))
    summary = summarize(new)
    previous, old, old_rules = None, {}, {}
    if (target / MANIFEST_NAME).is_file():
        previous = read_manifest(target)
        old = residue_index(json.loads((target / "residue_param_map.json").read_text(encoding="utf-8")))
        if (target / "interpretation_guidance.json").is_file():
            old_rules = guidance_index(json.loads(
                (target / "interpretation_guidance.json").read_text(encoding="utf-8")))
    hashes = {name: sha256_bytes(data) for name, data in fetched["files"].items()}
    unchanged = (previous is not None and previous["commit"] == fetched["commit"]
                 and {n: e["sha256"] for n, e in previous["files"].items()} == hashes)
    write = not dry_run and not unchanged
    if write:
        target.mkdir(parents=True, exist_ok=True)
        for path in target.iterdir():
            if path.name not in fetched["files"] and path.name != MANIFEST_NAME:
                path.unlink()
        for name, data in fetched["files"].items():
            (target / name).write_bytes(data)
        manifest = {
            "version": 1,
            "dataset": "rd-bridge",
            "description": "Derived, non-official bridge from EU Pesticides Database residue definitions "
                           "to EFSA PARAM codes. Copied verbatim; replace only with tools/ingest_rd_bridge.py.",
            "repository": fetched["repository"],
            "commit": fetched["commit"],
            "commit_date": fetched["commit_date"],
            "dataset_changed_at": fetched["dataset_changed_at"],
            "ingested_at": date.today().isoformat(),
            "files": {name: {"from": FILES[name], "sha256": hashes[name]} for name in FILES},
            "summary": summary,
        }
        (target / MANIFEST_NAME).write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    page_note = ""
    if write and (root / "wiki" / "chemmon-guidance").is_dir() and (root / ANNEX_DIR).is_dir():
        try:
            if write_page(root):
                page_note = f"\nRegenerated {PAGE_NAME} from the new snapshot.\n"
        except NamesMissing as exc:
            page_note = f"\nNOT regenerated {PAGE_NAME}: {exc}. The health check fails until it is.\n"
    diff = compare(old, new) if previous else None
    rule_diff = compare_rules(old_rules, new_rules) if previous else None
    report = render_report(previous, fetched, summary, diff, old, new, citing_pages(root), write,
                           rule_diff, citing_guidance_pages(root))
    report += page_note
    return report, write


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--source", default=DEFAULT_SOURCE, help="git URL or local clone (default: GitHub)")
    parser.add_argument("--ref", default="main", help="branch, tag or commit (default: main)")
    parser.add_argument("--dry-run", action="store_true", help="report changes without writing the snapshot")
    parser.add_argument("--report", type=Path, help="also write the markdown report to this path")
    args = parser.parse_args(argv)
    try:
        report, _ = ingest(ROOT, args.source, args.ref, args.dry_run)
    except subprocess.CalledProcessError as exc:
        print(f"git failed: {' '.join(exc.cmd)}\n{exc.stderr.decode(errors='replace')}", file=sys.stderr)
        return 2
    except ValueError as exc:
        print(f"rejected snapshot, nothing written: {exc}", file=sys.stderr)
        return 1
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(report, encoding="utf-8")
    print(report, end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
