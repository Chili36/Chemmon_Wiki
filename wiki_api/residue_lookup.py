"""Look up the pinned rd-bridge residue records for pesticides named in a question.

The generated pages list only pesticides whose definition changes by food or that lack a PARAM
link, so most pesticides (one definition, one code) appear on no page. For /wiki/ask and
/wiki/context-pack this module finds residue records whose name occurs in the question and
renders them as evidence under the generated page LOOKUP_PAGE. Matching is deterministic text
matching on residue names; no model is called. The rendering helpers are shared with
tools/rd_bridge_page.py.
"""
from __future__ import annotations

import functools
import hashlib
import json
import re
from pathlib import Path
from typing import Any

from wiki_api.datasets import (
    DATASETS_DIR, PARAM_CODE_RE, RD_BRIDGE_MAP, load_rd_bridge, read_manifest,
)

ANNEX_DIR = DATASETS_DIR / "eu-annex-i"
ANNEX_SOURCE = "datasets/eu-annex-i/products.json"
ATTRIBUTION_SOURCE = "datasets/rd-bridge/DATA_SOURCES.md"
LOOKUP_PAGE = "pesticide-residue-definition-lookup.md"
MAX_RECORDS = 6
EXAMPLE_ID = 10  # acetamiprid: a default and an animal-product definition
HTML_COMMENT_RE = re.compile(r"<!--(.*?)-->", re.DOTALL)
FOOD_PREFIX_RE = re.compile(r"(?:^|\s)(?:in|on|from) $")
MARKERS_RE = re.compile(r"\s*\((?:R|F|A|L|\*|\+|\+\+)\)")

# rd-bridge match methods that give a whole-definition PARAM link (docs/MAPPING_METHOD.md).
# "model" is a model's choice for a definition the rules could not link; it is shown like the
# others by maintainer decision (#36). near/ambiguous/none are suggestions or gaps.
TRUSTED_METHODS = {"exact", "spelling", "compound_set", "cas", "alias", "model"}
UNTRUSTED_LABEL = {"near": "near match only", "ambiguous": "ambiguous match", "none": "no match"}


class NamesMissing(ValueError):
    pass


def short_name(name: str) -> str:
    name = re.sub(r"\s*\((?:R|F|A|L|\*)\)", "", name).strip()
    short = re.split(r"\s*:|\s+\(|\((?=[a-z]{3,}\s)", name, maxsplit=1)[0].strip()
    expressed = re.search(r"expressed as ([\w-]+)", name)
    if short.lower().startswith("sum of") and expressed:
        return f"{expressed.group(1).capitalize()} ({short[0].lower()}{short[1:]})"
    return short


def _clean(name: str) -> str:
    name = re.sub(r"^\(?[a-z]\)\s*", "", name.strip())
    name = re.sub(r"\s*\(\d+\)$", "", name)
    name = re.sub(r"\s*-\s*", " - ", name) if name.isupper() else name
    return name.capitalize() if name.isupper() else name


def annex_labels(root: Path) -> dict[str, str]:
    """Readable names for Annex I codes, qualified by their parent where the source name is relative."""
    products = json.loads((root / ANNEX_DIR / "products.json").read_text(encoding="utf-8"))
    by_id = {p["product_id"]: p for p in products}
    children: dict[Any, list[dict]] = {}
    for p in products:
        children.setdefault(p["product_parent_id"], []).append(p)
    labels = {}
    for p in products:
        name, parent = p["product_name"].strip(), by_id.get(p["product_parent_id"])
        parent_name = parent["product_name"].strip() if parent else ""
        lettered = re.match(r"^\(?[a-z]\)", name)
        if name.endswith(" from"):
            kids = sorted(children.get(p["product_id"], []), key=lambda c: c["product_code"])
            label = f"{name} {', '.join(_clean(c['product_name']) for c in kids)}"
        elif lettered and parent_name.endswith(" from"):
            label = f"{parent_name} {_clean(name)}"
        elif re.match(r"^\(?[a-z]\)", parent_name) and parent and \
                by_id.get(parent["product_parent_id"], {}).get("product_name", "").strip().endswith(" from"):
            label = f"{_clean(parent_name).capitalize()} {_clean(name)[0].lower()}{_clean(name)[1:]}"
        else:
            label = _clean(name)
        labels[p["product_code"]] = label
    return labels


