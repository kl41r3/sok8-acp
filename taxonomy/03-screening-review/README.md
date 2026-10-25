# Screening and Layer Review

[records.json](records.json) contains one final selection decision for each of the 5,217 academic source records. It preserves the reason, rule, evidence level, source identity, prior scientific assessment, available initial recommendation and central scientific review, and actual reading scope. `include` and `exclude` define final selection. A prior `pending` assessment records the original evidence gap and does not create a third final-selection category.

The `layer-annotation/` directory contains:

- `annotations/A01.json` through `A14.json` and `B01.json` through `B14.json`: 2,602 independent initial judgments for 1,301 identifiers.
- `adjudications/C01.json` through `C14.json`: all 170 complete-label disagreements, resolved by a third coder.
- [execution.json](layer-annotation/execution.json): model, reasoning effort, observed execution times, and distinct anonymous context identifiers for the 42 jobs. Server checkpoint, temperature, and sampling seed were not exposed.

Each judgment records the exact evidence read, layer set or `not_evidenced`, mechanism, rationale, and quotations. Finalization adopts A's judgment when the full A/B label sets agree and C's judgment otherwise. It checks exact quotation membership against the distributed source text and supplementary passages before producing results.

The saved judgments are the scientific inputs to offline reconstruction. The [method](../01-method/layer-annotation.md) and [prompts](../05-code/layer-annotation/README.md) support an independent annotation run with fresh contexts.
