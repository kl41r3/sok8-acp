#!/usr/bin/env python3
"""Costly Case A: independent payoff checks and matched timeout comparisons."""
from pathlib import Path
from fractions import Fraction as F
import argparse
import csv
import itertools
import json
import platform
import sys
import numpy as np
import sympy as sp
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm
from matplotlib.patches import Patch

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parents[1] / "extensions"))
from plot_style import setup, export, dump, INK, BURGUNDY, GREEN

DESIGN = json.loads((ROOT / "design.json").read_text())
TOL = DESIGN["numerical_tie_tolerance_in_theta_squared_units"]
REGIONS = [
    "autonomy_no_user_gain", "autonomy_user_would_benefit",
    "review_user_benefits", "review_user_harmed", "review_user_indifferent",
]
COLORS = ["#E8EDF2", "#F0C66C", "#92CBB5", "#C66582", "#C7BBDA"]


def evaluate(theta, bias, cap, q, eta, kappa, policy):
    """Stable payoff differences; no division at zero-gain boundaries."""
    if policy not in ("CANCEL", "FALLBACK"):
        raise ValueError("Unknown timeout policy")
    t, b, d, q, e, k = np.broadcast_arrays(*map(
        lambda x: np.asarray(x, dtype=float), (theta, bias, cap, q, eta, kappa)))
    if not (np.all(np.isfinite([t, b, d, q, e, k])) and np.all(t > 0)
            and np.all(b >= 0) and np.all(d >= 0) and np.all(e >= 0)
            and np.all(k >= 0) and np.all((q >= 0) & (q <= 1))):
        raise ValueError("Invalid Case A parameters")
    action = np.minimum(t+b, d)
    user_auto = (action-t)**2
    agent_auto = -(action-t-b)**2
    late = np.zeros_like(action) if policy == "CANCEL" else action
    if policy == "FALLBACK":
        agent_gain = q*((action-t-b)**2-b*b)-e
        user_gain = q*user_auto-k
    else:
        agent_gain = q*t*(t+2*b)-(2*action*(t+b)-action*action+e)
        user_gain = q*t*t-(2*action*t-action*action+k)
    scale = t*t
    request = agent_gain > TOL*scale
    benefit = user_gain > TOL*scale
    harm = user_gain < -TOL*scale
    region = np.where(request, np.where(benefit, 2, np.where(harm, 3, 4)),
                      np.where(benefit, 1, 0))
    user_review = user_auto-user_gain
    agent_review = agent_auto+agent_gain
    return {
        "autonomous_action": action, "late_review_action": late,
        "agent_autonomy_utility": agent_auto, "agent_review_utility": agent_review,
        "user_autonomy_loss": user_auto, "user_review_loss": user_review,
        "agent_review_gain": agent_gain, "user_review_gain": user_gain,
        "review_requested": request, "user_benefits_from_review": benefit,
        "region": region,
        "selected_user_loss": np.where(request, user_review, user_auto),
    }


def rational_payoffs(t, b, d, q, eta, kappa, policy):
    """Independent exact evaluation of final actions, not threshold equations."""
    t,b,d,q,eta,kappa = map(lambda x: x if isinstance(x,F) else F(str(x)),
                           (t,b,d,q,eta,kappa))
    action = min(t+b,d)
    late = F(0) if policy == "CANCEL" else action
    va = -(action-t-b)**2
    vr = -q*b*b-(1-q)*(late-t-b)**2-eta
    la = (action-t)**2
    lr = kappa+(1-q)*(late-t)**2
    ag, ug = vr-va, la-lr
    eps = F(str(TOL))*t*t
    request, benefit, harm = ag > eps, ug > eps, ug < -eps
    region = (2 if benefit else 3 if harm else 4) if request else (1 if benefit else 0)
    return va,vr,la,lr,region


