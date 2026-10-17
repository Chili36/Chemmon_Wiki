#!/usr/bin/env python3
"""Generate the page of pesticides whose residue definition changes by food.

The page is built only from the pinned snapshots in chemmon_docs/datasets/
(rd-bridge residue map and EU Annex I product names). It is never edited by
hand: tools/ingest_rd_bridge.py regenerates it, and the health check fails
when it differs from what this module renders.

Usage:
  python tools/rd_bridge_page.py          # rewrite the page
  python tools/rd_bridge_page.py --check  # exit 1 if the page is out of date
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from wiki_api.datasets import (  # noqa: E402
    DATASETS_DIR, PARAM_CODE_RE, RD_BRIDGE_MAP, load_rd_bridge, read_manifest,
)

PAGE_NAME = "pesticide-residue-definitions-by-food.md"
ANNEX_DIR = DATASETS_DIR / "eu-annex-i"
ANNEX_SOURCE = "datasets/eu-annex-i/products.json"
ATTRIBUTION_SOURCE = "datasets/rd-bridge/DATA_SOURCES.md"
# rd-bridge match methods that give a trustworthy whole-definition PARAM link
# (docs/MAPPING_METHOD.md); near/ambiguous/none are suggestions or gaps.
TRUSTED_METHODS = {"exact", "spelling", "compound_set", "cas", "alias"}
UNTRUSTED_LABEL = {"near": "near match only", "ambiguous": "ambiguous match", "none": "no match"}


class NamesMissing(ValueError):
    pass


def short_name(name: str) -> str:
    name = re.sub(r"\s*\((?:R|F|A|L|\*)\)", "", name).strip()
    short = re.split(r"\s*[:(]", name, maxsplit=1)[0].strip()
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


def param_version(sources_md: str) -> str | None:
    """The PARAM catalogue version named in rd-bridge's DATA_SOURCES.md, if any."""
    match = re.search(r"PARAM catalogue, version \**([\d.]*\d)", sources_md)
    return match.group(1) if match else None


