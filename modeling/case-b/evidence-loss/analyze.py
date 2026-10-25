#!/usr/bin/env python3
"""Generate and independently verify Case B evidence-availability experiments."""
from dataclasses import asdict
from fractions import Fraction as F
from pathlib import Path
import argparse
import csv
import json
import sys
import sympy as sp
from model import Config, STATES, solve, forward, strict_gap, plain
from oracle import solve_and_forward

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parents[1]/"extensions"))
from plot_style import dump

DESIGN=json.loads((ROOT/"design.json").read_text())


def csv_write(path,rows):
    if not rows:
        raise ValueError("Empty scientific dataset")
    with path.open("w",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)


def verify_config(cfg,solved,paths):
    values,actions,references=solve_and_forward(asdict(cfg))
    cells=0
    for h in range(1,cfg.horizon+1):
        for state in STATES:
            if solved["values"][h][state]!=values[h][state]:
                raise AssertionError(("Independent rational value",cfg,h,state))
            d=solved["decisions"][h][state]
            if (d["effort"],d["report"][True],d["report"][False])!=actions[h][state]:
                raise AssertionError(("Independent rational choices",cfg,h,state))
            if cfg.policy=="STRICT":
                gap=strict_gap(cfg,h)
                if values[h]["G"]-values[h]["B"]!=gap:
                    raise AssertionError("Closed-form reputation gap")
                predicted=-cfg.high_cost+cfg.discount*cfg.rho*(1-cfg.epsilon)*(cfg.p_high-cfg.p_low)*strict_gap(cfg,h-1)
                if d["utility"]["H"]-d["utility"]["L"]!=predicted:
                    raise AssertionError("Closed-form effort incentive")
            if cfg.policy=="HOLD" and state=="G" and d["effort"]!="L":
                raise AssertionError("Absorbing good reputation under seller-controlled withholding")
            if h==1 and d["effort"]!="L":
                raise AssertionError("Terminal effort and tie rule")
            cells+=1
    for initial in STATES:
        actual=paths[initial];reference=references[initial]
        for key in ("high_effort","success","successful_task_bad_update_due_to_loss","successful_G_to_B_due_to_loss"):
            if actual["rates"][key]!=reference[key]:
                raise AssertionError(("Independent exact forward rate",cfg,initial,key))
        if actual["final_state"]!=reference["final_state"]:
            raise AssertionError("Independent exact final-state distribution")
        for x,y in zip(actual["rounds"],reference["rounds"]):
            for key in ("high_effort","success","successful_task_bad_update_due_to_loss","successful_G_to_B_due_to_loss","state_at_end"):
                if x[key]!=y[key]:
                    raise AssertionError("Independent exact round path")
        if actual["rates"]["success"]!=cfg.p_low+(cfg.p_high-cfg.p_low)*actual["rates"]["high_effort"]:
            raise AssertionError("Effort/success accounting")
        if cfg.policy=="HOLD" and initial=="G":
            if actual["rates"]["high_effort"]!=0 or actual["final_state"]["G"]!=1:
                raise AssertionError("State-preserving rule from G")
    return cells


def check_baselines():
    saved=json.loads((ROOT.parent/"data/theory.json").read_text())
    aliases=[("VOLUNTARY","VOLUNTARY",F(0)),("OBLIGATED_025","STRICT",F(1,4)),
             ("OBLIGATED_1","STRICT",F(1)),("COMPLAINT_025","COMPLAINT",F(1,4))]
    cells=0
    rates=[]
    for old,policy,rho in aliases:
        cfg=Config(policy,rho=rho,epsilon=0);solved=solve(cfg)
        paths={s:forward(cfg,solved,s) for s in STATES}
        cells+=verify_config(cfg,solved,paths)
        reference=saved["policies"][old]
        for h in range(1,9):
            for s in STATES:
                if abs(float(solved["values"][h][s])-reference["values"][h][s])>1e-10:
                    raise AssertionError("Original control value")
                x=solved["decisions"][h][s];y=reference["decisions"][h][s]
                if x["effort"]!=y["effort"]:
                    raise AssertionError("Original effort")
                if (x["report"][True],x["report"][False])!=(y["report"]["success"]=="REPORT",y["report"]["failure"]=="REPORT"):
                    raise AssertionError("Original reporting")
        for s in STATES:
            for metric in ("high_effort","success"):
                if abs(float(paths[s]["rates"][metric])-reference["forward"][s]["rates"][metric])>1e-10:
                    raise AssertionError("Original forward expectation")
            for dest in STATES:
                if abs(float(paths[s]["final_state"][dest])-reference["forward"][s]["final_state"][dest])>1e-10:
                    raise AssertionError("Original terminal state")
        rates.append({"policy":old,"high_effort_share":float(paths["G"]["rates"]["high_effort"]),
                      "task_success":float(paths["G"]["rates"]["success"])})
    return {"original_control_cells_recovered":cells,"original_forward_paths_recovered":8,"original_rates":rates}