def verify():
    t,b,a,d,q,e,k = sp.symbols("theta b action d q eta kappa", real=True)
    c=(a-t)**2
    vauto=-(a-t-b)**2
    tests = {
        "fallback_agent_gain": (-q*b*b+(1-q)*vauto-e-vauto)
                               -(q*((a-t-b)**2-b*b)-e),
        "fallback_user_gain": c-(k+(1-q)*c)-(q*c-k),
        "cancellation_agent_gain": (-q*b*b-(1-q)*(t+b)**2-e-vauto)
                                   -(q*t*(t+2*b)-2*a*(t+b)+a*a-e),
        "cancellation_user_gain": c-k-(1-q)*t*t
                                  -(q*t*t-2*a*t+a*a-k),
        "binding_fallback_gain_factor": ((d-t-b)**2-b*b)
                                         -(t-d)*(t-d+2*b),
        "binding_fallback_threshold_difference":
            k/(t-d)**2-e/((t-d)*(t-d+2*b))
            -(k*(t-d)*(t-d+2*b)-e*(t-d)**2)/
              ((t-d)**2*(t-d)*(t-d+2*b)),
        "same_choice_user_timeout_difference":
            (k+(1-q)*t*t)-(k+(1-q)*c)-(1-q)*(t*t-c),
    }
    for name, expression in tests.items():
        if sp.simplify(expression) != 0:
            raise AssertionError(name)
    rng=np.random.default_rng(DESIGN["verification"]["seed"])
    n=DESIGN["verification"]["random_payoff_tuples"]
    tv=10**rng.uniform(-2,2,n)
    bv=tv*10**rng.uniform(-3,1,n)
    dv=(tv+bv)*rng.uniform(0,1.5,n)
    qv=rng.uniform(0,1,n)
    ev=tv*tv*rng.uniform(0,.5,n)
    kv=tv*tv*rng.uniform(0,.5,n)
    action=np.minimum(tv+bv,dv)
    maximum_error=0.
    for policy in ("CANCEL","FALLBACK"):
        result=evaluate(tv,bv,dv,qv,ev,kv,policy)
        late=np.zeros(n) if policy=="CANCEL" else action
        va=-(action-tv-bv)**2
        vr=-qv*bv*bv-(1-qv)*(late-tv-bv)**2-ev
        la=(action-tv)**2
        lr=kv+(1-qv)*(late-tv)**2
        for key, reference in [("agent_review_utility",vr),("user_review_loss",lr)]:
            error=float(np.max(np.abs(result[key]-reference)/np.maximum(tv*tv, np.abs(reference))))
            maximum_error=max(maximum_error,error)
            if error>1e-10: raise AssertionError(key)
        normalized=(vr-va)/(tv*tv)
        away=np.abs(normalized)>1e-10
        if not np.array_equal(result["review_requested"][away],normalized[away]>0):
            raise AssertionError("Independent action comparison")
        selected=np.where(result["review_requested"],lr,la)
        if not np.allclose(selected,result["selected_user_loss"],rtol=1e-10,atol=1e-10):
            raise AssertionError("Selected user loss")
    exact=0
    for _ in range(DESIGN["verification"]["exact_rational_tuples"]):
        params=(F(int(rng.integers(1,21)),10),F(int(rng.integers(0,31)),10),
                F(int(rng.integers(0,51)),10),F(int(rng.integers(0,21)),20),
                F(int(rng.integers(0,11)),20),F(int(rng.integers(0,11)),20))
        for policy in ("CANCEL","FALLBACK"):
            va,vr,la,lr,region=rational_payoffs(*params,policy)
            result=evaluate(*map(float,params),policy)
            if int(result["region"])!=region:
                raise AssertionError(("Rational classification",params,policy))
            for key,reference in [("agent_review_gain",vr-va),("user_review_gain",la-lr)]:
                if abs(float(result[key])-float(reference))>1e-10:
                    raise AssertionError("Rational payoff")
            exact+=1
    # Endpoints, zero bias/costs, above-ideal and non-binding caps.
    edge_cases=0
    for bias,cap,q0,eta,kappa,policy in itertools.product(
            [0,.2,2],[0,.5,1,1.2,4],[0,.25,1],[0,.01],[0,.1],["CANCEL","FALLBACK"]):
        r=evaluate(1,bias,cap,q0,eta,kappa,policy)
        exact_ref=rational_payoffs(1,bias,cap,q0,eta,kappa,policy)
        if int(r["region"])!=exact_ref[-1]:
            raise AssertionError(("Boundary",bias,cap,q0,eta,kappa,policy))
        edge_cases+=1
    # Exact agent and user ties must not become requests or strict benefits.
    tie_cases=0
    for cap,q0 in itertools.product([F(0),F(1,4),F(1,2),F(3,4)], [F(0),F(1,4),F(1)]):
        m=(1-cap)*(1-cap+F(2,5))
        eta=q0*m;kappa=q0*(1-cap)**2
        r=evaluate(1,.2,float(cap),float(q0),float(eta),float(kappa),"FALLBACK")
        if bool(r["review_requested"]) or bool(r["user_benefits_from_review"]):
            raise AssertionError("Indifference rule")
        tie_cases+=1
    # Zero user cost alone suffices for fallback's weak user-benefit statement.
    zero=evaluate(tv,bv,dv,qv,ev,0,"FALLBACK")
    if not np.all(zero["user_review_loss"]<=zero["user_autonomy_loss"]+1e-10*tv*tv):
        raise AssertionError("Original fallback result")
    interval_cases=0
    for eta,kappa,policy in itertools.product(
            [F(0),F(1,100),F(1,10),F(3,10)],
            [F(0),F(1,20),F(1,10),F(3,10)],["CANCEL","FALLBACK"]):
        # Solve the independent direct-payoff expressions at q=0 and q=1.
        first=rational_payoffs(1,F(1,5),F(1,2),0,eta,kappa,policy)
        last=rational_payoffs(1,F(1,5),F(1,2),1,eta,kappa,policy)
        ag0,ag1=first[1]-first[0],last[1]-last[0]
        ug0,ug1=first[2]-first[3],last[2]-last[3]
        qa=-ag0/(ag1-ag0);qp=-ug0/(ug1-ug0)
        independent=max(F(0),min(F(1),qp)-max(F(0),qa))
        predicted_a=(F(19,20)+eta)/F(7,5) if policy=="CANCEL" else eta/F(9,20)
        predicted_p=F(3,4)+kappa if policy=="CANCEL" else 4*kappa
        if (qa,qp)!=(predicted_a,predicted_p):
            raise AssertionError("Independent cost-sensitivity thresholds")
        if abs(float(interval(float(predicted_a),float(predicted_p)))-float(independent))>1e-12:
            raise AssertionError("Feasible harmful-interval length")
        interval_cases+=1
    return {"symbolic_identities":len(tests),"random_parameter_tuples":n,
            "timeout_policy_payoff_checks":2*n,"exact_rational_policy_cases":exact,
            "boundary_policy_cases":edge_cases,"exact_tie_cases":tie_cases,
            "independent_cost_interval_cases":interval_cases,
            "maximum_normalized_direct_payoff_difference":maximum_error,"passed":True}