def _scope(exception: dict[str, Any], labels: dict[str, str]) -> str:
    def named(codes: list[str]) -> str:
        missing = [c for c in codes if c not in labels]
        if missing:
            raise NamesMissing(f"no Annex I name for {_cell(', '.join(map(str, missing)))}; "
                               "run tools/ingest_annex_i.py")
        return ", ".join(f"`{_digits(c)}`" for c in codes)
    text = named(exception["commodity_codes"])
    if exception.get("except_codes"):
        text += "; **except** " + named(exception["except_codes"])
    if exception.get("repairs"):
        text += " †"
    return text


def _code(scope: dict[str, Any]) -> str:
    method = scope.get("method")
    codes = scope.get("param_codes") or []
    if method in TRUSTED_METHODS and codes and all(PARAM_CODE_RE.fullmatch(str(c)) for c in codes):
        return ", ".join(f"`{c}`" for c in codes)
    return f"no trustworthy PARAM code ({_cell(UNTRUSTED_LABEL.get(method, method or 'unknown'))})"


def _cell(text: Any) -> str:
    """Make upstream text inert in markdown and in model evidence.

    Dataset text must not open HTML comments (a forged `Source:` locator),
    supply backticked codes that the claim check would trust, add wiki links,
    or break the table.
    """
    text = re.sub(r"\s+", " ", str(text)).replace("|", "/")
    text = text.replace("`", "'").replace("<", "&lt;").replace(">", "&gt;")
    return text.replace("[[", "[ [").replace("]]", "] ]").strip()


def _digits(value: Any) -> str:
    """A commodity code from upstream data, accepted only as plain digits."""
    value = str(value)
    if not re.fullmatch(r"\d{1,7}", value):
        raise ValueError(f"unexpected commodity code in dataset: {_cell(value)[:40]}")
    return value


def _scope_label(scope: dict[str, Any], labels: dict[str, str]) -> str:
    return _scope(scope, labels) if "commodity_codes" in scope else "Default"


def _relationship(text: Any) -> str:
    return _cell(str(text).replace("_", " "))


def _gap_term(term: Any) -> str:
    if not isinstance(term, dict):
        return f"- {_cell(term)}"
    code = str(term.get("code", ""))
    shown = f"`{code}`" if PARAM_CODE_RE.fullmatch(code) else _cell(code)
    return (f"- {shown} {_cell(term.get('name', ''))}: {_relationship(term.get('relationship', 'related'))}, "
            "**not an exact match**.")




def _norm(text: str) -> str:
    text = text.lower().replace("sulph", "sulf")
    return re.sub(r"[^a-z0-9]+", " ", text).strip()


@functools.lru_cache(maxsize=4096)
def name_keys(name: str) -> frozenset[str]:
    """Normalised names a question may use for a residue record."""
    name = MARKERS_RE.sub("", name).strip()
    keys = {re.split(r"\s*\(|:", name, maxsplit=1)[0]}
    if ":" in name:
        keys.add(re.split(r"\s*\(", name.split(":", 1)[1], maxsplit=1)[0])
    keys.update(re.findall(r"\((?:aka|also called|formerly)\s+([^()]+)\)", name, re.I))
    expressed = re.search(r"expressed as ([\w,-]+(?: [\w-]+)?)\s*\)?\s*$", name)
    if expressed and name.lower().startswith("sum of"):
        keys.add(expressed.group(1))
    return frozenset(k for k in (_norm(key) for key in keys) if len(k) >= 3)


def find_records(question: str, index: dict[int, dict[str, Any]], limit: int = MAX_RECORDS) -> list[dict[str, Any]]:
    """Records whose name occurs in the question as whole words, longest names first, at most `limit`."""
    text = f" {_norm(question)} "
    hits: dict[int, int] = {}

    def named(key: str) -> bool:
        # A name right after "in", "on" or "from" is the sampled food ("residues in cow milk"),
        # not the substance; several basic substances are named after foods. Only the few
        # characters before each occurrence are inspected, so long questions stay linear.
        needle = f" {key} "
        start = text.find(needle)
        while start != -1:
            if not FOOD_PREFIX_RE.search(text[max(0, start - 6):start + 1]):
                return True
            start = text.find(needle, start + 1)
        return False

    for rid, record in index.items():
        longest = max((len(k) for k in name_keys(record["name"]) if named(k)), default=0)
        if longest:
            hits[rid] = longest
    ordered = sorted(hits, key=lambda rid: (-hits[rid], rid))
    return [index[rid] for rid in ordered[:limit]]