def render(root: Path) -> str:
    manifest, index = load_rd_bridge(root)
    annex = read_manifest(root / ANNEX_DIR)
    labels = annex_labels(root)
    varying = sorted((r for r in index.values() if r.get("exceptions")),
                     key=lambda r: (short_name(r["name"]).lower(), r["residue_id"]))
    sources_md = (root / DATASETS_DIR / "rd-bridge" / "DATA_SOURCES.md").read_text(encoding="utf-8")
    version = param_version(sources_md)
    commit, short = manifest["commit"], manifest["commit"][:7]
    changed = manifest["dataset_changed_at"]
    n_exc = sum(len(r["exceptions"]) for r in varying)
    updated = max(manifest["ingested_at"], annex["retrieved_at"])

    rows, repairs, used = [], [], set()
    for record in varying:
        name = _cell(short_name(record["name"]))
        rows.append(f"| {name} | Default | {_cell(record['default']['definition'])} "
                    f"| {_code(record['default'])} |")
        for exception in record["exceptions"]:
            used.update(exception["commodity_codes"], exception.get("except_codes") or [])
            rows.append(f"| {name} | {_scope(exception, labels)} | {_cell(exception['definition'])} "
                        f"| {_code(exception)} |")
            for repair in exception.get("repairs") or []:
                repairs.append(f"- {name}: the EU footnote reads code `{_digits(repair['from'])}`; rd-bridge "
                               f"reads `{_digits(repair['to'])}` ({_cell(repair['reason'])}).")
        for scope in [record["default"], *record["exceptions"]]:
            for issue in scope.get("issues") or []:
                repairs.append(f"- {name}: {_cell(str(issue))}")
    ids = ", ".join(str(r["residue_id"]) for r in varying)
    legend = "\n".join(f"| `{_digits(c)}` | {_cell(labels[c])} |" for c in sorted(used))

    page = f'''---
title: "Pesticides Whose Residue Definition Changes by Food"
type: "reference"
domain: "pesticide"
last_updated: "{updated}"
sources:
  - "{RD_BRIDGE_MAP}"
  - "{ATTRIBUTION_SOURCE}"
  - "{ANNEX_SOURCE}"
related:
  - "[[pesticide-residue-definition-by-matrix]]"
  - "[[pesticide-reporting]]"
  - "[[legal-limits-database]]"
  - "[[vmpr-reporting]]"
select_when: "Whether a named pesticide's residue definition or PARAM code differs by food, which definition and whole-residue paramCode apply to a food such as milk, honey, meat, liver or cereals, or which pesticides have separate definitions for animal products."
---

# Pesticides Whose Residue Definition Changes by Food

<!-- Generated by tools/rd_bridge_page.py from the pinned dataset snapshots. Do not edit; run tools/ingest_rd_bridge.py. -->

<!-- Source: {RD_BRIDGE_MAP} @ {short}, residue_id {ids} -->

## How to use this list

- **Complete for this snapshot.** This page lists every pesticide whose EU residue definition differs by commodity in rd-bridge snapshot `{short}` (residue map of {changed}): {len(varying)} of {len(index)} definitions, with {n_exc} commodity-specific definitions. A pesticide in the EU Pesticides Database that is **not listed has one residue definition and one whole-residue PARAM code for all foods**.
- **Latest definitions, not historical ones.** The snapshot holds the latest EU-published definitions as of {changed}. For samples from earlier years, confirm the definition that applied on the sampling date in the legislation or EFSA's Legal Limits database.
- **Reading a row.** "Default" applies to every food not covered by one of that pesticide's exceptions. An exception covers the listed Annex I codes and everything under them, minus the codes after **except**. Code names are in the Annex I table at the end. Report the whole-residue code with `paramType` `P005A` (or `P004A` for a subset) and components with `P002A`; see [[pesticide-residue-definition-by-matrix]].
- **No trustworthy code.** Where rd-bridge has no reliable PARAM link, the row says so. Do not substitute a similar-looking code.
- **Placing a food.** Rows use Annex I codes of Regulation (EC) No 396/2005. Plain commodities (milk, bovine liver, honey) can be placed directly. Processed, composite or FoodEx2-coded foods need EFSA's FoodEx2-to-Annex I mapping; use rd-bridge `resolve`, which returns candidates rather than guessing.
- **Scope.** Pesticide residue definitions under Regulation (EC) No 396/2005 only. Veterinary medicines have separate VMPR marker residues ([[vmpr-reporting]]). Definitions and codes only: no MRL values or compliance judgements.
- **Authority.** rd-bridge is a derived, non-official bridge. The legislation decides; EFSA validates pesticide `paramCode`s against the sampled matrix with LL_04 using its Legal Limits database ([[legal-limits-database]]).

## Definitions by pesticide

| Pesticide | Scope (Annex I) | Residue definition | Whole-residue paramCode |
|---|---|---|---|
{chr(10).join(rows)}

## Interpreted source wording

† These scopes are rd-bridge interpretations of the EU footnote text, not verbatim:

{chr(10).join(repairs) if repairs else "- None in this snapshot."}

## Annex I codes used above

<!-- Source: {ANNEX_SOURCE}, retrieved {annex["retrieved_at"]} -->

Names from the EU Pesticides Database; sub-group names are qualified by their parent group.

| Code | Annex I commodity |
|---|---|
{legend}

<!-- Source: {ATTRIBUTION_SOURCE} @ {short} -->

## Sources and attribution

- rd-bridge contributors, *rd-bridge* reference dataset, commit `{_cell(commit)}`, {_cell(manifest["repository"])}. Derived and non-official; the project's data contributions are offered under CC BY 4.0 (see its DATA_SOURCES.md).
- European Commission, DG SANTE, *EU Pesticides Database*: residue definitions and Annex I product names (names retrieved {annex["retrieved_at"]}). The database is informational and has no legal value; only the legislation has legal force.
- European Food Safety Authority, *PARAM catalogue*{f", version {version}" if version else ""}.
- No endorsement by the European Commission, EFSA or any Member State is implied.
'''
    return page


def page_path(root: Path) -> Path:
    return root / "wiki" / "chemmon-guidance" / PAGE_NAME


def write(root: Path) -> bool:
    text = render(root)
    path = page_path(root)
    if path.is_file() and path.read_text(encoding="utf-8") == text:
        return False
    path.write_text(text, encoding="utf-8")
    return True


def main(argv: list[str]) -> int:
    if "--check" in argv:
        current = page_path(ROOT).read_text(encoding="utf-8") if page_path(ROOT).is_file() else None
        if current != render(ROOT):
            print(f"{PAGE_NAME} is out of date; run python tools/rd_bridge_page.py")
            return 1
        return 0
    print(f"{PAGE_NAME}: {'written' if write(ROOT) else 'unchanged'}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