def write_grid(output):
    cfg=DESIGN["main_figure"]
    x=np.linspace(cfg["cap_ratio_min"],cfg["cap_ratio_max"],cfg["cap_points"])
    q=np.linspace(0,1,cfg["q_points"])
    X,Q=np.meshgrid(x,q)
    results={}
    path=output/"decision-grid.csv"
    with path.open("w",newline="") as stream:
        fields=["policy","cap_ratio","q","autonomous_action","late_review_action",
                "agent_review_gain","user_review_gain","review_requested","region",
                "user_autonomy_loss","user_review_loss","selected_user_loss"]
        writer=csv.DictWriter(stream,fieldnames=fields);writer.writeheader()
        for policy in ("CANCEL","FALLBACK"):
            r=evaluate(cfg["theta"],cfg["bias"],X*cfg["theta"],Q,
                       cfg["agent_cost"],cfg["user_cost"],policy)
            results[policy]=r
            for i in range(X.size):
                row={key:float(r[key].ravel()[i]) for key in fields
                     if key in r and key not in ("region","review_requested")}
                row.update(policy=policy,cap_ratio=float(X.ravel()[i]),q=float(Q.ravel()[i]),
                           review_requested=bool(r["review_requested"].ravel()[i]),
                           region=REGIONS[int(r["region"].ravel()[i])])
                writer.writerow(row)
    return X,Q,results


def interval(qa,qp):
    return np.maximum(0,np.minimum(1,qp)-np.maximum(0,qa))


