"""Independent exact oracle: enumerate complete contingent actions and events.

No production transition, Bellman, or forward function is imported.
"""
from fractions import Fraction as F
from itertools import product


def parameters(config):
    return {k:(v if isinstance(v,F) else F(str(v))) if k not in ("policy","horizon") else v
            for k,v in config.items()}


def worlds(p,state,success,submit):
    # Independent Bernoulli enumeration, including zero-probability worlds.
    for delivered,audited,complaint in product((False,True),repeat=3):
        delivery_probability=(1-p["epsilon"]) if submit else F(0)
        audit_probability=p["rho"] if p["policy"] in ("STRICT","HOLD") else F(0)
        complaint_probability=p["rho"] if p["policy"]=="COMPLAINT" and not success else F(0)
        weight=(delivery_probability if delivered else 1-delivery_probability)
        weight*=audit_probability if audited else 1-audit_probability
        weight*=complaint_probability if complaint else 1-complaint_probability
        if weight==0:
            continue
        result=state
        if p["policy"] in ("STRICT","HOLD"):
            if audited and delivered:
                result="G" if success else "B"
            elif audited and not delivered and p["policy"]=="STRICT":
                result="B"
        elif delivered:
            result="G" if success else "B"
        if complaint:
            result="B"
        bad_success=p["policy"]=="STRICT" and audited and success and submit and not delivered
        yield weight,result,bad_success,bad_success and state=="G"


def solve_and_forward(config):
    p=parameters(config)
    event_tree={(s,o,r):tuple(worlds(p,s,o,r))
                for s,o,r in product(("G","B"),(True,False),(True,False))}
    values=[{"G":F(0),"B":F(0)}];actions=[{}]
    for h in range(1,p["horizon"]+1):
        new={};chosen={}
        for state in ("G","B"):
            options=[]
            # Iteration order implements the declared lexicographic tie rules.
            for effort,success_report,failure_report in product(("L","H"),(True,False),(False,True)):
                success_probability=p["p_high"] if effort=="H" else p["p_low"]
                future=F(0)
                for success,prob,report in ((True,success_probability,success_report),
                                            (False,1-success_probability,failure_report)):
                    for weight,dest,_,_ in event_tree[state,success,report]:
                        future+=prob*weight*values[-1][dest]
                value=(p["revenue_g"] if state=="G" else p["revenue_b"])
                value-=p["high_cost"] if effort=="H" else 0
                value+=p["discount"]*future
                options.append((value,effort,success_report,failure_report))
            best=max(x[0] for x in options)
            selected=next(x for x in options if x[0]==best)
            new[state]=best;chosen[state]=selected[1:]
        values.append(new);actions.append(chosen)
    paths={}
    for initial in ("G","B"):
        dist={"G":F(initial=="G"),"B":F(initial=="B")}
        high=F(0);successes=F(0);bad=F(0);downgrade=F(0);payoff=F(0)
        rounds=[]
        for t,h in enumerate(range(p["horizon"],0,-1)):
            new={"G":F(0),"B":F(0)}
            step_high=F(0);step_success=F(0);step_bad=F(0);step_downgrade=F(0)
            for state,mass in dist.items():
                effort,rs,rf=actions[h][state]
                prob=p["p_high"] if effort=="H" else p["p_low"]
                step_high+=mass*(effort=="H");step_success+=mass*prob
                payoff+=p["discount"]**t*mass*((p["revenue_g"] if state=="G" else p["revenue_b"])
                                               -(p["high_cost"] if effort=="H" else 0))
                for success,pr,report in ((True,prob,rs),(False,1-prob,rf)):
                    for weight,dest,error,down in event_tree[state,success,report]:
                        new[dest]+=mass*pr*weight
                        step_bad+=mass*pr*weight*error
                        step_downgrade+=mass*pr*weight*down
            if sum(new.values())!=1:
                raise AssertionError("Oracle mass")
            high+=step_high;successes+=step_success;bad+=step_bad;downgrade+=step_downgrade
            rounds.append({"high_effort":step_high,"success":step_success,
                           "successful_task_bad_update_due_to_loss":step_bad,
                           "successful_G_to_B_due_to_loss":step_downgrade,
                           "state_at_end":new.copy()})
            dist=new
        if payoff!=values[-1][initial]:
            raise AssertionError("Oracle control/payoff")
        paths[initial]={"high_effort":high/p["horizon"],"success":successes/p["horizon"],
                        "successful_task_bad_update_due_to_loss":bad/p["horizon"],
                        "successful_G_to_B_due_to_loss":downgrade/p["horizon"],
                        "final_state":dist,"rounds":rounds}
    return values,actions,paths
