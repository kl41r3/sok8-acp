# Literature Taxonomy

## Included literature: 1,301 identifiers

**[Open the complete literature and layer-classification table](included-literature-classifications-1301.csv).** Each row contains an included identifier, title, publication year, source, publication link, L1–L8 labels, and the classification rationale. The table covers all 1,301 included identifiers: 771 have at least one layer label and 530 have `not_evidenced`.

This CSV is at the same directory level as `01-method/` through `05-code/`. The [other result tables](04-final-selection/README.md) provide screening decisions, evidence quotations, independent-rating comparisons, subsets, and summary statistics. Their names describe the contents and end with a count; the results guide explains each count's unit.

## Workflow and reproduction

The five directories form a complete saved-input-to-result workflow:

| Directory | Purpose |
|---|---|
| [01-method](01-method/README.md) | Eligibility, source-specific retrieval, final selection, and functional classification criteria |
| [02-source-evidence](02-source-evidence/README.md) | Source records, complete abstracts read by layer coders, public dates, query observations, and supplementary passages |
| [03-screening-review](03-screening-review/README.md) | Selection decisions and reasons, original scientific-review context, paired layer ratings, and third-rater adjudications |
| [04-final-selection](04-final-selection/README.md) | Deterministic selection tables, identifier unions, final classifications, exact evidence, and period comparisons |
| [05-code](05-code/README.md) | Self-contained reconstruction and the layer-coding prompts and schema |

Run from the package root:

```sh
uv run --locked python -B taxonomy/05-code/reproduce.py --output /tmp/sokacp-taxonomy --taxonomy-only
```

The command reconstructs the top-level literature table and every table in `04-final-selection/` from `02-source-evidence/` and `03-screening-review/`, checks exact agreement with the distributed tables, and writes the reconstructed annotation packets to the output directory. Reconstructed results retain the distributed names and directory layout under the output's `taxonomy/` directory. It reads no original checkout, archived file, local path registry, or external service.

The reading order for one publication is its source entry in `02-source-evidence/records.json`, its source-record decision in `03-screening-review/records.json`, then its identifier-level classification in [the complete literature table](included-literature-classifications-1301.csv). Final classifications link to the relevant A/B ratings and, where needed, the C adjudication. [The evidence quotations](04-final-selection/classification-evidence-quotes-1709.csv) link quotations to the exact distributed abstract or supplementary passage, with Unicode character offsets.

The full source frame has 5,241 records and 5,208 exact identifiers. The academic-selection frame has 5,217 records and 5,184 exact identifiers. Inclusion is the union of source inclusions: 1,312 included source records yield 1,301 included typed identifiers. Source priority for assigning one analysis-source label is ACM, IEEE, AAAI, then IJCAI. This assignment does not discard other source memberships.
