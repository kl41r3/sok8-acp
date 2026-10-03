#!/usr/bin/env python3
"""Validate continuous optimization using a cap scan and direct-payoff quadrature."""
from pathlib import Path
import json
import hashlib
import numpy as np
from compute import evaluate, optimize, B, ETA, KAPPA

ROOT=Path(__file__).resolve().parent


def main():
    result=json.loads((ROOT/'summary.json').read_text())
    qc=result['q_critical']
    qs=[0,.25,.5,.75,.9,.95,.96,.97,qc-1e-5,qc,qc+1e-5,.975,.98,.99,1]
    ds=np.linspace(0,1.2,60001)
    theta=(np.arange(1000000)+.5)/1000000
    checks=[]
    for q in qs:
        opt=optimize(q)
        losses,shares=evaluate(q,ds)
        i=int(np.argmin(losses))
        assert opt['mean_user_loss']<=float(losses[i])+1e-11
        d=opt['d']
        auto_action=np.minimum(theta+B,d)
        va=-(auto_action-theta-B)**2
        vr=-q*B*B-(1-q)*(theta+B)**2-ETA
        review=vr>va
        direct=np.where(review,KAPPA+(1-q)*theta**2,(auto_action-theta)**2)
        loss_error=abs(float(direct.mean())-opt['mean_user_loss'])
        share_error=abs(float(review.mean())-opt['review_share'])
        assert loss_error<1e-7,(q,loss_error)
        assert share_error<1e-6,(q,share_error)
        checks.append({'q':q,'continuous_cap':d,'continuous_loss':opt['mean_user_loss'],
                       'dense_cap_grid_min_loss':float(losses[i]),'dense_cap_grid_cap':float(ds[i]),
                       'direct_quadrature_loss_error':loss_error,'direct_quadrature_review_share_error':share_error})
    for branch in result['at_switch'].values():
        loss,share=evaluate(qc,branch['d'])
        assert abs(float(loss)-branch['mean_user_loss'])<1e-12
        assert abs(float(share)-branch['review_share'])<1e-12
    data=np.genfromtxt(ROOT/'continuous-results.csv',delimiter=',',names=True,dtype=None,encoding='utf-8')
    assert len(data)==2001 and data['q'][0]==0 and data['q'][-1]==1
    report={'status':'Verified','scope':'specified Case A model only; no API calls',
            'continuous_q_plot_rows':2001,'global_cap_grid_points_per_check':60001,
            'direct_payoff_midpoint_cells_per_check':1000000,'checked_q_points':len(qs),
            'max_direct_quadrature_loss_error':max(x['direct_quadrature_loss_error'] for x in checks),
            'checks':checks,'equal_loss_switch_verified':True,
            'data_sha256':hashlib.sha256((ROOT/'continuous-results.csv').read_bytes()).hexdigest()}
    (ROOT/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='checks'},indent=2))


if __name__=='__main__':main()
