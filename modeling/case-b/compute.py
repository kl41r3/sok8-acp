#!/usr/bin/env python3
"""Case B: exact finite-horizon control calculation and bounded GLM probes."""
import csv
import hashlib
import itertools
import json
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent
DESIGN = {
    "case": "B",
    "interpretation": "Finite-horizon seller control problem with exogenous state-dependent upfront revenue, not a buyer-seller equilibrium.",
    "revenue": {"G": 1.0, "B": 0.4},
    "success_probability": {"H": 0.9, "L": 0.3},
    "effort_cost": {"H": 0.15, "L": 0.0},
    "discount": 0.95,
    "horizon": 8,
    "policies": {
        "VOLUNTARY": {"rho": 0.0, "rule": "Observe result then report/withhold. Reported success sets G, reported failure sets B, no report holds current state."},
        "OBLIGATED_025": {"rho": 0.25, "rule": "Task pre-registered. Independent audit probability rho. If audited, reported success sets G; failure or withheld evidence sets B. If unaudited, state holds."},
        "OBLIGATED_1": {"rho": 1.0, "rule": "Task pre-registered. Independent audit probability rho. If audited, reported success sets G; failure or withheld evidence sets B. If unaudited, state holds."},
        "COMPLAINT_025": {"rho": 0.25, "rule": "Voluntary certificate rule, plus independently a failed task triggers a complaint setting B with probability rho."},
    },
    "validator": "Perfect and truthful; successful task gets pass, failed task gets fail. Validator reliability is not experimentally estimated.",
    "tie_break": {"effort": "L", "success_report": "REPORT", "failure_report": "WITHHOLD"},
    "llm_cells": {"policies": ["VOLUNTARY", "OBLIGATED_1", "COMPLAINT_025"], "remaining_horizons": [1, 4], "states": ["G", "B"], "draws": 2},
    "llm_probe": "One-step complete-information decisions, exact continuation values supplied. Not multi-round LLM trajectories.",
    "api": {"model": "glm-5.3-flash", "official_china_only": True, "fallback": False, "retries": 0, "stop_on_error": True},
    "seed": 5303002,
    "prompt_revision": 2,
    "revision_reason": "Initial campaign omitted numeric rho in prompt; preserved and excluded. Revised prompt explicitly gives rho before any revision2 live call.",
    "limitations": ["Arbitrary payoff schedule and probabilities are mechanism illustrations, not fitted market estimates.", "Not a full equilibrium or an estimate of deployed ERC-8004 quality.", "No actual ERC-8004 scoring rule is attributed to this simulator.", "Small GLM probe count supports only descriptive agreement/regret.", "No seller identity reset, imperfect verification, direct refund penalty, or price adjustment is modeled."],
}


