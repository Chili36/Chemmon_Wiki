"""Independent content review: a fresh model call checks changed wiki lines against the source PDFs.

The audits in #68 and #69 found errors only when a reader who had not written the text compared
it with the source. This module makes that step repeatable and enforceable:

  python -m wiki_api.content_review              list the pages that need a review (no model call)
  python -m wiki_api.content_review --review     review them; record the clean ones
  python -m wiki_api.content_review --review --full [PAGE ...]    review every line, not only changes
  python -m wiki_api.content_review --waive PAGE --reason "..."   accept the last findings for a page

`docs/content-review.json` records the hash of each page as reviewed. The wiki doctor fails when a
page differs from its record, so unreviewed content cannot pass CI. The reviewer sees the page, the
PDFs and the wiki pages linked to or from it (to catch two pages that disagree), never the writer's notes. It is a second reader, not proof: it can miss errors.
"""
from __future__ import annotations

import argparse
import base64
import difflib
import hashlib
import json
import os
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any, Iterable

from wiki_api.wiki_store import split_frontmatter

RECORD_PATH = Path("docs/content-review.json")
REGISTRY_PATH = Path("docs/source-tables.json")
WIKI_DIR = Path("wiki/chemmon-guidance")
REPORT_DIR = Path("reports/content-review")
DATASET_DIR = Path("chemmon_docs")
DATASET_WHOLE_FILE_BYTES = 60_000   # larger JSON lists are cut down to the records the page cites
CONTEXT_PAGE_CHARS = 240_000       # linked pages sent as context; the rest are named as left out
WIKI_LINK_RE = re.compile(r"\[\[([a-zA-Z0-9_\-]+)(?:\|[^\]]+)?\]\]")
RESIDUE_ID_RE = re.compile(r"residue_id\s+(\d+(?:\s*(?:,|and)\s*\d+)*)")
DEFAULT_MODEL = "claude-opus-5-5"
MODEL_ENV = "CONTENT_REVIEW_MODEL"
MAX_OUTPUT_TOKENS = 64000
DEFAULT_EFFORT = "xhigh"
EFFORT_ENV = "CONTENT_REVIEW_EFFORT"
# Front matter that makes no claim about the source; a change limited to these needs no model call.
METADATA_KEYS = {"last_updated", "related", "select_when", "title", "type", "domain"}
BLOCKING_CONFIDENCE = {"HIGH", "MEDIUM"}
FINDING_TYPES = ["wrong", "narrowed_or_widened", "unsourced", "misquote", "bad_citation",
                 "contradiction", "cross_page", "discrepancy_note", "lost_knowledge"]
# Removed text may have moved to another page, which the reviewer cannot see, so it never blocks.
NON_BLOCKING_TYPES = {"lost_knowledge"}

