"""Deterministic page selection for /wiki/context-pack.

Unlike /wiki/ask, this runs no LLM: callers put it on a latency-sensitive
critical path (DMT param search deconstructs a query *before* retrieval and
needs the guidance that bears on it). Selection is driven by the `domain`
frontmatter every page already declares under SCHEMA.md, so the mapping lives
in wiki data rather than in caller code.

Callers pass semantic identifiers only -- a reporting domain and optional
topic hints -- never page names. This module resolves which pages apply and
reports how each one was chosen.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from .wiki_store import WikiPage, WikiStore


CROSS_CUTTING = "cross-cutting"
UNIVERSAL = "all"

# Caller vocabularies differ from the wiki's frontmatter enum: DMT's PARAM
# catalogue uses the five EFSA domain analysis hierarchies (vmprParam,
# pestParam, chemAnalysis, addAnalysis, flavAnalysis -- see
# [[reporting-flags]]), while SCHEMA.md folds additives and flavourings into
# a single `additives` domain. Accept both and normalise here.
DOMAIN_ALIASES: dict[str, str] = {
    "vmpr": "vmpr",
    "vet": "vmpr",
    "vmprparam": "vmpr",
    "is_vet": "vmpr",
    "pesticide": "pesticide",
    "pesticides": "pesticide",
    "pest": "pesticide",
    "pestparam": "pesticide",
    "ppp": "pesticide",
    "is_pest": "pesticide",
    "contaminant": "contaminant",
    "contaminants": "contaminant",
    "occ": "contaminant",
    "chemanalysis": "contaminant",
    "additive": "additives",
    "additives": "additives",
    "add": "additives",
    "addanalysis": "additives",
    "flavouring": "additives",
    "flavourings": "additives",
    "flavour": "additives",
    "flav": "additives",
    "flavanalysis": "additives",
    "baby-food": "baby-food",
    "baby_food": "baby-food",
    "babyfood": "baby-food",
    "baby": "baby-food",
    "cross-cutting": CROSS_CUTTING,
    "cross_cutting": CROSS_CUTTING,
    "all": UNIVERSAL,
}

_TOKEN_RE = re.compile(r"[a-z0-9]+")

# Tokens too common in this corpus to carry signal.
_STOPWORDS = frozenset(
    {
        "and",
        "are",
        "chemmon",
        "efsa",
        "for",
        "from",
        "how",
        "the",
        "this",
        "wiki",
        "with",
        "page",
        "reporting",
        "ssd2",
    }
)


def normalize_domain(raw: str | None) -> str | None:
    """Map a caller's domain vocabulary onto the wiki frontmatter enum.

    Returns None for unknown or missing values, which makes selection fall
    back to relevance ranking over the whole corpus rather than erroring --
    an unrecognised domain should degrade the pack, not break the caller.
    """
    if not raw:
        return None
    key = str(raw).strip().lower().replace(" ", "-")
    return DOMAIN_ALIASES.get(key) or DOMAIN_ALIASES.get(key.replace("-", "_"))


def _tokens(text: str) -> set[str]:
    return {
        token
        for token in _TOKEN_RE.findall(text.lower())
        if len(token) > 2 and token not in _STOPWORDS
    }


@dataclass(frozen=True)
class SelectedPage:
    page: WikiPage
    selected_by: str  # "domain" | "cross-cutting" | "relevance"
    score: float


def _relevance(page: WikiPage, query_tokens: set[str]) -> float:
    """Token overlap against the page's name, title and index summary.

    Deliberately not scored against page *body*: bodies are long and would let
    an incidental mention outrank a page that is actually about the topic.
    """
    if not query_tokens:
        return 0.0
    page_tokens = _tokens(f"{page.name} {page.title} {page.summary}")
    if not page_tokens:
        return 0.0
    return len(query_tokens & page_tokens) / len(query_tokens)


def select_pages(
    store: WikiStore,
    *,
    search_term: str,
    domain: str | None,
    topics: list[str] | None = None,
    max_pages: int = 6,
) -> tuple[list[SelectedPage], dict]:
    """Select context-pack pages for a query, deterministically.

    Tiers, in order, capped at ``max_pages``:

    1. ``domain``      -- pages whose frontmatter domain matches the request
    2. ``cross-cutting`` -- rules that apply across domains
    3. ``relevance``   -- remaining pages ranked by token overlap

    Returns the selection plus a trace explaining every choice, so callers can
    see which pages the service resolved and why without guessing.
    """
    normalized = normalize_domain(domain)
    topics = topics or []
    query_tokens = _tokens(" ".join([search_term, *topics]))

    catalog = store.catalog()
    chosen: list[SelectedPage] = []
    seen: set[str] = set()

    def take(page: WikiPage, reason: str, score: float, *, limit: int) -> None:
        if page.name in seen or len(chosen) >= limit:
            return
        seen.add(page.name)
        chosen.append(SelectedPage(page=page, selected_by=reason, score=score))

    # When the caller passes explicit topic hints it is telling us what it is
    # *doing* (e.g. parameter coding), which cross-domain reference pages serve
    # better than an nth domain page. Reserve part of the budget for the
    # relevance tier so a domain with many pages cannot starve it.
    reserved = max(1, max_pages // 3) if (topics and query_tokens) else 0
    tiered_limit = max(1, max_pages - reserved)

    # Tier 1 -- exact domain match. Sorted by relevance so that when a domain
    # has more pages than the budget, the most on-topic ones survive.
    if normalized and normalized not in {UNIVERSAL, CROSS_CUTTING}:
        tier = [p for p in catalog if p.domain == normalized]
        tier.sort(key=lambda p: (-_relevance(p, query_tokens), p.name))
        for page in tier:
            take(page, "domain", _relevance(page, query_tokens), limit=tiered_limit)

    # Tier 2 -- cross-cutting rules.
    tier2 = [p for p in catalog if p.domain == CROSS_CUTTING]
    tier2.sort(key=lambda p: (-_relevance(p, query_tokens), p.name))
    for page in tier2:
        take(page, CROSS_CUTTING, _relevance(page, query_tokens), limit=tiered_limit)

    # Tier 3 -- relevance fill from the remaining corpus. Pages tagged to a
    # *different* domain are excluded: a pesticide query should not pull baby
    # food rules just because the wording overlaps.
    allowed = {UNIVERSAL} if normalized else {UNIVERSAL, CROSS_CUTTING}
    remainder = [
        p for p in catalog if p.name not in seen and (p.domain in allowed or not normalized)
    ]
    scored = [(p, _relevance(p, query_tokens)) for p in remainder]
    scored = [(p, s) for p, s in scored if s > 0]
    scored.sort(key=lambda item: (-item[1], item[0].name))
    for page, score in scored:
        take(page, "relevance", score, limit=max_pages)

    # Backfill: if relevance did not use its reserved slots, hand them back to
    # the tiered pages rather than returning a short pack.
    if len(chosen) < max_pages:
        leftovers = [p for p in catalog if p.name not in seen]
        if normalized and normalized not in {UNIVERSAL, CROSS_CUTTING}:
            leftovers = [p for p in leftovers if p.domain in {normalized, CROSS_CUTTING}]
        else:
            leftovers = [p for p in leftovers if p.domain == CROSS_CUTTING]
        leftovers.sort(key=lambda p: (-_relevance(p, query_tokens), p.name))
        for page in leftovers:
            reason = "domain" if page.domain == normalized else CROSS_CUTTING
            take(page, reason, _relevance(page, query_tokens), limit=max_pages)

    trace = {
        "requested_domain": domain,
        "normalized_domain": normalized,
        "domain_recognized": normalized is not None,
        "query_tokens": sorted(query_tokens),
        "max_pages": max_pages,
        "counts": {
            "domain": sum(1 for c in chosen if c.selected_by == "domain"),
            "cross_cutting": sum(1 for c in chosen if c.selected_by == CROSS_CUTTING),
            "relevance": sum(1 for c in chosen if c.selected_by == "relevance"),
        },
        "pages": [
            {"page_name": c.page.name, "selected_by": c.selected_by, "score": round(c.score, 4)}
            for c in chosen
        ],
    }
    return chosen, trace
