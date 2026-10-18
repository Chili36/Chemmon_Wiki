"""Send only the relevant entries of the by-food list page when a question names pesticides on it.

The list stays one catalogue page, so page selection is unaffected. When the selector picks it and
the question names listed pesticides, the answerer gets the page's reading guide, those pesticides'
lines, their interpreted-wording notes, the Annex I legend and the attribution, instead of all
entries. A question naming none of them gets the whole page. Matching is whole-word text matching
in code; no model is called.
"""
from __future__ import annotations

import re

BY_FOOD_PAGE = "pesticide-residue-definitions-by-food.md"
ENTRY_RE = re.compile(r"^- \*\*(.+?)\*\*:", re.M)
NOTE_RE = re.compile(r"^- (.+?):", re.M)


def _norm(text: str) -> str:
    text = text.lower().replace("sulph", "sulf")
    return re.sub(r"[^a-z0-9]+", " ", text).strip()


def _named(name: str, question: str) -> bool:
    key = _norm(re.split(r"\s*\(", name, maxsplit=1)[0])
    return len(key) >= 3 and f" {key} " in question


def excerpt(content: str, question: str) -> str | None:
    """The page trimmed to the named entries, or None when it names none (or has no entry list)."""
    parts = re.split(r"\n(?=## )", content)
    sections = {p.split("\n", 1)[0]: i for i, p in enumerate(parts)}
    entries_at = sections.get("## Definitions by pesticide")
    if entries_at is None:
        return None
    asked = f" {_norm(question)} "
    lines = parts[entries_at].splitlines()
    kept = [line for line in lines if (m := ENTRY_RE.match(line)) and _named(m.group(1), asked)]
    if not kept:
        return None
    names = [ENTRY_RE.match(line).group(1) for line in kept]
    out = list(parts)
    out[entries_at] = "\n".join(["## Definitions by pesticide", "", *kept, ""])
    notes_at = sections.get("## Interpreted source wording")
    if notes_at is not None:
        notes = [line for line in parts[notes_at].splitlines()
                 if (m := NOTE_RE.match(line)) and m.group(1) in names]
        out[notes_at] = "\n".join(["## Interpreted source wording", "", *(notes or ["- None for these pesticides."]), ""])
    return "\n".join(out)
