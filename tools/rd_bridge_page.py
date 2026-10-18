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


def _legend(codes: list[str], labels: dict[str, str]) -> str:
    """Annex I names for the codes used. Commodities by farmed animal and tissue (101ATTT) follow
    Annex I's numbering, so they are explained once instead of listed one by one."""
    tissue = re.compile(r"^101([1-7])(0[1-5]0|000)$")
    farmed = [c for c in codes if tissue.match(c)]
    named = [c for c in codes if c not in farmed]
    text = "; ".join(f"`{_digits(c)}` {_cell(labels[c])}" for c in named)
    if farmed:
        animals = sorted({(m.group(1), labels.get(f"101{m.group(1)}000", "")) for m in map(tissue.match, farmed)})
        def tissue_name(code: str, animal: str) -> str:
            # "Swine edible offals (other than liver and kidney)" -> "edible offals (...)"
            name = labels.get(code, "")
            prefix = labels.get(f"101{animal}000", "").replace("Commodities from ", "")
            return name[len(prefix):].strip() if prefix and name.lower().startswith(prefix.lower()) else name
        tissues = sorted({(m.group(2), tissue_name(c, m.group(1)))
                          for c, m in ((c, tissue.match(c)) for c in farmed) if m.group(2) != "000"})
        animal_text = ", ".join(f"{a} {_cell(label.replace('Commodities from ', ''))}" for a, label in animals)
        tissue_text = ", ".join(f"{t} {_cell(name)}" for t, name in tissues)
        text += (f"; `101ATTT` commodities from a farmed animal (A: {animal_text})"
                 + (f" and tissue (TTT: {tissue_text}; 000 the whole animal group)" if tissues else ""))
    return text


def _short_code(scope: dict[str, Any]) -> str:
    code = _code(scope)
    return "no reliable code" if code.startswith("no trustworthy") else code.replace("`", "")


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

    lines, repairs, used = [], [], set()
    for record in varying:
        name = _cell(short_name(record["name"]))
        parts = [f"default: {_cell(record['default']['definition'])} ({_short_code(record['default'])})"]
        for exception in record["exceptions"]:
            used.update(exception["commodity_codes"], exception.get("except_codes") or [])
            parts.append(f"{_scope(exception, labels).replace('; **except**', ' except')}: "
                         f"{_cell(exception['definition'])} ({_short_code(exception)})")
            for repair in exception.get("repairs") or []:
                repairs.append(f"- {name}: EU footnote reads `{_digits(repair['from'])}`, read as "
                               f"`{_digits(repair['to'])}` ({_cell(repair['reason'])}).")
        for scope in [record["default"], *record["exceptions"]]:
            for issue in scope.get("issues") or []:
                repairs.append(f"- {name}: {_cell(str(issue))}")
        lines.append(f"- **{name}**: " + "; ".join(parts))
    ids = ", ".join(str(r["residue_id"]) for r in varying)
    legend = _legend(sorted(used), labels)

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

## How to read this list

- **Complete:** every pesticide whose EU residue definition differs by food in rd-bridge snapshot `{short}` (map of {changed}): {len(varying)} of {len(index)} definitions. A pesticide not listed has **one definition and one whole-residue code for all foods**.
- **Scopes:** "default" covers every food not in an exception. An exception covers the Annex I codes given and everything under them, minus the codes after "except"; † marks a scope rd-bridge interpreted from the EU footnote. The code in brackets is the whole-residue `paramCode`: report it with `paramType` `P005A` (`P004A` for a subset) and the analysed parts with `paramType` `P002A`; see [[pesticide-residue-definition-by-matrix]].
- **Status:** latest EU definitions from a derived, non-official source. For older samples use the definition valid on the sampling date; the legislation decides and EFSA validates with LL_04 ([[legal-limits-database]]). "no reliable code" means rd-bridge found no trustworthy PARAM link; do not substitute a similar code. Annex I code names are at the end.
- **Limits:** pesticides under Regulation (EC) No 396/2005 only (veterinary medicines: [[vmpr-reporting]]); definitions, not MRL values. A processed or composite food may not fall in one Annex I code: check the candidate scopes instead of guessing.

## Definitions by pesticide

{chr(10).join(lines)}

## Interpreted source wording

{chr(10).join(repairs) if repairs else "- None in this snapshot."}

<!-- Source: {ANNEX_SOURCE}, retrieved {annex["retrieved_at"]} -->

## Annex I codes

{legend}.

<!-- Source: {ATTRIBUTION_SOURCE} @ {short} -->

## Sources and attribution

- rd-bridge contributors, *rd-bridge*, commit `{_cell(commit)}`, {_cell(manifest["repository"])}; derived, non-official, data contributions under CC BY 4.0. European Commission, DG SANTE, *EU Pesticides Database* (residue definitions, Annex I names, retrieved {annex["retrieved_at"]}; informational, no legal value). EFSA, *PARAM catalogue*{f", version {version}" if version else ""}. No endorsement by the European Commission, EFSA or any Member State is implied.
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
