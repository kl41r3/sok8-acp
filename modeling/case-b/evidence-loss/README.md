# Case B extension: truthful evidence that becomes unavailable

The original four-policy model in ../ is preserved byte for byte.
This extension changes evidence availability, retains truthful
certification, and recomputes effort and contingent reporting.

## Timing and policies

1. A task is registered. The seller knows the rule, monitoring probability
   rho, evidence-loss probability epsilon and remaining horizon.
2. Reputation fixes upfront revenue: R_G=1 or R_B=0.4. The seller chooses
   H (cost 0.15, success probability 0.9) or L (cost 0, success 0.3).
3. The seller observes the outcome and submits its truthful certificate
   or withholds it.
4. Submitted evidence independently becomes unavailable with probability
   epsilon. Received certificates remain accurate.
5. The independent monitoring draw is revealed after effort and reporting;
   reputation is updated.

Effort and reporting cannot depend on realized loss or monitoring.
Evidence production is costless; loss is exogenous and outcome-independent.
Discount is 0.95, baseline horizon eight rounds, and terminal value zero.

| Event | STRICT | HOLD |
|---|---|---|
| Monitored, received success | G | G |
| Monitored, received failure | B | B |
| Monitored, missing certificate | B | Prior state |
| Unmonitored task | Prior state | Prior state |

Both rules use matched timing and parameters. They are hypothetical,
not attributed to deployed protocols. VOLUNTARY and COMPLAINT remain
implemented to recover all four original policies at epsilon=0.

## Conditional analytical results

Let V_n(s) be optimal discounted seller payoff with n rounds remaining,
and Delta V_n = V_n(G)-V_n(B). Under STRICT, success is submitted and
failure withheld (also the reporting convention at indifference).
For each effort, current states differ only in current revenue and the
unmonitored continuation term. Thus maximizing effort is identical in
the two states, and:

    Delta V_n = (R_G-R_B) + delta(1-rho) Delta V_(n-1)
              = (R_G-R_B) sum_{j=0}^{n-1} [delta(1-rho)]^j.

High effort has advantage:

    -c + delta rho (1-epsilon) (p_H-p_L) Delta V_(n-1).

H is chosen only if this is strictly positive. With baseline payoffs
and full monitoring, every n >= 2 selects H iff epsilon < 32/57
(approximately 0.5614). Equality selects L. The final round always
selects L because current revenue is already fixed and continuation
value is zero; that terminal effect is not attributed to disclosure.

Under HOLD from G, withholding failure preserves the highest-revenue
state. L attains the upper bound on revenue net of nonnegative cost,
so it is optimal at every horizon. This need not apply from B, which
is solved separately, or with performance-contingent payments,
complaints or additional sanctions.

## Numerical comparison

Eight-round expectations from G, other payoffs fixed:

| Rule | rho | epsilon | H share | Actual success | Successful-task bad updates caused by loss |
|---|---:|---:|---:|---:|---:|
| STRICT | 1 | 0 | 87.5% | 82.5% | 0% |
| STRICT | 1 | 0.1 | 87.5% | 82.5% | 8.25% |
| STRICT | 1 | 0.5 | 87.5% | 82.5% | 41.25% |
| STRICT | 1 | 0.6 | 0% | 30% | 18% |
| HOLD | 1 | 0.1 | 0% | 30% | 0% |

All percentages use all tasks as denominator. Fewer adverse updates can
reflect fewer successful tasks rather than better evidence handling.
These are exact model expectations, not Monte Carlo or empirical rates.

The output separates actual success from favorable evidence, strategic
withholding from accidental loss, and successful-task adverse updates
from actual G-to-B downgrades. A loss-induced bad update can occur when
the prior state is already B; a downgrade additionally requires prior G.
Monitoring coverage equals selected received plus selected missing
evidence. Missing evidence is decomposed into strategic and accidental
components. All rates are expected totals divided by horizon, not
conditioned on success or monitoring.

## Reproduction and verification

From the repository root:

    python -B modeling/case-b/evidence-loss/analyze.py --output outputs/case-b-evidence-loss

model.py uses exact Fraction arithmetic. oracle.py imports no production
functions: it independently enumerates eight effort/contingent-report
choices and Bernoulli event trees. Every saved configuration is checked
for identical values, effort, reports, both initial-state paths,
per-round core metrics and final-state probabilities. Forward discounted
payoffs must equal optimized values.

Exact ties choose L, report success and withhold failure. The reporting
convention affects evidence counts even where effort and payoff agree.

The main grid has 21 monitoring values x 21 loss values x two rules:
882 configurations and 1,764 rows for both initial states. Supporting
sensitivity crosses horizons {1,4,8,16}, costs {0.05,0.15,0.30},
monitoring {0.25,1} and loss {0,0.1,0.3,0.6}: 192 configurations and
384 rows, partly overlapping the main grid.
After deduplication and extra boundaries, 1,064 configurations,
16,736 control cells and 2,128 forward paths are independently checked.
An extra 16 cells verify the exact epsilon=32/57 tie. The 64 original
control cells and eight original paths are recovered separately.

Frozen extension outputs are in results/:

| File | Meaning |
|---|---|
| main-grid.csv | Both rules and initial states across rho and epsilon |
| cost-horizon-sensitivity.csv | Cost and horizon robustness |
| control-cells.csv | Values, exact rational gains, effort and reports |
| round-paths.csv | Per-round metrics and state probabilities |
| representative-solutions.json | Full solutions for 12 selected configurations |
| summary.json | Design, examples, identities and limits |
| validation.json | Exact checks and figure specifications |
| case-b-evidence-availability.pdf/svg/png | Success and loss-induced bad updates |
| case-b-effort-sensitivity.pdf/svg/png | Effort, cost and horizon comparisons |

Figures are seven inches wide with fonts of at least eight points and
vector text. Use full text width. Lines connect discrete sensitivity
samples; the full-monitoring threshold is derived and checked separately.

## Limits

Loss can weaken STRICT's continuation incentive and penalize successful
tasks despite truthful certification. HOLD avoids those adverse updates
but preserves selective withholding from G. This is a tradeoff, not a
welfare ranking or an optimal missing-evidence rule.

Fixed revenues, horizon, identity and independent hidden monitoring are
assumptions. Buyer participation, endogenous prices, audit and evidence
costs, appeals, retries, seller exit, identity reset and strategic outages
are absent. Institutional remedies need further modeling and evidence.
No claim is made about actual LLM behavior, equilibrium marketplace
outcomes, or deployed protocol effectiveness.

## Final manuscript layouts

The seven-inch plots above are diagnostic exports. The four final,
caption-free one-column layouts are in `figures/modeling/` at the repository
root, with editable SVGs and PNGs in its `previews/` directory. Regenerate
them using `python -B modeling/figures/build.py --output outputs/manuscript-figures`.
They are 3.30 inches wide and retain at least eight-point text at native size.
