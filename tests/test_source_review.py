from pathlib import Path
import json
import pytest
from wiki_api.source_review import corpus_snapshot, source_review_status, rule_inventory_status, wiki_rule_definitions

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def reviewed(tmp_path):
    (tmp_path/'docs').mkdir()
    (tmp_path/'chemmon_docs').mkdir()
    (tmp_path/'wiki/chemmon-guidance').mkdir(parents=True)
    (tmp_path/'chemmon_docs/source.pdf').write_bytes(b'original source')
    (tmp_path/'wiki/chemmon-guidance/topic.md').write_text('# Original topic')
    (tmp_path/'index.md').write_text('# Original index')
    record = {'version': 1, 'reviewed_at': '2026-01-01', 'reviewer': 'Test', 'scope': ['One section'],
              'limitations': ['Not exhaustive'], 'snapshot': corpus_snapshot(tmp_path),
              'findings': [{'id': 'test', 'status': 'open', 'source': 'chemmon_docs/source.pdf', 'locator': 'p.1',
                            'observation': 'Missing exception', 'action': 'Review exception', 'wiki_pages': ['topic.md']}]}
    (tmp_path/'docs/source-review.json').write_text(json.dumps(record))
    return tmp_path


def test_review_current_does_not_hide_open_findings(reviewed):
    status = source_review_status(reviewed)
    assert status['status'] == 'current'
    assert status['open_findings'][0]['id'] == 'test'


@pytest.mark.parametrize('change', ['source', 'topic', 'index', 'add', 'remove'])
def test_review_detects_corpus_drift_and_retains_findings(reviewed, change):
    path = {'source': 'chemmon_docs/source.pdf', 'topic': 'wiki/chemmon-guidance/topic.md',
            'index': 'index.md', 'add': 'wiki/chemmon-guidance/new.md', 'remove': 'wiki/chemmon-guidance/topic.md'}[change]
    if change == 'remove':
        (reviewed/path).unlink()
    else:
        (reviewed/path).write_bytes(b'changed')
    status = source_review_status(reviewed)
    assert status['status'] == 'stale'
    assert path in status['changed_paths']
    assert status['open_findings']


@pytest.mark.parametrize('fault', ['hash', 'path', 'resolution', 'duplicate', 'source', 'date', 'scope'])
def test_malformed_review_cannot_look_current(reviewed, fault):
    path = reviewed/'docs/source-review.json'
    record = json.loads(path.read_text())
    if fault == 'hash': record['snapshot']['index.md'] = 'not-a-hash'
    if fault == 'path': record['snapshot']['../escape'] = 'a'*64
    if fault == 'resolution': record['findings'][0]['status'] = 'resolved'
    if fault == 'duplicate': record['findings'].append(record['findings'][0])
    if fault == 'source': record['findings'][0]['source'] = 'missing.pdf'
    if fault == 'date': record['reviewed_at'] = '2999-01-01'
    if fault == 'scope': record['scope'] = []
    path.write_text(json.dumps(record))
    assert source_review_status(reviewed)['status'] == 'invalid'


def test_rule_inventory_is_source_derived_and_explicit_about_inactive_rules():
    record = json.loads((ROOT/'docs/rule-inventory.json').read_text())
    assert record['source_counts'] == {'GBR':92, 'CHEMMON':104, 'LL':11, 'PRE':17, 'USE':29}
    rules = {r['wiki_id']: r for r in record['rules']}
    assert rules['CHEMMON84_a']['source_id'] == 'CHEMON84_a'
    assert rules['LL_01_FA_FF']['pdf_page'] == 142
    assert rules['LL_04_b']['pdf_page'] == 143
    assert rules['GBR1']['status'] == 'inactive'
    assert rules['CHEMMON49']['status'] == 'inactive'
    assert rules['GBR6']['applicability'] == 'biological-only'
    result = rule_inventory_status(ROOT)
    assert result['status'] == 'current'
    assert result['missing_active_ids'] == []
    assert 'GBR1' not in result['missing_active_ids']
    assert 'GBR6' not in result['missing_active_ids']
    assert result['unexpected_wiki_ids'] == result['inactive_wiki_ids'] == []


