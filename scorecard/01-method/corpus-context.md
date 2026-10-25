# Consensus and dissent ledger, calibrated corpus v2

Snapshot date: 2026-08-02

Calibration and synthesis date: 2026-08-05

Evidence base: 304 final tagged records. Strata are academic 164, protocol specification 117, industry survey 11, and institutional report 12. Origin labels are Web2 196, Web3 82, and hybrid 26. Layer tags are multi-label: L1 163, L2 102, L3 89, L4 130, L5 145, L6 36, L7 40, and L8 40.

This ledger uses codebook 2.0.0. It is owner-calibrated and agent-assisted. Only the 22 calibration cards are human-reviewed. The old 2026-07-30 ledger is preserved at `data/precalibration_2026-08-05/consensus_dissent_ledger_invalidated.md`.

## L1 Identity and Trust

Consensus: agent commerce requires portable identity plus behavioral trust evidence. Registry membership alone does not establish capability or honest execution. Reputation, independent validation, attestation, and Sybil-resistant signals are recurring mechanisms. Evidence: `spec-erc8004`, `arxiv-2510.27554v1`, `arxiv-2512.06914v2`.

Dissent: the root of trust remains unsettled. Sources distribute trust among conventional credentials and institutions, on-chain registries and stake, hardware attestation, and hybrid combinations. ERC-8004 is a hybrid calibration anchor because it connects A2A and MCP endpoints to on-chain registries, but this does not make every credential system hybrid.

Open issue: identity, reputation, and authorization are frequently conflated. The calibrated boundary treats identity evidence as L1 and bounded authority as L4.

## L2 Discovery and Capability

Consensus: agents need machine-readable descriptions and a way to locate counterparties before exchange. Capability advertisement without validation creates adverse selection and Sybil exposure. Evidence: `sur-ehtesham2025-agent-interop`, `spec-erc8004`, `arxiv-2510.27554v1`.

Dissent: centralized directories offer governance and immediate revocation, while open registries offer portability and composability. Payment history can inform discovery, but its use as a reputation signal does not by itself make the source an L5 payment mechanism.

Open issue: no common assurance vocabulary binds an advertised capability to evidence that the capability works.

## L3 Orchestration and Delegation

Consensus: task negotiation, tool invocation, routing, and handoff form a distinct interim function. Execution traces improve observability, but a completed task state does not prove that delegated intent was faithfully followed. Evidence: `sur-ehtesham2025-agent-interop`, `arxiv-2512.06914v2`, `arxiv-2502.10637v1`.

Dissent: some sources treat orchestration as transport and workflow state, while others require economic commitments, provenance, or proof of correct effort.

Open issue: multi-hop delegation lacks an end-to-end chain binding the principal's intent to each downstream agent action.

## L4 Authorization and Mandate

Consensus: agent authority must be scoped by purpose, amount, counterparty, time, and replay protection. Signed mandates create evidence of authorization, but signature validity alone does not prove faithful execution. Evidence: `spec-ap2`, `arxiv-2512.06914v2`, `ind-google-ap2-blog`.

Dissent: conventional account and card credentials emphasize institutional recourse, while Web3 mechanisms emphasize verifiability and programmable enforcement. Hybrid designs translate between these guarantees but also inherit both failure surfaces.

Open issue: static mandates do not adapt to changing runtime trust, and revocation semantics are not consistently propagated into settlement.

## L5 Payment and Settlement

Consensus: machine-native commerce needs explicit authorization, execution, settlement evidence, replay resistance, and idempotency. Payment completion is distinct from service delivery. Evidence: `spec-x402`, `spec-ap2`, `arxiv-2502.10637v1`, `ind-crossmint-compare`.

Dissent: sources place the settlement trust anchor in card networks, payment processors, facilitators, smart contracts, or direct on-chain transfers. Irreversibility is treated either as useful finality or as a recourse deficit.

Open issue: no common primitive atomically binds correct service delivery to cross-rail payment finality.

## L6 Commerce Lifecycle

Consensus: discovery, cart construction, checkout, order state, fulfillment, returns, and refunds form a lifecycle that cannot be reduced to a payment call. Evidence is thinner than for L1, L4, or L5, with 36 tagged records. Evidence: `spec-ucp`, `spec-acp`, `ind-crossmint-compare`.

Dissent: protocol sources disagree on whether the lifecycle should be one end-to-end standard or a composition of specialized protocols. Industry comparisons often describe broad coverage that specifications only partially implement.

Open issue: post-purchase state and refund portability remain merchant-specific and weakly interoperable.

## L7 Presentation and Interaction

Consensus: user-facing presentation, observability, and intervention are separate from agent-to-agent transport. The word interaction is insufficient for an L7 tag unless the source defines what a principal sees or can control. Evidence: `ind-eco-7layers`, `sur-ehtesham2025-agent-interop`.

Dissent: some taxonomies end at interface delivery, while others treat presentation as a cross-cutting concern rather than an economic layer.

Open issue: no shared interface semantics expose mandate scope, trust evidence, payment state, and recourse options consistently across protocols.

## L8 Dispute Resolution and Arbitration

Consensus: receipts, logs, and attestations provide evidence but do not by themselves provide remedy. Ex post enforcement requires a forum, decision rule, and enforceable consequence. The corpus contains 40 L8 records, but they are dominated by proposals, adapted mechanisms, and partial receipt formats rather than a native, widely adopted agentic dispute standard. Evidence: `ietf-draft-kotecha-agentic-dispute-protocol`, `ietf-draft-birkholz-verifiable-agent-conversations`, `arxiv-2502.10637v1`.

Dissent: candidate roots of authority include platform chargebacks, courts, decentralized juries, optimistic oracles, slashing, and cryptographic proof-based remedies. They differ in latency, jurisdiction, subjectivity, and reversibility.

Open issue: an agent-speed mechanism for subjective disputes that interoperates across Web2 and Web3 settlement remains absent from deployed standards.

## Cross-layer tensions

T1. Identity does not imply authority. L1 credentials do not prove that an agent holds a valid L4 mandate.

T2. Authority does not imply faithful execution. A valid L4 signature does not prove correct L3 behavior.

T3. Payment does not imply delivery. L5 settlement can finalize without evidence that the promised service was correctly delivered.

T4. Lifecycle state does not propagate consistently. L6 order, fulfillment, return, and refund states are not portable across merchant and payment protocols.

T5. Presentation can hide guarantee loss. L7 interfaces may display a successful action while omitting the weaker guarantees at a Web2 to Web3 seam.

T6. Evidence does not imply remedy. Receipts and attestations support an L8 claim but do not select a forum or enforce a verdict.

T7. Hybrid composition is the minority case. Only 26 of 304 records are calibrated as hybrid, indicating that explicit trust translation is less developed than within-ecosystem mechanisms.

T8. The stack is coverage-complete but assurance-incomplete. All eight functions have research or proposal coverage, yet L8 lacks a native, widely adopted agentic enforcement protocol.