def render_record(record: dict[str, Any], labels: dict[str, str]) -> str:
    """One residue record: scopes and whole-residue codes as a table, parts and gaps as prose."""
    name = _cell(short_name(record["name"]))
    rows, notes = [], []
    for scope in [record["default"], *record.get("exceptions", [])]:
        where = _scope_label(scope, labels)
        code = _code(scope)
        if code.startswith("no trustworthy"):
            code = "no PARAM code found"
        rows.append(f"| {where} | {_cell(scope['definition'])} | {code} |")
        parts = [c for c in scope.get("components") or []
                 if c.get("role", "analyte") == "analyte" and c.get("param_codes")]
        whole = set(scope.get("param_codes") or [])
        parts = [c for c in parts if set(c["param_codes"]) != whole]
        if len(parts) > 1 and code != "no PARAM code found":
            listed = "; ".join(f"{_cell(c.get('name') or c.get('text', ''))} "
                               + ", ".join(f"`{p}`" for p in c["param_codes"] if PARAM_CODE_RE.fullmatch(str(p)))
                               for c in parts)
            notes.append(f"- {where}: parts that can be reported as `P002A`: {listed}.")
        gap = scope.get("catalogue_gap")
        if isinstance(gap, dict):
            notes.append(f"- {where}: catalogue gap. {_cell(gap.get('reason', ''))} "
                         f"{_cell(gap.get('resolution', ''))}")
            notes += [f"  {_gap_term(t)}" for t in gap.get("related_terms") or []]
    table = ["| Scope (Annex I) | Residue definition | Whole-residue paramCode |", "|---|---|---|", *rows]
    return "\n".join([f"### {name}", "", *table, "", *notes]).rstrip() + "\n"


def _codes_legend(records: list[dict[str, Any]], labels: dict[str, str]) -> str:
    used = sorted({c for r in records for s in r.get("exceptions", [])
                   for c in [*s["commodity_codes"], *(s.get("except_codes") or [])]})
    if not used:
        return ""
    return "\nAnnex I codes: " + "; ".join(f"`{_digits(c)}` {_cell(labels.get(c, ''))}" for c in used) + ".\n"


def _record_block(record: dict[str, Any], labels: dict[str, str], short: str) -> str:
    return (f"<!-- Source: {RD_BRIDGE_MAP} @ {short}, residue_id {record['residue_id']} -->\n\n"
            + render_record(record, labels) + _codes_legend([record], labels))