SYSTEM_PROMPT = """You are an independent reviewer of one page of a wiki that restates EFSA's \
chemical monitoring (ChemMon) reporting guidance for people and language models who code SSD2 data. \
You did not write the page. The attached PDFs are the only authority. Your job is to find where the \
changed lines of the page disagree with the PDFs. An error you miss can make someone report wrong data.

Work line by line; do not judge a line from memory or from how plausible it sounds. For every changed \
line that makes a factual claim, add one entry to `checks`:
1. Find the passage in the PDF that the line restates (the page cites pages like "(ChemMon 2026 p71)"; \
if it cites none, search the documents; a rule ID is defined in its rule-table row). PDF page N is printed page N.
2. Copy that passage into `source_quote` verbatim, including the rest of its sentence, table row or \
note: words such as "except", "only", "for example", "unless", "if", "also" and footnotes or notes in \
the same row are where the errors hide.
3. Compare the line with the quote element by element: codes, field names, rule IDs, severity (Error / \
Warning), requirement strength (must / mandatory / should / recommended / strongly recommended / highly \
recommended are all different), data domains, conditions and exceptions, whether a list is exhaustive \
or an example, numbers, dates, regulation numbers, text in quotation marks (must be verbatim) and the \
cited page number. If the same thing is stated in more than one place in the source (prose and a rule \
table), check both; they can differ.
4. Set `verdict`: "supported" only if every element matches; "finding" if any element differs (and add \
it to `findings`); "not_found" if no passage exists (an unsourced finding); "not_a_claim" for headings, \
links, blank lines and metadata.

Report a finding when a changed line:
- wrong: contradicts the source.
- narrowed_or_widened: limits a rule or requirement to fewer domains or cases than the source, or extends it.
- unsourced: is presented as coming from the guidance but is found nowhere in the attached documents.
- misquote: puts text in quotation marks that is not verbatim in the source.
- bad_citation: cites a page that does not contain the claim.
- contradiction: contradicts another statement on the same page.
- discrepancy_note: is a "Source discrepancy:" note that misstates either side or resolves the conflict \
in a way the source does not support.
- cross_page: disagrees with a statement on one of the other wiki pages given as context (a different \
code, severity, strength, domain, condition, number or page for the same rule, field or requirement). \
Put that page's file name in `other_page` and its statement in the problem, then read the source and \
say which page it supports. Report it even when the changed line is the correct one: the other page then \
needs the fix. A page that says less than another is not a disagreement.
- lost_knowledge: (removed lines only) a statement the source supports was removed and neither this \
page nor a context page carries it.

Unchanged lines are context. Report one only if a changed line contradicts it.
Not findings: style, wording, correct paraphrase, formatting, length, structure. Rule IDs are spelled \
CHEMON, which is correct. A line labelled "Wiki note (not in the guidance):" is the wiki's own reading \
and is allowed unless it contradicts the source. The other wiki pages are context only: do not review \
their lines against the source, apart from settling a cross_page finding. Wiki links like [[page-name]] \
may point to pages that were not given; do not report what those might say. For findings that involve \
no other page, leave `other_page` empty.

Some pages also cite a dataset (rd-bridge, EU Annex I) with locators such as "residue_id 253". Those \
files are attached as text. A large file is cut down to the records the page cites, so a dataset claim \
whose record is not in the excerpt has a bad citation. Check dataset claims against the excerpt in the \
same way; use source_page 0 for them.

Quote the wiki text and the source text verbatim and briefly. Confidence: HIGH when you read both and \
they plainly differ; MEDIUM when they differ but the source is ambiguous; LOW for a suspicion you could \
not settle. Do not pad: an empty findings list is the right answer for a correct page. Say in \
not_checked what you could not verify and why; write "nothing" if you checked every changed line."""

FINDINGS_SCHEMA: dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "required": ["checks", "findings", "not_checked"],
    "properties": {
        "checks": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["line", "source_page", "source_quote", "verdict"],
                "properties": {
                    "line": {"type": "integer"},
                    "source_page": {"type": "integer"},
                    "source_quote": {"type": "string"},
                    "verdict": {"type": "string", "enum": ["supported", "finding", "not_found", "not_a_claim"]},
                },
            },
        },
        "not_checked": {"type": "string"},
        "findings": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["line", "type", "confidence", "severity", "wiki_quote", "other_page", "source",
                             "source_page", "source_quote", "problem", "suggested_fix"],
                "properties": {
                    "line": {"type": "integer"},
                    "type": {"type": "string", "enum": FINDING_TYPES},
                    "confidence": {"type": "string", "enum": ["HIGH", "MEDIUM", "LOW"]},
                    "severity": {"type": "string", "enum": ["wrong data", "misleading", "minor"]},
                    "wiki_quote": {"type": "string"},
                    "other_page": {"type": "string"},
                    "source": {"type": "string"},
                    "source_page": {"type": "integer"},
                    "source_quote": {"type": "string"},
                    "problem": {"type": "string"},
                    "suggested_fix": {"type": "string"},
                },
            },
        },
    },
}


class ReviewError(RuntimeError):
    """The review could not be completed; never treat this as a clean result."""


@dataclass(frozen=True)
class PageChange:
    name: str
    text: str
    sha256: str
    changed_lines: list[int]          # 1-based line numbers in the current file
    removed_lines: list[str]
    metadata_only: bool
    is_new: bool


@dataclass
class PageResult:
    name: str
    sha256: str
    lines_reviewed: int
    findings: list[dict] = field(default_factory=list)
    not_checked: str = ""
    usage: dict = field(default_factory=dict)
    context_pages: list[str] = field(default_factory=list)
    context_omitted: list[str] = field(default_factory=list)
    full: bool = False

    @property
    def blocking(self) -> list[dict]:
        return [f for f in self.findings if is_blocking(f)]


def is_blocking(finding: dict) -> bool:
    return finding.get("confidence") in BLOCKING_CONFIDENCE and finding.get("type") not in NON_BLOCKING_TYPES


# --- record -----------------------------------------------------------------

