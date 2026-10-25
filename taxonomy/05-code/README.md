# Reconstruction Code

Run from the package root:

```sh
uv run --locked python -B taxonomy/05-code/reproduce.py --output /tmp/sokacp-results
```

This entry point reconstructs the taxonomy. The output directory must be new or empty and outside the release package. Use the root `reproduce.py` to reconstruct both the taxonomy and the protocol scorecard.

The program:

1. Joins source evidence and screening decisions, reconstructs the exact-identifier union, and reconciles source, selection, and identifier counts.
2. Builds the 1,301 annotation packets from saved abstracts, identity bindings, and public dates.
3. Checks the saved A/B/C schemas, coverage, reading scopes, exact quotations, distinct execution contexts, and model configuration.
4. Identifies the complete-label A/B disagreements, requires exactly those adjudications, and reconstructs final labels, evidence offsets, paired comparisons, and descriptive statistics.
5. Derives the 771-record analysis subset, 207-record recent subset, source assignment, and period/layer shares.
6. Compares the top-level `included-literature-classifications-1301.csv` and all CSV/JSON results in `04-final-selection/` byte for byte.

Generated files use the same descriptive names and directory layout as the distributed results, under the output's `taxonomy/` directory. The [results guide](../04-final-selection/README.md) explains the count suffixes and their units. Counts in filenames describe this frozen corpus snapshot and are verified against the reconstructed contents.

The taxonomy computation uses Python's standard library. The locked scientific packages support the protocol scorecard figures. No source-workspace resolver, external archive, local session log, API key, or network call is used by reconstruction.

[Layer-coding prompts and schema](layer-annotation/README.md) document the scientific judgment step. The code aggregates saved judgments; it does not generate new scientific labels.
