"""Shared full-page evidence contract for answers, exports and evaluations."""
from __future__ import annotations
import hashlib
from pathlib import Path
from .page_excerpt import BY_FOOD_PAGE, excerpt
from .wiki_store import WikiStore


def selected_names(store: WikiStore, names: list[str], limit: int) -> list[str]:
    allowed = set(store.list_pages())
    return list(dict.fromkeys(store.normalize_page_name(n) for n in names
        if store.normalize_page_name(n) in allowed))[:limit]


def full_evidence(store: WikiStore, name: str, question: str | None = None) -> dict:
    """A page as answer evidence. With a question, the by-food list page is trimmed to the
    pesticides the question names (page_excerpt); every other page is sent whole."""
    page = store.read_page(name)
    content = store.clean_content_for_model(page)
    trimmed = excerpt(content, question) if question and page.name == BY_FOOD_PAGE else None
    return {'page_name': page.name, 'title': page.title, 'summary': page.summary,
            'domain': page.domain, 'content': trimmed or content,
            'sources': page.sources, 'source_pages': list(page.source_pages),
            # Still full evidence for the answerer: only irrelevant list entries were left out.
            'evidence_kind': 'full', 'excerpt': bool(trimmed), 'citable': True,
            'sha256': hashlib.sha256(page.content.encode()).hexdigest(),
            'last_updated': page.last_updated}


def bounded_pack(store: WikiStore, names: list[str], max_pages: int, max_chars: int,
                 question: str | None = None) -> dict:
    """Policy takes one page slot; whole evidence pages are never truncated."""
    policy = (store.root / 'RUNTIME_POLICY.md').read_text()
    if len(policy) > max_chars:
        raise ValueError('character budget cannot hold the runtime policy')
    pages = [{'page_name': 'RUNTIME_POLICY.md', 'title': 'ChemMon evidence policy',
              'content': policy, 'evidence_kind': 'policy', 'citable': False,
              'sources': [], 'source_pages': [],
              'sha256': hashlib.sha256(policy.encode()).hexdigest()}]
    chars = len(policy)
    omitted = []
    for name in selected_names(store, names, 10):
        page = full_evidence(store, name, question=question)
        if len(pages) >= max_pages or chars + len(page['content']) > max_chars:
            omitted.append({'page_name': name, 'reason': 'page_budget' if len(pages) >= max_pages else 'character_budget'})
            continue
        pages.append(page)
        chars += len(page['content'])
    evidence = [p['page_name'] for p in pages if p['citable']]
    return {'pages': pages, 'pages_used': [p['page_name'] for p in pages],
            'citable_pages': evidence, 'omitted_pages': omitted,
            'status': ('evidence_available' if evidence else 'budget_exhausted' if omitted or max_pages == 1 else 'no_evidence'),
            'budget': {'max_pages': max_pages, 'max_chars': max_chars, 'used_pages': len(pages),
                       'used_chars': chars, 'character_scope': 'page content, including policy; metadata excluded'}}
