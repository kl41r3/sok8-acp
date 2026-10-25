# Case A/B technical extensions

This revision preserves the original model implementations and baseline
results, then adds two bounded extensions:

| Extension | Question | Main limit |
|---|---|---|
| Case A: costly fallback | When does the agent request review that raises user loss, and how does the timeout action change that choice? | Fixed mandate; fallback must remain feasible and preauthorized |
| Case B: evidence availability | How do post-submission evidence loss and missing-evidence rules affect optimal effort, reporting, and adverse updates? | Fixed revenues; finite horizon; truthful received evidence and independent loss |

Read `../case-a/fallback/README.md` and `../case-b/evidence-loss/README.md` for
derivations, timing, ties, metric denominators, and scientific limitations.

## Reproduce

Use Python 3.12 and install the root `requirements.txt`, as documented in the
root README. The existing command now includes both extensions and all four
final manuscript figures:

```sh
python -B reproduce.py --output outputs/reproduction
```

For an extension-only run:

```sh
python -B modeling/extensions/reproduce.py --output outputs/model-extensions
```

Use a new output directory each time. The extension runner:

1. Checks protected upstream files against `baseline-files.json`.
2. Regenerates the models and compares nine frozen datasets byte for byte.
3. Runs symbolic checks and independent rational enumeration, recovering the
   original Case B policies and both initial-state paths.
4. Regenerates the four one-column manuscript figures, verifies their input
   hashes and layout audit, and reports byte agreement for all twelve exports.

Add `--exact-figures` to the extension-only command to require byte-identical
PDF/SVG/PNG exports as well. Rendering bytes may vary by platform; scientific
dataset comparison remains exact in every run.

`verification.json` records the checks and ends with `passed: true` on success.
No credentials or live model APIs are used. Dependency installation requires
network access; calculation and figure export run locally.

The public-upstream commit and protected file hashes are recorded in
`baseline-files.json`. This revision does not replace literature-selection
data, source identifiers, historical experiments, or the framework diagram.
Root documentation, the runner, traceability, and integrity inventories are
updated to make the additions discoverable and reproducible. No new license
is assigned. Manuscript source is maintained separately.

`RESPONSE_MATRIX.md` maps each extension to the review concern it addresses.
These calculations establish conditional results, not empirical agent
behavior, an optimal mechanism, or a universal welfare ranking.
