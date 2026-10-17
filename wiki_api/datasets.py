"""Pinned dataset sources and checks for wiki claims derived from them.

A dataset snapshot lives under ``chemmon_docs/datasets/<name>/`` next to the
source PDFs. It is raw material: files are copied verbatim from a pinned
upstream commit and recorded with checksums in ``manifest.json``. Wiki pages
cite claims from it with a claim-adjacent comment such as::

    <!-- Source: datasets/rd-bridge/residue_param_map.json @ 104448e, residue_id 10, 210 -->

Every PARAM code and backticked Annex I commodity code after that comment, up to the next
``Source:`` comment, must appear in the cited records. This catches drift when
a new snapshot changes a code; it does not check prose meaning.

Readings of residue-definition wording cite rd-bridge's curated interpretation
rules by ID instead::

    <!-- Source: datasets/rd-bridge/interpretation_guidance.json @ b4e9020, rule OECD-EXPRESSION-BASIS -->

The cited rules must exist in the snapshot, and no PARAM code may appear under
such a comment: codes need a residue_id citation.
"""
from __future__ import annotations

import hashlib
import json
import re
from datetime import date
from pathlib import Path
from typing import Any

DATASETS_DIR = Path("chemmon_docs") / "datasets"
MANIFEST_NAME = "manifest.json"
RD_BRIDGE_DIR = DATASETS_DIR / "rd-bridge"
RD_BRIDGE_MAP = "datasets/rd-bridge/residue_param_map.json"
RD_BRIDGE_GUIDANCE = "datasets/rd-bridge/interpretation_guidance.json"
GUIDANCE_SCHEMA_VERSION = 1

SOURCE_COMMENT_RE = re.compile(r"<!--\s*Source:(.*?)-->", re.DOTALL)
DATASET_LOCATOR_RE = re.compile(
    r"^\s*(datasets/[^\s@,]+)\s*@\s*([0-9a-f]{7,40})\s*,\s*residue_id\s+(\d+(?:\s*,\s*\d+)*)\s*$"
)
GUIDANCE_LOCATOR_RE = re.compile(
    r"^\s*(datasets/[^\s@,]+)\s*@\s*([0-9a-f]{7,40})\s*,\s*rules?\s+([A-Z0-9-]+(?:\s*,\s*[A-Z0-9-]+)*)\s*$"
)
RULE_ID_RE = re.compile(r"[A-Z0-9]+(?:-[A-Z0-9]+)*")
PARAM_CODE_RE = re.compile(r"\bRF-[0-9A-Z]+(?:-[0-9A-Z]+)+\b")
# Annex I codes are written in backticks, so compound numbers such as "AE 0172747" are not read as codes.
ANNEX_CODE_RE = re.compile(r"`([01]\d{6})`")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_manifest(dataset_dir: Path) -> dict[str, Any]:
    """Validate a manifest. Git snapshots pin a commit; API snapshots record a URL and retrieval date."""
    manifest = json.loads((dataset_dir / MANIFEST_NAME).read_text(encoding="utf-8"))
    if not isinstance(manifest, dict) or manifest.get("version") != 1:
        raise ValueError("unsupported manifest")
    if manifest.get("kind", "git") == "git":
        if not re.fullmatch(r"[0-9a-f]{40}", str(manifest.get("commit", ""))):
            raise ValueError("commit must be a full 40-character SHA")
        dates = ("commit_date", "dataset_changed_at", "ingested_at")
        if not manifest.get("repository"):
            raise ValueError("missing repository")
    elif manifest["kind"] == "api":
        dates = ("retrieved_at",)
        if not str(manifest.get("url", "")).startswith("https://"):
            raise ValueError("api snapshot needs an https url")
    else:
        raise ValueError(f"unknown manifest kind {manifest['kind']}")
    for key in dates:
        date.fromisoformat(str(manifest.get(key)))
    files = manifest.get("files")
    if not isinstance(files, dict) or not files:
        raise ValueError("files must be a nonempty object")
    for name, entry in files.items():
        if (Path(name).name != name or not isinstance(entry, dict)
                or not re.fullmatch(r"[0-9a-f]{64}", str(entry.get("sha256", "")))):
            raise ValueError(f"invalid file entry {name}")
    return manifest


