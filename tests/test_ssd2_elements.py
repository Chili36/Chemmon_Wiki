"""SSD2 element reference: extraction from the source tables and the generated page."""
from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

from tools import ssd2_elements
from tools.health_check import run_health_check
from tools.ssd2_elements import JSON_PATH, PAGE_NAME, PAGE_OF, chemmon_table, render, ssd2_descriptions

ROOT = Path(__file__).resolve().parents[1]

# Layout as pdftotext prints Table 7: wrapped names, labels and SSD1 cells, and
# a long SSD1 name that pushes its codes into the name column.
TABLE7_PAGE = """\
     D.03     sampCountry         Country of sampling                 xs:string (2)        COUNTRY       Mandatory                sampCountry                       S.04
     D.11     sampInfo.OrigSam    Additional sample taken              xs:string (100)                    Optional
                pId               information
     M.13     exprResPerc         Expression of result percentage     CompoundType                       Optional                 moistPerc, fatPerc            R.23 R.24
     N.06     evalInfo.restriction   Restriction or exception        xs: string (250)     ADDFOOD       Optional
              Exception
www.efsa.europa.eu/publications                                  EFSA Supporting publication 2026:EN-9911
"""

SSD2_PAGE = """\
Element   Section   Section     Element Name    Element Label        Type(a)           S/R/C   M   Controlled                     Description
Code      Code                                                                                     terminology
M.14      M         Result      exprResType     Expression of        xs:string (5)     S           EXPRRES       Code to describe how the result has been
                                                result type                                                      expressed: whole weight.
M.15      M         Result      resQualValue    Result qualitative   xs:string (3)     S           POSNEG        This field should be completed only if the
                                                                                                                 result value is qualitative.
EFSA Journal 2013;11(10):3424                                                                                                                              29
                                                                                                                                   18314732, 2013, 10, Downloaded from https://efsa.onlinelibrary.wiley.com
"""


def test_table7_rows_join_wrapped_cells():
    rows = {r["code"] + r["name"]: r for r in chemmon_table([TABLE7_PAGE])}
    assert rows["D.03sampCountry"]["terminology"] == "COUNTRY"
    assert rows["D.03sampCountry"]["chemmon_status"] == "mandatory"
    assert rows["D.11sampInfo.origSampId"]["label"] == "Additional sample taken information"
    assert rows["M.13exprResPerc"]["ssd1_name"] == "moistPerc, fatPerc"
    assert rows["M.13exprResPerc"]["ssd1_code"] == "R.23, R.24"
    assert rows["N.06evalInfo.restrictionException"]["type"] == "xs:string (250)"


def test_descriptions_skip_headers_and_margins():
    descriptions = ssd2_descriptions([SSD2_PAGE])
    assert descriptions["M.14"] == "Code to describe how the result has been expressed: whole weight."
    assert descriptions["M.15"] == "This field should be completed only if the result value is qualitative."


def test_repository_json_is_complete_and_linked():
    data = json.loads((ROOT / JSON_PATH).read_text(encoding="utf-8"))
    elements = data["elements"]
    names = [e["name"] for e in elements]
    assert len(elements) == 97 and len(set(names)) == len(names)
    assert {e["chemmon_status"] for e in elements} == {"mandatory", "optional", "not applicable"}
    for element in elements:
        assert element["wiki_page"] == PAGE_OF.get(element["name"]), element["name"]


def test_each_linked_page_names_its_elements():
    for name, page in PAGE_OF.items():
        text = (ROOT / "wiki" / "chemmon-guidance" / f"{page}.md").read_text(encoding="utf-8")
        assert re.search(rf"\b{re.escape(name.split('.')[-1])}\b", text), f"{page} does not name {name}"


def test_repository_page_is_current():
    path = ROOT / "wiki" / "chemmon-guidance" / PAGE_NAME
    assert path.read_text(encoding="utf-8") == render(ROOT)


def test_health_rejects_edited_page(tmp_path):
    root = tmp_path / "wiki-root"
    shutil.copytree(ROOT / "wiki", root / "wiki")
    shutil.copy(ROOT / "index.md", root / "index.md")
    (root / "docs").mkdir()
    shutil.copy(ROOT / JSON_PATH, root / JSON_PATH)
    message = f"{PAGE_NAME}: differs from docs/ssd2-elements.json"
    assert not any(message in e for e in run_health_check(root).errors)
    page = root / "wiki" / "chemmon-guidance" / PAGE_NAME
    page.write_text(page.read_text(encoding="utf-8").replace("| M |", "| O |", 1), encoding="utf-8")
    assert any(message in e for e in run_health_check(root).errors)


def test_page_states_counts_from_the_json():
    text = render(ROOT)
    data = json.loads((ROOT / JSON_PATH).read_text(encoding="utf-8"))
    used = [e for e in data["elements"] if e["chemmon_status"] != "not applicable"]
    assert f"all {len(used)} elements used in ChemMon reporting" in text
    assert text.count("\n| ") - text.count("\n| Code |") == len(used)
    assert ssd2_elements.SECTIONS["N"] == "Evaluation"
