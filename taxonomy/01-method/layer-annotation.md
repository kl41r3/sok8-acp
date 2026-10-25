# Layer Annotation Method

Method version: **2.0.0**. This English edition preserves the classification rules used in the 2026-10-19 annotation run. The scientific criteria below govern the saved dual ratings and adjudications.

## Purpose and unit of analysis

This method identifies the eight-layer functions substantively studied by each included publication. The unit of annotation is a distinct typed identifier in the final inclusion set. Existing publication and version relationships remain attached to that identifier. Layer annotation adds functional labels to the inclusion record.

## Classification and evidence

Every initial assessment and final decision assigns exactly one of these values to `classification`:

- A nonempty list of unique labels, sorted from L1 to L8, such as `["L3", "L5"]`.
- The string `"not_evidenced"`, when the evidence read establishes none of the eight functions.

Multiple labels are allowed without selecting a primary layer. Empty lists, `unclear`, `pending`, and combinations of layer labels with `not_evidenced` are invalid outputs.

Each positive label requires an exact quotation from the same publication and version, a retrievable source location, and a rationale connecting the quotation to the function. A `not_evidenced` decision records the research mechanism and one reason:

| Reason | Meaning |
|---|---|
| `outside_layer_functions` | The research focus described in the evidence falls outside the eight functions. |
| `insufficient_evidence` | The description provides insufficient detail to establish a function. |
| `evidence_unavailable` | Material needed to establish a function remained unavailable after documented retrieval attempts. |

These reasons explain a single classification outcome. Execution failures and skipped records require operational correction. Access failures encountered during a completed assessment are recorded with the resulting evidence-based decision.

## Layer definitions

The layer names follow the current manuscript. A positive label requires both an explicit description of the function and substantive treatment through design, analysis, evaluation, or comparison. Background mentions, keywords, default platform behavior, and broad research objectives alone provide insufficient support.

| Layer | Name | Qualifying research | Insufficient grounds on their own |
|---|---|---|---|
| L1 | Identity and Trust | Identity, authentication, credentials, reputation, trust estimation, or trust judgments grounded in provenance or counterparty evidence. | General references to security, privacy, rationality, or reliability without an identity or trust mechanism. |
| L2 | Discovery and Capability | Capability or resource description, publication, search, or selection of providers, resources, and counterparties according to suitability. | Optimizing auction winners, resource quantities, or returns; mentioning matching without specifying its objects or criteria. |
| L3 | Orchestration and Delegation | Inter-agent messages or interaction rules, coordination of tasks and roles, delegation, or subcontracting. A specified mechanism coordinating interdependent actions among agents qualifies. | Merely using a multi-agent system; one bidder optimizing its bids in an existing market; prediction and optimization steps internal to one model. |
| L4 | Authorization and Mandate | Principal authorization, consent, permissions, role policies, authorization scope or revocation, or permission constraints enforced during execution. | Budget optimization, valuations, capacity limits, or other economic and physical constraints; assuming authorization solely because an agent acts for someone. |
| L5 | Payment and Settlement | Payment obligations or rules, transfers, escrow, settlement, or commitment and release of funds. Theoretical payment rules qualify. | Price prediction, bidding, profit optimization, first-price or second-price terminology alone, or payment mentioned only as context. |
| L6 | Commerce Lifecycle | Formation and management of transactions, orders, and contracts; checkout, fulfillment, delivery, acceptance, modification, cancellation, or refunds. | Bargaining strategy or allocation efficiency alone; incidental contracts and orders in a simulation; order matching without studying commitment formation. |
| L7 | Presentation and Interaction | Human-facing presentation, preference input, explanation, approval, supervision, intervention, or commercial interactions between actual humans and agents and their outcomes. | Inter-agent communication, simulated human personas, humans acting only as programmers, or internal logs with no established human audience. |
| L8 | Dispute Resolution and Arbitration | Evidence, decision rules, adjudicators, arbitration, remedies, and enforcement connected to dispute or breach claims. | General conflict, security, or punishment; routine payment after acceptance; refunds without a dispute or breach-handling procedure. |

### Boundary decisions