def symbolic_checks():
    g,b,rho,eps,ph,pl,delta,cost,vg,vb=sp.symbols("R_G R_B rho epsilon p_H p_L delta c V_G V_B")
    def future(revenue,p):
        # Difference in current state affects only the unmonitored branch.
        current=vg if revenue==g else vb
        return (1-rho)*current+rho*((1-eps)*p*vg+(1-(1-eps)*p)*vb)
    checks=[
        (g+delta*future(g,ph))-(b+delta*future(b,ph))
        -((g-b)+delta*(1-rho)*(vg-vb)),
        (g-cost+delta*future(g,ph))-(g+delta*future(g,pl))
        -(-cost+delta*rho*(1-eps)*(ph-pl)*(vg-vb)),
    ]
    for expression in checks:
        if sp.simplify(expression)!=0:
            raise AssertionError("Case B symbolic identity")
    return len(checks)


def run(output):
    output=Path(output);output.mkdir(parents=True,exist_ok=True)
    declared=DESIGN
    defaults=Config("STRICT")
    if (defaults.revenue_g,defaults.revenue_b,defaults.p_high,defaults.p_low,
            defaults.high_cost,defaults.discount,defaults.horizon)!=(
            F(str(declared["revenue"]["G"])),F(str(declared["revenue"]["B"])),
            F(str(declared["success_probability"]["H"])),F(str(declared["success_probability"]["L"])),
            F(str(declared["effort_cost"]["H"])),F(str(declared["discount"])),declared["horizon"]):
        raise AssertionError("Design and implementation defaults disagree")
    if (declared["effort_cost"]["L"]!=0 or declared["main_grid"]["rho_min"]!=0
            or declared["main_grid"]["rho_max"]!=1 or declared["main_grid"]["epsilon_min"]!=0
            or declared["main_grid"]["epsilon_max"]!=1):
        raise AssertionError("Unsupported design domain")
    baseline=check_baselines()
    symbolic=symbolic_checks()
    cache={};controls=[];round_rows=[];representatives={}
    counts={"independent_control_cells":0,"independent_forward_paths":0,"independent_round_paths":0}
    selected={
        Config(p,rho=r,epsilon=e)
        for p in ("STRICT","HOLD") for r in (F(1,4),F(1))
        for e in (F(0),F(1,10),F(3,5))
    }

    def experiment(cfg):
        if cfg in cache:
            return cache[cfg]
        run_id=f"B{len(cache)+1:04d}"
        solved=solve(cfg);paths={s:forward(cfg,solved,s) for s in STATES}
        cells=verify_config(cfg,solved,paths)
        counts["independent_control_cells"]+=cells
        counts["independent_forward_paths"]+=2
        counts["independent_round_paths"]+=2*cfg.horizon
        for h in range(1,cfg.horizon+1):
            for state in STATES:
                d=solved["decisions"][h][state]
                controls.append({"run_id":run_id,**cfg.numbers(),"remaining":h,"state":state,
                                 "value":float(solved["values"][h][state]),"effort":d["effort"],
                                 "success_report":"REPORT" if d["report"][True] else "WITHHOLD",
                                 "failure_report":"REPORT" if d["report"][False] else "WITHHOLD",
                                 "effort_gain_exact":str(d["utility"]["H"]-d["utility"]["L"]),
                                 "value_exact":str(solved["values"][h][state])})
        rows=[]
        for initial in STATES:
            result=paths[initial]
            rows.append({"run_id":run_id,**cfg.numbers(),"initial":initial,
                         **{k:float(v) for k,v in result["rates"].items()},
                         "final_G_probability":float(result["final_state"]["G"]),
                         "discounted_seller_payoff":float(result["discounted_seller_payoff"])})
            for step in result["rounds"]:
                round_rows.append({"run_id":run_id,"initial":initial,"round":step["round"],
                                   "remaining":step["remaining"],
                                   "G_at_end":float(step["state_at_end"]["G"]),
                                   **{k:float(step[k]) for k in result["rates"]}})
        cache[cfg]=rows
        if cfg in selected:
            representatives[run_id]={"config":cfg.numbers(),"solution":plain(solved),"paths":plain(paths)}
        if len(cache)%100==0:
            print(f"Independently verified {len(cache)} exact Case B configurations.",flush=True)
        return rows

    main=[];n_rho=DESIGN["main_grid"]["rho_points"];n_eps=DESIGN["main_grid"]["epsilon_points"]
    for policy in ("STRICT","HOLD"):
        for i in range(n_rho):
            for j in range(n_eps):
                main.extend(experiment(Config(policy,rho=F(i,n_rho-1),epsilon=F(j,n_eps-1))))
    supporting=[]
    grid=DESIGN["supporting_sensitivity"]
    for policy in ("STRICT","HOLD"):
        for h in grid["horizons"]:
            for c in grid["high_effort_costs"]:
                for rho in grid["rho"]:
                    for eps in grid["epsilon"]:
                        supporting.extend(experiment(Config(policy,rho=rho,epsilon=eps,horizon=h,high_cost=c)))

    # Exact equality at the full-monitoring effort threshold: low effort at ties.
    threshold_cfg=Config("STRICT",rho=1,epsilon=F(32,57))
    threshold_solution=solve(threshold_cfg)
    threshold_paths={s:forward(threshold_cfg,threshold_solution,s) for s in STATES}
    threshold_cells=verify_config(threshold_cfg,threshold_solution,threshold_paths)
    for h in range(2,9):
        if threshold_solution["decisions"][h]["G"]["utility"]["H"]!=threshold_solution["decisions"][h]["G"]["utility"]["L"]:
            raise AssertionError("Exact effort threshold tie")
    for policy in ("STRICT","HOLD"):
        # Cost-free, no-continuation and equal-revenue boundaries.
        for cfg in [Config(policy,high_cost=0),Config(policy,discount=0),
                    Config(policy,revenue_g=F(2,5),revenue_b=F(2,5))]:
            experiment(cfg)
    # A received certificate stays truthful; this is an availability example.
    availability_example={"condition":"Fixed high effort, full monitoring, epsilon=0.1; not an optimized one-round policy",
                          "true_success":.9,"true_failure":.1,"received_success":.81,
                          "successful_evidence_lost":.09,"strict_bad_updates":.19}
    if F(9,10)*F(1,10)!=F(9,100):
        raise AssertionError("Availability example")

    csv_write(output/"main-grid.csv",main)
    csv_write(output/"cost-horizon-sensitivity.csv",supporting)
    csv_write(output/"control-cells.csv",controls)
    csv_write(output/"round-paths.csv",round_rows)
    dump(output/"representative-solutions.json",representatives)
    examples=[]
    for policy,rho,eps in [
        ("STRICT",F(1,4),F(0)),("STRICT",F(1,4),F(1,10)),
        ("STRICT",F(1),F(1,10)),("STRICT",F(1),F(1,2)),("STRICT",F(1),F(3,5)),
        ("HOLD",F(1),F(1,10)),
    ]:
        examples.extend(row for row in cache[Config(policy,rho=rho,epsilon=eps)] if row["initial"]=="G")
    summary={
        "design":DESIGN,"baseline":baseline,"selected_examples":examples,
        "availability_example":availability_example,
        "strict_full_monitoring_threshold":{
            "epsilon_exact":"32/57","epsilon":float(F(32,57)),
            "condition":"For the stated default payoffs and every remaining horizon >=2, high effort iff epsilon<32/57; equality selects L. Final-round effort is always L.",
        },
        "strict_closed_form":{
            "value_gap":"Delta V_n = (R_G-R_B) * sum_{j=0}^{n-1} [delta*(1-rho)]^j",
            "effort_gain":"-c + delta*rho*(1-epsilon)*(p_H-p_L)*Delta V_(n-1)",
            "scope":"STRICT only, fixed state revenues, costless truthful certification, independent hidden draws and current timing.",
        },
        "state_preserving_rule":{
            "condition":"From G, optimal withholding keeps the maximum-revenue state absorbing; L is optimal at every horizon. Initial B is separately solved.",
            "scope":"Does not include direct performance-contingent payments, external complaints or other penalties.",
        },
        "main_grid_rows":len(main),"supporting_rows":len(supporting),
        "unique_configurations":len(cache),
        "claim_limits":"Success, effort, and erroneous updates are separate outcomes. No market-welfare or globally optimal missing-evidence rule is estimated.",
    }
    dump(output/"summary.json",summary)
    checks={"symbolic_identities":symbolic,**baseline,**counts,
            "unique_exact_configurations":len(cache),
            "exact_full_monitoring_threshold_tie_cells":threshold_cells,
            "all_policy_comparisons_exact":True,"passed":True}
    dump(output/"validation.json",checks)
    from plot import plot
    specs=plot(output,output)
    checks["figures"]=specs;dump(output/"validation.json",checks)
    return checks


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",type=Path,required=True)
    args=parser.parse_args()
    print(json.dumps(run(args.output),indent=2))
