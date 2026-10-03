#!/usr/bin/env python3
"""Independent q x d sensitivity of Case A. No optimization and no API."""
from pathlib import Path
import csv
import hashlib
import json
import numpy as np

ROOT=Path(__file__).resolve().parent/'data'
B,ETA,KAPPA=.15,.005,.01


def evaluate(q,d):
    q,d=np.broadcast_arrays(np.asarray(q,dtype=float),np.asarray(d,dtype=float))
    safe_q=np.where(q>0,q,1.)
    r=np.clip((d+np.sqrt((1-q)*d*d+q*q*B*B+q*ETA))/safe_q-B,0,1)
    # Enforce the exact no-review region, including its zero-measure boundary.
    entry=1+B-np.sqrt(q*B*B+(1-q)*(1+B)**2+ETA)
    r=np.where((q==0)|(d>=entry),1.,r)
    t=np.clip(d-B,0,r)
    loss=B*B*t+((r-d)**3-(t-d)**3)/3+KAPPA*(1-r)+(1-q)*(1-r**3)/3
    review=1-r
    return loss,review,(1-q)*review


def main():
    design={'parameters':{'b':B,'eta':ETA,'kappa':KAPPA,'theta':'Uniform[0,1]'},
            'q':{'minimum':0,'maximum':1,'step':.002,'points':501},
            'd':{'minimum':0,'maximum':1.2,'step':.002,'points':601},
            'independent_inputs':True,'d_optimization':False,
            'integration':'closed-form piecewise polynomial expectation under strategic self-selection',
            'fixed_d_slices':[.1,.25,.55,.85],
            'API_calls':0,'manuscript_edits':False,
            'original_design_sha256':hashlib.sha256((ROOT.parent/'probes/design.json').read_bytes()).hexdigest()}
    serialized=json.dumps(design,indent=2)+'\n'
    if (ROOT/'design.json').exists():assert (ROOT/'design.json').read_text()==serialized
    else:(ROOT/'design.json').write_text(serialized)
    q=np.arange(501)/500;d=np.arange(601)/500
    loss,review,cancel=evaluate(q[:,None],d[None,:])
    np.savez_compressed(ROOT/'independent-grid.npz',q=q,d=d,mean_user_loss=loss,review_share=review,cancellation_share=cancel)
    with (ROOT/'independent-grid.csv').open('w',newline='') as f:
        w=csv.writer(f);w.writerow(['q','d','mean_user_loss','review_share','cancellation_share'])
        for i,qi in enumerate(q):
            for j,dj in enumerate(d):
                w.writerow([f'{qi:.3f}',f'{dj:.3f}',format(loss[i,j],'.17g'),format(review[i,j],'.17g'),format(cancel[i,j],'.17g')])
    with (ROOT/'fixed-d-slices.csv').open('w',newline='') as f:
        w=csv.writer(f);w.writerow(['q','d','mean_user_loss','review_share','cancellation_share'])
        for di in design['fixed_d_slices']:
            ll,rr,cc=evaluate(q,di)
            for qi,l,r,c in zip(q,ll,rr,cc):w.writerow([qi,di,l,r,c])
    selected=[]
    for di in design['fixed_d_slices']:
        for qi in [0,.5,.75,.9,.95,.97,.99,1]:
            l,r,c=evaluate(qi,di)
            selected.append({'q':qi,'d':di,'mean_user_loss':float(l),'review_share':float(r),'cancellation_share':float(c)})
    summary={'status':'Computed','independent_parameter_pairs':loss.size,'grid_shape_q_by_d':list(loss.shape),
             'd_optimization':False,'API_calls':0,'selected_points':selected,
             'scope':'Deterministic Case A model sensitivity to independently fixed q and d; no real platform outcomes or LLM behavior'}
    (ROOT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))


if __name__=='__main__':main()
