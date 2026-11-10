import json
from pathlib import Path

from wiki_api import doctor
from wiki_api.doctor import Page

ROOT = Path(__file__).resolve().parent.parent

RULES_PAGE = Page("business-rules-cross-cutting.md", {}, """
| Rule ID | Severity | Condition and requirement | Scope | Source page |
| --- | --- | --- | --- | --- |
| CHEMON58 | Error | sampCountry must equal reportingOrgCountry. | PPP/VMPR | 127 |
| CHEMON03 | Error | anMethCode.base is mandatory. | All | 113 |
""")


def _pages(*extra):
    return {p.name: p for p in (RULES_PAGE, *extra)}


def test_repository_has_no_doctor_errors():
    report = doctor.run_doctor(ROOT)
    assert report.errors == [], doctor.render_text(report)


def test_rule_scope_flags_a_paragraph_that_narrows_the_canonical_scope():
    page = Page("ssd2-sampling-country.md", {}, "Intro.\n\n- For pesticides, `sampCountry` must match\n  the reporting country. (`CHEMON58`)\n", 10)
    issues = list(doctor.check_rule_scope(_pages(page)))
    assert [(i.check, i.location) for i in issues] == [("rule_scope", "ssd2-sampling-country.md:13")]
    assert "PPP/VMPR" in issues[0].message


def test_rule_scope_accepts_full_scope_links_and_marked_exceptions():
    full = Page("a.md", {}, "For pesticides and VMPR, CHEMON58 compares countries.\n")
    linked = Page("b.md", {}, "CHEMON58 is defined in [[business-rules-pesticide]].\n")
    marked = Page("c.md", {}, "For pesticides CHEMON58 applies. <!-- doctor-ignore: rule_scope -->\n")
    unscoped = Page("d.md", {}, "For pesticides, CHEMON03 requires a method code.\n")
    assert list(doctor.check_rule_scope(_pages(full, linked, marked, unscoped))) == []


def test_rule_scope_reads_the_old_spelling_too():
    page = Page("x.md", {}, "For pesticides only (CHEMMON58).\n")
    assert len(list(doctor.check_rule_scope(_pages(page)))) == 1


def test_misspelt_rule_ids_are_errors(tmp_path):
    pages = {"x.md": Page("x.md", {}, "See CHEMMON58 and CHEMON58.")}
    issues = list(doctor.check_rule_id_spelling(tmp_path, pages))
    assert [(i.severity, i.location) for i in issues] == [("error", "wiki/chemmon-guidance/x.md")]


def _registry(tmp_path, tables):
    (tmp_path / "docs").mkdir()
    (tmp_path / "guide.pdf").write_bytes(b"%PDF")
    (tmp_path / "np.pdf").write_bytes(b"%PDF")
    (tmp_path / "docs/source-tables.json").write_text(json.dumps({
        "version": 1,
        "sources": {"chemmon": {"file": "guide.pdf", "aliases": ["ChemMon"]},
                    "no-presence": {"file": "np.pdf", "aliases": ["No-presence"]}},
        "tables": tables}))


def test_cited_table_must_be_registered(tmp_path):
    _registry(tmp_path, [{"source": "chemmon", "table": 2, "status": "transcribed",
                          "pages": ["p.md"], "must_contain": ["| N317A |"]}])
    page = Page("p.md", {"sources": ["guide.pdf"], "source_pages": ["pp. 23-27 (Table 2)", "p. 146 (Table 12)"]},
                "| N317A |")
    issues, summary = doctor.check_source_tables(tmp_path, {"p.md": page})
    assert [i.message for i in issues] == [
        "source_pages cites chemmon Table 12, which is not in docs/source-tables.json. "
        "Register it and say whether the page transcribes or only summarises it."]
    assert summary == {"tables": 1, "by_status": {"transcribed": 1}}


def test_transcribed_table_must_keep_its_rows(tmp_path):
    _registry(tmp_path, [{"source": "chemmon", "table": 2, "status": "transcribed",
                          "pages": ["p.md"], "must_contain": ["| N317A |", "| N422A |"]}])
    page = Page("p.md", {"sources": ["guide.pdf"], "source_pages": ["Table 2"]}, "Plan flags only. | N422A |")
    issues, _ = doctor.check_source_tables(tmp_path, {"p.md": page})
    assert len(issues) == 1 and "1 required string(s) missing" in issues[0].message


def test_gaps_need_an_issue_and_are_reported_as_warnings(tmp_path):
    _registry(tmp_path, [
        {"source": "chemmon", "table": 11, "status": "partial", "pages": ["p.md"], "issue": "#65", "missing": "ACTION"},
        {"source": "chemmon", "table": 12, "status": "not-covered", "pages": ["p.md"]},
        {"source": "chemmon", "table": 1, "status": "summarised", "pages": ["p.md"]}])
    issues, _ = doctor.check_source_tables(tmp_path, {"p.md": Page("p.md", {}, "")})
    assert sorted((i.severity, i.message.split(":")[0]) for i in issues) == [
        ("error", "chemmon Table 1"), ("error", "chemmon Table 12"), ("warning", "chemmon Table 11 is partial (#65)")]


def test_table_attribution_follows_the_nearest_source_alias(tmp_path):
    _registry(tmp_path, [])
    registry = doctor.load_registry(tmp_path)
    entry = "ChemMon 2026 pp. 144-147 (Section 7; Tables 11-12); No-presence 2026 Table 1 pp. 15-16"
    cited, unattributed = doctor.cited_tables(entry, ["guide.pdf", "np.pdf"], registry)
    assert cited == [("chemmon", 11), ("chemmon", 12), ("no-presence", 1)] and unattributed == []
    assert doctor.cited_tables("Table 3", ["guide.pdf", "np.pdf"], registry) == ([], [3])


def test_log_must_be_newest_first(tmp_path):
    log = tmp_path / "log.md"
    log.write_text("# Log\n\n## [2026-10-21] ingest | A\n\n## 2026-10-24 — B\n\n## [2026-04-07] setup | C\n")
    issues = list(doctor.check_log_chronology(log))
    assert [i.message for i in issues] == ["Log entries must be newest first; 2026-10-24 appears after 2026-10-21."]


def test_every_page_needs_an_incoming_link():
    a = Page("a.md", {"related": ["[[b]]"]}, "")
    b = Page("b.md", {}, "See [[b]] itself.")
    assert [i.location for i in doctor.check_incoming_links({"a.md": a, "b.md": b})] == ["a.md"]
