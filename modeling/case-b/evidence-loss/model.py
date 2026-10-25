"""Exact seller-control recursion with independent certificate delivery loss."""
from dataclasses import dataclass, asdict
from fractions import Fraction as F
from itertools import product

STATES = ("G", "B")
EFFORTS = ("L", "H")
REPORTS = (True, False)
POLICIES = ("STRICT", "HOLD", "VOLUNTARY", "COMPLAINT")


def frac(value):
    return value if isinstance(value, F) else F(str(value))


@dataclass(frozen=True)
class Config:
    policy: str
    rho: F = F(1,4)
    epsilon: F = F(0)
    horizon: int = 8
    high_cost: F = F(3,20)
    discount: F = F(19,20)
    revenue_g: F = F(1)
    revenue_b: F = F(2,5)
    p_high: F = F(9,10)
    p_low: F = F(3,10)

    def __post_init__(self):
        for name in ("rho","epsilon","high_cost","discount","revenue_g","revenue_b","p_high","p_low"):
            object.__setattr__(self,name,frac(getattr(self,name)))
        if self.policy not in POLICIES:
            raise ValueError("Unknown policy")
        if any(not 0<=getattr(self,k)<=1 for k in ("rho","epsilon","discount","p_high","p_low")):
            raise ValueError("Probability or discount outside [0,1]")
        if (self.high_cost<0 or not self.revenue_g>=self.revenue_b>=0
                or self.p_high<self.p_low or not isinstance(self.horizon,int)
                or isinstance(self.horizon,bool) or self.horizon<1):
            raise ValueError("Invalid seller-control parameters")

    def numbers(self):
        return {k:(float(v) if isinstance(v,F) else v) for k,v in asdict(self).items()}


def transition(cfg, state, success, report):
    """Closed-form reputation transition, conditional on a reporting decision."""
    if state not in STATES:
        raise ValueError("Unknown state")
    available=(1-cfg.epsilon) if report else F(0)
    cert="G" if success else "B"
    dist={s:F(0) for s in STATES}
    if cfg.policy in ("STRICT","HOLD"):
        missing="B" if cfg.policy=="STRICT" else state
        dist[state]+=1-cfg.rho
        dist[cert]+=cfg.rho*available
        dist[missing]+=cfg.rho*(1-available)
    else:
        dist[cert]+=available
        dist[state]+=1-available
        if cfg.policy=="COMPLAINT" and not success:
            dist={s:(1-cfg.rho)*p for s,p in dist.items()}
            dist["B"]+=cfg.rho
    if sum(dist.values())!=1 or any(p<0 for p in dist.values()):
        raise AssertionError("Invalid transition probabilities")
    return dist


def solve(cfg):
    values=[{s:F(0) for s in STATES}]
    decisions=[{}]
    transitions={(s,o,r):transition(cfg,s,o,r)
                 for s,o,r in product(STATES,(True,False),REPORTS)}
    for h in range(1,cfg.horizon+1):
        current={};row={};prev=values[-1]
        for s in STATES:
            report_values={};chosen={};report_optimal={}
            for success in (True,False):
                scores={report:sum(prob*prev[dest] for dest,prob in transitions[s,success,report].items())
                        for report in REPORTS}
                best=max(scores.values())
                report_optimal[success]=[r for r in REPORTS if scores[r]==best]
                preference=success
                chosen[success]=preference if preference in report_optimal[success] else report_optimal[success][0]
                report_values[success]=scores
            utility={}
            for effort in EFFORTS:
                p=cfg.p_high if effort=="H" else cfg.p_low
                future=p*max(report_values[True].values())+(1-p)*max(report_values[False].values())
                utility[effort]=(cfg.revenue_g if s=="G" else cfg.revenue_b)-(cfg.high_cost if effort=="H" else 0)+cfg.discount*future
            best=max(utility.values())
            effort_optimal=[e for e in EFFORTS if utility[e]==best]
            effort=effort_optimal[0]  # L is first, so exact ties retain low effort.
            current[s]=best
            row[s]={"effort":effort,"optimal_efforts":effort_optimal,"utility":utility,
                    "report":chosen,"optimal_reports":report_optimal,"report_values":report_values}
        values.append(current);decisions.append(row)
    return {"values":values,"decisions":decisions}


METRICS = (
    "high_effort","success","submitted_evidence","received_evidence",
    "monitored_tasks","selected_received_evidence","selected_missing_evidence",
    "selected_strategic_missing","selected_accidental_missing",
    "missing_bad_updates","successful_task_bad_update_due_to_loss",
    "successful_G_to_B_due_to_loss","complaints","G_at_start",
)


