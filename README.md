# sok8-acp

Offline code, data, analytical definitions and English translations of the requested Method policies for the current agentic-commerce taxonomy. The user approved this first 33-file batch for **`kl41r3/sok8-acp`, private, branch `main`**. The user-selected repository name does not designate a new protocol or a complete ACP implementation.

Start with the [submission review](REVIEW.md), [Method policies](method/README.md), [eight-function analytical codebook](taxonomy/docs/analytical-codebook.md) and [data dictionary](taxonomy/docs/data-dictionary.md). [MANIFEST](MANIFEST.json) binds every proposed file's size, SHA-256 and applicable CSV schema; [PROVENANCE](PROVENANCE.json) distinguishes the frozen candidate, translated policies and this packaging revision.

This initial batch contains the complete reviewed taxonomy/Method baseline. `modeling/` is excluded and deferred to a separate later commit after its work and checks finish. The manifest and checksums cover every file in this batch; subsequent batches require their own updated seals.

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

The first command generates temporary results and compares all five expected files byte-for-byte. The second saves results in a new or empty directory; generated outputs are excluded from Git. The third checks this entire first batch; Modeling is deferred to a separate later commit. The offline workflow also checks frozen input hashes, schemas and structural constraints. See [reproduction instructions](taxonomy/docs/reproduction.md), [query/count table](taxonomy/data/query-counts.csv), [gate scopes](taxonomy/data/gate-matrix.csv) and [method boundaries](taxonomy/docs/method-boundaries.md).

Query counts, processing receipts and gate scopes are saved upstream observations; the code does not regenerate native search or review evidence. The package does not repeat source collection, full-text retrieval or AI screening, establish the correctness of inclusion judgments, or consolidate independent works/versions. The eight-function codebook provides definitions and comparison questions but **no per-record function labels**. Complete function classifications, frequencies, saturation and agreement cannot be reproduced from this package. Scientific, coverage and work/version acceptance remain Partial or Unknown. The 1,312 included source records yield 1,301 typed keys; typed keys are not independent papers. The 237 user-directed non-inclusions preserve scientific pending status.

## Contents, translation and rights

`taxonomy/` preserves all 23 frozen-candidate files and its internal seal byte-for-byte. The original documents' term "public candidate" identifies that source artifact, not this private target. Statements about nonpublication and licensing retain their frozen context. Manuscript locators in claim mapping identify upstream discussion only; this reviewed taxonomy/Method base contains no manuscript `.tex`, `.bib`, PDF or `paper/` directory. Modeling figures are excluded from this batch and will be handled by their owner in a separate later commit.

`method/` contains complete English translations of the three requested policy documents and a short context/dependency guide. The authoritative source documents remain unchanged outside the repository. Their original and translated SHA-256 values are recorded in PROVENANCE. The translated policies preserve brief user-decision quotations and opaque message identifiers under the user's explicit document-inclusion request; they differ from the redacted `taxonomy/` projections. Historical NotRun statements refer to policy-approval time, not current execution status. Some original relative references remain external dependencies, as listed in the Method guide.

This is private GitHub preservation and collaboration, not public redistribution. Ownership/license coverage for new code, documents and derived data remains unresolved; no MIT or CC license has been assigned. The upstream MIT notice is license evidence only. Primary full text, abstracts, screenshots, unrestricted internal conversations, raw service envelopes, credentials, original research Git and archives are excluded. Original material and prior package versions remain locally preserved.