def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def generated_pages(root: Path) -> set[str]:
    """Pages rendered from data; the health check compares them with their generator instead."""
    repo = Path(__file__).resolve().parent.parent
    if str(repo) not in sys.path:
        sys.path.insert(0, str(repo))
    from tools.health_check import GENERATED_PAGES
    return {name for name, *_ in GENERATED_PAGES}


def load_record(root: Path) -> dict:
    path = root / RECORD_PATH
    if not path.is_file():
        return {"version": 1, "pages": {}}
    record = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(record, dict) or record.get("version") != 1 or not isinstance(record.get("pages"), dict):
        raise ValueError(f"{RECORD_PATH}: unsupported content review record")
    return record


def save_record(root: Path, record: dict, *, prune: bool = False) -> None:
    """Write the record. With prune, drop entries for pages that were deleted or renamed."""
    if prune:
        current = page_texts(root)
        for name in sorted(set(record["pages"]) - set(current)):
            print(f"{name}: no longer a wiki page, removed from the record")
            del record["pages"][name]
    record["pages"] = dict(sorted(record["pages"].items()))
    (root / RECORD_PATH).write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def page_texts(root: Path) -> dict[str, str]:
    skip = generated_pages(root)
    return {p.name: p.read_text(encoding="utf-8") for p in sorted((root / WIKI_DIR).glob("*.md"))
            if p.name not in skip}


def stale_pages(root: Path, record: dict | None = None) -> dict[str, str]:
    """Page name -> why it needs a review."""
    record = load_record(root) if record is None else record
    stale = {}
    for name, text in page_texts(root).items():
        entry = record["pages"].get(name)
        if entry is None:
            stale[name] = "never reviewed"
        elif entry.get("sha256") != sha256_text(text):
            stale[name] = f"changed since its review on {entry.get('reviewed_at', '?')}"
    return stale


def unresolved_pages(root: Path, record: dict | None = None) -> dict[str, list[dict]]:
    """Pages whose recorded version has blocking findings that were neither fixed nor waived."""
    record = load_record(root) if record is None else record
    texts = page_texts(root)
    return {name: entry["unresolved"] for name, entry in record["pages"].items()
            if entry.get("unresolved") and name in texts and entry.get("sha256") == sha256_text(texts[name])}


def _squash(text: str) -> str:
    return " ".join(text.split())


def still_unresolved(previous: dict | None, text: str) -> list[dict]:
    """Earlier blocking findings that a later partial review has not dealt with.

    A finding is dealt with when its quoted wiki text is no longer on the page: the line was changed,
    so it was reviewed again. A finding whose quote cannot be found (the reviewer misquoted) stays
    until a full review or a waiver.
    """
    page = _squash(text)
    kept = []
    for finding in (previous or {}).get("unresolved", []):
        quote = _squash(str(finding.get("wiki_quote", "")))
        if not finding.get("quote_on_page") or quote in page:
            kept.append(finding)
    return kept


def record_problems(root: Path) -> Iterable[tuple[str, str]]:
    """(location, message) pairs for the wiki doctor."""
    try:
        record = load_record(root)
    except (ValueError, json.JSONDecodeError) as exc:
        yield RECORD_PATH.as_posix(), str(exc)
        return
    if not (root / RECORD_PATH).is_file():
        yield RECORD_PATH.as_posix(), "Content review record is missing."
        return
    texts = page_texts(root)
    for name, why in sorted(stale_pages(root, record).items()):
        yield name, (f"Page {why}. Run `python -m wiki_api.content_review --review {name}` "
                     "so a fresh reader checks the changed lines against the source PDFs.")
    for name, findings in sorted(unresolved_pages(root, record).items()):
        lines = ", ".join(str(f.get("line")) for f in findings)
        yield name, (f"The last content review found {len(findings)} blocking problem(s) on line(s) {lines}. "
                     f"Fix the page, or run `python -m wiki_api.content_review --waive {name} --reason ...`.")
    for name in sorted(set(record["pages"]) - set(texts)):
        yield RECORD_PATH.as_posix(), f"Record lists {name}, which is not a reviewable wiki page."


# --- what changed -----------------------------------------------------------

def git_show(root: Path, rev: str, path: Path) -> str | None:
    result = subprocess.run(["git", "show", f"{rev}:{path.as_posix()}"], cwd=root, capture_output=True, text=True)
    return result.stdout if result.returncode == 0 else None