def render_lookup_page(root: Path) -> str:
    manifest, index = load_rd_bridge(root)
    annex = read_manifest(root / ANNEX_DIR)
    labels = annex_labels(root)
    short, changed = manifest["commit"][:7], manifest["dataset_changed_at"]
    updated = max(manifest["ingested_at"], annex["retrieved_at"])
    n_scopes = sum(1 + len(r.get("exceptions", [])) for r in index.values())
    example = _record_block(index[EXAMPLE_ID], labels, short) if EXAMPLE_ID in index else ""
    return f'''---
title: "Pesticide Residue Definition Lookup"
type: "reference"
domain: "pesticide"
last_updated: "{updated}"
sources:
  - "{RD_BRIDGE_MAP}"
  - "{ATTRIBUTION_SOURCE}"
  - "{ANNEX_SOURCE}"
related:
  - "[[pesticide-residue-definition-by-matrix]]"
  - "[[pesticide-residue-definitions-by-food]]"
  - "[[pesticide-residue-definitions-without-param-link]]"
  - "[[pesticide-residue-definition-wording]]"
  - "[[ssd2-analysis-parameter-coding]]"
select_when: "The residue definition, whole-residue paramCode or parts for a named pesticide, including pesticides with a single residue definition for all foods (for example glyphosate or diquat)."
---

# Pesticide Residue Definition Lookup

<!-- Generated by tools/rd_bridge_page.py from the pinned dataset snapshots. Do not edit; run tools/ingest_rd_bridge.py. -->

## How this lookup works

- **Every pesticide in the snapshot.** When a question names a pesticide, the wiki service attaches that pesticide's record from rd-bridge snapshot `{short}` (residue map of {changed}) under "Records for this question". The snapshot holds {len(index)} residue definitions with {n_scopes} scopes, including the many pesticides with one definition and one code for all foods, which no other page lists.
- **No record attached** means the question named no pesticide in the snapshot under a name the lookup recognises; try the name used in the EU Pesticides Database.
- **Reading a record.** "Default" applies to every food not covered by an exception; an exception covers the listed Annex I codes and everything under them, minus the codes after **except**; † marks a scope rd-bridge interpreted from the EU footnote text. Report the whole-residue code with `paramType` `P005A` when every part was analysed (`P004A` for a subset) and the parts with `P002A`; see [[pesticide-residue-definition-by-matrix]] and [[pesticide-residue-definition-wording]].
- **No PARAM code found** means rd-bridge found no PARAM term for that definition; see [[pesticide-residue-definitions-without-param-link]]. Do not substitute a similar code.
- **Latest definitions only.** For samples from earlier years, confirm the definition that applied on the sampling date.
- **Authority.** rd-bridge is a derived, non-official bridge from the EU Pesticides Database (DG SANTE) to EFSA PARAM. The legislation decides; EFSA validates `paramCode`s against its Legal Limits database (LL_04).

## Example record

{example}
<!-- Source: {ATTRIBUTION_SOURCE} @ {short} -->

## Sources and attribution

- rd-bridge contributors, *rd-bridge* reference dataset, commit `{_cell(manifest["commit"])}`, {_cell(manifest["repository"])}. Derived and non-official; data contributions under CC BY 4.0 (see its DATA_SOURCES.md).
- European Commission, DG SANTE, *EU Pesticides Database*; European Food Safety Authority, *PARAM catalogue*. No endorsement by the European Commission, EFSA or any Member State is implied.
'''


@functools.lru_cache(maxsize=4)
def _snapshot(root: str, stamp: tuple) -> tuple[dict, dict, dict, str]:
    path = Path(root)
    manifest, index = load_rd_bridge(path)
    page = (path / "wiki" / "chemmon-guidance" / LOOKUP_PAGE).read_text(encoding="utf-8")
    return manifest, index, annex_labels(path), page


def _stamp(root: Path) -> tuple:
    """Modification times of the files the lookup reads; a new snapshot invalidates the cache."""
    files = [root / RD_BRIDGE_MAP.replace("datasets/", "chemmon_docs/datasets/", 1),
             root / ANNEX_DIR / "products.json", root / "wiki" / "chemmon-guidance" / LOOKUP_PAGE]
    return tuple(f.stat().st_mtime_ns for f in files)


def lookup_markdown(root: Path, question: str) -> str | None:
    """The lookup page body plus the records the question names, or None when it names none."""
    manifest, index, labels, page = _snapshot(str(root.resolve()), _stamp(root))
    records = find_records(question, index)
    if not records:
        return None
    body = page.split("\n---\n", 1)[1] if page.startswith("---") else page
    body = body.split("## Example record", 1)[0].rstrip()
    blocks = "\n".join(_record_block(r, labels, manifest["commit"][:7]) for r in records)
    return f"{body}\n\n## Records for this question\n\n{blocks}"


def lookup_evidence(root: Path, question: str) -> dict[str, Any] | None:
    """Citable evidence for /wiki/ask and /wiki/context-pack, in the shape of evidence.full_evidence."""
    try:
        raw = lookup_markdown(root, question)
    except (OSError, ValueError, KeyError, json.JSONDecodeError):
        return None
    if raw is None:
        return None
    content = HTML_COMMENT_RE.sub(lambda m: m.group(1).strip() if m.group(1).strip().startswith("Source:") else "", raw)
    content = re.sub(r"\n{3,}", "\n\n", content).strip()
    return {"page_name": LOOKUP_PAGE, "title": "Pesticide Residue Definition Lookup",
            "summary": "Residue records for the pesticides named in this question, from the pinned rd-bridge snapshot.",
            "domain": "pesticide", "content": content,
            "sources": [RD_BRIDGE_MAP, ATTRIBUTION_SOURCE, ANNEX_SOURCE], "source_pages": [],
            "evidence_kind": "full", "citable": True,
            "sha256": hashlib.sha256(content.encode()).hexdigest(), "last_updated": None}
