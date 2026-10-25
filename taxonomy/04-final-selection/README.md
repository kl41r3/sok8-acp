# Screening, Classification, and Analysis Results

**Start with the [complete literature and classification table: 1,301 identifiers](../included-literature-classifications-1301.csv)**, located directly inside `taxonomy/`. It includes identifiers, titles, years, publication links, layer labels, mechanisms, rationales, and decision provenance.

The files below provide the supporting results. Filename suffixes count CSV data rows (excluding the header) or JSON decision records. For the two summary JSON objects, the suffix instead names the population being summarized: 5,217 source records or 1,301 included identifiers. These counts describe the distributed frozen corpus snapshot.

## Screening and Identifier Consolidation

| File | Count and contents |
|---|---|
| [screening-decisions-all-source-records-5217.csv](screening-decisions-all-source-records-5217.csv) | 5,217 academic source records, with titles, identifiers, include/exclude decisions, screening rules, and reasons |
| [screening-decisions-all-identifiers-5184.csv](screening-decisions-all-identifiers-5184.csv) | 5,184 distinct typed identifiers across the screening frame, with consolidated decisions and all source-record memberships |
| [included-identifiers-1301.csv](included-identifiers-1301.csv) | The 1,301 included identifiers and their source memberships; an identifier-only inclusion list without titles or layer labels |
| [screening-counts-by-source-4.csv](screening-counts-by-source-4.csv) | Four source totals: ACM, IEEE, AAAI, and IJCAI, each with screened, included, and excluded record counts |
| [screening-summary-source-records-5217.json](screening-summary-source-records-5217.json) | Summary of the 5,217-record academic screening frame, including 1,312 included source records, 1,301 included identifiers, and source-frame context |

## Final Classifications and Subsets

| File | Count and contents |
|---|---|
| [final-classification-decisions-1301.json](final-classification-decisions-1301.json) | 1,301 structured final decisions, with label sets, evidence quotations, mechanisms, rationales, reading scopes, and judgment locators |
| [literature-with-layer-labels-771.csv](literature-with-layer-labels-771.csv) | The 771 included identifiers assigned at least one layer; the same columns as the top-level literature table |
| [literature-with-layer-labels-2023-onward-207.csv](literature-with-layer-labels-2023-onward-207.csv) | The 207 labeled identifiers dated 2023 or later; the same columns as the top-level literature table |

`not_evidenced` means the read evidence supports no layer assignment; the identifier remains part of the included corpus. The top-level table contains all 1,301 included identifiers, while the two subsets contain only labeled identifiers.

## Independent Ratings and Evidence

| File | Count and contents |
|---|---|
| [independent-ratings-and-adjudication-1301.csv](independent-ratings-and-adjudication-1301.csv) | 1,301 paired A/B label comparisons, exact-agreement indicators, adjudication indicators, and final classifications |
| [classification-evidence-quotes-1709.csv](classification-evidence-quotes-1709.csv) | 1,709 evidence quotations used by final decisions, with associated layers, rationales, released source locations, and character offsets; an identifier can have multiple quotations |

Initial exact agreement is 1,131/1,301 (86.93%); the other 170 records use third-rater adjudication. Evidence offsets count Unicode code points, use an exclusive end position, and select the first exact quotation occurrence. Classification CSVs use semicolon-separated layer labels; JSON judgments use an array for positive labels.

## Summary Statistics

| File | Count and contents |
|---|---|
| [classification-summary-included-identifiers-1301.json](classification-summary-included-identifiers-1301.json) | Summary of the 1,301 included identifiers: 771 labeled, 530 `not_evidenced`, layer totals, agreement, adjudication, model configuration, and reading scopes |
| [layer-counts-and-shares-by-period-16.csv](layer-counts-and-shares-by-period-16.csv) | 16 period/layer rows: eight layers before 2023 and from 2023 onward, each with a count, denominator, and share |
| [labeled-literature-counts-by-source-4.csv](labeled-literature-counts-by-source-4.csv) | Four analysis-source totals among the 771 labeled identifiers: ACM 156, IEEE 590, AAAI 14, and IJCAI 11 |

Layer totals L1–L8 are 106, 178, 476, 59, 152, 68, 115, and 7. A record can contribute to multiple layers. Period shares use 564 and 207 labeled identifiers as their respective denominators. One analysis-source label is assigned per identifier using the priority ACM, IEEE, AAAI, then IJCAI; all source memberships remain available in the identifier tables.

## Reconstruction

[reproduce.py](../05-code/reproduce.py) regenerates the top-level literature CSV and every CSV/JSON file listed here from the saved evidence and decisions, then checks byte-for-byte agreement. Reconstructed files retain the distributed names and directory layout. The annotation input packets are also written under the reconstructed `04-final-selection/` directory for inspection.