def texts_at(root: Path, rev: str) -> dict[str, str]:
    """The reviewable pages as of a git revision."""
    listing = subprocess.run(["git", "ls-tree", "--name-only", rev, WIKI_DIR.as_posix() + "/"],
                             cwd=root, capture_output=True, text=True, check=True).stdout.split("\n")
    skip = generated_pages(root)
    names = [Path(line).name for line in listing if line.endswith(".md") and Path(line).name not in skip]
    return {name: text for name in names if (text := git_show(root, rev, WIKI_DIR / name)) is not None}


def default_base(root: Path) -> str:
    for ref in ("origin/main", "main"):
        result = subprocess.run(["git", "merge-base", "HEAD", ref], cwd=root, capture_output=True, text=True)
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    raise ReviewError("Cannot find a base commit; pass --base.")


def page_change(name: str, old: str | None, new: str) -> PageChange:
    digest = sha256_text(new)
    new_lines = new.splitlines()
    if old is None:
        return PageChange(name, new, digest, list(range(1, len(new_lines) + 1)), [], False, True)
    changed, removed = [], []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, old.splitlines(), new_lines, autojunk=False).get_opcodes():
        if tag in {"replace", "insert"}:
            changed.extend(range(j1 + 1, j2 + 1))
        if tag in {"replace", "delete"}:
            removed.extend(old.splitlines()[i1:i2])
    old_meta, old_body = split_frontmatter(old)
    new_meta, new_body = split_frontmatter(new)
    strip = lambda meta: {k: v for k, v in meta.items() if k not in METADATA_KEYS}  # noqa: E731
    metadata_only = old_body == new_body and strip(old_meta) == strip(new_meta)
    return PageChange(name, new, digest, changed, [r for r in removed if r.strip()], metadata_only, False)


def _ranges(numbers: list[int]) -> str:
    out, start, prev = [], None, None
    for n in numbers:
        if start is None:
            start = prev = n
        elif n == prev + 1:
            prev = n
        else:
            out.append(f"{start}-{prev}" if prev != start else str(start))
            start = prev = n
    if start is not None:
        out.append(f"{start}-{prev}" if prev != start else str(start))
    return ", ".join(out)


# --- the review -------------------------------------------------------------

def source_documents(root: Path, frontmatter: dict) -> list[tuple[str, Path]]:
    """(label, pdf path) for the page's sources, in registry order so the cached prefix is shared."""
    registry = json.loads((root / REGISTRY_PATH).read_text(encoding="utf-8"))["sources"]
    wanted = {Path(s).name for s in frontmatter.get("sources", []) or [] if isinstance(s, str)}
    documents = []
    for key, src in registry.items():
        path = root / src["file"]
        if path.name in wanted:
            label = (src.get("aliases") or [key])[0]
            documents.append((f"{label} ({key})", path))
    return documents


def linked_pages(name: str, text: str, texts: dict[str, str]) -> tuple[list[str], list[str]]:
    """Pages to send as context: those this page links to, then those that link to it.

    Returns (included, omitted); pages are left out, by name, once the size limit is reached.
    """
    def links(source: str) -> set[str]:
        return {f"{target}.md" for target in WIKI_LINK_RE.findall(source)}

    outgoing = sorted(n for n in links(text) if n in texts and n != name)
    incoming = sorted(n for n, other in texts.items()
                      if n != name and n not in outgoing and name in links(other))
    included, omitted, used = [], [], 0
    for candidate in outgoing + incoming:
        if used + len(texts[candidate]) > CONTEXT_PAGE_CHARS:
            omitted.append(candidate)
            continue
        included.append(candidate)
        used += len(texts[candidate])
    return included, omitted


def dataset_excerpts(root: Path, change_text: str, frontmatter: dict) -> list[tuple[str, str]]:
    """(label, text) for the dataset files in the page's `sources`."""
    cited = {int(n) for group in RESIDUE_ID_RE.findall(change_text) for n in re.findall(r"\d+", group)}
    excerpts = []
    for source in frontmatter.get("sources", []) or []:
        if not isinstance(source, str) or not source.startswith("datasets/"):
            continue
        path = root / DATASET_DIR / source
        if not path.is_file():
            raise ReviewError(f"dataset source not found: {source}")
        text = path.read_text(encoding="utf-8")
        label = source
        if path.suffix == ".json" and len(text.encode("utf-8")) > DATASET_WHOLE_FILE_BYTES:
            data = json.loads(text)
            if not (isinstance(data, list) and all(isinstance(r, dict) and "residue_id" in r for r in data)):
                raise ReviewError(f"{source} is too large to send whole and has no residue_id records to select")
            records = [r for r in data if r["residue_id"] in cited]
            text = json.dumps(records, indent=1, ensure_ascii=False)
            label = f"{source} (only the {len(records)} of {len(data)} records whose residue_id the page cites)"
        excerpts.append((label, text))
    return excerpts


