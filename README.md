# Agentic Commerce: NeurIPS Workshop Artifacts

This repository contains the literature taxonomy and protocol scorecard for the NeurIPS Workshop manuscript. Saved source evidence, screening and classification judgments, protocol evidence packets, model ratings, author decisions, result tables, and plotting code support inspection and offline reconstruction.

**[Browse all 1,301 included literature identifiers and classifications](taxonomy/included-literature-classifications-1301.csv)** or **[open the final eight-protocol scorecard](scorecard/final-scores-8.csv)**.

## Reproduce

Install [uv](https://docs.astral.sh/uv/), then run from this directory:

```sh
uv sync --locked
uv run --locked python -B reproduce.py --output /tmp/sok8-workshop-results
```

Choose a new or empty output directory outside the repository. Python 3.12.14 and the dependencies are pinned by `.python-version`, `pyproject.toml`, and `uv.lock`. Initial setup downloads the environment; computation then runs offline without credentials or paid APIs. Allow a few minutes and approximately 500 MB for the environment and outputs.

The command reconstructs and compares 14 taxonomy result files, five scorecard tables, and nine scorecard figure files byte for byte. Generated results are placed under `literature/taxonomy/` and `scorecard/` inside the output directory. The repository's inputs and expected results remain unchanged. Plotting reads the newly reconstructed score table.

## Contents

| Directory | Materials | Entry point |
|---|---|---|
| `taxonomy/` | Eligibility and annotation methods, source evidence, screening decisions, independent ratings, adjudications, and literature classifications | [Taxonomy guide](taxonomy/README.md) |
| `scorecard/` | Five-dimensional protocol rubric, evidence packets, three chat models over three rounds, author decisions, locked scores, agreement statistics, and figures | [Scorecard guide](scorecard/README.md) |

The academic-selection frame contains 5,217 source records: 1,312 included and 3,905 excluded. Exact identifier consolidation gives 1,301 included identifiers; 771 receive functional layer labels and 530 receive `not_evidenced`. Of the labeled identifiers, 207 date from 2023 onward. The [taxonomy methods](taxonomy/01-method/README.md) distinguish source records, identifiers, and the functional analysis set.

The protocol scorecard retains the evidence-coded pilot locked on 17 August 2026: eight protocols, five dimensions, and eleven author-set cells. Its evidence packets contain the earlier 304-record corpus context and supplementary specification URLs. The pilot's scores and source context remain frozen; the expanded literature taxonomy does not constitute a new protocol-scoring study. The [scorecard guide](scorecard/README.md) explains this relationship and maps the manuscript's score matrix, profiles, and adjudications to files.

## Reproduction scope and source rights

Reconstruction starts from the saved evidence and scientific decisions. It establishes deterministic selection and classification aggregation, score aggregation, author-decision application, inter-model agreement, and figure generation. A new database search or new model judgments would be a separate study. The saved ratings provide model identifiers, dates, temperatures, prompts, evidence locators, and normalized judgments; they do not measure production protocol reliability.

Abstracts and quotations retain their source attribution and remain subject to their respective source rights. No blanket license is applied to third-party material. Publisher PDFs, credentials, private conversations, manuscript sources, and internal audit records are outside the released tree. Earlier repository contents remain available in Git history.
