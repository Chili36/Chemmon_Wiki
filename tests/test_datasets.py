"""Dataset snapshots: ingest from a pinned commit, manifest integrity and claim drift."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

from tools.health_check import run_health_check
from tools.ingest_rd_bridge import ingest
from wiki_api.datasets import RD_BRIDGE_DIR, claim_problems, manifest_problems
from wiki_api.source_review import corpus_snapshot

ROOT = Path(__file__).resolve().parents[1]

RECORDS = [
    {"residue_id": 10, "version": 1, "name": "Acetamiprid (R)",
     "default": {"definition": "Acetamiprid", "param_codes": ["RF-0014-001-PPP"]},
     "exceptions": [{"commodity_codes": ["1000000"], "except_codes": ["1040000"],
                     "definition": "Sum of acetamiprid and IM-2-1", "param_codes": ["RF-00003326-PAR"],
                     "components": [{"name": "IM-2-1", "param_codes": ["RF-00002836-PAR"]}]}]},
    {"residue_id": 1, "version": 1, "name": "Glyphosate",
     "default": {"definition": "Glyphosate", "param_codes": ["RF-0230-001-PPP"]}, "exceptions": []},
]

GUIDANCE = {
    "schema_version": 1,
    "sources": {"OECD-2009": {"title": "OECD Guidance Document on the Definition of Residue",
                              "url": "https://doi.org/10.1787/66ca5caa-en", "locator": "ENV/JM/MONO(2009)30",
                              "type": "nonbinding_guidance"}},
    "rules": [
        {"id": "OECD-EXPRESSION-BASIS", "sources": ["OECD-2009"], "locator": "Scenario 1",
         "principle": "'Expressed as X' identifies the substance used to express the result."},
        {"id": "EU-TEXT-CONTROLS", "sources": ["OECD-2009"], "locator": "Annexes",
         "principle": "The exact EU definition is authoritative."},
    ],
}

GUIDANCE_PAGE = """---
title: Wording
type: domain-guide
domain: pesticide
last_updated: "2026-10-17"
sources: ["datasets/rd-bridge/interpretation_guidance.json"]
related: []
---
# Wording

<!-- Source: datasets/rd-bridge/interpretation_guidance.json @ {commit}, rule {rules} -->

'Expressed as X' names the basis for the result.{extra}
"""

PAGE = """---
title: Topic
type: domain-guide
domain: pesticide
last_updated: "2026-10-13"
sources: ["datasets/rd-bridge/residue_param_map.json"]
related: []
---
# Topic

<!-- Source: datasets/rd-bridge/residue_param_map.json @ {commit}, residue_id 10 -->

| Scope | Code |
|---|---|
| Default | `RF-0014-001-PPP` |
| `1000000` except `1040000` | `{code}` |

