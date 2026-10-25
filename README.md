# Agentic commerce: data and reproducible analyses

This repository accompanies *Agentic Commerce Protocols: A Systematic Mapping and Evaluation*. It contains the frozen selection data, the source-to-claim synthesis ledger, and executable analyses for the paper's two conditional models.

## Reproduce

Use Python 3.12 in a new virtual environment:

```sh
python3.12 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python -B reproduce.py --output outputs/reproduction
```

The command verifies release checksums, reproduces five taxonomy outputs byte for byte, exports Tables 1–5, checks all 66 synthesis source links, proves five Case A symbolic identities, checks 100,000 direct-payoff cases, regenerates the 40,401-row threshold surface, and independently verifies Case B's 64 decision cells and eight forward expectations with rational arithmetic. It also verifies the costly-fallback and evidence-loss extensions, compares nine new datasets byte for byte, and regenerates the original plots, extension diagnostics, and four final manuscript figures. A successful run writes `outputs/reproduction/verification.json` with `passed: true`. Choose a new output directory for each run. The calculation uses no credentials or external model API; network access is needed only to install dependencies. Allow a few minutes and approximately 500 MB of free space including the environment.

## Contents

| Path | Purpose |
|---|---|
| `taxonomy/` | Frozen inputs, selection overlay, five expected outputs and standard-library reproduction code |
| `synthesis/` | 40 mapped-corpus sources, five supplementary scholarly sources, 21 official documents, six claim contrasts and Tables 2–5 inputs |
| `modeling/case-a/thresholds/` | Original Case A thresholds, symbolic/payoff checks, surface data and baseline plot |
| `modeling/case-b/` | Original Case B finite-horizon solver, 64 cells and baseline plot |
| `figures/` | Editable Figure 1 framework and its published PDF |
| `modeling/case-a/fallback/` | Costly fallback, matched cancellation comparison, independent checks and frozen results |
| `modeling/case-b/evidence-loss/` | Evidence availability, STRICT/HOLD comparison, independent oracle and sensitivity results |
| `modeling/extensions/` | Extension runner, protected baseline inventory and review-response map |
| `modeling/figures/` | Portable code for the four final one-column manuscript figures |
| `figures/modeling/` | Four caption-free PDFs, editable SVGs, PNG previews and layout verification |
| `method/` | Preserved English translations of the source and screening policies |
| `claim-to-artifact.csv` | Paper labels mapped to inputs, generation code, outputs and checks |

The taxonomy calculation reproduces 5,217 selection-track records, 1,312 included source records, 237 author-directed non-inclusions preserving their earlier pending decisions, and 1,301 included typed identifiers. Source records and identifiers are different counting units. Native searches and scientific screening judgments are supplied as frozen inputs. The public projections omit licensed source bodies and internal review conversations.

The synthesis ledger supports the six stated comparisons. It records each source's role and actual reading scope. These are purposively selected mechanism contrasts, with 40 sources linked to included corpus identifiers. The five supplementary scholarly sources remain outside that inclusion count. Protocol versions are identified by dated specification URLs or recorded snapshot notes.

Case A describes incentive thresholds under the paper's payoff assumptions; the plotted zero-fee surface is a special case of the symbolic equations. Case B describes eight-round seller control with fixed state-dependent revenue and unobserved monitoring draws until after effort/reporting. Neither model is fitted to field outcomes.

## Case A/B extensions

The original models and historical evidence are preserved. Case A adds review
costs to feasible, preauthorized timeout fallback and compares it with
cancellation under matched assumptions. Preserving execution does not remove
cost-induced conflicts between the agent's request and the user's benefit.
Case B adds independent post-submission evidence loss, reoptimizes effort and
reporting under STRICT/HOLD missing-evidence rules, and varies effort cost and
horizon. Truthful certificates can coexist with selective disclosure or
loss-induced adverse updates. These are conditional comparisons, not optimal
mechanisms, observed agent behavior, or a welfare ranking.

The existing reproduction command includes the extensions. For focused commands,
timing, ties, metric definitions and limitations, see
[`modeling/extensions/README.md`](modeling/extensions/README.md). The four final
figures are 3.30 inches wide, use at least eight-point text, and contain no
embedded title or caption. Their reproducible source and export instructions
are in [`modeling/figures/README.md`](modeling/figures/README.md). Original baseline
plots remain available; the extension READMEs also document wider diagnostic
exports. Manuscript source is maintained separately.

## Framework figure

`figures/Taxonomy_Editable.drawio` is the editable source of Figure 1. Install draw.io desktop separately, then export it with:

```sh
drawio --export --format pdf --crop --output framework.pdf figures/Taxonomy_Editable.drawio
```

On macOS the executable is `/Applications/draw.io.app/Contents/MacOS/draw.io`. Pass it to `reproduce.py --drawio <executable>` to include export in a run. PDF export was tested with draw.io 31.4.5. The original PDF uses EB Garamond; absent that font, draw.io substitutes another font, so export layout/font bytes can differ. The original PDF is included and checksum-verified.

## Historical analyses

The earlier independent-cap Case A grid, optimized-cap supplements, and saved GLM probes remain under `modeling/`. They are historical exploratory artifacts; the current paper uses `case-a/thresholds/` and the exact Case B control calculation. To additionally regenerate and replay the historical evidence locally, add `--legacy`. No live API call is made. See `modeling/README.md`.

## Integrity and reuse

`MANIFEST.json` records file sizes, hashes and CSV schemas/counts. `SHA256SUMS` also seals the manifest. See `REVIEW.md` for validation scope and `PROVENANCE.json` for provenance. Manuscript LaTeX and the full manuscript PDF are maintained separately. This release grants no new blanket software or data license; retained third-party notices remain applicable. Metadata/source identifiers link to the original publishers and protocol authors.