def figures(output,X,Q,results):
    setup()
    cfg=DESIGN["main_figure"]
    cmap=ListedColormap(COLORS)
    norm=BoundaryNorm(np.arange(-.5,5.5,1),cmap.N)
    fig,axes=plt.subplots(1,2,figsize=(7,3.85))
    fig.subplots_adjust(left=.085,right=.98,bottom=.37,top=.80,wspace=.23)
    for ax,policy,title in zip(axes,["CANCEL","FALLBACK"],
                               ["(a) Cancel after timeout","(b) Execute capped fallback"]):
        ax.pcolormesh(X,Q,results[policy]["region"],cmap=cmap,norm=norm,
                      shading="nearest",rasterized=True)
        ax.contour(X,Q,results[policy]["agent_review_gain"],levels=[0],colors=[INK],linewidths=1.1)
        ax.contour(X,Q,results[policy]["user_review_gain"],levels=[0],colors=[BURGUNDY],linewidths=1.1,linestyles="--")
        ax.set(xlabel=r"Relative cap, $d/\theta$",xlim=(0,1.2),ylim=(0,1))
        ax.set_title(title,loc="left",pad=8)
        ax.set_xticks([0,.3,.6,.9,1.2]);ax.set_yticks([0,.25,.5,.75,1])
    axes[0].set_ylabel(r"Timely review probability, $q$")
    fig.text(.5,.93,r"Matched costs: $b/\theta=0.20$, $\eta/\theta^2=0.10$, $\kappa/\theta^2=0.05$",
             ha="center",fontsize=9)
    labels=["No request; no strict user benefit","No request; user would benefit",
            "Requested; user benefits","Requested; user harmed",
            "Requested; user indifferent"]
    fig.legend([Patch(facecolor=c) for c in COLORS],labels,loc="lower center",
               bbox_to_anchor=(.5,.015),ncol=2,frameon=False,columnspacing=1.5,
               handlelength=1.2,handletextpad=.5,fontsize=8.2)
    fig.text(.5,.215,"Solid: agent indifference. Dashed: user indifference. Agent ties retain autonomy.",
             ha="center",fontsize=8.2)
    main=export(fig,output,"case-a-cancellation-fallback")

    s=DESIGN["cost_sensitivity"]
    e=np.linspace(0,s["agent_cost_max"],s["cost_points"])
    k=np.linspace(0,s["user_cost_max"],s["cost_points"])
    K,E=np.meshgrid(k,e);t,b,d=s["theta"],s["bias"],s["cap"]
    auto=(t-d)**2;m=(t-d)*(t-d+2*b)
    widths={}
    with (output/"cost-sensitivity.csv").open("w",newline="") as stream:
        w=csv.writer(stream);w.writerow(["policy","user_cost","agent_cost","agent_threshold",
                                        "user_threshold","harmful_interval_width","beneficial_review_declined_width"])
        for policy in ("CANCEL","FALLBACK"):
            qa=(2*d*(t+b)-d*d+E)/(t*(t+2*b)) if policy=="CANCEL" else E/m
            qp=(2*d*t-d*d+K)/(t*t) if policy=="CANCEL" else K/auto
            widths[policy]=interval(qa,qp)
            missed=interval(qp,qa)
            for j in range(K.size):
                w.writerow([policy,float(K.ravel()[j]),float(E.ravel()[j]),float(qa.ravel()[j]),
                            float(qp.ravel()[j]),float(widths[policy].ravel()[j]),float(missed.ravel()[j])])
    fig,axes=plt.subplots(1,2,figsize=(7,3.15))
    fig.subplots_adjust(left=.09,right=.88,bottom=.23,top=.80,wspace=.24)
    maximum=max(float(x.max()) for x in widths.values())
    for ax,policy,title in zip(axes,["CANCEL","FALLBACK"],["(a) Cancellation","(b) Capped fallback"]):
        im=ax.pcolormesh(K,E,widths[policy],cmap="RdPu",vmin=0,vmax=maximum,shading="nearest",rasterized=True)
        ax.set_title(title,loc="left");ax.set_xlabel(r"User review cost, $\kappa/\theta^2$")
        ax.set_xticks([0,.1,.2,.3]);ax.set_yticks([0,.1,.2,.3])
    axes[0].set_ylabel(r"Agent review cost, $\eta/\theta^2$")
    cax=fig.add_axes([.91,.23,.018,.57]);cb=fig.colorbar(im,cax=cax)
    cb.set_label("Harmful interval width",fontsize=8.5)
    fig.text(.5,.94,r"Cost sensitivity at $d/\theta=0.5$ and $b/\theta=0.2$",ha="center",fontsize=9)
    fig.text(.5,.035,"Widths are lengths of feasible q intervals, not observed transaction frequencies.",
             ha="center",fontsize=8.2)
    supplementary=export(fig,output,"case-a-cost-sensitivity")
    return [main,supplementary]


def run(output):
    output=Path(output);output.mkdir(parents=True,exist_ok=True)
    checks=verify()
    X,Q,results=write_grid(output)
    cfg=DESIGN["counterexample"]
    examples={}
    for policy in ("CANCEL","FALLBACK"):
        r=evaluate(cfg["theta"],cfg["bias"],cfg["cap"],cfg["timely_probability"],
                   cfg["agent_cost"],cfg["user_cost"],policy)
        examples[policy]={key:(bool(value) if np.asarray(value).dtype==bool else float(value))
                          for key,value in r.items() if key!="region"}
        examples[policy]["region"]=REGIONS[int(r["region"])]
    if not (examples["FALLBACK"]["review_requested"]
            and examples["FALLBACK"]["user_review_loss"]>examples["FALLBACK"]["user_autonomy_loss"]):
        raise AssertionError("Costly fallback counterexample")
    summary={"design":DESIGN,"counterexample":examples,
             "decision_grid_rows":int(2*X.size),
             "cost_sensitivity_rows":2*DESIGN["cost_sensitivity"]["cost_points"]**2,
             "interpretation":"No distribution over transaction parameters is assumed. These grid rows are not independent observations."}
    dump(output/"summary.json",summary)
    specs=figures(output,X,Q,results)
    dump(output/"validation.json",{"verification":checks,"figures":specs,
                                  "python":platform.python_version(),"passed":True})
    return checks


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",type=Path,required=True)
    args=parser.parse_args()
    print(json.dumps(run(args.output),indent=2))