def manifest_problems(root: Path) -> list[str]:
    """Report hand edits, missing files and unlisted files in dataset snapshots."""
    problems: list[str] = []
    base = root / DATASETS_DIR
    if not base.is_dir():
        return problems
    for dataset_dir in sorted(p for p in base.iterdir() if p.is_dir()):
        rel = dataset_dir.relative_to(root).as_posix()
        try:
            manifest = read_manifest(dataset_dir)
        except FileNotFoundError:
            problems.append(f"{rel}: missing {MANIFEST_NAME}")
            continue
        except (ValueError, TypeError, json.JSONDecodeError) as exc:
            problems.append(f"{rel}/{MANIFEST_NAME}: {exc}")
            continue
        for name, entry in manifest["files"].items():
            path = dataset_dir / name
            if not path.is_file():
                problems.append(f"{rel}/{name}: listed in manifest but missing")
            elif sha256_bytes(path.read_bytes()) != entry["sha256"]:
                problems.append(f"{rel}/{name}: checksum differs from manifest; "
                                "snapshots are replaced by the ingest tool, never edited")
        listed = set(manifest["files"]) | {MANIFEST_NAME}
        for path in sorted(dataset_dir.iterdir()):
            if path.name not in listed:
                problems.append(f"{rel}/{path.name}: not listed in manifest")
    return problems


def residue_index(records: Any) -> dict[int, dict[str, Any]]:
    """Validate the rd-bridge map shape and index it by residue_id."""
    if not isinstance(records, list) or not records:
        raise ValueError("residue map must be a nonempty list")
    index: dict[int, dict[str, Any]] = {}
    for record in records:
        if not isinstance(record, dict) or not isinstance(record.get("residue_id"), int):
            raise ValueError("every record needs an integer residue_id")
        if record["residue_id"] in index:
            raise ValueError(f"duplicate residue_id {record['residue_id']}")
        if not isinstance(record.get("name"), str) or not isinstance(record.get("default"), dict):
            raise ValueError(f"residue_id {record['residue_id']}: missing name or default")
        exceptions = record.get("exceptions", [])
        if not isinstance(exceptions, list) or not all(
            isinstance(e, dict) and isinstance(e.get("commodity_codes"), list) for e in exceptions
        ):
            raise ValueError(f"residue_id {record['residue_id']}: malformed exceptions")
        for exception in exceptions:
            codes = exception["commodity_codes"] + (exception.get("except_codes") or [])
            codes += [r.get(k) for r in exception.get("repairs") or [] for k in ("from", "to")]
            if not all(isinstance(c, str) and re.fullmatch(r"\d{1,7}", c) for c in codes):
                raise ValueError(f"residue_id {record['residue_id']}: commodity codes must be digits")
        for scope in [record["default"], *exceptions]:
            if not isinstance(scope.get("param_codes", []), list) or not all(
                isinstance(c, str) for c in scope.get("param_codes") or []
            ):
                raise ValueError(f"residue_id {record['residue_id']}: param_codes must be a list of strings")
        index[record["residue_id"]] = record
    return index


def guidance_index(data: Any) -> dict[str, dict[str, Any]]:
    """Validate rd-bridge's interpretation guidance and index its rules by ID."""
    if not isinstance(data, dict) or data.get("schema_version") != GUIDANCE_SCHEMA_VERSION:
        raise ValueError(f"interpretation guidance must declare schema_version {GUIDANCE_SCHEMA_VERSION}")
    if not isinstance(data.get("rules"), list) or not data["rules"]:
        raise ValueError("interpretation guidance needs a non-empty rules list")
    sources = data.get("sources")
    if not isinstance(sources, dict):
        raise ValueError("interpretation guidance needs a sources mapping")
    index: dict[str, dict[str, Any]] = {}
    for rule in data["rules"]:
        rule_id = rule.get("id") if isinstance(rule, dict) else None
        if not isinstance(rule_id, str) or not RULE_ID_RE.fullmatch(rule_id):
            raise ValueError("every guidance rule needs an upper-case id")
        if rule_id in index:
            raise ValueError(f"duplicate guidance rule {rule_id}")
        if not isinstance(rule.get("principle"), str) or not rule["principle"].strip():
            raise ValueError(f"guidance rule {rule_id}: missing principle")
        if not isinstance(rule.get("locator"), str) or not rule["locator"].strip():
            raise ValueError(f"guidance rule {rule_id}: missing locator")
        refs = rule.get("sources")
        if not isinstance(refs, list) or not refs or any(r not in sources for r in refs):
            raise ValueError(f"guidance rule {rule_id}: sources must name entries in the sources mapping")
        for ref in refs:
            entry = sources[ref]
            if not isinstance(entry, dict) or not all(
                    isinstance(entry.get(k), str) and entry[k].strip() for k in ("title", "url", "locator")):
                raise ValueError(f"guidance source {ref}: needs a title, url and locator")
        index[rule_id] = rule
    return index


