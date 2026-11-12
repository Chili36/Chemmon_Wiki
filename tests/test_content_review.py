import json
from contextlib import contextmanager
from pathlib import Path
from types import SimpleNamespace

import pytest

from wiki_api import content_review as cr

OLD = """---
title: "T"
last_updated: "2026-01-01"
sources:
  - "guide.pdf"
---

# T

CHEMON58 applies to pesticides. (ChemMon 2026 p127)

Unchanged line.
"""


def _root(tmp_path, pages):
    (tmp_path / "docs").mkdir()
    (tmp_path / cr.WIKI_DIR).mkdir(parents=True)
    (tmp_path / "guide.pdf").write_bytes(b"%PDF-1.4 guide")
    (tmp_path / "other.pdf").write_bytes(b"%PDF-1.4 other")
    (tmp_path / cr.REGISTRY_PATH).write_text(json.dumps({"sources": {
        "chemmon": {"file": "guide.pdf", "aliases": ["ChemMon"]},
        "ssd2": {"file": "other.pdf", "aliases": ["SSD2 2013"]}}}))
    for name, text in pages.items():
        (tmp_path / cr.WIKI_DIR / name).write_text(text)
    return tmp_path


class FakeClient:
    def __init__(self, answer, stop_reason="end_turn"):
        self.requests = []
        message = SimpleNamespace(stop_reason=stop_reason, usage=SimpleNamespace(input_tokens=5, output_tokens=7),
                                  content=[SimpleNamespace(type="text", text=json.dumps(answer))])

        @contextmanager
        def stream(**request):
            self.requests.append(request)
            yield SimpleNamespace(get_final_message=lambda: message)

        self.messages = SimpleNamespace(stream=stream)


def test_page_change_lists_changed_and_removed_lines():
    new = OLD.replace("applies to pesticides.", "applies to pesticides and VMPR.")
    change = cr.page_change("p.md", OLD, new)
    assert change.changed_lines == [10] and not change.metadata_only and not change.is_new
    assert change.removed_lines == ["CHEMON58 applies to pesticides. (ChemMon 2026 p127)"]


def test_metadata_only_changes_need_no_model_call():
    assert cr.page_change("p.md", OLD, OLD.replace("2026-01-01", "2026-11-11")).metadata_only
    cited = OLD.replace('sources:', 'source_pages:\n  - "p. 127"\nsources:')
    assert not cr.page_change("p.md", OLD, cited).metadata_only  # a citation is a claim about the source


def test_new_page_is_reviewed_in_full():
    change = cr.page_change("p.md", None, OLD)
    assert change.is_new and change.changed_lines == list(range(1, len(OLD.splitlines()) + 1))


def test_record_problems_flag_unreviewed_and_changed_pages(tmp_path):
    root = _root(tmp_path, {"a.md": OLD, "b.md": OLD})
    assert [loc for loc, _ in cr.record_problems(root)] == [cr.RECORD_PATH.as_posix()]
    cr.save_record(root, {"version": 1, "pages": {
        "a.md": {"sha256": cr.sha256_text(OLD), "reviewed_at": "2026-11-11"},
        "gone.md": {"sha256": "0" * 64}}})
    problems = dict(cr.record_problems(root))
    assert "never reviewed" in problems["b.md"] and "gone.md" in problems[cr.RECORD_PATH.as_posix()]
    (root / cr.WIKI_DIR / "a.md").write_text(OLD + "New claim.\n")
    assert "changed since its review on 2026-11-11" in dict(cr.record_problems(root))["a.md"]


def test_request_sends_the_pages_pdfs_and_marks_changed_lines(tmp_path):
    root = _root(tmp_path, {})
    change = cr.page_change("p.md", OLD, OLD.replace("pesticides.", "pesticides and VMPR."))
    request = cr.build_request(root, change, "model-x", "high")
    content = request["messages"][0]["content"]
    assert [b["title"] for b in content if b["type"] == "document"] == ["ChemMon (chemmon)"]
    both = cr.page_change("r.md", None, OLD.replace('  - "guide.pdf"', '  - "guide.pdf"\n  - "other.pdf"'))
    blocks = cr.build_request(root, both, "model-x")["messages"][0]["content"]
    assert sum("cache_control" in b for b in blocks) == 2  # plus the system prompt: within the limit of four
    assert "Changed lines to review: 10" in content[-1]["text"] and "  10| CHEMON58" in content[-1]["text"]
    assert request["output_config"]["effort"] == "high"
    no_source = cr.page_change("q.md", None, "# No sources\n")
    with pytest.raises(cr.ReviewError):
        cr.build_request(root, no_source, "model-x")


