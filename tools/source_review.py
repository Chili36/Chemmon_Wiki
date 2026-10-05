#!/usr/bin/env python3
"""Prepare immutable-source review material, or inspect saved review status."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from wiki_api.source_review import corpus_snapshot, source_review_status, rule_inventory_status


def prepare(root: Path, output: Path) -> None:
    output = output.resolve()
    if output == root.resolve() or any(output.is_relative_to(root / d) for d in ('wiki', 'chemmon_docs', 'docs')):
        raise ValueError('use a new review directory outside authored content')
    output.mkdir(parents=True, exist_ok=False)
    sources = sorted((root / 'chemmon_docs').glob('*.pdf'))
    mapping = []
    for n, source in enumerate(sources, 1):
        text = subprocess.run(['pdftotext', '-layout', str(source), '-'], check=True, capture_output=True, text=True).stdout
        pages = text.split('\f')
        if not pages[-1].strip():
            pages.pop()
        name = f'source-{n}.txt'
        (output / name).write_text('\n'.join(f'=== PDF PAGE {i} ===\n{p}' for i, p in enumerate(pages, 1)))
        mapping.append({'source': source.relative_to(root).as_posix(), 'extracted': name,
                        'pages': len(pages), 'sparse_pages': [i for i, p in enumerate(pages, 1) if len(p.split()) < 20]})
    (output / 'preparation.json').write_text(json.dumps({'snapshot': corpus_snapshot(root), 'sources': mapping,
        'notice': 'Extraction only. No semantic review or completeness verdict.'}, indent=2) + '\n')


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--prepare', type=Path, help='new output directory; requires pdftotext')
    args = parser.parse_args()
    if args.prepare:
        prepare(ROOT, args.prepare)
        print(f'Review material prepared in {args.prepare}')
        return 0
    status = {'review': source_review_status(ROOT), 'rules': rule_inventory_status(ROOT)}
    print(json.dumps(status, indent=2, ensure_ascii=False))
    return int(any(s['status'] != 'current' for s in status.values()))

if __name__ == '__main__':
    sys.exit(main())