def build_request(root: Path, change: PageChange, model: str, effort: str = DEFAULT_EFFORT,
                  context: dict[str, str] | None = None, omitted: list[str] | None = None) -> dict:
    frontmatter, _ = split_frontmatter(change.text)
    documents = source_documents(root, frontmatter)
    datasets = dataset_excerpts(root, change.text, frontmatter)
    if not documents and not datasets:
        raise ReviewError(f"{change.name}: its `sources` name no PDF from docs/source-tables.json and no "
                          "dataset file; nothing to review it against.")
    content: list[dict] = []
    for label, path in documents:
        content.append({
            "type": "document", "title": label,
            "source": {"type": "base64", "media_type": "application/pdf",
                       "data": base64.standard_b64encode(path.read_bytes()).decode("ascii")},
        })
    # At most four cache breakpoints per request, and the system prompt uses one. The first PDF
    # is shared by nearly every page; the last closes the whole document prefix.
    for block in {id(b): b for b in content[:1] + content[-1:]}.values():
        block["cache_control"] = {"type": "ephemeral"}
    for label, text in datasets:
        content.append({"type": "text", "text": f"Dataset file: {label}\n\n{text}"})
    for other, text in (context or {}).items():
        content.append({"type": "text", "text": f"Other wiki page (context, not under review): {other}\n\n{text}"})
    numbered = "\n".join(f"{i:>4}| {line}" for i, line in enumerate(change.text.splitlines(), 1))
    parts = [f"Wiki page under review: {change.name}",
             "Attached sources: " + "; ".join(label for label, _ in documents + datasets),
             "The page with line numbers:", numbered,
             ("Review every line of this page." if change.is_new
              else f"Changed lines to review: {_ranges(change.changed_lines)}"),
             "`checks` must hold one entry for each of these lines, with no line left out or merged "
             f"with another: {_ranges(lines_needing_verdict(change))}"]
    if context:
        parts.append("Context pages given above: " + ", ".join(context))
    if omitted:
        parts.append("Linked pages NOT given (too large to fit): " + ", ".join(omitted))
    if change.removed_lines:
        parts.append("Lines removed by this change:\n" + "\n".join(f"- {line}" for line in change.removed_lines))
    content.append({"type": "text", "text": "\n\n".join(parts)})
    return {
        "model": model,
        "max_tokens": MAX_OUTPUT_TOKENS,
        "system": [{"type": "text", "text": SYSTEM_PROMPT, "cache_control": {"type": "ephemeral"}}],
        "messages": [{"role": "user", "content": content}],
        "output_config": {"effort": effort, "format": {"type": "json_schema", "schema": FINDINGS_SCHEMA}},
    }


def call_model(request: dict, client: Any = None) -> tuple[dict, dict]:
    """Send one review request; return (parsed answer, usage). Raises ReviewError if it did not complete."""
    if client is None:
        from wiki_api.anthropic_native import native_client
        client = native_client()
    with client.messages.stream(**request) as stream:
        message = stream.get_final_message()
    if message.stop_reason != "end_turn":
        raise ReviewError(f"review stopped with {message.stop_reason!r}; no result recorded")
    text = "".join(b.text for b in message.content if getattr(b, "type", None) == "text")
    try:
        answer = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ReviewError(f"reviewer returned invalid JSON: {exc}") from exc
    usage = {k: int(getattr(message.usage, k, 0) or 0) for k in
             ("input_tokens", "output_tokens", "cache_creation_input_tokens", "cache_read_input_tokens")}
    return answer, usage


STRUCTURAL_LINE_RE = re.compile(
    r"^\s*(?:#{1,6}\s.*|-{3,}|\|?[\s:|-]+\||<!--.*-->|```.*|(?:[-*]\s+)?\[\[[^\]]+\]\][\s.,;]*)?\s*$")


def lines_needing_verdict(change: PageChange) -> list[int]:
    """Changed lines that can carry a claim about the source.

    Left out: blank lines, headings, rules, table separators, comment-only and link-only lines, and
    front matter other than `sources` and `source_pages` entries (naming a source document or its
    pages is a claim; a title or date is not).
    """
    lines = change.text.splitlines()
    end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), 0) if lines[:1] == ["---"] else 0
    in_source_pages, cited = False, set()
    for i in range(1, end):
        if re.match(r"^\S", lines[i]):
            in_source_pages = lines[i].startswith(("source_pages:", "sources:"))
        elif in_source_pages:
            cited.add(i + 1)
    return [n for n in change.changed_lines
            if (n in cited if n <= end + 1 else not STRUCTURAL_LINE_RE.match(lines[n - 1]))]


