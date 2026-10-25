# Case A extension: review costs and timeout fallback

This adds a matched timeout-policy comparison to the original model in
../thresholds/. Original code, results and the zero-fee figure are preserved.
Manuscript source is maintained separately.

## Assumptions and derivation

The user prefers theta > 0; the agent prefers theta+b, b >= 0.
A fixed mandate permits [0,d], d >= 0, so autonomy executes
a = min(theta+b,d). Agent utility is -(a-theta-b)^2 and user loss is
(a-theta)^2. Review costs eta >= 0 to the agent and kappa >= 0 to the
user are incurred whenever review is requested, whether timely or late.
With probability q, timely review implements theta under renewed user
authority. After timeout, CANCEL executes 0; FALLBACK executes a.
All other parameters and assumptions are matched.

Fallback must remain feasible and preauthorized at the deadline. It cannot
restore an already expired service or purchase opportunity. The agent
requests review only for a strict utility improvement. These preferences
and information are assumptions, not measurements of deployed behavior.

Write C = (a-theta)^2 and M = (a-theta-b)^2-b^2. Under FALLBACK:

- Agent gain from review: q M - eta.
- User gain from review: q C - kappa.
- Requested-review user loss: kappa + (1-q) C.

Requested review is harmful exactly when q M > eta and q C < kappa.
If M > 0 and C > 0, this is eta/M < q < kappa/C, intersected with [0,1].
Equality in the user condition is indifference. If M <= 0, nonnegative
eta rules out a strict request. If C = 0, review cannot strictly benefit
the user. Computation uses gains rather than division and handles these
boundaries, zero bias, q endpoints, above-ideal caps and nonbinding caps.

When d < theta, M = (theta-d)(theta-d+2b) > 0 and C = (theta-d)^2.
Thus q_A^F = eta/[(theta-d)(theta-d+2b)] and
q_P^F = kappa/(theta-d)^2.

For CANCEL the corresponding gains are:

- Agent: q theta(theta+2b) - [2a(theta+b)-a^2+eta].
- User: q theta^2 - [2a theta-a^2+kappa].

These recover the original cancellation thresholds. Holding action and
review choice fixed, cancellation loss minus fallback loss equals
(1-q)[theta^2-C]. This is not positive for every possible a, and changing
the rule also changes the agent's choice. No unconditional ranking of
endogenous outcomes is claimed.

With kappa = 0, fallback review weakly reduces user loss regardless of
eta, preserving the original zero-fee fallback result. Positive kappa
removes that guarantee.

## Checked counterexample

At theta=1, b=0.2, d=0.5, q=0.2, eta=0.01, kappa=0.1:

| Quantity | Autonomy | Fallback review |
|---|---:|---:|
| Agent utility | -0.49 | -0.41 |
| User loss | 0.25 | 0.30 |

The agent requests review although user loss increases. This refutes
automatic alignment with costly review; it does not imply that fallback
generally worsens outcomes.

## Reproduction

From the repository root:

    python -B modeling/case-a/fallback/analyze.py --output outputs/case-a-fallback

Frozen extension outputs are in results/:

| File | Meaning |
|---|---|
| decision-grid.csv | 96,882 matched CANCEL/FALLBACK parameter rows |
| cost-sensitivity.csv | 20,402 rows varying eta and kappa |
| summary.json | Design, counts and counterexample |
| validation.json | Verification and figure specifications |
| case-a-cancellation-fallback.pdf/svg/png | Main comparison |
| case-a-cost-sensitivity.pdf/svg/png | Supporting cost comparison |

The main figure fixes theta=1, b=0.2, eta=0.10, kappa=0.05 and crosses
201 q values with 241 cap ratios from 0 to 1.2. The supporting figure
fixes d=0.5 and varies each cost over 101 points from 0 to 0.3.
Its colors are lengths of harmful-request q intervals, not transaction
frequencies. Profiles are illustrative, not calibrated.

Verification includes seven symbolic identities, 100,000 parameter tuples
under both rules, 2,000 independent rational policy cases, 360 boundary
cases, 12 exact ties and 32 independent cost-interval checks.
Numerical classification tolerance is 1e-12 times theta^2. Agent
indifference retains autonomy; user indifference is recorded separately.

Figures are seven inches wide with fonts of at least eight points and
editable SVG text. Use full text width: single-column reduction also
reduces physical font size.

## Limits

This studies escalation within a fixed mandate. It neither chooses an
optimal mandate nor solves a general delegation mechanism. Parameter
distributions, endogenous review speed, reviewer accuracy or capacity,
and market-wide welfare are not modeled. Costs share the quadratic-loss
units of the original model.

## Final manuscript layouts

The seven-inch plots above are diagnostic exports. The four final,
caption-free one-column layouts are in `figures/modeling/` at the repository
root, with editable SVGs and PNGs in its `previews/` directory. Regenerate
them using `python -B modeling/figures/build.py --output outputs/manuscript-figures`.
They are 3.30 inches wide and retain at least eight-point text at native size.
