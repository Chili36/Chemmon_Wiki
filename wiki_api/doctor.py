"""Wiki doctor: deterministic maintenance checks for the ChemMon wiki.

Ported from the FoodEx2 wiki doctor and extended with checks for the gaps
found in #63: source tables cited but never transcribed, rule scopes that
narrow on secondary pages, and the CHEMMON misspelling of CHEMON rule IDs.

Run: python -m wiki_api.doctor [--format text|json|github] [--strict-warnings]
                               [--check-external-links]

The doctor includes every tools/health_check.py finding, so it is a superset
of the health check. It checks structure and recorded claims; it does not
certify that a page's meaning matches its source.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
import json
from pathlib import Path
import re
import ssl
import sys
from typing import Iterable, Literal
import urllib.error
import urllib.request

from .wiki_store import WikiStore, split_frontmatter

Severity = Literal["error", "warning"]

REGISTRY_PATH = Path("docs/source-tables.json")
STATUSES = {"transcribed", "generated", "rule-inventory", "summarised", "partial", "not-covered"}
GAP_STATUSES = {"partial", "not-covered"}

WIKI_LINK_RE = re.compile(r"\[\[([a-zA-Z0-9_\-]+)(?:\|[^\]]+)?\]\]")
MARKDOWN_LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)\)")
EXTERNAL_LINK_RE = re.compile(r"^[a-z][a-z0-9+.-]*:", re.IGNORECASE)
FENCED_CODE_RE = re.compile(r"(^|\n)(```|~~~).*?(?=\n\2|\Z)(?:\n\2)?", re.DOTALL)
INLINE_CODE_RE = re.compile(r"`[^`\n]*`")
HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)
LOG_DATE_RE = re.compile(r"^## (?:\[(\d{4}-\d{2}-\d{2})\]|(\d{4}-\d{2}-\d{2}))", re.MULTILINE)
# Table numbers have one or two digits; "Table 1, 2026 changes" cites Table 1 only.
_TABLE_NO = r"\d{1,2}(?!\d)"
TABLE_REF_RE = re.compile(rf"\bTables?\s+({_TABLE_NO}(?:\s*(?:[-–/,]|and)\s*{_TABLE_NO})*)")
MISSPELT_RULE_RE = re.compile(r"\bCHEMMON\d")
# Matches both spellings so the scope check works independently of the spelling check.
RULE_ID_RE = re.compile(r"\bCHEMM?ON\d+(?:_[a-z])?\b")
IGNORE_SCOPE_MARK = "<!-- doctor-ignore: rule_scope -->"

# Domain words as they appear in rule scope cells and prose.
DOMAIN_PATTERNS = {
    "PPP": re.compile(r"pesticid|\bPPP\b|\bPEST\b", re.IGNORECASE),
    "VMPR": re.compile(r"\bVMPR\b|veterinar", re.IGNORECASE),
    "CONT": re.compile(r"contaminant|\bCONT\b|\bOCC\b", re.IGNORECASE),
    "ADD": re.compile(r"additive|\bFA\b|\bADD\b", re.IGNORECASE),
    "FLAV": re.compile(r"flavouring|\bFF\b|\bFLAV\b", re.IGNORECASE),
}
HTTP_TIMEOUT_SECONDS = 8
HTTP_USER_AGENT = "ChemMon-Wiki-Doctor/1.0"


@dataclass(frozen=True)
class DoctorIssue:
    severity: Severity
    check: str
    location: str
    message: str

    def as_dict(self) -> dict[str, str]:
        return {"severity": self.severity, "check": self.check,
                "location": self.location, "message": self.message}


@dataclass(frozen=True)
class DoctorReport:
    issues: list[DoctorIssue]
    source_tables: dict | None = None

    @property
    def errors(self) -> list[DoctorIssue]:
        return [i for i in self.issues if i.severity == "error"]

    @property
    def warnings(self) -> list[DoctorIssue]:
        return [i for i in self.issues if i.severity == "warning"]

    def as_dict(self) -> dict[str, object]:
        return {"error_count": len(self.errors), "warning_count": len(self.warnings),
                "issues": [i.as_dict() for i in self.issues], "source_tables": self.source_tables}


def run_doctor(root: Path | str = ".", *, check_external_links: bool = False,
               include_health: bool = True) -> DoctorReport:
    root = Path(root)
    store = WikiStore(root)
    pages = _load_pages(store)
    issues: list[DoctorIssue] = []
    if include_health:
        issues.extend(_check_health(root))
    issues.extend(check_rule_id_spelling(root, pages))
    table_issues, table_summary = check_source_tables(root, pages)
    issues.extend(table_issues)
    issues.extend(check_rule_scope(pages))
    issues.extend(check_content_review(root))
    issues.extend(check_log_chronology(store.log_path))
    issues.extend(check_markdown_links(store, pages))
    issues.extend(check_incoming_links(pages))
    if check_external_links:
        issues.extend(_check_external_links(pages))
    order = {"error": 0, "warning": 1}
    return DoctorReport(sorted(issues, key=lambda i: (order[i.severity], i.check, i.location)),
                        table_summary)


# --- page loading -----------------------------------------------------------

@dataclass(frozen=True)
class Page:
    name: str
    frontmatter: dict
    body: str
    body_offset: int = 0  # lines before the body, so body line N is file line N + offset


def _load_pages(store: WikiStore) -> dict[str, Page]:
    pages = {}
    for name in store.list_pages():
        raw = (store.guidance_dir / name).read_text(encoding="utf-8")
        data, body = split_frontmatter(raw)
        pages[name] = Page(name, data, body, len(raw.splitlines()) - len(body.splitlines()))
    return pages


def _prose(text: str) -> str:
    text = FENCED_CODE_RE.sub("\n", HTML_COMMENT_RE.sub("", text))
    return INLINE_CODE_RE.sub("", text)


# --- health check -----------------------------------------------------------

def _check_health(root: Path) -> Iterable[DoctorIssue]:
    repo = Path(__file__).resolve().parent.parent
    if str(repo) not in sys.path:
        sys.path.insert(0, str(repo))
    from tools.health_check import run_health_check  # tools/ is not a package dependency of the API

    report = run_health_check(root)
    for message in report.errors:
        yield DoctorIssue("error", "health", _health_location(message), message)
    for message in report.warnings:
        yield DoctorIssue("warning", "health", _health_location(message), message)


def _health_location(message: str) -> str:
    head = message.split(":", 1)[0]
    return head if head.endswith(".md") or head.endswith(".json") else "wiki"


# --- rule ID spelling -------------------------------------------------------

def check_rule_id_spelling(root: Path, pages: dict[str, Page]) -> Iterable[DoctorIssue]:
    """The source spells rule IDs CHEMON; CHEMMON<n> was a wiki-only misspelling (#63)."""
    texts = {f"wiki/chemmon-guidance/{n}": p.body + "\n" + json.dumps(p.frontmatter, default=str)
             for n, p in pages.items()}
    index = root / "index.md"
    if index.is_file():
        texts["index.md"] = index.read_text(encoding="utf-8")
    for location, text in sorted(texts.items()):
        count = len(MISSPELT_RULE_RE.findall(text))
        if count:
            yield DoctorIssue("error", "rule_id_spelling", location,
                              f"{count} rule ID(s) spelled CHEMMON<n>; the source spells them CHEMON<n>.")


# --- source tables ----------------------------------------------------------

def load_registry(root: Path) -> dict:
    return json.loads((root / REGISTRY_PATH).read_text(encoding="utf-8"))


def table_numbers(text: str) -> list[int]:
    numbers: list[int] = []
    for match in TABLE_REF_RE.finditer(text):
        raw = match.group(1)
        found = [int(x) for x in re.findall(r"\d+", raw)]
        if len(found) == 2 and re.search(r"\d\s*[-–]\s*\d", raw):
            found = list(range(found[0], found[1] + 1))
        numbers.extend(found)
    return numbers


def cited_tables(entry: str, page_sources: list[str], registry: dict) -> tuple[list[tuple[str, int]], list[int]]:
    """Return ((source_key, table), ...) cited by one source_pages entry, plus unattributed tables.

    A table belongs to the nearest source alias before it in the entry (e.g. "No-presence 2026
    Table 1"); with no alias it belongs to the page's only source.
    """
    aliases = [(alias, key) for key, src in registry["sources"].items() for alias in src.get("aliases", [])]
    by_file = {Path(src["file"]).name: key for key, src in registry["sources"].items()}
    default = None
    keys = {by_file.get(Path(s).name) for s in page_sources}
    if len(keys) == 1 and None not in keys:
        default = keys.pop()
    cited, unattributed = [], []
    for match in TABLE_REF_RE.finditer(entry):
        preceding = entry[:match.start()]
        best = max(((preceding.rfind(alias), key) for alias, key in aliases if alias in preceding),
                   default=(-1, None))
        key = best[1] or default
        for number in table_numbers(match.group(0)):
            (cited.append((key, number)) if key else unattributed.append(number))
    return cited, unattributed


def check_source_tables(root: Path, pages: dict[str, Page]) -> tuple[list[DoctorIssue], dict | None]:
    issues: list[DoctorIssue] = []
    loc = REGISTRY_PATH.as_posix()
    try:
        registry = load_registry(root)
    except FileNotFoundError:
        return [DoctorIssue("error", "source_tables", loc, "Source table registry is missing.")], None
    except json.JSONDecodeError as exc:
        return [DoctorIssue("error", "source_tables", loc, f"Registry is not valid JSON: {exc}")], None

    for key, src in registry.get("sources", {}).items():
        if not (root / src.get("file", "")).is_file():
            issues.append(DoctorIssue("error", "source_tables", loc, f"Source {key} file not found: {src.get('file')}"))

    entries: dict[tuple[str, int], dict] = {}
    for entry in registry.get("tables", []):
        ident = (entry.get("source"), entry.get("table"))
        label = f"{ident[0]} Table {ident[1]}"
        if ident in entries:
            issues.append(DoctorIssue("error", "source_tables", loc, f"{label} is registered twice."))
        entries[ident] = entry
        status = entry.get("status")
        if ident[0] not in registry.get("sources", {}):
            issues.append(DoctorIssue("error", "source_tables", loc, f"{label}: unknown source."))
        if status not in STATUSES:
            issues.append(DoctorIssue("error", "source_tables", loc, f"{label}: unknown status {status!r}."))
            continue
        listed = entry.get("pages", [])
        for name in listed:
            if name not in pages:
                issues.append(DoctorIssue("error", "source_tables", loc, f"{label}: page {name} does not exist."))
        if status == "summarised" and not entry.get("reason"):
            issues.append(DoctorIssue("error", "source_tables", loc, f"{label}: summarised tables need a reason."))
        if status in GAP_STATUSES:
            if not entry.get("issue"):
                issues.append(DoctorIssue("error", "source_tables", loc, f"{label}: {status} tables need a tracking issue."))
            else:
                what = entry.get("missing", "rows not carried over")
                title = f" ({entry['title']})" if entry.get("title") else ""
                issues.append(DoctorIssue("warning", "source_tables", ", ".join(listed) or loc,
                                          f"{label}{title} is {status} ({entry['issue']}): {what}"))
        if status == "transcribed" and not (entry.get("must_contain") or entry.get("verified_by")):
            issues.append(DoctorIssue("error", "source_tables", loc,
                                      f"{label}: transcribed tables need must_contain strings or verified_by."))
        text = "\n".join(pages[n].body for n in listed if n in pages)
        missing = [s for s in entry.get("must_contain", []) if s not in text]
        if missing:
            shown = "; ".join(m if len(m) <= 80 else m[:77] + "..." for m in missing[:3])
            issues.append(DoctorIssue("error", "source_tables", ", ".join(listed),
                                      f"{label}: {len(missing)} required string(s) missing from the page(s): {shown}"))

    for name, page in sorted(pages.items()):
        sources = [s for s in page.frontmatter.get("sources", []) if isinstance(s, str)]
        for raw in page.frontmatter.get("source_pages", []) or []:
            if not isinstance(raw, str):
                continue
            cited, unattributed = cited_tables(raw, sources, registry)
            for number in unattributed:
                issues.append(DoctorIssue("error", "source_tables", name,
                                          f"source_pages cites Table {number} but names no source; prefix it, e.g. 'ChemMon 2026'."))
            for ident in cited:
                if ident not in entries:
                    issues.append(DoctorIssue("error", "source_tables", name,
                                              f"source_pages cites {ident[0]} Table {ident[1]}, which is not in {loc}. "
                                              "Register it and say whether the page transcribes or only summarises it."))

    counts: dict[str, int] = {}
    for entry in entries.values():
        counts[entry.get("status", "?")] = counts.get(entry.get("status", "?"), 0) + 1
    return issues, {"tables": len(entries), "by_status": dict(sorted(counts.items()))}


# --- rule scope -------------------------------------------------------------

def _rule_key(rule: str) -> str:
    return rule.replace("CHEMMON", "CHEMON")


def domains(text: str) -> set[str]:
    return {key for key, pattern in DOMAIN_PATTERNS.items() if pattern.search(text)}


def canonical_scopes(pages: dict[str, Page]) -> dict[str, tuple[set[str], str]]:
    """Rule ID -> (domains in its scope cell, defining page) from business-rules tables."""
    scopes: dict[str, tuple[set[str], str]] = {}
    for name, page in pages.items():
        if not name.startswith("business-rules-") or name == "business-rules-2026-changes.md":
            continue
        column = None
        for line in page.body.splitlines():
            if not line.startswith("|"):
                column = None
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if column is None:
                headers = [c.lower() for c in cells]
                column = next((i for i, h in enumerate(headers) if h in {"scope", "domain"}), -1)
                continue
            if column < 0 or column >= len(cells):
                continue
            match = RULE_ID_RE.fullmatch(cells[0].replace("`", "").strip())
            found = domains(cells[column])
            if match and found:
                scopes[_rule_key(match.group(0))] = (found, name)
    return scopes


def _units(body: str) -> Iterable[tuple[int, str]]:
    """Paragraphs and list items with wrapped lines joined; tables and headings skipped."""
    start, buffer = 0, []
    for number, line in enumerate(body.splitlines() + [""], 1):
        stripped = line.strip()
        new_item = bool(re.match(r"^(?:[-*+]|\d+\.)\s", stripped))
        if not stripped or stripped.startswith(("|", "#")) or new_item:
            if buffer:
                yield start, " ".join(buffer)
            buffer = []
            if new_item:
                start, buffer = number, [stripped]
            continue
        if not buffer:
            start = number
        buffer.append(stripped)


def check_rule_scope(pages: dict[str, Page]) -> Iterable[DoctorIssue]:
    """A paragraph citing one rule and naming fewer domains than its canonical scope is wrong.

    Catches CHEMON58 described as pesticides-only while Table 10 scopes it to pesticides and VMPR.
    Mark a deliberate narrowing with <!-- doctor-ignore: rule_scope --> in the paragraph.
    """
    scopes = canonical_scopes(pages)
    for name, page in sorted(pages.items()):
        for line, unit in _units(page.body):
            if IGNORE_SCOPE_MARK in unit:
                continue
            ids = {_rule_key(r) for r in RULE_ID_RE.findall(unit)}
            if len(ids) != 1:
                continue
            rule = ids.pop()
            if rule not in scopes or scopes[rule][1] == name:
                continue
            named = domains(WIKI_LINK_RE.sub("", HTML_COMMENT_RE.sub("", unit)))
            canon, defining = scopes[rule]
            if named and named < canon:
                yield DoctorIssue("error", "rule_scope", f"{name}:{line + page.body_offset}",
                                  f"{rule} is described for {'/'.join(sorted(named))}, but {defining} scopes it to "
                                  f"{'/'.join(sorted(canon))}.")


# --- content review ---------------------------------------------------------

def check_content_review(root: Path) -> Iterable[DoctorIssue]:
    """Every page must match the version an independent reader checked against the PDFs (#72)."""
    from wiki_api.content_review import record_problems

    for location, message in record_problems(root):
        yield DoctorIssue("error", "content_review", location, message)


# --- ported FoodEx2 checks --------------------------------------------------

def check_log_chronology(log_path: Path) -> Iterable[DoctorIssue]:
    dates = [a or b for a, b in LOG_DATE_RE.findall(log_path.read_text(encoding="utf-8"))]
    for previous, current in zip(dates, dates[1:]):
        if current > previous:
            yield DoctorIssue("error", "log_chronology", "log.md",
                              f"Log entries must be newest first; {current} appears after {previous}.")


def check_markdown_links(store: WikiStore, pages: dict[str, Page]) -> Iterable[DoctorIssue]:
    root = store.root.resolve()
    for name, page in sorted(pages.items()):
        for target in MARKDOWN_LINK_RE.findall(FENCED_CODE_RE.sub("\n", page.body)):
            path = target.split("#", 1)[0]
            if not path or EXTERNAL_LINK_RE.match(path):
                continue
            candidate = (store.guidance_dir / path).resolve()
            if not candidate.is_relative_to(root):
                yield DoctorIssue("error", "markdown_links", name, f"Local link escapes the repo: {target}")
            elif not candidate.exists():
                yield DoctorIssue("error", "markdown_links", name, f"Broken local link: {target}")


def check_incoming_links(pages: dict[str, Page]) -> Iterable[DoctorIssue]:
    """Every topic page needs a link from another topic page so graph expansion can reach it."""
    incoming = {name: 0 for name in pages}
    for name, page in pages.items():
        related = " ".join(r for r in page.frontmatter.get("related", []) or [] if isinstance(r, str))
        for target in set(WIKI_LINK_RE.findall(page.body + " " + related)):
            if f"{target}.md" in incoming and f"{target}.md" != name:
                incoming[f"{target}.md"] += 1
    for name, count in sorted(incoming.items()):
        if count == 0:
            yield DoctorIssue("error", "incoming_links", name, "No other topic page links to this page.")


def _check_external_links(pages: dict[str, Page]) -> Iterable[DoctorIssue]:
    links: dict[str, set[str]] = {}
    for name, page in pages.items():
        for target in MARKDOWN_LINK_RE.findall(page.body):
            if target.startswith(("http://", "https://")):
                links.setdefault(target.split("#", 1)[0], set()).add(name)
    for url, where in sorted(links.items()):
        problem = _external_problem(url)
        if problem:
            yield DoctorIssue("warning", "external_links", ", ".join(sorted(where)), problem)


def _ssl_context() -> ssl.SSLContext:
    try:  # python.org builds on macOS ship without a CA bundle; certifi supplies one
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        return ssl.create_default_context()


def _external_problem(url: str) -> str | None:
    last = None
    context = _ssl_context()
    for method in ("HEAD", "GET"):
        request = urllib.request.Request(url, method=method, headers={"User-Agent": HTTP_USER_AGENT})
        try:
            with urllib.request.urlopen(request, timeout=HTTP_TIMEOUT_SECONDS, context=context) as response:
                if response.status < 400:
                    return None
                last = f"HTTP {response.status}"
        except urllib.error.HTTPError as exc:
            last = f"HTTP {exc.code}"
            if exc.code not in {403, 405, 501}:
                break
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            last = str(getattr(exc, "reason", exc))
    return f"External link failed ({last}): {url}"


# --- output -----------------------------------------------------------------

def render_text(report: DoctorReport) -> str:
    lines = [f"Wiki doctor: {len(report.errors)} error(s), {len(report.warnings)} warning(s)"]
    if report.source_tables:
        counts = ", ".join(f"{v} {k}" for k, v in report.source_tables["by_status"].items())
        lines.append(f"Source tables: {report.source_tables['tables']} registered ({counts}).")
    if not report.issues:
        lines.append("All deterministic wiki maintenance checks passed.")
    for severity in ("error", "warning"):
        matching = [i for i in report.issues if i.severity == severity]
        if matching:
            lines += ["", f"{severity.title()}s:"]
            lines += [f"- [{i.check}] {i.location}: {i.message}" for i in matching]
    return "\n".join(lines)


def _escape(value: str) -> str:
    return value.replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")


def render_github(report: DoctorReport) -> str:
    lines = [render_text(report)]
    for issue in report.issues:
        path = issue.location.split(":", 1)[0].split(",", 1)[0].strip()
        if path.endswith(".md") and "/" not in path and path not in {"index.md", "log.md"}:
            path = f"wiki/chemmon-guidance/{path}"
        file_part = f",file={_escape(path)}" if path.endswith((".md", ".json")) else ""
        lines.append(f"::{issue.severity} title={issue.check}{file_part}::{_escape(issue.message)}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run deterministic ChemMon wiki maintenance checks.")
    parser.add_argument("--root", default=".", help="Repository root (default: current directory).")
    parser.add_argument("--format", choices=("text", "json", "github"), default="text")
    parser.add_argument("--strict-warnings", action="store_true", help="Exit non-zero on warnings.")
    parser.add_argument("--check-external-links", action="store_true",
                        help="Also request external http(s) links; failures are warnings.")
    args = parser.parse_args(argv)
    report = run_doctor(Path(args.root), check_external_links=args.check_external_links)
    if args.format == "json":
        print(json.dumps(report.as_dict(), indent=2, ensure_ascii=False))
    elif args.format == "github":
        print(render_github(report))
    else:
        print(render_text(report))
    return 1 if report.errors or (args.strict_warnings and report.warnings) else 0


if __name__ == "__main__":
    sys.exit(main())