def unchecked_lines(change: PageChange, checks: list[dict]) -> list[int]:
    """Claim-bearing changed lines that the reviewer gave no verdict for."""
    seen = {c.get("line") for c in checks}
    return [n for n in lines_needing_verdict(change) if n not in seen]


def review_page(root: Path, change: PageChange, model: str, client: Any = None,
                effort: str = DEFAULT_EFFORT, texts: dict[str, str] | None = None) -> PageResult:
    """Review one page. `texts` holds the other wiki pages; linked ones are sent as context."""
    included, omitted = linked_pages(change.name, change.text, texts or {})
    context = {name: texts[name] for name in included} if texts else {}
    answer, usage = call_model(build_request(root, change, model, effort, context, omitted), client)
    lines = change.text.splitlines()
    checks = answer.get("checks", [])
    skipped = unchecked_lines(change, checks)
    if skipped:  # ask once more for just those lines; the PDFs are read from the cache
        rest = PageChange(change.name, change.text, change.sha256, skipped, [], False, False)
        more, more_usage = call_model(build_request(root, rest, model, effort, context, omitted), client)
        checks = checks + more.get("checks", [])
        answer["findings"] = answer.get("findings", []) + more.get("findings", [])
        notes = [str(a.get("not_checked", "")) for a in (answer, more)]
        answer["not_checked"] = "; ".join(n for n in notes if n.strip().lower().rstrip(".") != "nothing") or "nothing"
        usage = {k: usage.get(k, 0) + more_usage.get(k, 0) for k in usage}
        skipped = unchecked_lines(change, checks)
    if skipped:
        raise ReviewError(f"reviewer gave no verdict for line(s) {_ranges(skipped)}; no result recorded")
    reported = {f.get("line") for f in answer.get("findings", [])}
    silent = sorted({c.get("line") for c in checks if c.get("verdict") in {"finding", "not_found"}} - reported)
    if silent:
        raise ReviewError(f"reviewer marked line(s) {_ranges(silent)} as wrong or unsourced but reported "
                          "no finding for them; no result recorded")
    findings = []
    for finding in answer.get("findings", []):
        quote = " ".join(str(finding.get("wiki_quote", "")).split())
        # A quote that is not on the page means the reviewer misread it; keep the finding but say so.
        finding["quote_on_page"] = bool(quote) and quote in " ".join(" ".join(lines).split())
        findings.append(finding)
    return PageResult(change.name, change.sha256, len(lines_needing_verdict(change)), findings,
                      str(answer.get("not_checked", "")), usage, included, omitted, change.is_new)


def record_entry(result: PageResult, reviewer: str, method: str, waived: list[dict] | None = None,
                 reason: str | None = None, previous: dict | None = None) -> dict:
    """The record for a page. `full_review` (when every line was last reviewed) survives later entries."""
    entry = {"sha256": result.sha256, "reviewed_at": date.today().isoformat(), "reviewer": reviewer,
             "method": method, "lines_reviewed": result.lines_reviewed}
    if result.full and method == "model":
        entry["full_review"] = {"date": entry["reviewed_at"], "reviewer": reviewer}
    elif previous and previous.get("full_review"):
        entry["full_review"] = previous["full_review"]
    if result.context_omitted:
        entry["context_not_sent"] = result.context_omitted
    if result.not_checked and result.not_checked.strip().lower().rstrip(".") != "nothing":
        entry["not_checked"] = result.not_checked
    if waived:
        entry["waived"] = [{"line": f.get("line"), "type": f.get("type"), "wiki_quote": f.get("wiki_quote"),
                            "other_page": f.get("other_page", ""), "problem": f.get("problem")} for f in waived]
    if reason:
        entry["reason"] = reason
    return entry


# --- command line -----------------------------------------------------------

def _report_path(root: Path) -> Path:
    return root / REPORT_DIR / "latest.json"


def _load_report(root: Path) -> dict:
    path = _report_path(root)
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {"pages": {}}


