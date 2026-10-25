# Release verification

This release was checked in an isolated Python 3.12.14 virtual environment using `requirements.txt`. The root command regenerated all current-paper computational results without an API call. The GitHub workflow repeats that command, including the historical replay, on Ubuntu with Python 3.12.

| Check | Result |
|---|---|
| Frozen taxonomy | All 23 package files retain their previous bytes; five regenerated outputs match their expected files byte for byte |
| Selection totals | 5,217 selection records; 1,312 included records; 237 author non-inclusions; 1,301 included typed identifiers |
| Synthesis | 66 unique source keys with retrievable locators; all 40 mapped-source identifiers join to the included set; six contrasts have valid decisive references |
| Tables | Tables 1–5 exported from the shipped data; 27 distinct search expressions |
| Current Case A | Five symbolic identities and 100,000 direct-payoff checks pass; 40,401 surface rows reproduce byte for byte |
| Current Case B | 64 cells agree with independent exact-rational enumeration; eight forward paths agree in effort, success and final-state probabilities |
| Model figures | Both PDFs, SVGs and PNGs regenerated from freshly computed data; Case B plotted-values CSV agrees byte for byte |
| Historical analyses | 301,101-cell grid, saved response re-scoring and historical plot generation pass without live requests |
| Framework | Editable draw.io source present; PDF export tested with draw.io 31.4.5; font substitution changes rendering when EB Garamond is unavailable |
| Package | Files sealed by SHA-256; CSV schemas/counts included in manifest; no manuscript `.tex` or full manuscript PDF included |

The arithmetic checks validate the supplied frozen selection decisions. Scientific corpus screening, native retrieval, independent-work/version identification, and field-wide function frequencies are outside this calculation. Source reading scope is recorded in `synthesis/sources.json`. The model results are conditional on their stated assumptions.

The release adds original analysis code and bibliographic/analytical metadata. Existing saved probe evidence and method policies retain their original provenance. The package was inspected for credentials, private absolute paths, service envelopes and manuscript content. No new blanket license is assigned. This is the author's public artifact repository; it is not an anonymous review mirror.

`verification.json` is produced by each execution so that readers can inspect their own environment and checks. GitHub Actions shows the status of the exact pushed revision.

## Additive Case A/B revision

The extension runner checks the protected upstream inventory, regenerates nine
datasets with exact byte agreement, and independently verifies the new
conditional calculations. Case A adds seven identities and matched-cost
checks; Case B recovers all 64 original control cells and eight paths, then
checks 1,064 configurations, 16,736 control cells and 2,128 initial-state paths.
The exact full-monitoring threshold tie is checked separately.

The four final manuscript figures are exported at native one-column width.
The runner checks input hashes, dimensions, minimum font sizes, canvas bounds,
and absence of embedded titles/captions. It reports PDF/SVG/PNG byte agreement;
`--exact-figures` on the extension runner additionally enforces identical bytes.
Platform rendering can vary, while scientific dataset comparison remains exact.
The existing workflow invokes the extended root command without new dependencies.
Historical replay and the framework export option are preserved.

These are computational checks, not a new behavioral study or a market-welfare
evaluation. Manuscript and anonymous-service updates are separate activities.
