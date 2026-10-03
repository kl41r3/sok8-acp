#!/usr/bin/env python3
"""Continuous-cap numerical optimization of Case A; no API calls."""
from pathlib import Path
import csv
import hashlib
import json
import math
import numpy as np

ROOT = Path(__file__).resolve().parent
B, ETA, KAPPA = .15, .005, .01


def entry_cap(q):
    """Review can occur on positive-measure theta only below this cap."""
    return 1+B-math.sqrt(q*B*B+(1-q)*(1+B)**2+ETA)


def evaluate(q, d):
    """Analytic polynomial integrals under Uniform[0,1], not quadrature."""
    ds = np.asarray(d, dtype=float)
    if q == 0:
        r = np.ones_like(ds)
    else:
        r = np.clip((ds+np.sqrt((1-q)*ds**2+q*q*B*B+q*ETA))/q-B, 0, 1)
    t = np.clip(ds-B, 0, r)
    loss = B*B*t+((r-ds)**3-(t-ds)**3)/3
    loss += KAPPA*(1-r)+(1-q)*(1-r**3)/3
    return loss, 1-r


def review_derivative(q, d):
    ds = np.asarray(d, dtype=float)
    s = np.sqrt((1-q)*ds**2+q*q*B*B+q*ETA)
    r = (ds+s)/q-B
    t = np.clip(ds-B, 0, r)
    rp = (1+(1-q)*ds/s)/q
    return 2*ds*(r-t)-(r*r-t*t)+((r-ds)**2-KAPPA-(1-q)*r*r)*rp


def bisect(f, lo, hi, tol=2e-13):
    fl, fh = f(lo), f(hi)
    assert fl*fh <= 0, (lo, hi, fl, fh)
    for _ in range(100):
        mid = (lo+hi)/2
        fm = f(mid)
        if hi-lo < tol or fm == 0:
            return mid
        if fl*fm <= 0:
            hi, fh = mid, fm
        else:
            lo, fl = mid, fm
    return (lo+hi)/2


def review_minimum(q, brackets=512, include_no_review_boundary=True):
    upper = entry_cap(q)
    if q == 0 or upper <= 0:
        return None
    ds = np.linspace(0, upper, brackets+1)
    deriv = review_derivative(q, ds)
    candidates = [0., upper] if include_no_review_boundary else [0.]
    if 0 < B < upper:
        candidates.append(B)
    for i in np.flatnonzero(deriv[:-1]*deriv[1:] < 0):
        candidates.append(bisect(lambda x: float(review_derivative(q,x)), ds[i], ds[i+1]))
    candidates.extend(ds[np.flatnonzero(deriv == 0)].tolist())
    results = [(float(evaluate(q,d)[0]), d, float(evaluate(q,d)[1])) for d in candidates]
    loss,d,share = min(results)
    return {'d':d, 'mean_user_loss':loss, 'review_share':share,
            'stationary_roots_found':len(candidates)-1-int(include_no_review_boundary)-int(0 < B < upper)}


def optimize(q, brackets=512):
    # No-review region is d >= entry_cap(q). Its unconstrained optimum is .85.
    no_d = max(.85, entry_cap(q))
    no_loss,no_share = evaluate(q,no_d)
    best = {'q':q,'d':no_d,'mean_user_loss':float(no_loss),
            'review_share':float(no_share),'regime':'no_review'}
    review = review_minimum(q,brackets)
    if review and review['mean_user_loss'] < best['mean_user_loss']-1e-13:
        best.update({k:review[k] for k in ['d','mean_user_loss','review_share']},regime='review')
    return best


def write_csv(name, rows):
    with (ROOT/name).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)


def main():
    design={'parameters':{'b':B,'eta':ETA,'kappa':KAPPA,'theta':'Uniform[0,1]'},
            'q_domain':[0,1],'plot_q_points':2001,'continuous_cap_domain':[0,1.2],
            'integration':'analytic piecewise polynomial integrals',
            'optimization':'continuous stationary-root bisection plus boundaries, comparing review/no-review branches',
            'root_brackets':512,'validation_root_brackets':4096,'root_interval_tolerance':2e-13,
            'scope':'Conditional model sensitivity; no API, no manuscript edit, no general mechanism optimality',
            'source_design_sha256':hashlib.sha256((ROOT.parent/'five-q/design.json').read_bytes()).hexdigest()}
    serialized=json.dumps(design,indent=2)+'\n'
    if (ROOT/'design.json').exists():
        assert (ROOT/'design.json').read_text()==serialized
    else:
        (ROOT/'design.json').write_text(serialized)
    rows=[optimize(float(q)) for q in np.linspace(0,1,2001)]
    write_csv('continuous-results.csv',rows)
    # Compare with the feasible no-review branch: .85 may induce review at high q.
    changes=[i for i in range(1,len(rows)) if rows[i]['regime']!=rows[i-1]['regime']]
    assert len(changes)==1,changes
    idx=changes[0]
    advantage=lambda q:review_minimum(q,include_no_review_boundary=False)['mean_user_loss']-float(evaluate(q,max(.85,entry_cap(q)))[0])
    critical=bisect(advantage,rows[idx-1]['q'],rows[idx]['q'])
    rb=review_minimum(critical,include_no_review_boundary=False)
    assert rb['review_share']>.1
    assert abs(advantage(critical))<1e-12
    # Numerical optimization validation with eight times denser stationary-root brackets.
    errors=[]
    for row in rows:
        check=optimize(row['q'],4096)
        errors.append(max(abs(row[k]-check[k]) for k in ['d','mean_user_loss','review_share']))
    assert max(errors)<1e-9,max(errors)
    selected_q=[0,.25,.5,.75,.8,.85,.9,.925,.94,.95,.96,.97,.975,.98,.99,1]
    selected=[optimize(q) for q in selected_q]
    write_csv('selected-results.csv',selected)
    # q=1 review-region loss is d^3/3 + s^3/3 + kappa*(1-d-s).
    s=math.sqrt(B*B+ETA)-B
    analytical_d1=math.sqrt(KAPPA)
    analytical_loss1=analytical_d1**3/3+s**3/3+KAPPA*(1-analytical_d1-s)
    assert abs(rows[-1]['d']-analytical_d1)<1e-10
    assert abs(rows[-1]['mean_user_loss']-analytical_loss1)<1e-12
    result={'status':'Verified continuous numerical optimization',
            'q_plot_points':len(rows),'q_critical':critical,
            'at_switch':{'no_review':{'d':max(.85,entry_cap(critical)),
                                    'mean_user_loss':float(evaluate(critical,max(.85,entry_cap(critical)))[0]),
                                    'review_share':0},'review':rb},
            'q1_analytic':{'d':analytical_d1,'mean_user_loss':analytical_loss1,'review_share':1-analytical_d1-s},
            'sampled_points':selected,'validation':{'denser_root_brackets_max_difference':max(errors),'q1_analytic_agrees':True},
            'scope':'Continuous d numerical minima of the specified cap/review model; q is densely sampled for plotting. No empirical uncertainty or LLM curve.'}
    (ROOT/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
