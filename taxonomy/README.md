# Taxonomy corpus: local release candidate

This package organizes the current corpus/query/final-selection evidence used by the taxonomy Method and Appendix. It is a **local preparation**, with no assigned release version, DOI, dataset URL, public repository or publication. Dataset redistribution rights and the license for newly staged code remain unresolved. The existing upstream software notice is retained as evidence in [licensing](docs/licensing-and-release-readiness.md).

The frozen frame contains 5,241 source rows and 5,208 typed identifiers. The academic selection track has 5,217 source rows: 1,312 included, 3,668 original rule/evidence exclusions and 237 user-directed non-inclusions of unresolved records. Scientific pending states remain unchanged. The 1,301 included typed identifiers are not independent works. Three IEEE standards and 21 AAMAS relation-only cases are separate. Work/version quantities remain Unknown, and scientific/coverage/work-version acceptance remains Partial.

## Code and data

- Offline entrypoint: [code/reproduce.py](code/reproduce.py).
- Frozen identifier/decision projection: [data/records.csv](data/records.csv); administrative overlay: [data/selection-overlay.csv](data/selection-overlay.csv).
- Exact query and field/count table: [data/query-counts.csv](data/query-counts.csv); scoped gates: [data/gate-matrix.csv](data/gate-matrix.csv).
- Expected final selections, source counts and typed-key views: [expected/](expected/); claim mapping: [docs/claim-to-artifact.csv](docs/claim-to-artifact.csv).
- Analytical function definitions: [docs/analytical-codebook.md](docs/analytical-codebook.md); no corpus function labels are distributed.
- Schemas and exclusions: [docs/data-dictionary.md](docs/data-dictionary.md); frozen policies and limitations: [docs/method-boundaries.md](docs/method-boundaries.md).

## Reproduce offline

Python 3.9 or later; standard library only. No package install, model, credentials, network, GPU or source service is required. Allow approximately 100 MB free RAM and 10 MB for generated outputs. Run from this directory:

```sh
python3 -B code/reproduce.py --check-only
python3 -B code/reproduce.py --output outputs/run
```

The first command checks all package hashes and CSV schemas, applies the frozen overlay, and compares five regenerated files byte-for-byte to `expected/` using temporary output. The second saves those five files in a new or empty directory. Existing outputs are never overwritten. Expected terminal status: `Verified offline mechanical reproduction`; included source rows 1312, included typed identifiers 1301, all typed identifiers 5208, and preserved scientific pending selection rows 237. [Detailed instructions](docs/reproduction.md) state the exact scope and checks.

The query table and processing receipts are frozen saved observations. This workflow does not requery native engines, rerun AI screening or retrieve licensed evidence. It preserves the saved typed keys and does not reconstruct independently accepted work/version entities or create new taxonomy labels. See [verification](docs/verification.md).