def events(cfg, state, success, report):
    """Physical event enumeration for forward metrics, separate from transition()."""
    deliveries=[(False,F(1))] if not report else [(True,1-cfg.epsilon),(False,cfg.epsilon)]
    draws=[(True,cfg.rho),(False,1-cfg.rho)] if cfg.policy in ("STRICT","HOLD") else [(False,F(1))]
    complaint_draws=[(True,cfg.rho),(False,1-cfg.rho)] if cfg.policy=="COMPLAINT" and not success else [(False,F(1))]
    rows=[]
    for (received,pd),(audited,pa),(complaint,pc) in product(deliveries,draws,complaint_draws):
        probability=pd*pa*pc
        if probability==0:
            continue
        missing=not received
        loss=report and not received
        if cfg.policy in ("STRICT","HOLD"):
            dest=state
            if audited:
                dest=("G" if success else "B") if received else ("B" if cfg.policy=="STRICT" else state)
        else:
            dest=("G" if success else "B") if received else state
            if complaint:
                dest="B"
        adverse=cfg.policy=="STRICT" and audited and success and loss
        rows.append({
            "probability":probability,"state":dest,
            "received_evidence":received,"monitored_tasks":audited,
            "selected_received_evidence":audited and received,
            "selected_missing_evidence":audited and missing,
            "selected_strategic_missing":audited and not report,
            "selected_accidental_missing":audited and loss,
            "missing_bad_updates":cfg.policy=="STRICT" and audited and missing,
            "successful_task_bad_update_due_to_loss":adverse,
            "successful_G_to_B_due_to_loss":adverse and state=="G",
            "complaints":complaint,
        })
    if sum(x["probability"] for x in rows)!=1:
        raise AssertionError("Event probability mass")
    return rows


def forward(cfg, solved, initial):
    if initial not in STATES:
        raise ValueError("Unknown initial state")
    dist={s:F(s==initial) for s in STATES}
    totals={k:F(0) for k in METRICS}
    rounds=[];discounted_payoff=F(0)
    physical={(s,o,r):events(cfg,s,o,r) for s,o,r in product(STATES,(True,False),REPORTS)}
    for t,h in enumerate(range(cfg.horizon,0,-1)):
        step={k:F(0) for k in METRICS};step["G_at_start"]=dist["G"]
        new={s:F(0) for s in STATES}
        for state,mass in dist.items():
            decision=solved["decisions"][h][state]
            effort=decision["effort"]
            p=cfg.p_high if effort=="H" else cfg.p_low
            step["high_effort"]+=mass*(effort=="H")
            step["success"]+=mass*p
            discounted_payoff+=cfg.discount**t*mass*((cfg.revenue_g if state=="G" else cfg.revenue_b)
                                                    -(cfg.high_cost if effort=="H" else 0))
            for success,prob in [(True,p),(False,1-p)]:
                report=decision["report"][success]
                step["submitted_evidence"]+=mass*prob*report
                for event in physical[state,success,report]:
                    weight=mass*prob*event["probability"]
                    new[event["state"]]+=weight
                    for key in METRICS:
                        if key not in ("high_effort","success","submitted_evidence","G_at_start"):
                            step[key]+=weight*event[key]
        if sum(new.values())!=1:
            raise AssertionError("Forward probability mass")
        if cfg.policy in ("STRICT","HOLD"):
            if step["selected_received_evidence"]+step["selected_missing_evidence"]!=step["monitored_tasks"]:
                raise AssertionError("Monitoring coverage accounting")
            if step["selected_accidental_missing"]+step["selected_strategic_missing"]!=step["selected_missing_evidence"]:
                raise AssertionError("Missing-evidence decomposition")
        for k,v in step.items():
            totals[k]+=v
        rounds.append({"round":t+1,"remaining":h,"state_at_start":dist.copy(),
                       "state_at_end":new.copy(),**step})
        dist=new
    if discounted_payoff!=solved["values"][cfg.horizon][initial]:
        raise AssertionError("Forward discounted payoff differs from optimized value")
    return {"initial":initial,"rates":{k:v/cfg.horizon for k,v in totals.items()},
            "expected_totals":totals,"final_state":dist,"rounds":rounds,
            "discounted_seller_payoff":discounted_payoff}


def strict_gap(cfg,remaining):
    """Reputation value gap under STRICT, derived from the two Bellman equations."""
    return (cfg.revenue_g-cfg.revenue_b)*sum(
        (cfg.discount*(1-cfg.rho))**j for j in range(remaining))


def plain(value):
    if isinstance(value,F):
        return float(value)
    if isinstance(value,dict):
        return {str(k):plain(v) for k,v in value.items()}
    if isinstance(value,list):
        return [plain(v) for v in value]
    return value
