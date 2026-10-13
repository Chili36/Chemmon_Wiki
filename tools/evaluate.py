#!/usr/bin/env python3
"""Reproducible selection / frozen-evidence answer comparisons. Offline by default."""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import statistics
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from wiki_api.wiki_store import WikiStore
from wiki_api.source_review import corpus_snapshot, sha256
from wiki_api.evidence import full_evidence, selected_names
from wiki_api.page_selector import WikiPageSelector, SELECTION_SYSTEM_PROMPT
from wiki_api.answerer import WikiAnswerer, ANSWERER_SYSTEM_PROMPT


def validate_cases(dataset: dict, store: WikiStore) -> list[dict]:
    if dataset.get('version') != 1 or not isinstance(dataset.get('cases'), list) or not dataset['cases']:
        raise ValueError('expected a version 1 case dataset')
    seen = set()
    for case in dataset['cases']:
        if case['id'] in seen:
            raise ValueError('duplicate case ID')
        seen.add(case['id'])
        if not case.get('question', '').strip() or case.get('split') not in {'development', 'held-out'}:
            raise ValueError('case needs question and split')
        if not 1 <= case.get('max_pages', 6) <= 10:
            raise ValueError('invalid case page budget')
        if case.get('review_status') not in {'draft', 'human-reviewed'}:
            raise ValueError('case needs review_status')
        if case['review_status'] == 'human-reviewed' and not case.get('reviewer'):
            raise ValueError('human-reviewed case needs reviewer')
        if not case.get('rubric') or not isinstance(case.get('expected_page_groups'), list):
            raise ValueError('case needs rubric and required-page groups')
        groups = case['expected_page_groups']
        if any(not isinstance(g, list) or not g for g in groups):
            raise ValueError('expected-page alternatives cannot be empty')
        for name in [n for g in groups for n in g] + case.get('evidence_pages', []) + case.get('forbidden_pages', []):
            if name not in store.list_pages():
                raise ValueError(f'unknown topic {name}')
        if not isinstance(case.get('evidence_pages'), list) or len(case['evidence_pages']) > case.get('max_pages', 6):
            raise ValueError('frozen evidence exceeds page budget')
    return dataset['cases']


def selection_metrics(case: dict, pages: list[dict]) -> dict:
    names = {p['page_name'] for p in pages}
    groups = case['expected_page_groups']
    hits = sum(bool(names.intersection(group)) for group in groups)
    wrong = [p['page_name'] for p in pages if p.get('domain') in case.get('forbidden_domains', [])
             or p['page_name'] in case.get('forbidden_pages', [])]
    return {'required_page_recall': hits / len(groups) if groups else None,
            'empty_selection_correct': not names if case.get('expect_empty_selection') else None,
            'wrong_domain_or_path_count': len(wrong), 'wrong_domain_or_path_pages': wrong}


def grade_metrics(case: dict, result: dict, grades: dict | None = None) -> dict:
    allowed = {p['page_name'] for p in result.get('evidence', []) if p['evidence_kind'] == 'full'}
    citations = result.get('citations', [])
    valid = sum(c in allowed for c in citations)
    grade = (grades or {}).get(case['id'])
    if grade:
        if not grade.get('reviewer') or not grade.get('reviewed_at'):
            raise ValueError('answer grades require reviewer and date')
        if any(type(grade.get(k)) is not bool for k in ('answer_correct', 'citations_supported')):
            raise ValueError('grades require boolean correctness and citation support')
    return {'citation_membership_precision': valid / len(citations) if citations else None,
            'invalid_citations': [c for c in citations if c not in allowed],
            # Membership is mechanical. Support and correctness require claim-level review.
            'answer_correct': grade['answer_correct'] if grade else None,
            'citations_supported': grade['citations_supported'] if grade else None,
            'grade_reviewer': grade['reviewer'] if grade else None}


def estimated_cost(usage: dict, prices: dict, model: str) -> float | None:
    if usage.get('calls') == 0:
        return 0.0
    rate = prices.get(model)
    if rate is None:
        return None
    return round((usage.get('input_tokens', 0) * rate['input_per_million'] +
                  usage.get('output_tokens', 0) * rate['output_per_million']) / 1e6, 8)


