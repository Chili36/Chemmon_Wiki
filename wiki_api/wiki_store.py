from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
from typing import Any

import yaml


INDEX_ENTRY_RE = re.compile(r"^- \[[^\]]+\]\(([^)]+)\):\s*(.+)$")
GUIDING_PRINCIPLES_HEADER = "## Guiding Principles"
HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)
WIKI_LINK_RE = re.compile(r"\[\[([a-zA-Z0-9_\-]+)(?:\|[^\]]+)?\]\]")
ROOT_PAGES = {
    "index.md": "Wiki Index",
    "README.md": "README",
    "PROJECT_CONTEXT.md": "Project Context",
    "SCHEMA.md": "Wiki Schema",
    "INGEST_WORKFLOW.md": "Ingest Workflow",
    "log.md": "Wiki Log",
    "SOURCE_REVIEW.md": "Source Review",
    "MAINTENANCE_WORKFLOW.md": "Maintenance Workflow",
    "EVALUATION.md": "Answer Quality Evaluation",
    "RUNTIME_POLICY.md": "ChemMon Evidence Policy",
    "2026-10-05-foodex2-parity.md": "Improvement Plan",
}
ROOT_PAGE_PATHS = {name: name for name in ROOT_PAGES}
ROOT_PAGE_PATHS["2026-10-05-foodex2-parity.md"] = "docs/plans/2026-10-05-foodex2-parity.md"


@dataclass(frozen=True)
class WikiPage:
    name: str
    title: str
    summary: str
    sources: list[str]
    related: list[str]
    content: str
    body: str
    page_type: str = "reference"
    domain: str = "all"
    last_updated: str | None = None
    source_pages: tuple[str, ...] = ()
    select_when: str | None = None


def split_frontmatter(raw: str) -> tuple[dict[str, Any], str]:
    lines = raw.splitlines()
    if len(lines) < 3 or lines[0].strip() != "---":
        return {}, raw
    closing_idx = None
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            closing_idx = idx
            break
    if closing_idx is None:
        return {}, raw
    frontmatter = "\n".join(lines[1:closing_idx])
    body = "\n".join(lines[closing_idx + 1 :]).lstrip("\n")
    data = yaml.safe_load(frontmatter) or {}
    if not isinstance(data, dict):
        data = {}
    return data, body


class WikiStore:
    def __init__(self, root: Path | str):
        self.root = Path(root)
        self.guidance_dir = self.root / "wiki" / "chemmon-guidance"
        self.index_path = self.root / "index.md"
        self.log_path = self.root / "log.md"

    @property
    def _summaries(self) -> dict[str, str]:
        raw = self.index_path.read_text(encoding="utf-8")
        summaries: dict[str, str] = {}
        for line in raw.splitlines():
            match = INDEX_ENTRY_RE.match(line)
            if not match:
                continue
            target, summary = match.groups()
            name = Path(target).name
            summaries[name] = summary.strip()
        summaries["index.md"] = "Top-level catalog for the ChemMon wiki layer."
        summaries["log.md"] = "Chronological record of wiki ingests and changes."
        return summaries

    @property
    def _guiding_principles(self) -> list[str]:
        raw = self.index_path.read_text(encoding="utf-8")
        lines = raw.splitlines()
        in_section = False
        principles: list[str] = []
        for line in lines:
            if line.strip() == GUIDING_PRINCIPLES_HEADER:
                in_section = True
                continue
            if in_section and line.startswith("## "):
                break
            if in_section and line.startswith("- "):
                principles.append(line[2:].strip())
        return principles

    def list_pages(self) -> list[str]:
        names = [page.name for page in self.guidance_dir.glob("*.md")]
        return sorted(names)

    def allowed_page_names(self) -> set[str]:
        return {name for name, path in ROOT_PAGE_PATHS.items() if (self.root / path).is_file()} | set(self.list_pages())

    def normalize_page_name(self, page_name: str) -> str:
        cleaned = page_name.strip().replace("\\", "/")
        if cleaned in {"index.md", "log.md"}:
            return cleaned
        if cleaned.startswith("./"):
            cleaned = cleaned[2:]
        if cleaned.startswith("raw/chemmon-guidance/"):
            cleaned = cleaned.split("/")[-1]
        else:
            cleaned = Path(cleaned).name
        return cleaned

    def read_page(self, page_name: str) -> WikiPage:
        normalized_name = self.normalize_page_name(page_name)
        if normalized_name not in self.allowed_page_names():
            raise FileNotFoundError(f"Unknown wiki page: {page_name}")
        if normalized_name in ROOT_PAGES:
            path = self.root / ROOT_PAGE_PATHS[normalized_name]
        else:
            path = self.guidance_dir / normalized_name
        raw = path.read_text(encoding="utf-8")
        frontmatter, body = split_frontmatter(raw)
        title = str(frontmatter.get("title") or ROOT_PAGES.get(normalized_name, normalized_name))
        sources = [
            str(item) for item in frontmatter.get("sources", []) if isinstance(item, str)
        ]
        related = [
            str(item) for item in frontmatter.get("related", []) if isinstance(item, str)
        ]
        summaries = self._summaries
        summary = summaries.get(page_name, "")
        return WikiPage(
            name=normalized_name,
            title=title,
            summary=summaries.get(normalized_name, summary),
            sources=sources,
            related=related,
            content=raw,
            body=body,
            page_type="orientation" if normalized_name in ROOT_PAGES else str(frontmatter.get("type", "reference")),
            domain=str(frontmatter.get("domain", "all")),
            last_updated=str(frontmatter["last_updated"]) if frontmatter.get("last_updated") else None,
            source_pages=tuple(str(item) for item in frontmatter.get("source_pages", []) if isinstance(item, str)),
            select_when=frontmatter.get("select_when") if isinstance(frontmatter.get("select_when"), str) else None,
        )

    def catalog(self, *, include_orientation: bool = False) -> list[WikiPage]:
        names = self.list_pages()
        if include_orientation:
            names = [name for name in ROOT_PAGES if name in self.allowed_page_names()] + names
        return [self.read_page(name) for name in names]

    def selector_catalog(self, *, use_hints: bool = True) -> str:
        """Topic metadata is for discovery; it is not answer evidence."""
        return "\n".join(
            f"- {p.name} | {p.page_type} | domain={p.domain} | {(p.select_when if use_hints else None) or p.summary or p.title}"
            for p in self.catalog()
        )

    def backlinks(self, page_name: str) -> list[str]:
        target = self.read_page(page_name).name.removesuffix(".md")
        return sorted(
            page.name for page in self.catalog()
            if page.name != target + ".md"
            and target in WIKI_LINK_RE.findall(page.body + "\n" + "\n".join(page.related))
        )

    def guiding_principles(self) -> list[str]:
        return list(self._guiding_principles)

    def clean_content_for_model(self, page: WikiPage) -> str:
        # Preserve claim-adjacent source locators while removing other comments.
        def source_comment(match: re.Match[str]) -> str:
            text = match.group(0)[4:-3].strip()
            return text if text.startswith("Source:") else ""

        cleaned = HTML_COMMENT_RE.sub(source_comment, page.body)
        cleaned_lines: list[str] = []
        for raw_line in cleaned.splitlines():
            line = raw_line.rstrip()
            cleaned_lines.append(line.rstrip())

        collapsed: list[str] = []
        blank_run = 0
        for line in cleaned_lines:
            if line.strip():
                blank_run = 0
                collapsed.append(line)
            else:
                blank_run += 1
                if blank_run <= 1:
                    collapsed.append("")
        return "\n".join(collapsed).strip()
