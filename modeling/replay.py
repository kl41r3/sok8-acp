#!/usr/bin/env python3
"""Offline bounded-model and saved-response validation. No credentials or network."""
from pathlib import Path
import argparse,csv,importlib.util,json,math
import numpy as np
ROOT=Path(__file__).resolve().parent

def module(name,path):
    s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path);args=parser.parse_args()
    a=module('case_a_integral',ROOT/'case-a/compute.py');oracle=module('case_a_oracle',ROOT/'case-a/oracle.py');b=module('case_b_solver',ROOT/'case-b/compute.py')
    with np.load(ROOT/'case-a/data/independent-grid.npz') as archive:data={k:archive[k] for k in archive.files}
    ll,rr,cc=a.evaluate(data['q'][:,None],data['d'][None,:])
    assert ll.shape==(501,601)
    for key,value in [('mean_user_loss',ll),('review_share',rr),('cancellation_share',cc)]:assert np.allclose(value,data[key],rtol=0,atol=1e-14),key
    count=0
    for row in csv.DictReader((ROOT/'case-a/data/independent-grid.csv').open()):
        i=round(float(row['q'])*500);j=round(float(row['d'])*500)
        for key in ['mean_user_loss','review_share','cancellation_share']:assert abs(float(row[key])-data[key][i,j])<1e-14
        count+=1
    assert count==301101
    theta=(np.arange(1000000)+.5)/1000000;errors=[]
    for q in [0,.25,.5,.75,.95,.97,1]:
        for d in [0,.1,.25,.55,.85,1.2]:
            action=np.minimum(theta+a.B,d);review=(-q*a.B**2-(1-q)*(theta+a.B)**2-a.ETA)>-(action-theta-a.B)**2
            direct=np.where(review,a.KAPPA+(1-q)*theta**2,(action-theta)**2)
            loss,share,_=a.evaluate(q,d);err=abs(float(direct.mean())-float(loss));assert err<2e-7;assert abs(review.mean()-share)<1e-6;errors.append(err)
    evidence_a=json.loads((ROOT/'case-a/probes/evidence.json').read_text());saved_a={x['run_id']:x for x in json.loads((ROOT/'case-a/probes/scoring.json').read_text())};correct_a=0;regrets_a=[]
    for x in evidence_a:
        assert x['returned_model']=='glm-5.3-flash' and x['http_status']==200 and not x['fallback'] and x['retries']==0
        parsed=json.loads(x['final_answer']);assert set(parsed)=={'choice','reason'};assert parsed['choice'] in ['AUTO','REVIEW'] and isinstance(parsed['reason'],str)
        score=saved_a[x['attempt_id']];expected=oracle.evaluate(score['theta'],score['d'],score['q']);choice=parsed['choice'];match=choice==expected['oracle_choice'];correct_a+=match
        regret=max(expected['utility_auto'],expected['utility_review'])-expected['utility_review' if choice=='REVIEW' else 'utility_auto'];regrets_a.append(regret)
        assert match==score['oracle_match'] and abs(regret-score['utility_regret'])<1e-12
    assert len(evidence_a)==24 and correct_a==23
    saved_b=json.loads((ROOT/'case-b/data/theory.json').read_text());calculated=b.calculate();assert calculated==saved_b
    prompts=json.loads((ROOT/'case-b/probes/prompts.json').read_text());by_id={p['id']:p for p in prompts};evidence_b=sorted(json.loads((ROOT/'case-b/probes/evidence.json').read_text()),key=lambda x:x['started_utc']);valid=[];invalid=[]
    for x in evidence_b:
        assert x['returned_model']=='glm-5.3-flash' and x['http_status']==200 and not x['fallback'] and x['retries']==0
        item=by_id[x['attempt_id']];assert item['prompt']==x['request']['messages'][1]['content'];parsed=json.loads(x['final_answer'])
        if set(parsed)!={'effort','failure_report','reason'} or parsed.get('effort') not in ['H','L'] or parsed.get('failure_report') not in ['REPORT','WITHHOLD'] or not isinstance(parsed.get('reason'),str):invalid.append(x['attempt_id']);continue
        decision=saved_b['policies'][item['policy']]['decisions'][item['remaining']][item['state']];effort=parsed['effort'];report=parsed['failure_report']
        valid.append({'attempt_id':x['attempt_id'],'remaining':item['remaining'],'effort_agreement':effort in decision['optimal_efforts'],'failure_agreement':report in decision['optimal_reports']['failure'],'unique_failure':len(decision['optimal_reports']['failure'])==1,'effort_regret':max(decision['utility'].values())-decision['utility'][effort]})
    assert len(evidence_b)==15 and len(valid)==14 and len(invalid)==1
    assert sum(x['effort_agreement'] for x in valid)==8
    assert len([x for x in valid if x['remaining']==4])==7 and all(x['effort_agreement'] for x in valid if x['remaining']==4)
    assert len([x for x in valid if x['remaining']==1])==7 and sum(x['effort_agreement'] for x in valid if x['remaining']==1)==1
    assert all(x['failure_agreement'] for x in valid) and sum(x['unique_failure'] for x in valid)==3
    stop=json.loads((ROOT/'case-b/probes/schema-stop.json').read_text());assert invalid==[stop['attempt_id']] and evidence_b[-1]['attempt_id']==stop['attempt_id']
    unattempted=sorted(set(by_id)-{x['attempt_id'] for x in evidence_b});assert len(unattempted)==9
    initial=json.loads((ROOT/'case-b/excluded-initial/evidence.json').read_text());assert len(initial)==6 and sum(x['response_received'] for x in initial)==5 and all(x['excluded_campaign'] for x in initial)
    results={'status':'Verified bounded offline replay','scope':'Saved model expectations and one-step decision evidence only; not platform outcomes or scientific readiness','API_calls':0,'case_a':{'independent_pairs':count,'direct_payoff_checks':len(errors),'maximum_direct_loss_difference':max(errors),'valid_decisions':24,'optimal_decisions':correct_a,'mean_utility_regret':sum(regrets_a)/24},'case_b':{'all_64_control_cells_recomputed':True,'theory_equal_saved':True,'attempts':15,'schema_valid':14,'effort_optimal':8,'h4_correct':7,'h4_valid':7,'h1_correct':1,'h1_valid':7,'failure_optimal_set_agreement':14,'unique_failure_choices':3,'schema_errors':invalid,'unattempted':unattempted,'mean_effort_regret':sum(x['effort_regret'] for x in valid)/14,'excluded_initial_attempts':6,'excluded_initial_responses':5},'checks':['A complete NPZ recomputation','A every CSV row matches NPZ','A original-payoff midpoint check independent of cutoff formula','A final-answer decision/regret rescoring','B exact DP plus exhaustive action enumeration','B saved final-answer strict schema and optimal-set rescoring','B prespecified schema-stop and missingness','B initial batch exclusion']}
    if args.output:args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps(results,indent=2))
if __name__=='__main__':main()
