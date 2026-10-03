# Case A: bounded autonomy with deadline-sensitive review

The principal sensitivity analysis varies review timeliness `q in [0,1]` and autonomy cap `d in [0,1.2]` independently. There are 501 x 601 = **301,101** pairs, spaced 0.002 apart. No cap is optimized as `q` changes. The bias `b=0.15`, provider review cost `eta=0.005`, user review cost `kappa=0.01` and prior `theta ~ Uniform[0,1]` remain fixed.

## Model and closed-form expectation

The provider prefers action `theta+b`. Autonomous action is `a=min(theta+b,d)`, with provider utility `V_A=-(a-theta-b)^2`. Review gives the perfect user action `theta` with probability `q`; otherwise the task is canceled to action zero. The provider's expected review utility is `V_R=-q*b^2-(1-q)*(theta+b)^2-eta`. The provider selects REVIEW iff `V_R>V_A`, choosing AUTO on a tie.

The user's losses are `(a-theta)^2` for AUTO and `kappa+(1-q)*theta^2` for REVIEW. Consequently

```text
L(q,d) = integral_0^1 [(1-I_R)*(min(theta+b,d)-theta)^2
                      + I_R*(kappa+(1-q)*theta^2)] dtheta,
I_R = 1{V_R > V_A}.
```

For `q>0`, let

```text
r = clip((d+sqrt((1-q)*d^2+q^2*b^2+q*eta))/q-b, 0, 1),
t = clip(d-b, 0, r).
L = b^2*t + ((r-d)^3-(t-d)^3)/3
    + kappa*(1-r) + (1-q)*(1-r^3)/3.
Review share = 1-r; cancellation share = (1-q)*(1-r).
```

For `q=0`, `r=1` and no type reviews. The code also enforces the exact no-review boundary `d >= 1+b-sqrt(q*b^2+(1-q)*(1+b)^2+eta)`. The expectation is an analytic piecewise integral; dense parameter spacing is not a probabilistic confidence interval.

## Main results and figures

[Independent-grid CSV](data/independent-grid.csv) and [compressed matrices](data/independent-grid.npz) retain every pair and its loss/review/cancellation values. The matrix shape is q-by-d. [Fixed-cap slices](data/fixed-d-slices.csv) cover `d=0.10,0.25,0.55,0.85` at every q point.

| Fixed cap | Loss at q=0.5 | Loss at q=1 |
|---|---:|---:|
| d=0.10 | 0.172500 | 0.0091763435 |
| d=0.85 | 0.018000 | 0.0182180102 |

Thus improving review timeliness can reduce or slightly increase user loss depending on the independently fixed cap, because the provider's self-selection and the user's review cost both matter. The model does not estimate actual human response delays or commercial incentives.

[Heatmap PDF](figures/independent-qd-heatmaps.pdf) plots loss and review share over both independent inputs. [Fixed-cap PDF](figures/fixed-d-curves.pdf) holds each curve's cap constant. PNG/SVG copies accompany both. [compute.py](compute.py) implements the closed-form expectation; [plot.py](plot.py), [theme.yaml](theme.yaml) and [plot_utils.py](plot_utils.py) preserve the generation logic and typography. Main figures are seven inches wide with at least nine-point visible type. Heatmap cells are rasterized inside vector outputs, while axes and labels remain vector; all values remain available in the matrices.

Caption: Case A's user loss and review share under independently set review timeliness q and autonomy cap d. The other parameters are fixed; each point reflects provider self-selection under the stated utilities. There is no q-dependent optimization of d and no empirical sampling uncertainty.

## GLM decision pilot

[Probe design](probes/design.json), [scenario oracle](probes/cells.csv), [actual evaluation evidence](probes/evidence.json), [scoring](probes/scoring.json) and [summary](probes/summary.json) preserve the original experiment. Twelve scenarios use theta in `{0.2,0.5,0.8}`, d in `{0.25,0.55}`, q in `{1,0.5}`; each has two fresh calls, reversing option order. Both request messages and their exact final JSON-string outputs are retained. `oracle.py` calculates utility and regret independently of the model.

All 24 outputs are schema-valid; **23/24** choose the maximizing option. Mean utility regret is 0.0055208333. `A05-draw2` is the sole mismatch: it chooses AUTO and reports an incorrect AUTO payoff. The correct AUTO utility is -0.16, whereas REVIEW is -0.0275. This is a bounded calculation/choice error, not evidence of a general model propensity. At theta=0.8, d=0.55, the timely-review change from q=0.5 to q=1 switches the optimal decision and is reproduced by both calls. At theta=0.8, d=0.25, q=0.5, REVIEW is provider-optimal even though the user loss rises from 0.3025 to 0.33.

## Preserved supplements and verification

[supplemental/five-q](supplemental/five-q/) retains the original 6,005-policy midpoint grid, five grid optima, frozen design and original offline oracle. [supplemental/optimized-cap](supplemental/optimized-cap/) retains the separate 2,001-q continuous-cap optimization, figure and code. That supplement computes `min_d L(q,d)` and a q-dependent optimal cap; it must not be interpreted as the effect of changing q at a fixed d. Its optimized switch near q=0.9724 is separate from the independent-parameter plots.

The main replay checks every CSV/matrix pair, recomputes every analytic matrix value, checks 42 selected pairs directly from the original utilities using one million theta midpoints, and re-scores all 24 final answers. The saved numerical and figure checks are in [verification](data/verification.json) and [figure audit](data/figure-audit.json). The maximum direct-payoff loss difference is about 1.31e-8. For supplements, their original offline scripts can be run in the clean reproduction copy; do not overwrite the release inputs. No protocol is executed and no API call is made by replay.