def run_suite(store: WikiStore, dataset: dict, *, mode: str, models: list[str], live: bool = False,
              split: str = 'development', catalog_mode: str = 'hints', prices: dict | None = None,
              selector_factory=WikiPageSelector, answerer_factory=WikiAnswerer) -> dict:
    cases = [c for c in validate_cases(dataset, store) if c['split'] == split]
    if not cases:
        raise ValueError('no cases in requested split')
    frozen = corpus_snapshot(store.root)
    catalog = store.selector_catalog(use_hints=catalog_mode == 'hints')
    prompt = SELECTION_SYSTEM_PROMPT if mode == 'select' else ANSWERER_SYSTEM_PROMPT
    report = {'version': 1, 'created_at': datetime.now(timezone.utc).isoformat(),
              'mode': mode, 'execution': 'live' if live else 'dry-run', 'split': split,
              'label_status': 'human-reviewed' if all(c['review_status'] == 'human-reviewed' for c in cases) else 'draft',
              'settings': {'models': models, 'catalog_mode': catalog_mode, 'answer_max_tokens': 2000,
                           'graph_expansion': False, 'temperature': 'provider default', 'pricing': prices or {}},
              'corpus_snapshot': frozen, 'prompt_sha256': hashlib.sha256(prompt.encode()).hexdigest(),
              'catalog_sha256': hashlib.sha256(catalog.encode()).hexdigest(),
              'dataset_sha256': hashlib.sha256(json.dumps(dataset, sort_keys=True).encode()).hexdigest(),
              'limitations': ['Draft labels are exploratory, not a human-reviewed quality baseline.',
                             'Citation membership is not claim support. Correctness and support require human grades.',
                             'Provider-default sampling is recorded; repeated runs may differ.',
                             'Model comparison must hold corpus, questions, prompts and budgets fixed.'],
              'results': []}
    # Snapshot exact evidence once so every answer model receives identical content.
    evidence = {c['id']: [full_evidence(store, n) for n in c['evidence_pages']] for c in cases}
    for model in models:
        runner, initialization_error = None, None
        if live:
            try:
                runner = selector_factory(store=store, model_str=model, use_hints=catalog_mode == 'hints') if mode == 'select' else answerer_factory(model_str=model, max_tokens=2000)
            except Exception as exc:
                initialization_error = type(exc).__name__
        for case in cases:
            entry = {'case_id': case['id'], 'model': model, 'question': case['question'],
                     'max_pages': case.get('max_pages', 6), 'review_status': case['review_status'],
                     'rubric': case['rubric'], 'status': 'planned', 'metrics': {}}
            if mode == 'answer':
                entry['evidence'] = evidence[case['id']]
                entry['evidence_sha256'] = hashlib.sha256(json.dumps(entry['evidence'], sort_keys=True).encode()).hexdigest()
            if live:
                start = time.perf_counter()
                try:
                    if initialization_error:
                        entry.update({'status': 'error', 'error_type': initialization_error, 'phase': 'provider_initialization', 'wall_time_ms': 0})
                        report['results'].append(entry)
                        continue
                    if mode == 'select':
                        r = runner.run({'question': case['question'], 'max_pages': entry['max_pages']})
                        names = selected_names(store, r.pages_used, entry['max_pages'])
                        pages = [full_evidence(store, n) for n in names]
                        entry.update({'pages_used': names, 'metrics': selection_metrics(case, pages)})
                    else:
                        r = runner.run(case['question'], entry['evidence'])
                        entry.update({'answer': r.answer, 'citations': r.citations})
                        entry['metrics'] = grade_metrics(case, entry)
                    entry.update({'status': 'completed', 'usage': r.token_summary,
                                  'estimated_cost_usd': estimated_cost(r.token_summary, prices or {}, model)})
                except Exception as exc:
                    # Exception messages can contain request/provider details; retain only type.
                    entry.update({'status': 'error', 'error_type': type(exc).__name__})
                entry['wall_time_ms'] = int((time.perf_counter() - start) * 1000)
            report['results'].append(entry)
    if corpus_snapshot(store.root) != frozen:
        raise ValueError('corpus changed during evaluation; discard this run and retry on a frozen checkout')
    report['summary'] = summarize(report['results'])
    return report