def load_guidance(root: Path) -> dict[str, dict[str, Any]]:
    path = root / RD_BRIDGE_DIR / "interpretation_guidance.json"
    return guidance_index(json.loads(path.read_text(encoding="utf-8")))


def load_rd_bridge(root: Path) -> tuple[dict[str, Any], dict[int, dict[str, Any]]]:
    dataset_dir = root / RD_BRIDGE_DIR
    manifest = read_manifest(dataset_dir)
    records = json.loads((dataset_dir / "residue_param_map.json").read_text(encoding="utf-8"))
    return manifest, residue_index(records)


def record_codes(record: dict[str, Any]) -> tuple[set[str], set[str]]:
    """Return (PARAM codes, Annex I commodity codes) mentioned by one record."""
    params: set[str] = set()
    commodities: set[str] = set()
    for scope in [record["default"], *record.get("exceptions", [])]:
        params.update(scope.get("param_codes") or [])
        for component in scope.get("components") or []:
            params.update(component.get("param_codes") or [])
        commodities.update(scope.get("commodity_codes") or [])
        commodities.update(scope.get("except_codes") or [])
    return params, commodities


def dataset_citations(body: str) -> list[tuple[str, str, list[int], str]]:
    """Split a page at Source comments; return (path, commit, ids, text) per dataset citation."""
    comments = list(SOURCE_COMMENT_RE.finditer(body))
    citations = []
    for i, match in enumerate(comments):
        locator = DATASET_LOCATOR_RE.match(match.group(1))
        if not locator:
            continue
        end = comments[i + 1].start() if i + 1 < len(comments) else len(body)
        ids = [int(n) for n in re.split(r"\s*,\s*", locator.group(3))]
        citations.append((locator.group(1), locator.group(2), ids, body[match.end():end]))
    return citations


def guidance_citations(body: str) -> list[tuple[str, str, list[str], str]]:
    """Split a page at Source comments; return (path, commit, rule ids, text) per guidance citation."""
    comments = list(SOURCE_COMMENT_RE.finditer(body))
    citations = []
    for i, match in enumerate(comments):
        locator = GUIDANCE_LOCATOR_RE.match(match.group(1))
        if not locator:
            continue
        end = comments[i + 1].start() if i + 1 < len(comments) else len(body)
        rules = re.split(r"\s*,\s*", locator.group(3))
        citations.append((locator.group(1), locator.group(2), rules, body[match.end():end]))
    return citations


def _guidance_problems(root: Path, page: str, sources: list[str], body: str) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    citations = guidance_citations(body)
    # A comment naming the guidance file that the locator pattern rejects would otherwise be
    # skipped silently, leaving its claims unchecked.
    for match in SOURCE_COMMENT_RE.finditer(body):
        locator = match.group(1)
        if "interpretation_guidance.json" in locator and not GUIDANCE_LOCATOR_RE.match(locator):
            errors.append(f"{page}: malformed guidance locator: {' '.join(locator.split())[:120]}")
    if not citations:
        return errors, warnings
    try:
        manifest = read_manifest(root / RD_BRIDGE_DIR)
        index = load_guidance(root)
    except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
        return [f"{page}: cannot check guidance claims: {exc}"], warnings
    for path, commit, rules, text in citations:
        where = f"{page}: Source {path} @ {commit}"
        if path != RD_BRIDGE_GUIDANCE:
            errors.append(f"{where}: unknown dataset file")
            continue
        if path not in sources:
            errors.append(f"{page}: {path} is cited inline but missing from frontmatter sources")
        if not manifest["commit"].startswith(commit):
            warnings.append(f"{where}: reviewed against an older snapshot; current is "
                            f"{manifest['commit'][:7]}. Re-check and update the commit")
        for rule in rules:
            if rule not in index:
                errors.append(f"{where}: rule {rule} not in current snapshot")
        for code in sorted(set(PARAM_CODE_RE.findall(text))):
            errors.append(f"{where}: PARAM code {code} needs a residue_id citation")
    return errors, warnings


