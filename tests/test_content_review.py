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
