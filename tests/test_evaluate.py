from pathlib import Path
from types import SimpleNamespace
import copy
import json
import pytest
from tools.evaluate import run_suite, validate_cases, selection_metrics, grade_metrics, estimated_cost
from wiki_api.wiki_store import WikiStore

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def suite():
    return {'version': 1, 'cases': [{'id':'case', 'question':'What does GBR28 require?', 'split':'development',
        'max_pages':2, 'review_status':'draft', 'rubric':['Require resQualValue for BIN'],
        'expected_page_groups':[['business-rules-gbr.md','ssd2-result-units-and-limits.md']],
        'evidence_pages':['business-rules-gbr.md'], 'forbidden_domains':['vmpr'], 'forbidden_pages':[]}]}


def test_dry_run_never_initializes_provider(suite):
    def fail(**kwargs): raise AssertionError('provider initialized during dry run')
    report=run_suite(WikiStore(ROOT),suite,mode='select',models=['test/one'],selector_factory=fail)
    assert report['execution']=='dry-run'
    assert report['label_status']=='draft'
    assert report['results'][0]['status']=='planned'
    assert report['summary']['test/one']['mean_required_page_recall'] is None
    assert report['summary']['test/one']['estimated_total_cost_usd'] is None


def test_answer_models_receive_identical_frozen_evidence(suite):
    calls=[]
    class Answerer:
        def __init__(self, **kwargs): self.model=kwargs['model_str']
        def run(self, question, pages):
            calls.append((self.model,copy.deepcopy(pages)))
            return SimpleNamespace(answer='resQualValue is required for BIN.',citations=['business-rules-gbr.md'],
                token_summary={'calls':1,'input_tokens':100,'output_tokens':20})
    report=run_suite(WikiStore(ROOT),suite,mode='answer',models=['test/one','test/two'],live=True,answerer_factory=Answerer)
    assert calls[0][1]==calls[1][1]
    assert report['results'][0]['evidence_sha256']==report['results'][1]['evidence_sha256']
    for r in report['results']:
        assert r['metrics']['citation_membership_precision']==1
        assert r['metrics']['answer_correct'] is None
        assert r['metrics']['citations_supported'] is None
        assert r['estimated_cost_usd'] is None


def test_selection_scores_alternatives_and_wrong_domain_independently(suite):
    metrics=selection_metrics(suite['cases'][0],[{'page_name':'ssd2-result-units-and-limits.md','domain':'all'},
                                              {'page_name':'vmpr-reporting.md','domain':'vmpr'}])
    assert metrics['required_page_recall']==1
    assert metrics['wrong_domain_or_path_count']==1


def test_empty_selection_is_separate_from_page_recall(suite):
    case=suite['cases'][0];case.update(expected_page_groups=[],expect_empty_selection=True)
    assert selection_metrics(case,[])['empty_selection_correct'] is True
    assert selection_metrics(case,[])['required_page_recall'] is None


def test_citation_membership_does_not_certify_correctness(suite):
    result={'evidence':[{'page_name':'a.md','evidence_kind':'full'},{'page_name':'b.md','evidence_kind':'summary'}],
            'citations':['a.md','b.md','invented.md']}
    metrics=grade_metrics(suite['cases'][0],result)
    assert metrics['citation_membership_precision']==pytest.approx(1/3)
    assert metrics['answer_correct'] is None
    grade={'case':{'reviewer':'Reviewer','reviewed_at':'2026-10-05','answer_correct':False,'citations_supported':False}}
    assert grade_metrics(suite['cases'][0],result,grade)['answer_correct'] is False
    with pytest.raises(ValueError):
        grade_metrics(suite['cases'][0],result,{'case':{'answer_correct':True}})


def test_failed_case_is_reported_without_provider_error_details(suite):
    class Selector:
        def __init__(self,**kwargs): pass
        def run(self,payload): raise RuntimeError('sensitive provider details')
    report=run_suite(WikiStore(ROOT),suite,mode='select',models=['test/model'],live=True,selector_factory=Selector)
    assert report['results'][0]['status']=='error'
    assert report['summary']['test/model']['errors']==1
    assert 'sensitive' not in json.dumps(report)


def test_unknown_cost_remains_null_and_zero_call_costs_zero():
    assert estimated_cost({'calls':1,'input_tokens':100},{},'unknown') is None
    assert estimated_cost({'calls':0},{},'unknown')==0
    assert estimated_cost({'calls':1,'input_tokens':1_000_000,'output_tokens':100_000},
        {'m':{'input_per_million':2,'output_per_million':5}},'m')==2.5


@pytest.mark.parametrize('fault',['duplicate','unknown','over_budget','fake_review'])
def test_invalid_labels_are_rejected(suite,fault):
    if fault=='duplicate': suite['cases'].append(copy.deepcopy(suite['cases'][0]))
    if fault=='unknown': suite['cases'][0]['evidence_pages']=['not-real.md']
    if fault=='over_budget': suite['cases'][0]['max_pages']=0
    if fault=='fake_review': suite['cases'][0]['review_status']='human-reviewed'
    with pytest.raises(ValueError): validate_cases(suite,WikiStore(ROOT))


def test_real_case_set_has_reserved_cases_and_explicit_draft_status():
    cases=validate_cases(json.loads((ROOT/'evals/cases.json').read_text()),WikiStore(ROOT))
    assert len(cases)==16
    assert sum(c['split']=='held-out' for c in cases)==6
    assert all(c['review_status']=='draft' for c in cases)


def test_provider_initialization_failure_still_produces_a_report(suite):
    def fail(**kwargs): raise ValueError('credential details must not reach report')
    report=run_suite(WikiStore(ROOT),suite,mode='select',models=['test/model'],live=True,selector_factory=fail)
    assert report['summary']['test/model']['errors']==1
    assert report['summary']['test/model']['estimated_total_cost_usd'] is None
    assert report['results'][0]['phase']=='provider_initialization'
    assert 'credential details' not in json.dumps(report)
