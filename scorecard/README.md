# Protocol Scorecard

**[Final locked scores for eight protocols](final-scores-8.csv).** Dimensions are C (coherence), I (interoperability), A (assurance coverage), EM (emerging-market fitness), and S (standardization maturity). Each uses the original 0, 0.5, 1, 1.5, 2 rubric. The lock date is 17 August 2026.

## Read the evidence

| Path | Purpose |
|---|---|
| [01-method/rubric.md](01-method/rubric.md) | Original scoring anchors and four-field evidence requirements |
| [01-method/evidence-packets](01-method/evidence-packets/) | Eight protocol packets and the layer-coherence context supplied to raters |
| [01-method/corpus-context.md](01-method/corpus-context.md) | Retained synthesis behind that historical layer context |
| [01-method/referenced-records.json](01-method/referenced-records.json) | Referenced historical source metadata, original author synthesis, and supplementary source aliases |
| [01-method/annotation-contract.json](01-method/annotation-contract.json) | Original system prompt, framed round prompts, exact request template, endpoints, schema, and normalization rule |
| [02-judgments](02-judgments/) | Nine saved model-round records, protocol metadata, and [eleven accepted author decisions](02-judgments/author-decisions-11.json) |
| [03-results](03-results/) | Within-model medians, cross-model medians, adjudication audit, and inter-model agreement |
| [04-code](04-code/) | Offline reconstruction and editable figure-generation code |
| [figures](figures/) | Score matrix, individual profiles, and origin-group overlays in PDF, SVG, and PNG |

The three chat raters are `agnes-2.5-flash`, `deepseek-v4-flash`, and `qwen3.7-plus`. Each ran three framed rounds at temperatures 0, 0.3, and 0.6. Every request received the locked rubric, the layer-coherence packet, and one protocol packet. The historical corpus was not concatenated into the model context. Evidence packets were prepared with Grok 4.6, as recorded in the pilot. Saved records identify the returned model and execution date.

For each protocol and dimension, first take the median of the model's three rounds, then the median across the three chat models. Nine cells with model spread at least 1.0 and two additional Kleros scoring-object cells received an author's locked value. The other 29 cells retain their cross-model median. Eleven cells were adjudicated; three final values differ from that median. Blank original author reasons remain `null`; the extracted dispute questions are not substituted author justifications. Kleros is evaluated as a candidate L8 component in the commerce stack.

The original annotation code normalized saved responses: scores were snapped to the allowed half-steps, property labels were normalized, and A was recomputed from the count of seven properties labeled yes or partial. [The contract](01-method/annotation-contract.json) preserves that function and its constants. The nine JSONs are the resulting normalized judgments with per-cell promise, evidence, failure, metric, and locator notes. Three cells in Qwen round 3 (A2A A, EM, and S) lack the `evidence` field; the original bytes and gaps are preserved and checked, as listed in [schema-notes.json](02-judgments/schema-notes.json). Fifteen other notes retain an extra score field; aggregation follows the normalized protocol-level values. Raw service envelopes, failed retries, smoke calls, and an excluded embedding-model experiment are not used in reconstruction.

## Reconstruct

From the repository root, after `uv sync --locked`:

```sh
uv run --locked python -B scorecard/04-code/reproduce.py --output /tmp/sok8-scorecard-results
```

Use a new or empty output directory outside the repository. The command reconstructs all five result tables, checks them against the distributed files, renders from the generated `final-scores-8.csv`, and checks all nine figure files byte for byte. No external archive, API key, or network service is read. The independent literature workflow is described in [the taxonomy guide](../taxonomy/README.md).

Pairwise Cohen's kappa and Fleiss' kappa are calculated on the 40 cells of each model's within-model median, before author adjudication. Quadratic-weighted pairwise values round to 0.25, 0.44, and 0.42; the complete values and unweighted statistics are in [inter-model-agreement.json](03-results/inter-model-agreement.json). These describe inter-model agreement. No human inter-rater reliability is estimated.

## Manuscript mapping

| Reported object | Inputs and computation | Released result |
|---|---|---|
| Locked protocol score matrix, `fig:score-profiles` panel (a), and `tab:leaderboard` | Nine saved rating rounds, medians, and eleven author decisions | [final-scores-8.csv](final-scores-8.csv) and [score-matrix figure](figures/04_protocol_scorecard.pdf) |
| Protocol dimension profiles and `fig:score-profiles` panel (b) | Fresh final score table, retained chart geometry, and Web2/Web3 group metadata | [individual profiles](figures/05_protocol_radars.pdf) and [origin overlays](figures/origin-radar-overlay.pdf) |
| Eleven author-set cells, `tab:adjudicated` | Accepted author values and gate/object decisions | [author decisions](02-judgments/author-decisions-11.json) and [adjudication audit](03-results/adjudication-audit-11.csv) |
| Inter-model agreement in the scorecard appendix | Three pre-adjudication median vectors, each with 40 cells | [agreement statistics](03-results/inter-model-agreement.json) |

The plotting code retains the original geometry and palette, uses bundled DejaVu Sans for portable rendering, and reads score values from the fresh output table. Figures expose the same numerical scores and profiles; this release does not rebuild an entire manuscript PDF or its combined TikZ layout.

## Historical locators and evidence boundary

The scoring packets and rubric preserve their original text, including old `sok8/`, `records/`, and `paper/` path names. They describe the scoring study's original context. In this package, `sok8/evaluation/rubric.md` corresponds to [rubric.md](01-method/rubric.md), `sok8/evaluation/evidence_packets/` to [evidence-packets](01-method/evidence-packets/), and the old consensus ledger to [corpus-context.md](01-method/corpus-context.md). The accepted values from `records/evaluation-human-review.md` are transcribed in [author-decisions-11.json](02-judgments/author-decisions-11.json). Historical `record_id` values resolve through [referenced-records.json](01-method/referenced-records.json), which contains the 32 referenced records and the supplementary aliases. Some original locators name only a document or documentation site; missing section pointers have not been invented.

The earlier 304-record context and its layer counts belong to this frozen scoring pilot. The current [literature taxonomy](../taxonomy/README.md) uses a different source frame and methods. Its 1,301 included identifiers do not retroactively change the pilot's inputs or scores. Contemporary protocol behavior and adoption can differ from the saved evidence. This package reconstructs those saved decisions and calculations.
