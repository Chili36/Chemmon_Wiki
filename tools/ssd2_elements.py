#!/usr/bin/env python3
"""SSD2 element reference: a compact list of every element for column mapping.

docs/ssd2-elements.json is extracted from two fixed source tables, independently
of wiki text: the ChemMon 2026 element list (Table 7: label, type, controlled
terminology, ChemMon status, SSD1 name) and the SSD2 2013 element table
(descriptions). The wiki page ssd2-element-reference.md is rendered from the
JSON and never edited by hand; the health check fails when it differs.

Usage:
  python tools/ssd2_elements.py extract --output NEW.json  # from the PDFs; review, then adopt
  python tools/ssd2_elements.py page                       # rewrite the page from the JSON
  python tools/ssd2_elements.py page --check               # exit 1 if the page is out of date
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from wiki_api.source_review import sha256  # noqa: E402

JSON_PATH = Path("docs") / "ssd2-elements.json"
PAGE_NAME = "ssd2-element-reference.md"
CHEMMON_PDF = "*Chemical monitoring*.pdf"
SSD2_PDF = "*Standard Sample Description*.pdf"
CHEMMON_PAGES = (80, 84)  # physical pages of Table 7
SSD2_PAGES = (23, 32)  # physical pages of the SSD2 element table
CODE_RE = re.compile(r"^\s{0,8}([A-N]\.\d\d)\s{2,}")
STATUSES = ("Mandatory", "Optional", "Not applicable")

SECTIONS = {
    "A": "Local organisation", "B": "Sampling programme", "C": "Sampling event",
    "D": "Sample taken", "E": "Matrix sampled", "F": "Sample analysed",
    "G": "Matrix analysed", "H": "Sample analysed portion", "I": "Isolate",
    "J": "Laboratory", "K": "Parameter", "L": "Analytical method",
    "M": "Result", "N": "Evaluation",
}

# The wiki page that explains each element's ChemMon rules. A test checks that
# each page names its elements.
WIKI_PAGES = {
    "ssd2-programme-identification": ["progId"],
    "ssd2-programme-legal-reference": ["progLegalRef"],
    "ssd2-programme-strategy-and-type": ["sampStrategy", "progType"],
    "ssd2-sampling-method-and-point": ["sampMethod", "sampler", "sampPoint"],
    "ssd2-sampling-event-and-unit": ["sampEventId", "sampUnitType", "sampUnitSize", "sampUnitSizeUnit"],
    "ssd2-sample-identifiers": ["sampId", "sampInfo.origSampId"],
    "ssd2-sampling-country": ["sampCountry"],
    "ssd2-sampling-date": ["sampY", "sampM", "sampD"],
    "ssd2-matrix-sampled-matrix": ["sampMatCode", "sampMatText"],
    "ssd2-matrix-origin": ["origCountry", "origArea"],
    "ssd2-matrix-analysed-sample": ["sampAnId", "anMatCode", "anMatText"],
    "ssd2-analysis-context": ["analysisY", "anPortSeq"],
    "ssd2-analysis-laboratory": ["labId", "labAccred", "labCountry"],
    "ssd2-analysis-parameter-coding": ["paramType", "paramCode", "paramText"],
    "ssd2-analysis-methods": ["anMethRefId", "anMethRefCode", "anMethType", "anMethCode", "anMethText",
                              "anMethInfo"],
    "ssd2-result-identification": ["resId"],
    "ssd2-result-method-accreditation": ["accredProc", "CCalpha", "CCbeta"],
    "ssd2-result-units-and-limits": ["resUnit", "resLOD", "resLOQ", "resLLWR", "resULWR",
                                     "resInfo.notSummed", "resValUncertSD", "evalHighLimit"],
    "ssd2-result-value-and-type": ["resVal", "resQualValue", "resType"],
    "ssd2-result-recovery-correction": ["resValRec", "resValRecCorr"],
    "ssd2-result-expression-basis": ["exprResPerc", "exprResType"],
    "ssd2-result-uncertainty": ["resValUncert"],
    "ssd2-evaluation-limits": ["evalLowLimit", "evalLimitType"],
    "ssd2-evaluation-code": ["evalCode", "evalInfo.resAsses"],
    "ssd2-evaluation-actions": ["actTakenCode"],
    "ssd2-evaluation-conclusions": ["evalInfo.conclusion", "evalInfo.com"],
    "food-additives-reporting": ["evalInfo.restrictionException"],
    "contaminant-reporting": ["origFishAreaCode"],
    # Elements without a topic page: link the business rules that constrain them.
    "business-rules-gbr": ["localOrgInfo", "progInfo", "sampUnitIds", "repCountry", "sampMatType",
                           "origFishAreaText", "sampAnRefTime", "anMatInfo"],
    "business-rules-gbr-dates": ["sampEventInfo", "repYear", "sampMatInfo", "sampAnInfo", "analysisM",
                                 "analysisD"],
    "business-rules-gbr-consistency": ["localOrgId", "localOrgCountry", "sampSize", "sampSizeUnit",
                                       "procCountry", "anPortSize", "anPortSizeUnit", "anPortInfo"],
    "business-rules-cross-cutting": ["sampArea", "procArea"],
}
PAGE_OF = {name: page for page, names in WIKI_PAGES.items() for name in names}
# Table 7 spells this name with a capital O; the element section and the wiki use origSampId.
NAME_FIXES = {"sampInfo.OrigSampId": "sampInfo.origSampId"}


def _pdf(root: Path, pattern: str) -> Path:
    matches = list((root / "chemmon_docs").glob(pattern))
    if len(matches) != 1:
        raise ValueError(f"expected one source matching {pattern}")
    return matches[0]


def _pages(path: Path, first: int, last: int) -> list[str]:
    text = subprocess.run(["pdftotext", "-layout", str(path), "-"], check=True,
                          capture_output=True, text=True).stdout.split("\f")
    return text[first - 1:last]


def _segments(line: str) -> list[tuple[int, str]]:
    """Fields separated by two or more spaces, with their start columns."""
    return [(m.start(), m.group()) for m in re.finditer(r"\S+(?: \S+)*", line)]


def _clean(text: str) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    for a, b in (("„", "'"), ("‟", "'"), ("‘", "'"), ("’", "'"), ("“", '"'), ("”", '"')):
        text = text.replace(a, b)
    return text


def _join(parts: list[str]) -> str:
    """Join wrapped cell text; a part ending in a letter run cut mid-word (no space) is rejoined."""
    out = ""
    for part in parts:
        if out and (out.endswith("-") and not out.endswith(" -")):
            out = out[:-1] + part
        else:
            out = f"{out} {part}" if out else part
    return _clean(out)


def chemmon_table(pages: list[str]) -> list[dict[str, Any]]:
    """Rows of Table 7. Columns come from the widest row on each page; wrapped cells are joined."""
    rows: list[dict[str, Any]] = []
    for page in pages:
        lines = page.splitlines()
        code_lines = [l for l in lines if CODE_RE.match(l)]
        if not code_lines:
            continue
        starts = [s for s, _ in max((_segments(l) for l in code_lines), key=len)]
        if len(starts) != 8:
            raise ValueError("Table 7 page without a complete row")
        current = None
        for line in lines:
            if CODE_RE.match(line):
                current = {"cells": [[] for _ in starts]}
                rows.append(current)
            elif current is None or not line.strip() or "www.efsa.europa.eu" in line:
                if "www.efsa.europa.eu" in line:
                    current = None
                continue
            for start, text in _segments(line):
                col = max(i for i, s in enumerate(starts) if s <= start + 3)
                current["cells"][col].append(text)
    out = []
    for row in rows:
        c = row["cells"]
        name = "".join(c[1])  # names wrap mid-word (sampInfo.OrigSam / pId)
        if len(c[1]) > 1 and c[1][1][:1].isupper():  # evalInfo.restriction / Exception
            name = c[1][0] + c[1][1]
        status = " ".join(c[5])
        if status not in STATUSES:
            raise ValueError(f"{c[0]}: unexpected status {status!r}")
        # A long SSD1 name pushes its codes into the name cell (moistPerc, fatPerc R.23 R.24).
        ssd1_codes = re.compile(r"[A-Z]\.\d+(?: [A-Z]\.\d+)*")
        c[7] += [t for t in c[6] if ssd1_codes.fullmatch(t)]
        c[6] = [t for t in c[6] if not ssd1_codes.fullmatch(t)]
        out.append({
            "code": c[0][0], "name": NAME_FIXES.get(name, name), "label": _join(c[2]),
            "type": _join(c[3]).replace("xs: string", "xs:string").replace("xs:string(", "xs:string ("),
            "terminology": _join(c[4]).replace("‘Y’", "") or None,
            "chemmon_status": status.lower(),
            "ssd1_name": re.sub(r",\s*", ", ", _join(c[6])) or None,
            "ssd1_code": re.sub(r",?\s+", ", ", _join(c[7])).rstrip(",") or None,
        })
    return out


def ssd2_descriptions(pages: list[str]) -> dict[str, str]:
    """Description per element code from the SSD2 2013 table (last column)."""
    descriptions: dict[str, list[str]] = {}
    current = None
    for page in pages:
        lines = page.splitlines()
        code_lines = [l for l in lines if CODE_RE.match(l)]
        if not code_lines:
            continue
        column = Counter(_segments(l)[-1][0] for l in code_lines).most_common(1)[0][0]
        for line in lines:
            match = CODE_RE.match(line)
            if match:
                current = match.group(1)
                descriptions.setdefault(current, [])
            if current is None or re.match(r"(?:Element|Code)\s", line) or any(
                    s in line for s in ("EFSA Journal", "Standard Sample Description", "Downloaded from")):
                continue  # page header, footer and side margin
            for start, text in _segments(line):
                if start >= column - 3:
                    descriptions[current].append(text)
    return {code: _join(parts) for code, parts in descriptions.items()}


def extract(root: Path) -> dict[str, Any]:
    chemmon, ssd2 = _pdf(root, CHEMMON_PDF), _pdf(root, SSD2_PDF)
    elements = chemmon_table(_pages(chemmon, *CHEMMON_PAGES))
    descriptions = ssd2_descriptions(_pages(ssd2, *SSD2_PAGES))
    for element in elements:
        sub_element = "." in element["name"]  # ChemMon-specific parts of a compound element
        element["section"] = SECTIONS[element["code"][0]]
        element["description"] = None if sub_element else descriptions.get(element["code"])
        element["wiki_page"] = PAGE_OF.get(element["name"])
    return {
        "version": 1,
        "edition": "ChemMon 2026 Table 7; SSD2 2013 element table",
        "extracted_at": date.today().isoformat(),
        "method": "pdftotext -layout; Table 7 columns from the widest row per page, wrapped cells joined; "
                  "descriptions from the last column of the SSD2 2013 table",
        "limitations": [
            "chemmon_status is Table 7's generic status. Business rules make some optional elements "
            "mandatory by domain or case (e.g. resLOQ, CCalpha); see the linked wiki page.",
            "Descriptions are the generic SSD2 2013 definitions. ChemMon sub-elements of compound "
            "elements (name with a dot) have only their Table 7 label.",
        ],
        "sources": {p.relative_to(root).as_posix(): sha256(p) for p in (chemmon, ssd2)},
        "elements": elements,
    }


def load(root: Path) -> dict[str, Any]:
    return json.loads((root / JSON_PATH).read_text(encoding="utf-8"))


def _cell(text: Any) -> str:
    return re.sub(r"\s+", " ", str(text)).replace("|", "/").replace("<", "&lt;").replace(">", "&gt;").strip()


def render(root: Path) -> str:
    data = load(root)
    elements = data["elements"]
    used = [e for e in elements if e["chemmon_status"] != "not applicable"]
    unused = [e for e in elements if e["chemmon_status"] == "not applicable"]
    counts = Counter(e["chemmon_status"] for e in used)
    sections = []
    for letter, section in SECTIONS.items():
        rows = [e for e in used if e["code"][0] == letter]
        if not rows:
            continue
        lines = [f"## {letter}. {section}", "",
                 "| Code | Element | Label | M/O | Type | Catalogue | SSD1 | Meaning | Page |",
                 "|---|---|---|---|---|---|---|---|---|"]
        for e in rows:
            ssd1 = f"{e['ssd1_name']} ({e['ssd1_code']})" if e["ssd1_name"] else ""
            page = f"[[{e['wiki_page']}]]" if e["wiki_page"] else ""
            lines.append("| " + " | ".join(_cell(v) for v in (
                e["code"], f"`{e['name']}`", e["label"], e["chemmon_status"][0].upper(),
                e["type"].replace("xs:", ""), e["terminology"] or "", ssd1,
                e["description"] or "", page)) + " |")
        sections.append("\n".join(lines))
    unused_text = ", ".join(f"`{e['name']}`" for e in unused)
    sources = list(data["sources"])

    return f'''---
title: "SSD2 Element Reference"
type: "reference"
domain: "all"
last_updated: "{data["extracted_at"]}"
sources:
  - "{sources[0].removeprefix("chemmon_docs/")}"
  - "{sources[1].removeprefix("chemmon_docs/")}"
source_pages:
  - "ChemMon 2026 pp. 80-84 (Table 7)"
  - "SSD2 2013 pp. 23-32 (element table)"
related:
  - "[[ssd2-data-model]]"
  - "[[business-rules]]"
  - "[[controlled-terminology-catalogues]]"
select_when: "Listing all SSD2 elements, or mapping source-data columns to SSD2 element names: which element holds a given piece of information, its type, catalogue, ChemMon mandatory/optional status and SSD1 name."
---

# SSD2 Element Reference

<!-- Generated by tools/ssd2_elements.py from docs/ssd2-elements.json. Do not edit; run python tools/ssd2_elements.py page. -->

<!-- Source: {sources[0].removeprefix("chemmon_docs/")}, pp. 80-84 (Table 7); {sources[1].removeprefix("chemmon_docs/")}, pp. 23-32 -->

## How to read this list

- **Complete:** all {len(used)} elements used in ChemMon reporting ({counts["mandatory"]} mandatory, {counts["optional"]} optional), one row each. The same data is in `docs/ssd2-elements.json` for tools.
- **M/O** is the generic ChemMon status in Table 7. Business rules make some optional elements mandatory by domain or case (e.g. `resLOQ`, `CCalpha`); the linked page has those rules.
- **Meaning** is the generic SSD2 definition. Rows named with a dot (e.g. `evalInfo.com`) are ChemMon parts of a compound element and have only their label.
- **Catalogue** names the controlled terminology the value must come from; see [[controlled-terminology-catalogues]]. **SSD1** gives the old element name and code, useful when source data still uses SSD1 headers.
- Isolate elements are not used in ChemMon: {unused_text}.

{chr(10).join(s + chr(10) for s in sections)}'''


def page_path(root: Path) -> Path:
    return root / "wiki" / "chemmon-guidance" / PAGE_NAME


def write_page(root: Path) -> bool:
    text = render(root)
    path = page_path(root)
    if path.is_file() and path.read_text(encoding="utf-8") == text:
        return False
    path.write_text(text, encoding="utf-8")
    return True


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    ext = sub.add_parser("extract")
    ext.add_argument("--output", required=True, type=Path)
    pg = sub.add_parser("page")
    pg.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)
    if args.command == "extract":
        record = extract(ROOT)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("x", encoding="utf-8") as f:
            json.dump(record, f, indent=2, ensure_ascii=False)
            f.write("\n")
        print(f"{len(record['elements'])} elements")
        return 0
    if args.check:
        current = page_path(ROOT).read_text(encoding="utf-8") if page_path(ROOT).is_file() else None
        if current != render(ROOT):
            print(f"{PAGE_NAME} is out of date; run python tools/ssd2_elements.py page")
            return 1
        return 0
    print(f"{PAGE_NAME}: {'written' if write_page(ROOT) else 'unchanged'}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