def test_review_reports_findings_and_only_confident_ones_block(tmp_path):
    root = _root(tmp_path, {})
    change = cr.page_change("p.md", OLD, OLD.replace("pesticides.", "pesticides and VMPR."))
    finding = {"line": 10, "type": "wrong", "confidence": "HIGH", "severity": "wrong data",
               "wiki_quote": "CHEMON58 applies to pesticides and VMPR.", "source": "chemmon", "source_page": 127,
               "source_quote": "x", "problem": "y", "suggested_fix": "z"}
    answer = {"checks": [{"line": 10, "source_page": 127, "source_quote": "x", "verdict": "finding"}],
              "findings": [finding, {**finding, "confidence": "LOW"}, {**finding, "type": "lost_knowledge"},
                           {**finding, "wiki_quote": "not on the page"}],
              "not_checked": "nothing"}
    result = cr.review_page(root, change, "model-x", FakeClient(answer))
    assert len(result.findings) == 4 and len(result.blocking) == 2
    assert [f["quote_on_page"] for f in result.findings] == [True, True, True, False]
    assert "not_checked" not in cr.record_entry(result, "model-x", "model")


def test_a_review_that_skips_lines_or_stops_early_records_nothing(tmp_path):
    root = _root(tmp_path, {})
    change = cr.page_change("p.md", OLD, OLD.replace("pesticides.", "pesticides and VMPR."))
    with pytest.raises(cr.ReviewError, match="no verdict for line"):
        cr.review_page(root, change, "m", FakeClient({"checks": [], "findings": [], "not_checked": "nothing"}))
    silent = {"checks": [{"line": 10, "source_page": 0, "source_quote": "", "verdict": "not_found"}],
              "findings": [], "not_checked": "nothing"}
    with pytest.raises(cr.ReviewError, match="reported no finding"):
        cr.review_page(root, change, "m", FakeClient(silent))
    with pytest.raises(cr.ReviewError, match="refusal"):
        cr.review_page(root, change, "m", FakeClient({}, stop_reason="refusal"))


def test_repository_pages_all_match_their_content_review():
    assert list(cr.record_problems(Path(__file__).resolve().parent.parent)) == []


def test_saving_the_record_drops_deleted_pages(tmp_path):
    root = _root(tmp_path, {"a.md": OLD})
    record = {"version": 1, "pages": {"a.md": {"sha256": cr.sha256_text(OLD)}, "gone.md": {"sha256": "0" * 64}}}
    cr.save_record(root, record, prune=True)
    assert list(cr.load_record(root)["pages"]) == ["a.md"] and list(cr.record_problems(root)) == []


def test_dataset_sources_are_sent_cut_down_to_the_cited_records(tmp_path):
    root = _root(tmp_path, {})
    folder = root / cr.DATASET_DIR / "datasets/rd"
    folder.mkdir(parents=True)
    records = [{"residue_id": i, "name": "x" * 700} for i in range(1, 121)]
    (folder / "map.json").write_text(json.dumps(records))
    (folder / "notes.md").write_text("Licence terms.")
    page = OLD.replace('  - "guide.pdf"', '  - "datasets/rd/map.json"\n  - "datasets/rd/notes.md"') + \
        "\n<!-- Source: datasets/rd/map.json @ abc, residue_id 7, 30 and 119 -->\n"
    content = cr.build_request(root, cr.page_change("d.md", None, page), "m")["messages"][0]["content"]
    assert [b["type"] for b in content] == ["text", "text", "text"]  # no PDF, two dataset files, the page
    assert "only the 3 of 120 records" in content[0]["text"] and '"residue_id": 119' in content[0]["text"]
    assert '"residue_id": 8,' not in content[0]["text"] and "Licence terms." in content[1]["text"]
    missing = cr.page_change("e.md", None, OLD.replace('  - "guide.pdf"', '  - "datasets/rd/absent.json"'))
    with pytest.raises(cr.ReviewError, match="not found"):
        cr.build_request(root, missing, "m")


