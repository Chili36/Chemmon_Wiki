"""Fingerprint-scoped review records; structural checks never certify meaning."""
from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from datetime import date
from pathlib import Path

AUDIT_PATH = Path('docs/source-review.json')
INVENTORY_PATH = Path('docs/rule-inventory.json')


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def corpus_snapshot(root: Path) -> dict[str, str]:
    paths = sorted((root / 'chemmon_docs').glob('*.pdf'))
    paths += sorted(p for p in (root / 'chemmon_docs/datasets').rglob('*') if p.is_file())
    paths += sorted((root / 'wiki/chemmon-guidance').glob('*.md'))
    paths += [root / 'index.md']
    return {p.relative_to(root).as_posix(): sha256(p) for p in paths if p.is_file()}


def _read_record(root: Path, path: Path) -> dict:
    record = json.loads((root / path).read_text())
    if not isinstance(record, dict) or record.get('version') != 1:
        raise ValueError('unsupported review record')
    return record


def _validate_snapshot(snapshot: dict) -> None:
    if not isinstance(snapshot, dict) or not snapshot:
        raise ValueError('snapshot is missing')
    for name, digest in snapshot.items():
        if (not isinstance(name, str) or Path(name).is_absolute() or '..' in Path(name).parts
                or not isinstance(digest, str) or not re.fullmatch(r'[0-9a-f]{64}', digest)):
            raise ValueError('invalid snapshot path or hash')


def source_review_status(root: Path) -> dict:
    """Return current/stale/invalid/missing and retain open findings even on drift."""
    try:
        record = _read_record(root, AUDIT_PATH)
        _validate_snapshot(record.get('snapshot'))
        reviewed = date.fromisoformat(record['reviewed_at'])
        if reviewed > date.today():
            raise ValueError('review date is in the future')
        for key in ('reviewer', 'scope', 'limitations'):
            if not record.get(key):
                raise ValueError(f'missing {key}')
        findings = record.get('findings')
        if not isinstance(findings, list):
            raise ValueError('findings must be an array')
        seen = set()
        for finding in findings:
            if not isinstance(finding, dict):
                raise ValueError('invalid finding')
            for key in ('id', 'status', 'source', 'locator', 'observation', 'action', 'wiki_pages'):
                if not finding.get(key):
                    raise ValueError(f'finding missing {key}')
            if finding['id'] in seen or finding['status'] not in {'open', 'resolved'}:
                raise ValueError('duplicate finding or invalid status')
            seen.add(finding['id'])
            if finding['source'] not in record['snapshot']:
                raise ValueError('finding source outside snapshot')
            if not isinstance(finding['wiki_pages'], list) or any(
                'wiki/chemmon-guidance/' + p not in record['snapshot'] for p in finding['wiki_pages']
            ):
                raise ValueError('finding page outside snapshot')
            if finding['status'] == 'resolved' and not finding.get('resolution'):
                raise ValueError('resolved finding needs resolution')
        current = corpus_snapshot(root)
        supporting = record.get('supporting_artifacts', {})
        if supporting:
            _validate_snapshot(supporting)
            for name in supporting:
                if (root / name).is_file():
                    current[name] = sha256(root / name)
            record['snapshot'] = {**record['snapshot'], **supporting}
        changed = sorted(p for p in set(current) | set(record['snapshot'])
                         if current.get(p) != record['snapshot'].get(p))
        return {'status': 'stale' if changed else 'current', 'reviewed_at': record['reviewed_at'],
                'reviewer': record['reviewer'], 'scope': record['scope'],
                'limitations': record['limitations'], 'changed_paths': changed,
                'open_findings': [f for f in findings if f['status'] == 'open'],
                'resolved_count': sum(f['status'] == 'resolved' for f in findings)}
    except FileNotFoundError:
        return {'status': 'missing', 'open_findings': []}
    except (ValueError, KeyError, TypeError, OSError) as exc:
        return {'status': 'invalid', 'error': str(exc), 'open_findings': []}


def normalize_rule_id(raw: str) -> str:
    return re.sub(r'\s+', '', raw).replace('CHEMON', 'CHEMMON')


def wiki_rule_definitions(root: Path) -> dict[str, list[str]]:
    definitions: dict[str, list[str]] = {}
    for p in sorted((root / 'wiki/chemmon-guidance').glob('*.md')):
        if not (p.name.startswith('business-rules-') and p.name != 'business-rules-2026-changes.md'
                or p.name in {'fa-ff-no-presence-data-model.md', 'fa-ff-use-levels-data-model.md'}):
            continue
        for raw in re.findall(r'^\|\s*([^|]+?)\s*\|', p.read_text(), re.M):
            raw = raw.replace('`', '').strip()
            if re.fullmatch(r'(?:CHEMMON|GBR|LL_|PRE|USE)\w+(?:/\w+)*', raw):
                # Old merged IDs are intentionally not rewritten: they must be flagged.
                definitions.setdefault(normalize_rule_id(raw), []).append(p.name)
    return definitions


def rule_inventory_status(root: Path) -> dict:
    try:
        record = _read_record(root, INVENTORY_PATH)
        _validate_snapshot(record.get('sources'))
        rows = record['rules']
        if not isinstance(rows, list) or not rows:
            raise ValueError('empty rule inventory')
        expected = {}
        for row in rows:
            if not isinstance(row, dict) or row.get('source') not in record['sources']:
                raise ValueError('invalid rule source')
            if not isinstance(row.get('pdf_page'), int) or row['pdf_page'] < 1:
                raise ValueError('invalid rule locator')
            if row.get('status') not in {'active', 'inactive'} or row.get('family') not in {'GBR', 'CHEMMON', 'LL', 'PRE', 'USE'}:
                raise ValueError('invalid rule status/family')
            key = row['wiki_id']
            if key in expected:
                raise ValueError(f'duplicate source rule {key}')
            expected[key] = row
        changed = [p for p, digest in record['sources'].items()
                   if not (root / p).is_file() or sha256(root / p) != digest]
        if changed:
            return {'status': 'stale', 'changed_paths': changed}
        definitions = wiki_rule_definitions(root)
        active = {key for key, r in expected.items() if r['status'] == 'active' and r.get('applicability') != 'biological-only'}
        return {'status': 'current', 'source_counts': dict(Counter(r['family'] for r in rows)),
                'missing_active_ids': sorted(active - definitions.keys()),
                'unexpected_wiki_ids': sorted(definitions.keys() - expected.keys()),
                'duplicate_wiki_ids': {k: v for k, v in definitions.items() if len(v) > 1},
                'inactive_wiki_ids': sorted(k for k in definitions if k in expected and expected[k]['status'] == 'inactive'),
                'limitation': 'ID coverage only; matching IDs do not validate descriptions, scope or severity.'}
    except FileNotFoundError:
        return {'status': 'missing'}
    except (ValueError, KeyError, TypeError, OSError) as exc:
        return {'status': 'invalid', 'error': str(exc)}
