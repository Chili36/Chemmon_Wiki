"""Shared full-page evidence contract for answers, exports and evaluations."""
from __future__ import annotations
import hashlib
from pathlib import Path
from .wiki_store import WikiStore


def selected_names(store: WikiStore, names: list[str], limit: int) -> list[str]:
    allowed = set(store.list_pages())
    return list(dict.fromkeys(store.normalize_page_name(n) for n in names
        if store.normalize_page_name(n) in allowed))[:limit]


def full_evidence(store: WikiStore, name: str) -> dict:
    page = store.read_page(name)
    return {'page_name': page.name, 'title': page.title, 'summary': page.summary,
            'domain': page.domain, 'content': store.clean_content_for_model(page),
            'sources': page.sources, 'source_pages': list(page.source_pages),
            'evidence_kind': 'full', 'citable': True,
            'sha256': hashlib.sha256(page.content.encode()).hexdigest(),
            'last_updated': page.last_updated}


def bounded_pack(store: WikiStore, names: list[str], max_pages: int, max_chars: int,
                 extra: dict | None = None) -> dict:
    """Policy takes one page slot; whole evidence pages are never truncated. `extra` (the residue
    lookup for pesticides the question names) comes first after the policy and replaces the
    static page of the same name."""
    policy = (store.root / 'RUNTIME_POLICY.md').read_text()
    if len(policy) > max_chars:
        raise ValueError('character budget cannot hold the runtime policy')
    pages = [{'page_name': 'RUNTIME_POLICY.md', 'title': 'ChemMon evidence policy',
              'content': policy, 'evidence_kind': 'policy', 'citable': False,
              'sources': [], 'source_pages': [],
              'sha256': hashlib.sha256(policy.encode()).hexdigest()}]
    chars = len(policy)
    omitted = []
    candidates = [extra] if extra else []
    candidates += [n for n in selected_names(store, names, 10) if not extra or n != extra['page_name']]
    for item in candidates:
        page = item if isinstance(item, dict) else full_evidence(store, item)
        name = page['page_name']
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
