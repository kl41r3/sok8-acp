# Layer-level coherence packet (corpus synthesis, not a protocol rank)

Evidence: `sok8/corpus/consensus_dissent_ledger.md` (2026-08-05),
`sok8/corpus/data/calibrated_synthesis_summary.json`, multi-label n from
304 tagged records. Hybrid origin n = 26.

| Layer | n | Ledger consensus (locator) | Assigned information problem | Open failure |
|---|---|---|---|---|
| L1 | 163 | Portable identity plus behavioral trust; registry membership is not capability. `spec-erc8004`, `arxiv-2510.27554v1` | Adverse selection / identity | Sybil inflation; fragmented reputation. T1 |
| L2 | 102 | Machine-readable descriptions needed; advertisement without validation is adverse selection. `sur-ehtesham2025-agent-interop` | Adverse selection / discovery | No common binding of advertised capability to demonstrated performance |
| L3 | 89 | Task routing and traces exist; completed state does not prove intent fidelity. `arxiv-2512.06914v2` | Moral hazard / effort | Multi-hop handoff unbound. T2 |
| L4 | 130 | Authority must be scoped; signed mandates exist; signature ≠ faithful execution. `spec-ap2`, `ind-google-ap2-blog` | Moral hazard / commitment | Revocation not consistently propagated into settlement |
| L5 | 145 | Payment needs authorization, settlement evidence, replay resistance. Payment ≠ delivery. `spec-x402` | Moral hazard / payment | No atomic bind of delivery to finality. T3 |
| L6 | 36 | Lifecycle cannot be reduced to a payment call. Thin evidence. `spec-ucp` | Incomplete contracts / state | Post-purchase state merchant-specific. T4 |
| L7 | 40 | Presentation is distinct from transport. Thin evidence. `ind-eco-7layers` | Information revelation | Interface success can hide weaker seams. T5 |
| L8 | 40 | Receipts are not remedy. Need forum, rule, consequence. `ietf-draft-kotecha-agentic-dispute-protocol` | Contract enforcement | No native agent-speed standard. T6, T8 |

Tensions T1–T8: identity ≠ authority; authority ≠ execution; payment ≠ delivery;
lifecycle not portable; presentation can hide loss; evidence ≠ remedy;
hybrid is 26/304; coverage-complete but assurance-incomplete.

Human review: 22 calibration cards only. Corpus is owner-calibrated and
agent-assisted.
