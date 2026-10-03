# Modeling artifacts: Cases A and B

This folder contains the two conditional mathematical examples and the small **saved GLM decision pilot** discussed in the manuscript's Modeling section. Case A treats review timeliness `q` and autonomy cap `d` as **independent parameters**. Case B models seller effort/reporting under four observation policies. Neither case is a deployed protocol experiment, an estimated market model, or an end-to-end multi-round LLM transaction simulation.

| Artifact | Main result | Evidence |
|---|---|---|
| [Case A](case-a/README.md) | 501 x 601 independent `(q,d)` pairs; the effect of increasing timely review depends on the fixed cap | Exact expectations, complete CSV/NPZ, heatmaps, fixed-cap curves, editable code |
| Case A GLM decisions | 23/24 valid decisions maximize the specified utility | Actual prompts/settings/order/final answers and formula scoring |
| [Case B](case-b/README.md) | Eight-round expected success from G: 30%, 67.5%, 82.5%, 37.41% across voluntary, 25% task-bound, full task-bound, 25% complaint policies | Exact dynamic program, forward expectations and basic policy-comparison figure |
| Case B GLM decisions | 8/14 schema-valid effort decisions maximize the specified utility; 7/7 with four rounds left and 1/7 in the final round | Fifteen attempted revised requests, one schema error, nine unattempted cells; initial under-specified campaign excluded |

## Offline setup and commands

Use Python 3.12 or later. Numerical checks need NumPy; plots additionally need Matplotlib and PyYAML. The versions used to generate the retained figures are pinned in [requirements.txt](requirements.txt). These packages are dependencies, not model APIs. Install them in a local virtual environment:

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r modeling/requirements.txt
python -B modeling/replay.py --output outputs/modeling-replay.json
python -B modeling/reproduce.py --output outputs/modeling-reproduction --plots
```

Commands above are run from the package root. Choose a new output directory for reproduction. The workflow copies these scoped artifacts into that directory, regenerates Case A data, recomputes Case B control values, rechecks both pilots and regenerates the three main figures and the optimized-cap supplemental figure. It makes **zero API calls**, needs no credentials and performs no model fallback. The original released files stay unchanged. Typical resource needs are tens of MB of data and about a minute on a laptop; the independent validation uses one million deterministic theta midpoints per selected pair, not stochastic sampling.

Expected replay: `case_a.independent_pairs=301101`, `valid_decisions=24`, `optimal_decisions=23`; `case_b.attempts=15`, `schema_valid=14`, `effort_optimal=8`, exactly one schema failure and nine unattempted IDs. All 64 Case B remaining-horizon/state/policy control cells are recomputed, with exhaustive enumeration of eight contingent actions as a check. Numerical checks validate the specified implementation and saved evidence, not scientific readiness of an entire paper.

## Evidence, provenance and manuscript mapping

[api-settings.json](api-settings.json) fixes the observed endpoint, requested/returned model identifier, access date and decoding settings. The API was the official China `open.bigmodel.cn` endpoint, requested model `glm-5.3-flash`, temperature 0.3, JSON-object response format, enabled thinking with low reasoning effort, maximum 4,096 tokens, no automatic retries and no fallback. Individual projections retain the actual request messages and complete final-answer string. A's twelve scenarios have two fresh calls with reversed option order; B's two draws/cell use the saved seeded option ordering and request sequence. Returned model strings are not independent attestation of model weights.

[claim-map.csv](claim-map.csv) connects numbers, figures, inputs, generating code, checks and manuscript labels. The manuscript itself is delivered separately as an Overleaf package. [source-provenance.json](source-provenance.json) binds unchanged upstream source bytes and identifies adaptations or evidence projections. Authoritative raw responses and prior analyses remain locally preserved. No source original or excluded failure was repaired to improve the reported agreement.

The prior five-q grid and continuously optimized-cap followup are retained under `case-a/supplemental/`; they answer a separate design question and are not the independent-parameter result. The initial Case B campaign is retained as **excluded** evidence because its prompt omitted the numerical monitoring probability. The accepted revision stops on a nested-schema response; no unwrapping, retry, replacement or backfilling is applied.

## Rights and release boundary

The new code, English descriptions, figures and derived data originate in this project. No additional MIT/CC license is assigned; ownership and future public-redistribution coverage remain unresolved, as in the parent package. The shared plotting utility is a project-local helper, not a fetched external image. Assets include no primary article text, abstracts or third-party illustrations. The package excludes credentials, private filesystem locators, service request IDs/raw HTTP envelopes, unrestricted hidden reasoning, internal conversations, Wiki/history, caches and archived manuscripts. Selected synthetic task prompts and **final** answers are shipped because they are the evaluation evidence.

This is verified local preparation for the existing private target, not a remote upload or a claim of anonymous review readiness.