def test_linked_pages_are_context_outgoing_first_and_size_limited(monkeypatch):
    texts = {"a.md": "See [[b]] and [[missing]].", "b.md": "B " * 50, "c.md": "Links to [[a]]. " * 10, "d.md": "x"}
    assert cr.linked_pages("a.md", texts["a.md"], texts) == (["b.md", "c.md"], [])
    monkeypatch.setattr(cr, "CONTEXT_PAGE_CHARS", 120)
    assert cr.linked_pages("a.md", texts["a.md"], texts) == (["b.md"], ["c.md"])


def test_review_sends_linked_pages_and_names_the_ones_left_out(tmp_path, monkeypatch):
    root = _root(tmp_path, {})
    page = OLD + "\nSee [[other]] and [[huge]].\n"
    texts = {"p.md": page, "other.md": "CHEMON58 is an Error.", "huge.md": "y" * 500}
    monkeypatch.setattr(cr, "CONTEXT_PAGE_CHARS", 100)
    answer = {"checks": [{"line": n, "source_page": 1, "source_quote": "q", "verdict": "supported"}
                         for n in range(1, len(page.splitlines()) + 1)], "findings": [], "not_checked": "nothing"}
    client = FakeClient(answer)
    result = cr.review_page(root, cr.page_change("p.md", None, page), "m", client, texts=texts)
    sent = [b["text"] for b in client.requests[0]["messages"][0]["content"] if b["type"] == "text"]
    assert sent[0].startswith("Other wiki page (context, not under review): other.md")
    assert "Linked pages NOT given (too large to fit): huge.md" in sent[-1]
    assert result.context_pages == ["other.md"] and result.context_omitted == ["huge.md"] and result.full
    entry = cr.record_entry(result, "m", "model")
    assert entry["context_not_sent"] == ["huge.md"] and entry["full_review"]["reviewer"] == "m"


def test_a_later_partial_review_keeps_the_date_of_the_full_review():
    previous = {"full_review": {"date": "2026-11-12", "reviewer": "m"}}
    partial = cr.PageResult("p.md", "0" * 64, 3)
    assert cr.record_entry(partial, "m2", "model", previous=previous)["full_review"] == previous["full_review"]
    assert "full_review" not in cr.record_entry(partial, "m2", "model")
    adopted = cr.PageResult("p.md", "0" * 64, 0, full=True)
    assert "full_review" not in cr.record_entry(adopted, "none", "adopted")


def test_verdicts_are_required_for_claims_and_source_citations_only():
    page = OLD.replace('sources:', 'source_pages:\n  - "p. 127 (Table 10)"\nsources:') + "\n## Related\n\n- [[other]]\n"
    change = cr.page_change("p.md", None, page)
    lines = page.splitlines()
    needed = [lines[n - 1] for n in cr.lines_needing_verdict(change)]
    assert needed == ['  - "p. 127 (Table 10)"', '  - "guide.pdf"',
                      "CHEMON58 applies to pesticides. (ChemMon 2026 p127)", "Unchanged line."]
    swapped = cr.page_change("p.md", OLD, OLD.replace("guide.pdf", "other.pdf"))
    assert not swapped.metadata_only and cr.lines_needing_verdict(swapped) == [5]


def test_blocking_findings_on_a_recorded_page_fail_the_doctor_until_fixed_or_waived(tmp_path):
    root = _root(tmp_path, {"a.md": OLD})
    entry = {"sha256": cr.sha256_text(OLD), "reviewed_at": "2026-11-11",
             "unresolved": [{"line": 10, "type": "wrong", "problem": "x"}]}
    cr.save_record(root, {"version": 1, "pages": {"a.md": dict(entry)}})
    problems = dict(cr.record_problems(root))
    assert "1 blocking problem(s) on line(s) 10" in problems["a.md"]
    waived = cr.record_entry(cr.PageResult("a.md", entry["sha256"], 4), "m", "model", reason="reviewer misread p. 127",
                             waived=[{"line": 10, "type": "wrong", "wiki_quote": "q", "problem": "x"}], previous=entry)
    cr.save_record(root, {"version": 1, "pages": {"a.md": waived}})
    assert "unresolved" not in waived and list(cr.record_problems(root)) == []