def summarize(results: list[dict]) -> dict:
    summary = {}
    for model in dict.fromkeys(r['model'] for r in results):
        rows = [r for r in results if r['model'] == model]
        done = [r for r in rows if r['status'] == 'completed']
        def average(key):
            values = [r.get('metrics', {}).get(key) for r in done if r.get('metrics', {}).get(key) is not None]
            return statistics.mean(values) if values else None
        costs = [r.get('estimated_cost_usd') for r in done]
        summary[model] = {'cases': len(rows), 'completed': len(done), 'errors': sum(r['status'] == 'error' for r in rows),
                          'mean_required_page_recall': average('required_page_recall'),
                          'wrong_domain_or_path_cases': sum(bool(r.get('metrics', {}).get('wrong_domain_or_path_count')) for r in done) if any('wrong_domain_or_path_count' in r.get('metrics', {}) for r in done) else None,
                          'answer_accuracy': average('answer_correct'), 'citation_support_rate': average('citations_supported'),
                          'graded_answers': sum(r.get('metrics', {}).get('answer_correct') is not None for r in done),
                          'mean_wall_time_ms': statistics.mean(r['wall_time_ms'] for r in done) if done else None,
                          'estimated_total_cost_usd': sum(costs) if costs and len(done) == len(rows) and all(c is not None for c in costs) else None}
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cases', type=Path, default=ROOT/'evals/cases.json')
    parser.add_argument('--mode', choices=['select', 'answer'], default='select')
    parser.add_argument('--models', nargs='+', default=['openai/gpt-5.4-mini'])
    parser.add_argument('--split', choices=['development', 'held-out'], default='development')
    parser.add_argument('--catalog-mode', choices=['hints', 'summary'], default='hints')
    parser.add_argument('--live', action='store_true', help='explicitly enable paid model calls')
    parser.add_argument('--env-file', type=Path, help='load credentials for live runs only; never copied to reports')
    parser.add_argument('--prices', type=Path, help='optional dated pricing JSON; omitted prices are unknown, not free')
    parser.add_argument('--output', type=Path, required=True, help='new JSON report file')
    parser.add_argument('--grade-report', type=Path, help='grade an existing answer report offline')
    parser.add_argument('--grades', type=Path, help='JSON with report_sha256 and case-keyed human grades')
    args = parser.parse_args()
    if args.output.exists():
        parser.error('output exists; use a new report path to preserve comparisons')
    dataset = json.loads(args.cases.read_text())
    store = WikiStore(ROOT)
    validate_cases(dataset, store)
    if args.grade_report:
        if not args.grades or args.live:
            parser.error('grading requires --grades and is offline')
        report = json.loads(args.grade_report.read_text())
        grades = json.loads(args.grades.read_text())
        if grades.get('report_sha256') != sha256(args.grade_report):
            parser.error('grades do not match the exact saved report')
        case_map = {c['id']: c for c in dataset['cases']}
        if report['dataset_sha256'] != hashlib.sha256(json.dumps(dataset, sort_keys=True).encode()).hexdigest():
            parser.error('dataset differs from the saved report')
        for row in report['results']:
            if row['status'] == 'completed' and 'answer' in row:
                row['metrics'].update(grade_metrics(case_map[row['case_id']], row, grades.get('models', {}).get(row['model'], {})))
        report['summary'] = summarize(report['results'])
        report['graded_from_sha256'] = sha256(args.grade_report)
    else:
        if args.live and args.env_file:
            from dotenv import load_dotenv
            load_dotenv(args.env_file, override=False)
        prices = json.loads(args.prices.read_text())['models'] if args.prices else {}
        report = run_suite(store, dataset, mode=args.mode, models=args.models, live=args.live,
                           split=args.split, catalog_mode=args.catalog_mode, prices=prices)
        if args.prices:
            report['pricing_file_sha256'] = sha256(args.prices)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open('x') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
        f.write('\n')
    print(json.dumps({'execution': report['execution'], 'label_status': report['label_status'], 'summary': report['summary']}, indent=2))
    return int(any(r['status'] == 'error' for r in report['results']))

if __name__ == '__main__':
    sys.exit(main())
