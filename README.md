# sok8-acp

Offline code, data, analytical definitions and English translations of the requested Method policies for the current agentic-commerce taxonomy, plus the two conditional Modeling cases and their figures/data. This is the authorized second publication batch for **`kl41r3/sok8-acp`, public, branch `main`**. The user explicitly chose to keep the repository public and continue uploading Modeling. The first taxonomy/Method commit, originally verified private before the visibility changed, is `cd55fb5aa9360fc5df7c57b6d64f86253e870ad8`; the completed Modeling artifacts are added in a separate later commit, preserving that history. The user-selected repository name does not designate a new protocol or a complete ACP implementation.

Start with the [submission review](REVIEW.md), [Method policies](method/README.md), [eight-function analytical codebook](taxonomy/docs/analytical-codebook.md) [data dictionary](taxonomy/docs/data-dictionary.md) and [Modeling artifacts](modeling/README.md). [MANIFEST](MANIFEST.json) binds every released file's size, SHA-256 and applicable CSV schema; [PROVENANCE](PROVENANCE.json) distinguishes the frozen candidate, translated policies and this packaging revision.

Publication revision 6, batch 2 incorporates the verified 104-file Modeling package from local revision 5, retaining English-only Method policies and every frozen taxonomy byte. The root manifest/seal covers the complete combined package. Historical nonpublication statements inside unchanged source artifacts describe their preparation context; current publication state is stated here.

## Deterministic reproduction scope

The package reconstructs the following **five frozen selection, identifier and count outputs byte-for-byte**. This does not establish perfect reproduction of the entire taxonomy study. Inputs already contain upstream identifiers and existing screening decisions; the code applies the 237-entry administrative overlay, groups saved exact typed keys and reconciles counts.

| Output in `taxonomy/expected/` | Reconstructed content |
|---|---|
| `final-selection-records.csv` | Preserved scientific dispositions and final selections/bases for 5,241 source records |
| `source-counts.csv` | Selection, standard-track and relation-only counts for five sources |
| `identifier-selection.csv` | Source memberships and selection views for 5,208 exact typed keys |
| `included-identifiers.csv` | The current 1,301 included typed keys |
| `counts.json` | Frame, selection and exact-key repetition arithmetic |

Python 3.9 or later, standard library only. No network, model, credentials or dependency installation is required. From the repository root:

```sh
(cd taxonomy && python3 -I -S -B code/reproduce.py --check-only)
(cd taxonomy && python3 -I -S -B code/reproduce.py --output outputs/run)
shasum -a 256 -c SHA256SUMS
```

The first command generates temporary results and compares all five expected files byte-for-byte. The second saves results in a new or empty directory; generated outputs are excluded from Git. The third checks the complete combined-package seal, including Modeling. The offline workflow also checks frozen input hashes, schemas and structural constraints. See [reproduction instructions](taxonomy/docs/reproduction.md), [query/count table](taxonomy/data/query-counts.csv), [gate scopes](taxonomy/data/gate-matrix.csv) and [method boundaries](taxonomy/docs/method-boundaries.md).

Query counts, processing receipts and gate scopes are saved upstream observations; the code does not regenerate native search or review evidence. The package does not repeat source collection, full-text retrieval or AI screening, establish the correctness of inclusion judgments, or consolidate independent works/versions. The eight-function codebook provides definitions and comparison questions but **no per-record function labels**. Complete function classifications, frequencies, saturation and agreement cannot be reproduced from this package. Scientific, coverage and work/version acceptance remain Partial or Unknown. The 1,312 included source records yield 1,301 typed keys; typed keys are not independent papers. The 237 user-directed non-inclusions preserve scientific pending status.

## Modeling reproduction scope

[modeling/](modeling/README.md) contains Case A's independent q/d expectations and basic figures, the preserved original decision pilot and clearly separate optimized-cap supplements, plus Case B's exact control calculation, basic policy figure, revised decision pilot and excluded initial campaign evidence. Actual prompts, decoding settings, option order, complete final outputs, exact input data and editable computation/plotting code are retained. Replay makes no API calls or fallback. Credentials, raw service envelopes and unrestricted hidden reasoning remain excluded.

Case A's saved GLM pilot has 23/24 optimal decisions. Case B has 8/14 schema-valid optimal effort choices from 15 revised attempts; one schema error stopped the campaign with nine unattempted cells. The mathematical success probabilities are exact policy expectations, not real platform effects or multi-round GLM task success. Install the pinned numerical/plot dependencies and follow the separate Modeling README for offline replay and a clean regenerated output copy. This scope does not broaden the taxonomy's five-output reproduction claim.

## Contents, translation and rights

`taxonomy/` preserves all 23 frozen-candidate files and its internal seal byte-for-byte. The original documents' term "public candidate" identifies that frozen source artifact; the current public destination is authorized separately. Statements about nonpublication and licensing retain their frozen context. Manuscript locators in claim mapping identify upstream discussion only; this repository contains no manuscript `.tex`, `.bib`, paper PDF or `paper/` directory. Modeling figure PDFs are included as model assets.

`method/` contains complete English translations of the three requested policy documents and a short context/dependency guide. The authoritative source documents remain unchanged outside the repository. Their original and translated SHA-256 values are recorded in PROVENANCE. The translated policies preserve brief user-decision quotations and opaque message identifiers under the user's explicit document-inclusion request; they differ from the redacted `taxonomy/` projections. Historical NotRun statements refer to policy-approval time, not current execution status. Some original relative references remain external dependencies, as listed in the Method guide.

The user explicitly authorized public GitHub publication. Ownership/license coverage for new code, documents and derived data remains unresolved; no MIT or CC license has been assigned. The upstream MIT notice is license evidence only. Primary full text, abstracts, screenshots, unrestricted internal conversations, raw service envelopes, credentials, original research Git and archives are excluded. Original material and prior package versions remain locally preserved.
