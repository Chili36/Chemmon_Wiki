#!/usr/bin/env python3
"""Extract rule IDs from the fixed 2026 source tables, independently of wiki text.

Writes a candidate to a NEW file. Review the PDF columns and edition before
adopting it as docs/rule-inventory.json. Does not evaluate rule descriptions.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from wiki_api.source_review import sha256, normalize_rule_id

# Physical PDF pages, first-column width, known namespace, source filename pattern.
TABLES = [
    ('*Chemical monitoring*.pdf', 98, 112, 16, 'GBR'),
    ('*Chemical monitoring*.pdf', 113, 143, 21, 'CHEMMON'),
    ('*No*presence*.pdf', 19, 21, 21, 'PRE'),
    ('*use levels*.pdf', 24, 28, 33, 'USE'),
]
BIOLOGICAL_ONLY = {'GBR6', 'GBR60', 'GBR69', 'GBR77', 'GBR85', 'GBR93', 'GBR99'}


def extract_inventory(root: Path) -> dict:
    rules, sources, cache = [], {}, {}
    for pattern, first, last, width, family in TABLES:
        matches = list((root / 'chemmon_docs').glob(pattern))
        if len(matches) != 1:
            raise ValueError(f'expected one source matching {pattern}')
        path = matches[0]
        name = path.relative_to(root).as_posix()
        sources[name] = sha256(path)
        if name not in cache:
            cache[name] = subprocess.run(['pdftotext', '-layout', str(path), '-'], check=True,
                                          capture_output=True, text=True).stdout.split('\f')
        last_status = None
        for page in range(first, last + 1):
            lines = cache[name][page - 1].splitlines()
            for i, line in enumerate(lines):
                token = line[:width].strip()
                if not re.match(r'^(?:GBR\d|CHEMON\d|LL_\d|PRE\d|USE(?:\d|_LLDB))', token):
                    continue
                # Layout wraps suffixes (CHEMON84_ / a, LL_01_FA_F / F, LL_04/LL_0 / 4_b).
                j = i + 1
                while j < len(lines):
                    suffix = lines[j][:width].strip()
                    if re.fullmatch(r'(?:[a-z]|F|4_b)', suffix):
                        token += suffix
                        j += 1
                    else:
                        break
                status_match = re.search(r'\b(inactiv\w*|active)\b', line[width:], re.I)
                status = ('inactive' if status_match[1].lower().startswith('inactiv') else 'active') if status_match else last_status
                if status is None:
                    raise ValueError(f'cannot extract status for {token}, page {page}')
                last_status = status
                for source_id in token.split('/'):
                    wiki_id = normalize_rule_id(source_id)
                    rules.append({'source_id': source_id, 'wiki_id': wiki_id,
                        'family': 'LL' if source_id.startswith('LL_') else family,
                        'source': name, 'pdf_page': page, 'status': status,
                        'applicability': 'biological-only' if wiki_id in BIOLOGICAL_ONLY else 'check-rule-scope'})
    # These are source-table counts, not counts learned from existing wiki definitions.
    counts = {family: sum(r['family'] == family for r in rules) for family in ('GBR','CHEMMON','LL','PRE','USE')}
    return {'version': 1, 'edition': '2026 supplied PDFs', 'method': 'pdftotext -layout, first-column IDs in Tables 9/10 and FA/FF Table 3; wrapped suffixes joined; CHEMON mapped to wiki CHEMMON',
            'limitations': ['ID/status inventory only. Descriptions and applicability still need semantic review.',
                'Inactive and explicitly biological-only GBR rows retained but excluded from missing-active warnings.',
                'DOMAIN VALIDATION and FOODEX2 namespaces are outside this five-family inventory.'],
            'source_counts': counts, 'sources': sources, 'rules': rules}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    record = extract_inventory(ROOT)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open('x') as f:
        json.dump(record, f, indent=2, ensure_ascii=False)
        f.write('\n')
    print(json.dumps(record['source_counts']))

if __name__ == '__main__':
    main()
