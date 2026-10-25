# Evaluation rubric (locked for the 2026-08-17 evidence-coded pilot)

Source of the instrument: collaborator Result 2 in
`NeurIPS_AI4Good_Agentic_SoK_Interoperabiltiy/neurips_2026.tex` (§ Result 2 and
§ Analytical framework) and `sok8/evaluation/Readme.md`. This file locks the
anchors before any protocol is scored.

This pilot is evidence-coded, not human double-coded. It does not report
Cohen's κ. Two isolated agent passes may be used only as an agreement check.

## Object and non-object

Score documented protocol guarantees and observable artifacts. Do not score
production reliability under load, welfare effects, or undocumented roadmap
claims. Corpus absence is not universal mechanism absence; it means the
guarantee was not specified or demonstrated in the reviewed evidence.

Home layers for the eight protocols:

| Protocol | Home layer |
|---|---|
| ERC-8004 | L1 |
| MCP | L2 / L3 |
| A2A | L2 / L3 |
| AP2 | L4 |
| x402 | L5 |
| UCP | L6 |
| AG-UI | L7 |
| Kleros | L8 |

## Scale

Allowed values: `0`, `0.5`, `1`, `1.5`, `2`. Half-steps are for mixed
evidence inside one dimension, not for averaging across dimensions.

| Score | Meaning |
|---|---|
| 0 | Guarantee absent from deployed documentation. |
| 0.5 | Mentioned as intent or optional extension; no deployed artifact. |
| 1 | Partial or conditional: one chain, one vendor, one fault class, or not auditable end to end. |
| 1.5 | Concrete deployed artifact, but a named failure mode remains unclosed. |
| 2 | Observable and auditable in deployed documentation for the dimension's question. |

If the packet has no usable spec or locator, write `NA` and do not invent a
number.

## Dimensions

### C — Coherence

Question: does the protocol solve the information problem theory assigns its
home layer?

- 0: no mapping to that problem, or the spec solves a different layer's problem.
- 1: addresses the problem locally but leaves the assigned failure mode open.
- 2: the assigned problem has a named artifact, a failure mode, and a checkable metric.

### I — Interoperability

Question: do its guarantees propagate across layer seams and the Web2–Web3
boundary?

Evaluate against the flow \(F=(A,R,X,S,E,O)\) and the seven properties below.
Connectivity without propagation is not interoperability.

- 0: no specified binding to another layer or trust model.
- 1: optional or one-sided binding (adapter, suggested pairing, one ecosystem).
- 2: a specified, auditable binding that another protocol or rail can verify.

### A — Assurance coverage

Count how many of the seven properties the protocol addresses with an
observable artifact, then bin:

| Count | Score |
|---|---|
| 0–1 | 0 |
| 2–4 | 1 |
| 5–7 | 2 |

Always record the raw count and the yes / partial / no vector. Partial counts
as addressed for the bin, but must be marked partial in the vector.

The seven properties:

1. Authorization safety: action stays inside consent and mandate scope.
2. Execution correctness: intended task, amount, recipient, route, and asset are preserved.
3. Economic finality: the recipient can use the funds, not only see a confirmation.
4. Pricing correctness: quotes, fees, spreads, and oracles match settlement.
5. Auditability: the flow can be reconstructed from evidence records.
6. Compliance continuity: KYC, AML, sanctions, tax, or jurisdictional obligations remain attributable.
7. Recoverability: escalation, refund, rollback, compensation, or arbitration exists.

### EM — Emerging-market fitness

Question: does the protocol work where courts, cards, banks, and platform
support are weak?

Use the five institutional requirements from the original fitness table:
banking access, legal enforcement, formal ID, platform trust, currency
stability. Score the protocol, not the whole stack.

- 0: depends on the missing institution (cards, KYC bureau, court, platform).
- 1: reduces dependence on one or two institutions but still needs a fallback.
- 2: usable without that institution, with an artifact the loss-bearer can inspect.

### S — Standardization maturity

Question: is the specification stable, governed, and adopted?

- 0: blog post, unreleased draft, or single-vendor note with no versioned spec.
- 1: public spec or EIP/IETF draft; limited independent implementers.
- 2: versioned spec, named governance, and multiple independent implementations
  or a standards body process.

Do not use GitHub stars as the sole maturity signal.

## Four-field note (required on every cell)

Each scored cell must state:

1. promised guarantee
2. observable evidence
3. failure mode
4. measurable metric
5. score
6. locator: a `record_id` from `sok8/corpus/tagged_records.jsonl` and/or a
   spec URL with a section or paragraph pointer

Impressionistic words (`works`, `mostly interoperable`, `widely used`) are
not allowed without a locator.

## Layer-level coherence verdicts

Layer verdicts use the same four-field schema but are corpus synthesis, not
protocol ranks.

| Verdict | Meaning |
|---|---|
| Strong | Concrete artifacts and a checkable metric exist in deployed specs. |
| Partial | Artifacts exist; the assigned failure mode remains open. |
| Weak | Thin or merchant-specific artifacts; no portable metric. |
| Missing | No native, widely adopted protocol for the assigned problem. |

## Cases

CS1–CS4 use a fixed template: payment path, trust boundary, promised
guarantee, possible violation, responsible stakeholder, candidate metrics.
Status values: Partial, Weak, Missing. Upgrade a status only when a spec
clause closes the named failure mode.

## What scorers must not see

Scoring passes must not read `paper/tabs/tab_leaderboard.tex`,
`paper/figs/fig_radar.tex`, `paper/figs/fig_scorecard_profiles.tex`, or any
file that already contains the illustrative 0–2 matrix.