def _print_findings(result: PageResult) -> None:
    for f in result.findings:
        mark = "BLOCKING" if is_blocking(f) else "note"
        other = f" vs {f['other_page']}" if f.get("other_page") else ""
        print(f"  [{mark}] {result.name}:{f.get('line')} {f.get('type')}{other} "
              f"({f.get('confidence')}, {f.get('severity')})")
        print(f"      wiki:   {f.get('wiki_quote')}" + ("" if f.get("quote_on_page") else "  [quote not found on page]"))
        print(f"      source: {f.get('source')} p{f.get('source_page')}: {f.get('source_quote')}")
        print(f"      problem: {f.get('problem')}")
        print(f"      fix: {f.get('suggested_fix')}")
    if result.not_checked and result.not_checked.strip().lower().rstrip(".") != "nothing":
        print(f"  not checked: {result.not_checked}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("pages", nargs="*", help="page file names; default: every page that needs a review")
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--review", action="store_true", help="call the model and record clean pages")
    parser.add_argument("--base", help="git revision the changes are measured against (default: merge base with main)")
    parser.add_argument("--head", help="review the pages as of this revision instead of the working tree; records nothing")
    parser.add_argument("--model", default=os.environ.get(MODEL_ENV, DEFAULT_MODEL))
    parser.add_argument("--effort", default=os.environ.get(EFFORT_ENV, DEFAULT_EFFORT))
    parser.add_argument("--full", action="store_true",
                        help="with --review: review every line of the named pages (default: all pages), not only changes")
    parser.add_argument("--jobs", type=int, default=4, help="pages reviewed at the same time (default 4)")
    parser.add_argument("--waive", metavar="PAGE", help="record PAGE, accepting the findings of its last review")
    parser.add_argument("--adopt", action="store_true",
                        help="record pages as they are, without a model review (needs --reason); "
                             "for pages checked another way, e.g. a full manual audit")
    parser.add_argument("--reason", help="why findings are waived or pages adopted")
    args = parser.parse_args(argv)
    root = args.root.resolve()
    record = load_record(root)
    texts = page_texts(root)

    if args.waive:
        if not args.reason:
            parser.error("--waive needs --reason")
        last = _load_report(root)["pages"].get(args.waive)
        if args.waive not in texts or not last or last["sha256"] != sha256_text(texts[args.waive]):
            print(f"No review of the current {args.waive} in {REPORT_DIR}/latest.json; run --review first.")
            return 2
        result = PageResult(args.waive, last["sha256"], last["lines_reviewed"], last["findings"],
                            last.get("not_checked", ""), context_omitted=last.get("context_omitted", []),
                            full=last.get("full", False))
        record["pages"][args.waive] = record_entry(result, last["reviewer"], "model", result.blocking, args.reason,
                                                   previous=record["pages"].get(args.waive))
        save_record(root, record, prune=True)
        print(f"Recorded {args.waive} with {len(result.blocking)} waived finding(s).")
        return 0

    stale = stale_pages(root, record)
    if args.head:
        names = args.pages or sorted(texts)
    else:
        unknown = [p for p in args.pages if p not in texts]
        if unknown:
            parser.error(f"not a reviewable wiki page: {', '.join(unknown)}")
        names = args.pages or (sorted(texts) if args.full else sorted(stale))

    if args.adopt:
        if not args.reason:
            parser.error("--adopt needs --reason")
        for name in names:
            result = PageResult(name, sha256_text(texts[name]), 0)
            record["pages"][name] = record_entry(result, "none", "adopted", reason=args.reason,
                                                 previous=record["pages"].get(name))
        save_record(root, record, prune=True)
        print(f"Adopted {len(names)} page(s) without a model review.")
        return 0

    if not args.review:
        gone = sorted(set(record["pages"]) - set(texts))
        for name in gone:
            print(f"{name}: recorded but no longer a wiki page; --review removes the entry")
        if gone and not stale:
            return 1
        unresolved = unresolved_pages(root, record)
        for name in names:
            print(f"{name}: {stale.get(name, 'reviewed')}")
        for name, findings in sorted(unresolved.items()):
            print(f"{name}: {len(findings)} unresolved finding(s) from its last review; fix the page or --waive")
        if stale or unresolved:
            print(f"{len(stale)} page(s) need a content review; {len(unresolved)} have unresolved findings.")
        else:
            print("Every page matches its content review.")
        return 1 if stale or unresolved else 0

    base = None if args.full else (args.base or default_base(root))
    report = _load_report(root) if not args.head else {"pages": {}}
    context_texts = texts_at(root, args.head) if args.head else texts
    exit_code, totals, jobs = 0, {}, []
    for name in names:
        new = context_texts.get(name)
        if new is None:
            continue
        previous = record["pages"].get(name)
        change = page_change(name, None if args.full else git_show(root, base, WIKI_DIR / name), new)
        if not change.changed_lines and not change.removed_lines:
            if args.head or name not in stale:
                continue
            change = page_change(name, None, new)  # same as the base but unrecorded: review all of it
        if change.metadata_only:
            print(f"{name}: metadata only, no model review needed")
            if not args.head:
                record["pages"][name] = record_entry(PageResult(name, change.sha256, 0), "none",
                                                     "metadata-only", previous=previous)
                if kept := still_unresolved(previous, new):
                    record["pages"][name]["unresolved"] = kept
            continue
        jobs.append(change)

    def save() -> None:
        if args.head:
            return
        save_record(root, record, prune=True)
        _report_path(root).parent.mkdir(parents=True, exist_ok=True)
        _report_path(root).write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    def run(change: PageChange) -> PageResult | ReviewError:
        try:
            return review_page(root, change, args.model, effort=args.effort, texts=context_texts)
        except ReviewError as exc:
            return exc
        except Exception as exc:  # an API failure on one page must not lose the others
            return ReviewError(f"{type(exc).__name__}: {exc}")

    def finish(change: PageChange, result: PageResult | ReviewError) -> int:
        what = "every line" if change.is_new else f"{len(change.changed_lines)} changed line(s)"
        print(f"{change.name}: reviewed {what} with {args.model}", flush=True)
        if isinstance(result, ReviewError):
            print(f"  REVIEW FAILED: {result}")
            return 2
        for key, value in result.usage.items():
            totals[key] = totals.get(key, 0) + value
        if result.context_omitted:
            print(f"  linked pages not sent (size limit): {', '.join(result.context_omitted)}")
        _print_findings(result)
        report["pages"][change.name] = {
            "sha256": result.sha256, "reviewer": args.model, "base": base or "full",
            "lines_reviewed": result.lines_reviewed, "full": result.full, "findings": result.findings,
            "not_checked": result.not_checked, "context_pages": result.context_pages,
            "context_omitted": result.context_omitted}
        if result.full and not args.head and change.name in record["pages"]:
            # Every line has now been read, whatever the outcome; later entries keep this date.
            record["pages"][change.name]["full_review"] = {"date": date.today().isoformat(), "reviewer": args.model}
        code = 0
        if result.blocking:
            print(f"  {len(result.blocking)} blocking finding(s): fix the page and review again, or "
                  f"`--waive {change.name} --reason ...` if the reviewer is wrong.")
            code = 1
            entry = record["pages"].get(change.name)
            if entry and entry.get("sha256") == result.sha256 and not args.head:
                # The recorded version itself is in question; the doctor fails until it is fixed or waived.
                found = [{"line": f.get("line"), "type": f.get("type"), "wiki_quote": f.get("wiki_quote"),
                          "quote_on_page": f.get("quote_on_page", False), "problem": f.get("problem")}
                         for f in result.blocking]
                # Only a full review replaces the list; a partial one did not re-read the earlier lines.
                earlier = [] if result.full else still_unresolved(entry, change.text)
                known = {(f.get("wiki_quote"), f.get("problem")) for f in found}
                entry["unresolved"] = found + [f for f in earlier
                                               if (f.get("wiki_quote"), f.get("problem")) not in known]
        else:
            print("  clean")
            if not args.head:
                earlier = record["pages"].get(change.name)
                record["pages"][change.name] = record_entry(result, args.model, "model", previous=earlier)
                if not result.full and (kept := still_unresolved(earlier, change.text)):
                    record["pages"][change.name]["unresolved"] = kept
                    print(f"  {len(kept)} earlier finding(s) on unchanged text are still unresolved")
                    code = 1
        save()  # after every page, so a long run that dies keeps what it finished
        return code

    if jobs:
        print(f"Reviewing {len(jobs)} page(s) with {args.model}, {args.jobs} at a time ...", flush=True)
        codes = [finish(jobs[0], run(jobs[0]))]  # alone first, so the rest read the PDFs from the cache
        with ThreadPoolExecutor(max_workers=max(1, args.jobs)) as pool:
            futures = {pool.submit(run, change): change for change in jobs[1:]}
            for future in as_completed(futures):
                codes.append(finish(futures[future], future.result()))
        exit_code = max(codes)
    save()
    if totals:
        print("tokens: " + ", ".join(f"{k}={v}" for k, v in totals.items()))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