def dump(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def next_states(policy, state, success, report):
    rho = DESIGN["policies"][policy]["rho"]
    if policy.startswith("OBLIGATED"):
        audited = "G" if success and report == "REPORT" else "B"
        out = {"G": 0.0, "B": 0.0}
        out[state] += 1.0 - rho
        out[audited] += rho
        return out
    voluntary = ("G" if success else "B") if report == "REPORT" else state
    if policy.startswith("COMPLAINT") and not success:
        out = {"G": 0.0, "B": 0.0}
        out[voluntary] += 1.0 - rho
        out["B"] += rho
        return out
    return {"G": float(voluntary == "G"), "B": float(voluntary == "B")}


def continuation(policy, state, success, report, values):
    trans = next_states(policy, state, success, report)
    return sum(trans[s] * values[s] for s in ("G", "B"))


def solve(policy, horizon=8):
    values = [{"G": 0.0, "B": 0.0}]
    decisions = [{}]
    for remaining in range(1, horizon + 1):
        prev = values[-1]
        row, current = {}, {}
        for state in ("G", "B"):
            report_scores = {
                outcome: {r: continuation(policy, state, outcome == "success", r, prev) for r in ("REPORT", "WITHHOLD")}
                for outcome in ("success", "failure")
            }
            report_optimal = {outcome: [r for r, v in scores.items() if abs(v - max(scores.values())) < 1e-10] for outcome, scores in report_scores.items()}
            report_choice = {outcome: ("REPORT" if outcome == "success" else "WITHHOLD") if ("REPORT" if outcome == "success" else "WITHHOLD") in report_optimal[outcome] else report_optimal[outcome][0] for outcome in report_scores}
            utility = {}
            for effort in ("H", "L"):
                p = DESIGN["success_probability"][effort]
                utility[effort] = DESIGN["revenue"][state] - DESIGN["effort_cost"][effort] + DESIGN["discount"] * (p * max(report_scores["success"].values()) + (1 - p) * max(report_scores["failure"].values()))
            optimal_effort = [e for e, u in utility.items() if abs(u - max(utility.values())) < 1e-10]
            effort = "L" if "L" in optimal_effort else "H"
            current[state] = max(utility.values())
            row[state] = {"effort": effort, "utility": utility, "optimal_efforts": optimal_effort, "report": report_choice, "optimal_reports": report_optimal, "report_continuation": report_scores, "continuation_values": prev}
            # Independent exhaustive enumeration over four contingent report maps.
            brute = []
            for e, rs, rf in itertools.product(("H", "L"), ("REPORT", "WITHHOLD"), ("REPORT", "WITHHOLD")):
                p = DESIGN["success_probability"][e]
                brute.append(DESIGN["revenue"][state] - DESIGN["effort_cost"][e] + DESIGN["discount"] * (p * continuation(policy, state, True, rs, prev) + (1-p) * continuation(policy, state, False, rf, prev)))
            assert abs(max(brute) - current[state]) < 1e-10
        values.append(current)
        decisions.append(row)
    return values, decisions


def forward(policy, initial, decisions):
    distribution = {"G": float(initial == "G"), "B": float(initial == "B")}
    totals = {"high_effort": 0.0, "success": 0.0, "submitted_evidence": 0.0, "failure_evidence": 0.0, "observed_task_coverage": 0.0, "detected_failure": 0.0, "missing_evidence_penalty": 0.0, "G_at_start": 0.0}
    rows = []
    for t in range(DESIGN["horizon"]):
        remaining = DESIGN["horizon"] - t
        nxt = {"G": 0.0, "B": 0.0}
        step = {key: 0.0 for key in totals}
        step["G_at_start"] = distribution["G"]
        for state, mass in distribution.items():
            decision = decisions[remaining][state]
            effort = decision["effort"]
            p = DESIGN["success_probability"][effort]
            step["high_effort"] += mass * (effort == "H")
            step["success"] += mass * p
            for success, prob in ((True, p), (False, 1-p)):
                report = decision["report"]["success" if success else "failure"]
                step["submitted_evidence"] += mass * prob * (report == "REPORT")
                step["failure_evidence"] += mass * prob * (report == "REPORT" and not success)
                rho = DESIGN["policies"][policy]["rho"]
                if policy.startswith("OBLIGATED"):
                    coverage = rho
                    detected_failure = rho if not success else 0.0
                    missing = rho if report == "WITHHOLD" else 0.0
                elif policy.startswith("COMPLAINT"):
                    coverage = 1.0 if report == "REPORT" else rho if not success else 0.0
                    detected_failure = coverage if not success else 0.0
                    missing = 0.0
                else:
                    coverage = float(report == "REPORT")
                    detected_failure = coverage if not success else 0.0
                    missing = 0.0
                step["observed_task_coverage"] += mass * prob * coverage
                step["detected_failure"] += mass * prob * detected_failure
                step["missing_evidence_penalty"] += mass * prob * missing
                for new_state, trans_prob in next_states(policy, state, success, report).items():
                    nxt[new_state] += mass * prob * trans_prob
        assert abs(sum(nxt.values()) - 1.0) < 1e-10
        for key, val in step.items():
            totals[key] += val
        rows.append({"round": t+1, "remaining": remaining, "state_at_start": distribution, **step, "state_at_end": nxt})
        distribution = nxt
    return {"initial": initial, "expected_totals": totals, "rates": {k: v / DESIGN["horizon"] for k, v in totals.items()}, "final_state": distribution, "rounds": rows}



def calculate():
    theory={"policies":{}}
    for policy in DESIGN["policies"]:
        values,decisions=solve(policy)
        theory["policies"][policy]={"values":values,"decisions":decisions,"forward":{s:forward(policy,s,decisions) for s in ("G","B")}}
    return theory

if __name__=="__main__":
    print(json.dumps(calculate(),indent=2))