Component IM-2-1 is `RF-00002836-PAR`.
"""


def git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True, text=True).stdout.strip()


def commit_records(repo: Path, records: list[dict], message: str, guidance: dict | None = None) -> str:
    (repo / "data").mkdir(exist_ok=True)
    (repo / "data" / "residue_param_map.json").write_text(json.dumps(records))
    (repo / "data" / "interpretation_guidance.json").write_text(json.dumps(guidance or GUIDANCE))
    (repo / "DATA_SOURCES.md").write_text("CC BY 4.0 attribution\n")
    git(repo, "add", ".")
    git(repo, "-c", "user.name=t", "-c", "user.email=t@example.org", "commit", "-qm", message)
    return git(repo, "rev-parse", "HEAD")


@pytest.fixture
def upstream(tmp_path):
    repo = tmp_path / "rd-bridge"
    repo.mkdir()
    git(repo, "init", "-q", "-b", "main")
    commit_records(repo, RECORDS, "first")
    return repo


@pytest.fixture
def wiki(tmp_path):
    root = tmp_path / "wiki-root"
    (root / "wiki" / "chemmon-guidance").mkdir(parents=True)
    (root / "chemmon_docs").mkdir()
    return root


def write_page(root: Path, commit: str, code: str = "RF-00003326-PAR") -> Path:
    page = root / "wiki" / "chemmon-guidance" / "topic.md"
    page.write_text(PAGE.format(commit=commit[:7], code=code))
    return page


def check_page(root: Path, name: str = "topic.md") -> tuple[list[str], list[str]]:
    from wiki_api.wiki_store import split_frontmatter
    data, body = split_frontmatter((root / "wiki" / "chemmon-guidance" / name).read_text())
    return claim_problems(root, name, data["sources"], body)


def write_guidance_page(root: Path, commit: str, rules: str = "OECD-EXPRESSION-BASIS", extra: str = "") -> Path:
    page = root / "wiki" / "chemmon-guidance" / "wording.md"
    page.write_text(GUIDANCE_PAGE.format(commit=commit[:7], rules=rules, extra=extra))
    return page


def test_ingest_pins_commit_verbatim_and_is_idempotent(upstream, wiki):
    first = git(upstream, "rev-parse", "HEAD")
    report, written = ingest(wiki, str(upstream), "main")
    target = wiki / RD_BRIDGE_DIR
    manifest = json.loads((target / "manifest.json").read_text())
    assert written and manifest["commit"] == first
    assert manifest["summary"] == {"records": 2, "with_commodity_exceptions": 1, "exceptions": 1}
    assert (target / "residue_param_map.json").read_bytes() == (upstream / "data/residue_param_map.json").read_bytes()
    assert (target / "interpretation_guidance.json").read_bytes() == \
        (upstream / "data/interpretation_guidance.json").read_bytes()
    assert manifest_problems(wiki) == []
    assert "Snapshot: none ->" in report
    assert ingest(wiki, str(upstream), "main")[1] is False


def test_dry_run_and_invalid_upstream_write_nothing(upstream, wiki):
    assert ingest(wiki, str(upstream), "main", dry_run=True)[1] is False
    assert not (wiki / RD_BRIDGE_DIR).exists()
    commit_records(upstream, [{"name": "no id"}], "broken")
    with pytest.raises(ValueError):
        ingest(wiki, str(upstream), "main")
    assert not (wiki / RD_BRIDGE_DIR).exists()


def test_new_version_reports_changed_definitions_and_citing_pages(upstream, wiki):
    first = git(upstream, "rev-parse", "HEAD")
    ingest(wiki, str(upstream), "main")
    write_page(wiki, first)
    assert check_page(wiki) == ([], [])

    changed = json.loads(json.dumps(RECORDS))
    changed[0]["exceptions"][0]["param_codes"] = ["RF-99999999-PAR"]
    second = commit_records(upstream, changed, "new EU definition")
    report, written = ingest(wiki, str(upstream), "main")
    assert written
    assert "changed: residue_id 10 Acetamiprid (R)" in report
    assert "topic.md: cites changed residue_id 10" in report
    assert "residue_id 1 " not in report

    errors, warnings = check_page(wiki)
    assert any("RF-00003326-PAR not in cited residue records" in e for e in errors)
    assert any("older snapshot" in w for w in warnings)

    write_page(wiki, second, code="RF-99999999-PAR")
    assert check_page(wiki) == ([], [])


@pytest.mark.parametrize("fault,expected", [
    ("component_as_whole", "not the whole-residue code for scope 1000000, 1040000"),
    ("wrong_scope", "Annex I code 1020000 not in cited residue scopes"),
    ("unknown_id", "residue_id 99 not in current snapshot"),
    ("not_in_sources", "missing from frontmatter sources"),
])
def test_claim_check_rejects_unsupported_codes(upstream, wiki, fault, expected):
    commit = git(upstream, "rev-parse", "HEAD")
    ingest(wiki, str(upstream), "main")
    page = write_page(wiki, commit, code="RF-00002836-PAR" if fault == "component_as_whole" else "RF-00003326-PAR")
    text = page.read_text()
    if fault == "wrong_scope":
        text = text.replace("except `1040000`", "except `1020000`")
    elif fault == "unknown_id":
        text = text.replace("residue_id 10", "residue_id 10, 99")
    elif fault == "not_in_sources":
        text = text.replace('sources: ["datasets/rd-bridge/residue_param_map.json"]', "sources: []")
    page.write_text(text)
    assert any(expected in e for e in check_page(wiki)[0])


def test_guidance_citation_is_checked_against_pinned_rules(upstream, wiki):
    commit = git(upstream, "rev-parse", "HEAD")
    ingest(wiki, str(upstream), "main")
    write_guidance_page(wiki, commit, rules="OECD-EXPRESSION-BASIS, EU-TEXT-CONTROLS")
    assert check_page(wiki, "wording.md") == ([], [])


@pytest.mark.parametrize("fault,expected", [
    ("unknown_rule", "rule OECD-MADE-UP not in current snapshot"),
    ("param_code", "PARAM code RF-00003326-PAR needs a residue_id citation"),
    ("not_in_sources", "missing from frontmatter sources"),
    ("malformed", "malformed guidance locator"),
])
def test_guidance_citation_rejects_unsupported_claims(upstream, wiki, fault, expected):
    commit = git(upstream, "rev-parse", "HEAD")
    ingest(wiki, str(upstream), "main")
    rules = "OECD-EXPRESSION-BASIS, OECD-MADE-UP" if fault == "unknown_rule" else "OECD-EXPRESSION-BASIS"
    extra = " The sum is `RF-00003326-PAR`." if fault == "param_code" else ""
    page = write_guidance_page(wiki, commit, rules=rules, extra=extra)
    if fault == "not_in_sources":
        page.write_text(page.read_text().replace('sources: ["datasets/rd-bridge/interpretation_guidance.json"]',
                                                 "sources: []"))
    if fault == "malformed":  # a valid citation plus one the locator pattern rejects
        page.write_text(page.read_text() + f"\n<!-- Source: datasets/rd-bridge/interpretation_guidance.json "
                                           f"@ {commit[:7]}, rules OECD-MADE_UP -->\n\nMore wording.\n")
    assert any(expected in e for e in check_page(wiki, "wording.md")[0])


def test_changed_guidance_rule_is_reported_with_citing_pages(upstream, wiki):
    first = git(upstream, "rev-parse", "HEAD")
    ingest(wiki, str(upstream), "main")
    write_guidance_page(wiki, first)
    changed = json.loads(json.dumps(GUIDANCE))
    changed["rules"][0]["principle"] = "Reworded."
    commit_records(upstream, RECORDS, "reword guidance", guidance=changed)
    report, written = ingest(wiki, str(upstream), "main")
    assert written
    assert "changed: rule OECD-EXPRESSION-BASIS" in report
    assert "wording.md: cites changed rule OECD-EXPRESSION-BASIS" in report
    assert "EU-TEXT-CONTROLS" not in report
    assert any("older snapshot" in w for w in check_page(wiki, "wording.md")[1])


def test_each_listed_dataset_file_needs_its_own_locator(upstream, wiki):
    commit = git(upstream, "rev-parse", "HEAD")
    ingest(wiki, str(upstream), "main")
    page = write_page(wiki, commit)
    page.write_text(page.read_text().replace(
        'sources: ["datasets/rd-bridge/residue_param_map.json"]',
        'sources: ["datasets/rd-bridge/residue_param_map.json", "datasets/rd-bridge/interpretation_guidance.json"]'))
    warnings = check_page(wiki)[1]
    assert any("interpretation_guidance.json but has no claim-adjacent Source comment" in w for w in warnings)
    assert not any("residue_param_map.json but has no" in w for w in warnings)


def test_changed_source_entry_marks_the_rules_that_cite_it(upstream, wiki):
    first = git(upstream, "rev-parse", "HEAD")
    ingest(wiki, str(upstream), "main")
    write_guidance_page(wiki, first)
    changed = json.loads(json.dumps(GUIDANCE))
    changed["sources"]["OECD-2009"]["url"] = "https://doi.org/10.1787/new"
    commit_records(upstream, RECORDS, "move OECD source", guidance=changed)
    report, _ = ingest(wiki, str(upstream), "main")
    assert "changed: rule OECD-EXPRESSION-BASIS" in report and "changed: rule EU-TEXT-CONTROLS" in report
    assert "wording.md: cites changed rule OECD-EXPRESSION-BASIS" in report


@pytest.mark.parametrize("entry", [None, {"title": "OECD"}, {"title": "OECD", "url": "u", "locator": " "}])
def test_malformed_guidance_source_writes_nothing(upstream, wiki, entry):
    guidance = json.loads(json.dumps(GUIDANCE))
    guidance["sources"]["OECD-2009"] = entry
    commit_records(upstream, RECORDS, "bad source", guidance=guidance)
    with pytest.raises(ValueError, match="guidance source OECD-2009"):
        ingest(wiki, str(upstream), "main")
    assert not (wiki / RD_BRIDGE_DIR).exists()


@pytest.mark.parametrize("version", [None, 2])
def test_unsupported_guidance_schema_writes_nothing(upstream, wiki, version):
    guidance = {k: v for k, v in GUIDANCE.items() if k != "schema_version"}
    if version is not None:
        guidance["schema_version"] = version
    commit_records(upstream, RECORDS, "new guidance format", guidance=guidance)
    with pytest.raises(ValueError, match="schema_version"):
        ingest(wiki, str(upstream), "main")
    assert not (wiki / RD_BRIDGE_DIR).exists()


@pytest.mark.parametrize("rules", [
    [{"principle": "no id"}],
    [{"id": "OECD-X", "sources": ["OECD-2009"], "principle": "no locator"}],
    [{"id": "OECD-X", "sources": ["OECD-2009"], "locator": " ", "principle": "blank locator"}],
])
def test_malformed_guidance_writes_nothing(upstream, wiki, rules):
    guidance = {"schema_version": 1, "sources": GUIDANCE["sources"], "rules": rules}
    commit_records(upstream, RECORDS, "broken guidance", guidance=guidance)
    with pytest.raises(ValueError):
        ingest(wiki, str(upstream), "main")
    assert not (wiki / RD_BRIDGE_DIR).exists()


def test_hand_edited_snapshot_fails_health_and_marks_review_stale(upstream, wiki):
    ingest(wiki, str(upstream), "main")
    before = corpus_snapshot(wiki)
    assert "chemmon_docs/datasets/rd-bridge/residue_param_map.json" in before
    path = wiki / RD_BRIDGE_DIR / "residue_param_map.json"
    path.write_text(path.read_text().replace("Glyphosate", "Glyfosate"))
    (wiki / RD_BRIDGE_DIR / "notes.txt").write_text("stray")
    problems = manifest_problems(wiki)
    assert any("checksum differs" in p for p in problems)
    assert any("notes.txt: not listed" in p for p in problems)
    assert corpus_snapshot(wiki) != before


def test_repository_snapshot_and_dataset_claims_are_consistent():
    assert manifest_problems(ROOT) == []
    report = run_health_check()
    assert not any("datasets/" in message for message in report.errors + report.warnings)