1. **Bidding and coordination.** Offer and counteroffer rules or a specified distributed procedure coordinating agents can establish L3. Price prediction followed by optimization of one agent's bid cannot. A statement that agents cooperate requires details of the method and its coordinating role; record the missing information when these are absent.
2. **Pricing and payment.** L5 concerns who pays whom, how much, when, and under which escrow or release conditions. Distinguish payment rules in a model from actual fund transfers. Price estimates and returns alone fall outside this criterion.
3. **Matching and lifecycle.** Suitability-based counterparty selection can establish L2. Order acceptance, commitment formation, and changes in fulfillment state can establish L6. Assign each label from evidence of its specific function.
4. **Bargaining and contracts.** Offer sequences and interaction rules can establish L3. Add L6 when the study substantively addresses the resulting obligations, contractual commitments, or their management.
5. **Security and permissions.** Authentication and trust mechanisms map to L1; checks of which roles may perform which actions map to L4. General security design and attack detection require evidence of a qualifying function before receiving a label.
6. **Human interaction.** Studied interactions between actual humans and trading agents support L7. Humans appearing only as motivation, model templates, or programmers do not meet this criterion.
7. **Refunds and disputes.** Order refunds can support L6, and the associated fund flow can support L5. L8 requires a connection to the judgment and remedy of a dispute or breach claim.

For example, a mobile-auction abstract listing a platform, bidding strategy, and privacy scheme without explaining their functions can receive `not_evidenced` with `insufficient_evidence`. A travel-competition agent focused on price prediction and optimal bidding can receive `not_evidenced` with `outside_layer_functions`. Apply the criteria to each record's evidence.

## Annotation workflow

1. **Freeze scope and evidence.** Create one record per final included identifier. Verify its title, identifier, source memberships, and abstract. Preserve the complete abstract read, its physical file and JSON pointer, hash, and whitespace convention. Give A and B identical evidence packets containing the source material, with prior screening rationales and layer judgments withheld.
2. **Assess independently.** Two agents in separate contexts each read the complete evidence packet and provide a definite classification, per-layer evidence, and a concise rationale. Record unresolved questions in `followup_question` while classifying from the available evidence. Each agent works independently of the other's output and judges substantive mechanisms rather than generating labels from keywords, titles, or sources.
3. **Validate the records.** Check coverage, identifiers, classification types, label sets, evidence fields, and exact quotations. Return formatting or quotation errors to the original author and preserve the correction record. Scientific judgments remain independent of the observed agreement rate.
4. **Compare complete label sets.** Adopt the shared result directly when A and B assign identical sets or both assign `not_evidenced`. Any label difference triggers adjudication. Resolve disagreements through judgment rather than automatically taking the intersection or union. A question in `followup_question` alone does not trigger adjudication for an agreed record.
5. **Adjudicate disagreements.** Assign C to an independent agent that has not initially rated the record. C reads the same evidence, both assessments, and the points of disagreement, then applies the same criteria. C may adopt either assessment or assign another supported result. Preserve A, B, and C's decisions and explain how each disagreement was resolved. C supplies a definite classification.
6. **Supplement evidence where needed.** C first states a specific question whose answer could change the classification. Consult saved full text from the same publication and version, then obtain relevant passages from the publisher or official proceedings if needed. Read the portions required to answer the question. Preserve excerpts, section or page references, URLs, retrieval time, identity bindings, and hashes separately from the original abstract. Record access failures. C then retains every supported label, or assigns `not_evidenced` with a reason when none is supported. Preserve the original A/B inputs and judgments.
7. **Merge and verify.** Produce one final row per included identifier, the complete label set, eight derived indicator columns, evidence, mechanisms, provenance, paths, model records, initial agreement statistics, and adjudication changes. Verify unique and complete coverage, valid final classifications, and exact source support for every positive label. Report mechanical verification, AI agreement, and human scientific review as distinct checks.

## Annotation scope

All 1,301 included identifiers receive independent double coding under method 2.0.0, followed by adjudication of differing classifications. The original 100 records are reassessed from their abstracts in fresh contexts. The completed v2 assessments of the other 1,201 records remain part of the final dataset. Current results and statistics use this unified v2 population.

## Model, version control, and interpretation

Initial assessment, supplementary-evidence interpretation, and adjudication explicitly request `gpt-6-astra` with `reasoning_effort=high`. Record the requested configuration and independently verifiable runtime model identifier. A model substitution requires an explicit recorded change. Record unexposed server checkpoints, temperatures, and sampling seeds as unavailable. The agents provide separate judgments in independent contexts using the same model.

Freeze the method, prompts, and code hashes before execution. A change to classification criteria requires a new method version and an account of affected records. Reproduction verifies inputs, task allocation, comparisons, and aggregation from saved judgments; a fresh model invocation may produce different annotations.

Layer labels describe functions established by the evidence read. An unassigned layer indicates a lack of established support within that evidence scope. Counts describe included identifiers and their coded functions; protocol capability and deployment performance require their own evidence.

The [coding materials](../05-code/layer-annotation/README.md) contain the prompts and output schema. The [distributed results](../04-final-selection/README.md) are reconstructed from saved judgments by the [reconstruction code](../05-code/README.md).
