#!/usr/bin/env python3
"""Generate the dataset pages: residue definitions that change by food, and
definitions without a confirmed PARAM code.

The page is built only from the pinned snapshots in chemmon_docs/datasets/
(rd-bridge residue map and EU Annex I product names). It is never edited by
hand: tools/ingest_rd_bridge.py regenerates it, and the health check fails
when it differs from what this module renders.

Usage:
  python tools/rd_bridge_page.py          # rewrite the pages
  python tools/rd_bridge_page.py --check  # exit 1 if a page is out of date
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
GAPS_PAGE_NAME = "pesticide-residue-definitions-without-param-link.md"
ANNEX_DIR = DATASETS_DIR / "eu-annex-i"
ANNEX_SOURCE = "datasets/eu-annex-i/products.json"
ATTRIBUTION_SOURCE = "datasets/rd-bridge/DATA_SOURCES.md"
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


def render_gaps(root: Path) -> str:
    manifest, index = load_rd_bridge(root)
    annex = read_manifest(root / ANNEX_DIR)
    labels = annex_labels(root)
    sources_md = (root / DATASETS_DIR / "rd-bridge" / "DATA_SOURCES.md").read_text(encoding="utf-8")
    version = param_version(sources_md)
    commit, short = manifest["commit"], manifest["commit"][:7]
    changed = manifest["dataset_changed_at"]
    updated = max(manifest["ingested_at"], annex["retrieved_at"])
    records = sorted(index.values(), key=lambda r: (short_name(r["name"]).lower(), r["residue_id"]))

    gaps, rows, ids, used, n_scopes = [], [], [], set(), 0
    for record in records:
        name = _cell(short_name(record["name"]))
        cited = False
        for scope in [record["default"], *record.get("exceptions", [])]:
            n_scopes += 1
            gap = scope.get("catalogue_gap")
            trusted = scope.get("method") in TRUSTED_METHODS and scope.get("param_codes")
            if not gap and trusted:
                continue
            cited = True
            if "commodity_codes" in scope:
                used.update(scope["commodity_codes"], scope.get("except_codes") or [])
            where = _scope_label(scope, labels)
            if isinstance(gap, dict):
                terms = gap.get("related_terms") or []
                catalogue = f"PARAM {_cell(gap.get('param_catalogue_version') or version or '')}".strip()
                gaps += [f"### {name} ({where})", "",
                         f"- **Legal residue definition:** {_cell(scope['definition'])}",
                         f"- **Legal source:** {_cell(gap.get('legal_source', 'not recorded'))}"
                         + (f", applies from {_cell(gap['applies_from'])}" if gap.get("applies_from") else ""),
                         f"- **Gap in {catalogue}:** {_cell(gap.get('reason', ''))}",
                         "- **Related PARAM terms:**" if terms else "- **Related PARAM terms:** none recorded.",
                         *[f"  {_gap_term(t)}" for t in terms],
                         f"- **What to do:** {_cell(gap.get('resolution', 'Follow EFSA guidance.'))}", ""]
            else:
                status = UNTRUSTED_LABEL.get(scope.get("method"), _cell(scope.get("method") or "unknown"))
                refusal = scope.get("model_guess") or {}
                if refusal.get("reason"):
                    # A refused code must not appear where a reader could take it as the answer.
                    reason = PARAM_CODE_RE.sub("", str(refusal["reason"]))
                    reason = re.sub(r"\(\s*[,;\s]*\)", "", reason)
                    reason = re.sub(r"\s+([,.;)])", r"\1", re.sub(r",(\s*,)+", ",", reason))
                    status += f": {_cell(reason)}"
                rows.append(f"| {name} | {where} | {_cell(scope['definition'])} | {status} |")
        if cited:
            ids.append(str(record["residue_id"]))
    legend = "\n".join(f"| `{_digits(c)}` | {_cell(labels[c])} |" for c in sorted(used))
    n_gaps = sum(1 for line in gaps if line.startswith("### "))

    def count(n: int, noun: str) -> str:
        return f"{n} {noun}{'' if n == 1 else 's'}"
    catalogue = f"PARAM {version}" if version else "the PARAM catalogue"

    return f'''---
title: "Pesticide Residue Definitions Without a Confirmed PARAM Code"
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
  - "[[pesticide-residue-definition-wording]]"
  - "[[ssd2-analysis-parameter-coding]]"
  - "[[legal-limits-database]]"
select_when: "No PARAM code can be found for a pesticide residue definition, the only PARAM term found does not match the legal definition (for example a broader isomer sum), or whether a new EU residue definition such as benthiavalicarb under Regulation (EU) 2026/147 has a reportable paramCode."
---

# Pesticide Residue Definitions Without a Confirmed PARAM Code

<!-- Generated by tools/rd_bridge_page.py from the pinned dataset snapshots. Do not edit; run tools/ingest_rd_bridge.py. -->

<!-- Source: {RD_BRIDGE_MAP} @ {short}, residue_id {", ".join(ids) if ids else "none"} -->

## How to use this list

- **Two different situations.** A **confirmed catalogue gap** means the legal residue definition and the reportable PARAM terms do not match, and rd-bridge records the legal source and the related terms. **No confirmed PARAM link** means neither rd-bridge's matching rules nor its model found a term for the same substance among the PARAM pesticide terms in {catalogue}; the model's reason is shown where it gave one. This is **not proof that PARAM has no code**: the substance may be named differently or sit outside the pesticide hierarchy.
- **Do not substitute a similar code.** A term that only resembles the definition, such as a broader isomer sum or the individual substance, is not the whole-residue code. Look for the definition in the `ChemMonRep` reporting hierarchy and EFSA's Legal Limits database ([[legal-limits-database]]), and see [[ssd2-analysis-parameter-coding]] for `paramCode` rules. Where no matching code exists, ask EFSA instead of choosing a near match.
- **Coverage.** This page lists {count(n_gaps, "confirmed catalogue gap")} and {count(len(rows), "scope")} without a confirmed link, out of {n_scopes} residue-definition scopes in rd-bridge snapshot `{short}` (residue map of {changed}). Scopes not listed have a confirmed whole-residue PARAM link; see [[pesticide-residue-definitions-by-food]] for definitions that change by food.
- **Latest definitions only.** The snapshot holds the latest EU-published definitions. A definition that applies from a future date, or that applied to older samples, may differ; check the legal source and the sampling date.
- **Authority.** rd-bridge is a derived, non-official bridge. The legislation decides; EFSA validates pesticide `paramCode`s against the Legal Limits database.

## Confirmed catalogue gaps

{chr(10).join(gaps).rstrip() if gaps else "None in this snapshot."}

## No confirmed PARAM link

"Default" applies to every food not covered by an exception. † marks a scope that rd-bridge interpreted from the EU footnote text.

| Pesticide | Scope (Annex I) | Residue definition | rd-bridge status |
|---|---|---|---|
{chr(10).join(rows)}

## Annex I codes used above

<!-- Source: {ANNEX_SOURCE}, retrieved {annex["retrieved_at"]} -->

| Code | Annex I commodity |
|---|---|
{legend if legend else "| none | |"}

<!-- Source: {ATTRIBUTION_SOURCE} @ {short} -->

## Sources and attribution

- rd-bridge contributors, *rd-bridge* reference dataset, commit `{_cell(commit)}`, {_cell(manifest["repository"])}. Derived and non-official; the project's data contributions are offered under CC BY 4.0 (see its DATA_SOURCES.md).
- European Commission, DG SANTE, *EU Pesticides Database*: residue definitions and Annex I product names. The database is informational and has no legal value; only the legislation has legal force.
- European Food Safety Authority, *PARAM catalogue*{f", version {version}" if version else ""}.
- No endorsement by the European Commission, EFSA or any Member State is implied.
'''


GENERATED = {PAGE_NAME: render, GAPS_PAGE_NAME: render_gaps}


def page_path(root: Path, name: str = PAGE_NAME) -> Path:
    return root / "wiki" / "chemmon-guidance" / name


def write(root: Path) -> list[str]:
    """Rewrite every generated page; return the names of pages that changed."""
    written = []
    for name, render_page in GENERATED.items():
        text = render_page(root)
        path = page_path(root, name)
        if path.is_file() and path.read_text(encoding="utf-8") == text:
            continue
        path.write_text(text, encoding="utf-8")
        written.append(name)
    return written


def main(argv: list[str]) -> int:
    if "--check" in argv:
        stale = [name for name, render_page in GENERATED.items()
                 if not page_path(ROOT, name).is_file()
                 or page_path(ROOT, name).read_text(encoding="utf-8") != render_page(ROOT)]
        for name in stale:
            print(f"{name} is out of date; run python tools/rd_bridge_page.py")
        return 1 if stale else 0
    written = write(ROOT)
    for name in GENERATED:
        print(f"{name}: {'written' if name in written else 'unchanged'}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