def claim_problems(root: Path, page: str, sources: list[str], body: str) -> tuple[list[str], list[str]]:
    """Check dataset-derived codes on one page. Returns (errors, warnings)."""
    citations = dataset_citations(body)
    errors, warnings = _guidance_problems(root, page, sources, body)
    # Each locatable dataset file listed in frontmatter needs its own claim-adjacent locator;
    # a locator for one file does not stand in for the other.
    located = {path for path, *_ in citations} | {path for path, *_ in guidance_citations(body)}
    for path in (RD_BRIDGE_MAP, RD_BRIDGE_GUIDANCE):
        if path in sources and path not in located:
            warnings.append(f"{page}: lists {path} but has no claim-adjacent Source comment for it")
    others = [s for s in sources if s.startswith("datasets/") and s not in (RD_BRIDGE_MAP, RD_BRIDGE_GUIDANCE)]
    if others and not located:
        warnings.append(f"{page}: cites a dataset but has no claim-adjacent dataset Source comment")
    if not citations:
        return errors, warnings
    try:
        manifest, index = load_rd_bridge(root)
    except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
        return [f"{page}: cannot check dataset claims: {exc}"], warnings
    for path, commit, ids, text in citations:
        where = f"{page}: Source {path} @ {commit}"
        if path != RD_BRIDGE_MAP:
            errors.append(f"{where}: unknown dataset file")
            continue
        if path not in sources:
            errors.append(f"{page}: {path} is cited inline but missing from frontmatter sources")
        if not manifest["commit"].startswith(commit):
            warnings.append(f"{where}: reviewed against an older snapshot; current is "
                            f"{manifest['commit'][:7]}. Re-check and update the commit")
        missing = [n for n in ids if n not in index]
        if missing:
            errors.append(f"{where}: residue_id {', '.join(map(str, missing))} not in current snapshot")
            continue
        params: set[str] = set()
        commodities: set[str] = set()
        for n in ids:
            p, c = record_codes(index[n])
            params |= p
            commodities |= c
        for code in sorted(set(PARAM_CODE_RE.findall(text)) - params):
            errors.append(f"{where}: PARAM code {code} not in cited residue records")
        for code in sorted(set(ANNEX_CODE_RE.findall(text)) - commodities):
            errors.append(f"{where}: Annex I code {code} not in cited residue scopes")
        records = [index[n] for n in ids]
        for row in (line for line in text.splitlines() if line.lstrip().startswith("|")):
            problem = row_problem(row, records)
            if problem:
                errors.append(f"{where}: {problem}")
    return errors, warnings


def row_problem(row: str, records: list[dict[str, Any]]) -> str | None:
    """A table row pairs a scope with whole-residue codes; check that pairing.

    Rows naming Annex I codes must match an exception whose commodity and
    excluded codes all appear in the row. Rows marked "Default" must match a
    default definition. Component codes are allowed in prose, not here.
    """
    codes = set(PARAM_CODE_RE.findall(row))
    if not codes:
        return None
    annex = set(ANNEX_CODE_RE.findall(row))
    if annex:
        scopes = [e for r in records for e in r.get("exceptions", [])
                  if set(e["commodity_codes"]) | set(e.get("except_codes") or []) == annex]
        label = f"scope {', '.join(sorted(annex))}"
    elif "default" in row.lower():
        scopes = [r["default"] for r in records]
        label = "default scope"
    else:
        return None
    if not any(codes <= set(scope.get("param_codes") or []) for scope in scopes):
        return f"{', '.join(sorted(codes))} is not the whole-residue code for {label} in cited records"
    return None