def test_all_applicable_gbr_source_ids_have_one_canonical_definition():
    """Compare the wiki to the independently extracted PDF inventory."""
    record = json.loads((ROOT/'docs/rule-inventory.json').read_text())
    expected = {r['wiki_id'] for r in record['rules']
                if r['family'] == 'GBR' and r['status'] == 'active'
                and r['applicability'] != 'biological-only'}
    definitions = {key: pages for key, pages in wiki_rule_definitions(ROOT).items()
                   if key.startswith('GBR')}
    assert len(expected) == 83
    assert definitions.keys() == expected
    assert all(len(pages) == 1 for pages in definitions.values())


def test_rule_inventory_refuses_stale_pdf(reviewed):
    record = json.loads((ROOT/'docs/rule-inventory.json').read_text())
    (reviewed/'docs/rule-inventory.json').write_text(json.dumps(record))
    result = rule_inventory_status(reviewed)
    assert result['status'] == 'stale'
    assert 'missing_active_ids' not in result


def test_canonical_rule_extraction_excludes_annual_change_notes(tmp_path):
    d=tmp_path/'wiki/chemmon-guidance'; d.mkdir(parents=True)
    (d/'business-rules-gbr.md').write_text('| GBR1 | Error | definition |\n')
    (d/'business-rules-2026-changes.md').write_text('| GBR1 | Removed |\n')
    assert wiki_rule_definitions(tmp_path) == {'GBR1': ['business-rules-gbr.md']}


def test_supporting_catalogue_report_drift_invalidates_review(reviewed):
    from wiki_api.source_review import sha256
    evidence=reviewed/'docs/catalogue-check.json';evidence.write_text('{"rows":[]}')
    path=reviewed/'docs/source-review.json';record=json.loads(path.read_text())
    record['supporting_artifacts']={'docs/catalogue-check.json':sha256(evidence)}
    path.write_text(json.dumps(record))
    assert source_review_status(reviewed)['status']=='current'
    evidence.write_text('{"rows":["changed"]}')
    assert source_review_status(reviewed)['status']=='stale'


def test_reviewed_chemon_pre_use_severities_match_independent_source_evidence():
    """Guard against losing a rule or promoting a Warning during later edits."""
    import re
    from wiki_api.source_review import sha256
    report = json.loads((ROOT/'reports/source-review/2026-10-05-broader-review.json').read_text())
    inventory = json.loads((ROOT/'docs/rule-inventory.json').read_text())
    expected = {r['wiki_id']: r for r in inventory['rules']
                if r['family'] in {'CHEMMON', 'PRE', 'USE'}}
    reviewed_rows = {r['wiki_id']: r for r in report['rules']}
    assert len(reviewed_rows) == len(report['rules']) == 150
    assert reviewed_rows.keys() == expected.keys()
    assert all(sha256(ROOT/p) == digest for p, digest in report['sources'].items())
    definitions = wiki_rule_definitions(ROOT)
    for key, source in reviewed_rows.items():
        assert source['status'] == expected[key]['status']
        assert source['pdf_page'] == expected[key]['pdf_page']
        if source['status'] == 'inactive':
            assert key not in definitions
            continue
        assert definitions[key] == [source['canonical_page']]
        text = (ROOT/'wiki/chemmon-guidance'/source['canonical_page']).read_text()
        row = next(line for line in text.splitlines()
                   if re.match(r'^\|\s*' + re.escape(key) + r'\s*\|', line))
        cells = [cell.strip() for cell in row.split('|')[1:-1]]
        assert len(cells) == (5 if source['family'] == 'CHEMMON' else 4)
        assert cells[1] == source['severity'], key
        assert int(re.split(r'[-–]', cells[-1])[0]) == source['pdf_page'], key


def test_reviewed_parallel_field_inventory_has_no_omitted_names():
    """Coverage guard only; field meanings were compared with the full PDFs."""
    report = json.loads((ROOT/'reports/source-review/2026-10-05-broader-review.json').read_text())
    for model, count, page in [('PRE', 18, 'fa-ff-no-presence-data-model.md'),
                                ('USE', 31, 'fa-ff-use-levels-data-model.md')]:
        fields = [f for f in report['fields'] if f['model'] == model]
        assert len(fields) == len({f['name'] for f in fields}) == count
        text = (ROOT/'wiki/chemmon-guidance'/page).read_text()
        assert all('`' + field['name'] + '`' in text for field in fields)
