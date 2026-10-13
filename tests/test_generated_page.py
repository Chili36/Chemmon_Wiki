"""Generated page of food-dependent residue definitions and the Annex I name snapshot."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from tests.test_datasets import RECORDS, commit_records, git
from tools import ingest_annex_i
from tools.health_check import run_health_check
from tools.ingest_rd_bridge import ingest
from tools.rd_bridge_page import PAGE_NAME, NamesMissing, annex_labels, render, short_name, write
from wiki_api.datasets import claim_problems
from wiki_api.wiki_store import ROOT_PAGE_PATHS, split_frontmatter

ROOT = Path(__file__).resolve().parents[1]


def product(pid, parent, code, name):
    return {"product_id": pid, "product_parent_id": parent, "product_code": code, "product_name": name}


PRODUCTS = [
    product(1, None, "1000000", "PRODUCTS OF ANIMAL ORIGIN -TERRESTRIAL ANIMALS"),
    product(2, 1, "1010000", "Commodities from"),
    product(3, 2, "1012000", "(b) bovine"),
    product(4, 3, "1012010", "Muscle"),
    product(5, 1, "1020000", "Milk"),
    product(6, 1, "1040000", "Honey and other apiculture products (7)"),
] + [product(100 + n, None, f"0{n:06d}", f"Plant product {n}") for n in range(100)]


def fake_api(pages):
    def get(url):
        return pages[url]
    return get


def api_pages(rows, size=40):
    chunks = [rows[i:i + size] for i in range(0, len(rows), size)]
    urls = [ingest_annex_i.URL] + [f"https://example.org/page{i}" for i in range(1, len(chunks))]
    return {url: {"value": chunk, "nextLink": urls[i + 1] if i + 1 < len(urls) else None}
            for i, (url, chunk) in enumerate(zip(urls, chunks))}


@pytest.fixture
def root(tmp_path):
    root = tmp_path / "wiki-root"
    (root / "wiki" / "chemmon-guidance").mkdir(parents=True)
    (root / "chemmon_docs").mkdir()
    ingest_annex_i.ingest(root, fake_api(api_pages(PRODUCTS)))
    return root


@pytest.fixture
def upstream(tmp_path):
    repo = tmp_path / "rd-bridge"
    repo.mkdir()
    git(repo, "init", "-q", "-b", "main")
    records = json.loads(json.dumps(RECORDS))
    records[0]["default"]["method"] = "exact"
    records[0]["exceptions"][0]["method"] = "exact"
    records.append({"residue_id": 7, "version": 1, "name": "Sum of M4 and M6, expressed as pinoxaden(R)(A)",
                    "default": {"definition": "Sum of M4 and M6", "method": "exact", "param_codes": ["RF-1-PAR"]},
                    "exceptions": [{"commodity_codes": ["1020000"], "except_codes": [],
                                    "definition": "M4 only (AE 0172747)", "method": "near",
                                    "param_codes": ["RF-2-PAR"],
                                    "repairs": [{"from": "102000", "to": "1020000", "reason": "digit dropped"}]}]})
    commit_records(repo, records, "first")
    return repo


def test_annex_ingest_follows_pagination_and_rejects_bad_lists(root, tmp_path):
    products = json.loads((root / ingest_annex_i.TARGET / "products.json").read_text())
    assert len(products) == len(PRODUCTS)
    assert set(products[0]) == set(ingest_annex_i.FIELDS)
    for rows, message in ((PRODUCTS[:50], "suspiciously small"), (PRODUCTS + PRODUCTS[:1], "duplicate")):
        with pytest.raises(ValueError, match=message):
            ingest_annex_i.ingest(tmp_path / "other", fake_api(api_pages(rows)))
    assert not (tmp_path / "other").exists()


def test_annex_labels_qualify_relative_names(root):
    labels = annex_labels(root)
    assert labels["1012010"] == "Bovine muscle"
    assert labels["1012000"] == "Commodities from bovine"
    assert labels["1010000"] == "Commodities from bovine"
    assert labels["1040000"] == "Honey and other apiculture products"
    assert labels["1000000"] == "Products of animal origin - terrestrial animals"


def test_short_names():
    assert short_name("Thiabendazole(R)") == "Thiabendazole"
    assert short_name("2-phenylphenol (sum of 2-phenylphenol and its conjugates)(R)(F)") == "2-phenylphenol"
    assert short_name("Sum of M4 and M6 (both free and conjugated), expressed as pinoxaden(R)(A)") \
        == "Pinoxaden (sum of M4 and M6)"


def test_ingest_regenerates_complete_page_without_untrusted_codes(root, upstream):
    report, written = ingest(root, str(upstream), "main")
    assert written and f"Regenerated {PAGE_NAME}" in report
    page = (root / "wiki" / "chemmon-guidance" / PAGE_NAME).read_text()
    assert "2 of 3 definitions" in page and "not listed has one residue definition" in page
    assert "Glyphosate" not in page
    assert "| Acetamiprid | `1000000`; **except** `1040000` |" in page
    assert "RF-2-PAR" not in page and "no trustworthy PARAM code (near match only)" in page
    assert "reads code `102000`; rd-bridge reads `1020000`" in page
    assert "| `1040000` | Honey and other apiculture products |" in page
    data, body = split_frontmatter(page)
    assert claim_problems(root, PAGE_NAME, data["sources"], body) == ([], [])
    assert write(root) is False


def test_missing_annex_name_is_reported_not_guessed(root, upstream):
    records = json.loads(json.dumps(RECORDS))
    records[0]["exceptions"][0]["except_codes"] = ["1099999"]
    commit_records(upstream, records, "new scope")
    report, _ = ingest(root, str(upstream), "main")
    assert "NOT regenerated" in report and "1099999" in report
    with pytest.raises(NamesMissing):
        render(root)


def test_health_rejects_stale_or_edited_generated_page(root, upstream):
    for path in ROOT_PAGE_PATHS.values():
        (root / path).parent.mkdir(parents=True, exist_ok=True)
        (root / path).write_text("# Orientation\n")
    (root / "index.md").write_text(f"- [Gen](wiki/chemmon-guidance/{PAGE_NAME}): Generated list\n")
    ingest(root, str(upstream), "main")
    page = root / "wiki" / "chemmon-guidance" / PAGE_NAME
    # The fixture's related links point at pages this small wiki lacks; only check the generated-page rule.
    assert not any("differs from its dataset snapshot" in e for e in run_health_check(root).errors)
    page.write_text(page.read_text().replace("Acetamiprid", "Acetamiprid ", 1))
    assert any("differs from its dataset snapshot" in e for e in run_health_check(root).errors)


def test_repository_generated_page_is_current():
    assert (ROOT / "wiki" / "chemmon-guidance" / PAGE_NAME).read_text() == render(ROOT)
