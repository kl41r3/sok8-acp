#!/usr/bin/env python3
"""Verify the release and regenerate current-paper data, tables and numerical figures."""
import argparse
import collections
import csv
from fractions import Fraction as F
import hashlib
import itertools
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent

def require(condition, message):
    if not condition:
        raise ValueError(message)

def read(path):
    return json.loads(path.read_text())

def save(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def table(path, rows):
    with path.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        for row in rows:
            w.writerow({k: '|'.join(v) if isinstance(v, list) else v for k,v in row.items()})

def seal():
    manifest = read(ROOT/'MANIFEST.json')
    for item in manifest['files']:
        p=ROOT/item['path']
        require(p.is_file() and p.stat().st_size==item['bytes'] and sha(p)==item['sha256'], 'Release mismatch: '+item['path'])
        if 'csv' in item:
            with p.open(newline='',encoding='utf-8') as f:
                reader=csv.reader(f); header=next(reader); n=sum(1 for _ in reader)
            require(header==item['csv']['columns'] and n==item['csv']['rows'], 'CSV schema mismatch: '+item['path'])
    for line in (ROOT/'SHA256SUMS').read_text().splitlines():
        digest,path=line.split('  ',1)
        require(sha(ROOT/path)==digest,'Checksum mismatch: '+path)
    return len(manifest['files'])+2

def run(args, env):
    subprocess.run([sys.executable,'-B',*map(str,args)],cwd=ROOT,env=env,check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)

def numeric_equal(a,b,path='root'):
    if isinstance(a,dict):
        require(isinstance(b,dict) and a.keys()==b.keys(),'Object keys: '+path)
        for k in a:numeric_equal(a[k],b[k],path+'/'+k)
    elif isinstance(a,list):
        require(len(a)==len(b),'Array length: '+path)
        for i,(x,y) in enumerate(zip(a,b)):numeric_equal(x,y,path+'/'+str(i))
    elif isinstance(a,(int,float)) and not isinstance(a,bool):
        require(abs(a-b)<=1e-10,'Numeric mismatch: '+path)
    else: require(a==b,'Value mismatch: '+path)

def exact_case_b(theory):
    """Independent rational enumeration of effort and both contingent reports."""
    checked=0;forward_checked=0
    for policy,rho in [('VOLUNTARY',F(0)),('OBLIGATED_025',F(1,4)),('OBLIGATED_1',F(1)),('COMPLAINT_025',F(1,4))]:
        def transition(s,success,report):
            dest=('G' if success else 'B') if report else s
            if policy.startswith('OBLIGATED'):
                return [(1-rho,s),(rho,'G' if success and report else 'B')]
            if policy.startswith('COMPLAINT') and not success:return [(1-rho,dest),(rho,'B')]
            return [(F(1),dest)]
        values=[{'G':F(0),'B':F(0)}];choices=[{}]
        for h in range(1,9):
            v={};c={}
            for s in ['G','B']:
                options=[]
                for e,rs,rf in itertools.product(['L','H'],[True,False],[False,True]):
                    p=F(9,10) if e=='H' else F(3,10)
                    future=sum(prob*sum(t*values[-1][dest] for t,dest in transition(s,success,report)) for success,prob,report in [(True,p,rs),(False,1-p,rf)])
                    u=(F(1) if s=='G' else F(2,5))-(F(3,20) if e=='H' else 0)+F(19,20)*future
                    options.append((u,e,rs,rf))
                best=max(x[0] for x in options); chosen=next(x for x in options if x[0]==best)
                v[s]=best;c[s]=chosen[1:]
                ref=theory['policies'][policy]
                require(abs(float(best)-ref['values'][h][s])<1e-10,'Rational value mismatch')
                require(chosen[1]==ref['decisions'][h][s]['effort'],'Rational policy mismatch')
                for outcome,report in [('success',chosen[2]),('failure',chosen[3])]:
                    require(('REPORT' if report else 'WITHHOLD')==ref['decisions'][h][s]['report'][outcome],'Rational report mismatch')
                checked+=1
            values.append(v);choices.append(c)
        for initial in ['G','B']:
            dist={s:F(s==initial) for s in ['G','B']};high=F(0);successes=F(0)
            for h in range(8,0,-1):
                new={'G':F(0),'B':F(0)}
                for s,mass in dist.items():
                    e,rs,rf=choices[h][s];p=F(9,10) if e=='H' else F(3,10)
                    high+=mass*(e=='H');successes+=mass*p
                    for success,prob,report in [(True,p,rs),(False,1-p,rf)]:
                        for t,dest in transition(s,success,report):new[dest]+=mass*prob*t
                require(sum(new.values())==1,'Probability mass');dist=new
            ref=theory['policies'][policy]['forward'][initial]
            numeric_equal(float(high/8),ref['rates']['high_effort']);numeric_equal(float(successes/8),ref['rates']['success'])
            for s in dist:numeric_equal(float(dist[s]),ref['final_state'][s])
            forward_checked+=1
    return {'rational_control_cells':checked,'rational_forward_paths':forward_checked}

def synthesize(out,taxout):
    out.mkdir();sources=read(ROOT/'synthesis/sources.json');claims=read(ROOT/'synthesis/claims.json');tables=read(ROOT/'synthesis/tables.json')
    classes=dict(collections.Counter(s['source_class'] for s in sources))
    require(classes=={'official':21,'mapped_corpus':40,'supplementary_scholarship':5},'Source counts')
    keys={s['citation_key'] for s in sources};require(len(keys)==66,'Duplicate citation key')
    with (taxout/'included-identifiers.csv').open(newline='') as f: included=list(csv.DictReader(f))
    identifiers={row['union_identifier_key'] for row in included}
    for s in sources:
        require(s['public_locator'].startswith('https://'),'Source locator')
        if s['source_class']=='mapped_corpus':require(s['included_identifier'] in identifiers,'Corpus link: '+s['citation_key'])
        require(set(s['claim_ids'])<= {c['claim_id'] for c in claims},'Unknown claim')
    require(len(claims)==6 and all(set(c['decisive_citation_keys'])<=keys for c in claims),'Claim citations')
    with (taxout/'source-counts.csv').open(newline='') as f:counts=list(csv.DictReader(f))
    rows=[]
    for s in counts:
        if s['source'] not in ['ACM','IEEE','AAAI','IJCAI']:continue
        rows.append({'source':s['source'],'selection_rows':int(s['selection_track_records']),'included':int(s['included_source_records']),'rule_evidence_excluded':int(s['original_rule_or_evidence_excluded_records']),'author_not_included':int(s['user_directed_not_included_unresolved_records']),'final_not_included':int(s['final_not_included_records'])})
    rows.append({'source':'Total',**{k:sum(r[k] for r in rows) for k in rows[0] if k!='source'}})
    require(list(rows[-1].values())==['Total',5217,1312,3668,237,3905],'Table 1 totals')
    table(out/'table-1-source-selection.csv',rows)
    table(out/'table-2-stage-functions.csv',tables['stage_functions']);table(out/'table-3-queries.csv',tables['search_expressions']);table(out/'table-4-eligibility.csv',tables['eligibility_rules']);table(out/'table-5-synthesis.csv',claims)
    table(out/'source-claim-links.csv',[{'citation_key':s['citation_key'],'source_class':s['source_class'],'claim_id':c,'role':s['analytical_role'],'locator':s['public_locator']} for s in sources for c in s['claim_ids']])
    return {'sources':classes,'claims':6,'search_expressions':len(tables['search_expressions']),'tables':5}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=Path('outputs/reproduction'))
    parser.add_argument('--legacy',action='store_true',help='Also regenerate and replay historical exploratory artifacts.')
    parser.add_argument('--drawio',type=Path,help='Optional draw.io executable for editable framework PDF export.')
    args=parser.parse_args();out=args.output.resolve()
    require(not out.exists(),'Choose a new output directory.')
    files=seal();out.mkdir(parents=True)
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',MPLCONFIGDIR=str(out/'.mpl-cache'),XDG_CACHE_HOME=str(out/'.cache'))
    run([ROOT/'taxonomy/code/reproduce.py','--output',out/'taxonomy'],env)
    for expected in (ROOT/'taxonomy/expected').iterdir():require(sha(expected)==sha(out/'taxonomy'/expected.name),'Taxonomy output: '+expected.name)
    summary={'release_files_verified':files,'taxonomy_outputs_byte_identical':5,'synthesis':synthesize(out/'synthesis',out/'taxonomy')}
    run([ROOT/'modeling/case-a/thresholds/analyze.py','--output',out/'case-a'],env)
    require(sha(out/'case-a/threshold-surface.csv')==sha(ROOT/'modeling/case-a/thresholds/threshold-surface.csv'),'Case A surface')
    a=read(out/'case-a/validation.json');require(a['verification']['all_passed'],'Case A checks');summary['case_a']=a['verification']
    run([ROOT/'modeling/case-b/compute.py','--output',out/'case-b/data'],env)
    theory=read(out/'case-b/data/theory.json');numeric_equal(theory,read(ROOT/'modeling/case-b/data/theory.json'))
    summary['case_b']=exact_case_b(theory)
    run([ROOT/'modeling/case-b/plot.py','--data',out/'case-b/data/theory.json','--output',out/'case-b/figures'],env)
    require(sha(out/'case-b/figures/plotted-values.csv')==sha(ROOT/'modeling/case-b/figures/plotted-values.csv'),'Case B plotted data')
    summary['figures_generated']=['case-a-threshold-regions.pdf/svg/png','case-b-policy-comparison.pdf/svg/png']
    run([ROOT/'modeling/extensions/reproduce.py','--output',out/'model-extensions'],env)
    summary['model_extensions']=read(out/'model-extensions/verification.json')
    summary['figures_generated'] += ['case-a-cancellation-fallback.pdf/svg/png',
        'case-a-cost-sensitivity.pdf/svg/png','case-b-evidence-availability.pdf/svg/png',
        'case-b-effort-sensitivity.pdf/svg/png','case-a-review-fallback.pdf/svg/png',
        'case-b-evidence-loss.pdf/svg/png','app-case-a-review-costs.pdf/svg/png',
        'app-case-b-effort-sensitivity.pdf/svg/png']
    if args.drawio:
        subprocess.run([str(args.drawio),'--export','--format','pdf','--crop','--output',str(out/'framework.pdf'),str(ROOT/'figures/Taxonomy_Editable.drawio')],check=True)
        require((out/'framework.pdf').stat().st_size>0,'Framework export');summary['framework_export']='passed'
    if args.legacy:
        run([ROOT/'modeling/reproduce.py','--output',out/'legacy','--plots'],env);summary['legacy']='passed'
    summary['api_calls']=0;summary['python']=sys.version.split()[0];summary['passed']=True
    save(out/'verification.json',summary);print(json.dumps(summary,indent=2))

if __name__=='__main__':
    try:main()
    except subprocess.CalledProcessError as e:
        print(e.stdout or '',file=sys.stderr);print(e.stderr or '',file=sys.stderr);raise
