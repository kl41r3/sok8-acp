# Workflow template v2: abstract-first with targeted full-text exceptions

**Policy status: Approved; version: cross-source-v2-20261001.** The user confirmation was recorded at 2026-10-01 17:25:21 America/New_York. This version applies to subsequent runs; this task only confirmed the documents. Pilots, searches and retrieval outside ACM were NotRun at that point. See [source.md](source.md) for the approval basis and source roles, and [acceptance.md](acceptance.md) for workflow acceptance.

v2 applies to subsequent runs. The current 31 mixed Abstract/AllField ACM queries and abstract-level screening continue under the [frozen protocol](acm-completion-20261001/protocol.json) and [workflow snapshot preceding this version](archive/source-policy-v2-before-20261001T212521Z/workflow-template.md). Do not retrospectively claim that the historical run used v2 or automatically reassess old records.

## 1. Required parameters

| Parameter | Default and freeze requirements |
|---|---|
| run/approval/responsibility | Unique run_id, execution authorization scope, date, executor and integrator; policy confirmation does not mean a new run has executed. |
| scope/rule | Inherit I1/I2, T1/T2, V1 and protocol commercial associations from [ACM golden rule v1](golden-rule.md); separately retain a v2 copy and hash. Adapt future-run A0/X2 evidence paths as specified below; do not change the old rule file. |
| source/collection/venue | Exact entry point and collection; list venues separately and check overlap against existing coverage evidence. |
| discovery_fields/syntax | Default to Abstract; preserve approved concept logic and translate only platform syntax. If no equivalent field exists, record the closest scope and an **explicit deviation decision**; do not silently substitute metadata/AllField/full text. |
| cutoff/languages | End of 2026-09-19 in America/New_York; no starting year; English/Chinese; retain primary evidence of the public date of the current identifier-bound version. |
| document_types/versions | Individual papers, posters, demos, extended abstracts and surveys; exclude whole proceedings; publication status, preprint exceptions and the separate official-specification track follow source.md; do not change frozen-batch eligibility. |
| exact_queries/inputs | Actual expressions, URLs, fields, filters, sorting, original inputs/tool versions and hashes; a name match does not replace scope assessment. |
| retrieval_mode/stop | Default complete_export: retrieve all actual returns of the frozen queries. Do not substitute an RSS pool; bounded_pool requires an explicit deviation decision and boundary and cannot pass as complete retrieval. |
| commerce_associations | I2 requires both explicit protocol mechanisms and commercial relationships. The fixed Google A2A/AP2/MCP associations may reuse E001 evidence; do not infer other associations from acronyms or names. |
| planning | A total of 150 to 200 across all sources is a workload reference, not a per-source quota, inclusion target or stopping condition. |

## 2. Execution and evidence

| Stage | Operation and retained evidence |
|---|---|
| S0 Freeze | Confirm execution authorization; retain source policy, v2/base rule, parameters, queries and input hashes; mark each stage NotRun. |
| S1 Field/parser check | Use a few representative pages to check Boolean logic, Abstract field, collection, dates, IDs, abstract boundaries, sorting/pagination and export caps; record syntax transformations and deviation decisions. A readable page does not mean source discovery is complete. |
| S2 Complete retrieval | For each query retain URL/request, UTC time, actual filters/fields, native total Hq, pages/cursors, returned appearances Oq, original exports and hashes, and termination evidence. Record zero returns, failures, truncation and unretrieved scope separately. |
| S3 Identity/work consolidation | Consolidate appearances with the same normalized ID and retain all source/query memberships; establish work_id across IDs only with primary publication/version correspondence. Title/author similarity generates candidates only; preserve relationships for conference extensions. |
| S4 Abstract-first | Obtain the complete author abstract with the same paper's title/authors/ID and date/version evidence; retain original text, sections, URL, time and hash. Related recommendations, AI Summary and truncated cards do not replace original text. |
| S5 Judgment and targeted exceptions | Check type/date first, then assess the same I1/I2/X1 content scope. Use abstracts for clear cases; conduct targeted full-text review for genuinely uncertain cases under the next section, without automatic exclusion under old X2. |
| S6 Batches and central review | If parallel, sort IDs and freeze 3 to 4 disjoint batches with common rule/input hashes; workers write only their assigned outputs. Centrally review all inclusions, full-text exceptions, low-confidence/ambiguous cases, identity/version boundaries and major comparisons; retain supplements/overrides separately. |
| S7 Reconciliation and delivery | Give each candidate a disposition, duplicate target, evidence and reviewer; retain audit, search-log, exception records, counts, gaps and acceptance. Deliver record-level results only when independent works are not yet established. |

I1 still requires support for a software agent, commercial activity and a substantive interaction/authorization/transaction mechanism; I2 still requires both explicit protocol mechanisms and commercial relationships. Nondeployment, a non-leading venue or absence of a DOI is not a sufficient exclusion reason. Targeted full text changes only the available evidence level, not these scientific conditions.

## 3. Targeted full-text exceptions and A0/X2

**Trigger:** The abstract cannot reliably answer a specific question that affects the decision, such as substantive study of a mechanism, protocol identity or a commercial relationship. First record why the case is genuinely uncertain and the question to resolve; then locate identity-matched, version-matched full text and relevant sections. Do not generally upgrade records because they might be useful or introduce database-wide full-text queries.

**Decision path:** First seek a primary author abstract when it is missing. If none is obtained and no qualifying exception evidence exists, assign `pending/missing_primary_abstract`, not directly out of scope. Abstract ambiguity does not automatically invoke old X2 exclusion; conduct targeted review. Unavailable required full text yields `pending/fulltext_unavailable`; reading that still does not resolve the question yields `pending/scope_uncertain`. If located original text clearly supports or does not support the scope, form the final judgment under original I1/I2/X1 with a reason; do not equate unread evidence with irrelevance. Type/date controls retain the inherited rules; exceptions do not retroactively change eligibility.

**Evidence record:** For each exception retain recordID, trigger reason, question, version/identity evidence, full-text source/hash, actual sections or page ranges read, verbatim quotations and locations, original abstract judgment, review result and reviewer. Reading relevant passages does not establish that the whole paper was read. Insufficient evidence cannot support capability or effectiveness claims; this workflow does not validate payment security or protocol execution.

Fill `evidence_level` for every record: `abstract`, `fulltext-exception`, `control-only` or `unavailable`. A record decided using body text must be `fulltext-exception`. If its abstract is missing, retain `abstract_available=false`. Retain exception trigger/retrieval/review status; body text without location binding and central review cannot support a final judgment. Store supplementary evidence and hashes separately without overwriting original inputs or judgments.

## 4. Counts and minimum outputs

`Hq` is the official hit count per query, `Oq` is actual appearances, `U` is normalized identifier entities, `W` is evidenced independent works and `V` is versions. `ΣHq` is not an independent-work count; do not replace Unknown with 0. `O = U + same-identifier repeated appearances`; `U = include + exclude + pending`.

Report abstract and full-text-exception include/exclude/pending separately, listing control-only and unavailable separately; mutually exclusive evidence-level subtotals must equal U. List exception triggers, actual targeted reads and unavailable cases separately. Official specifications and implementations have a separate ledger and do not enter academic-work counts.

- **search-log:** queryID, exact_query, actual field/collection, deviation decision, filters/sort, URL/time, Hq/Oq, page/cursor, cap/completeness, raw_path/hash, and failure/termination evidence.
- **audit:** recordID, normalized ID, work_id/version_relation, title/authors, source/query memberships, type/publication status/date evidence, decision/clause/reason, evidence_level, abstract_available, original text/hash, quotations/locations, confidence/ambiguity, reviewer and rule/policy hashes.
- **exception-review:** the exception fields above, original/final judgment, supplement/override paths and hashes; model review does not imply human consensus.

## 5. Termination and versions

Deliver the frozen scope after complete query-return retrieval ends, individual dispositions and reviews are traceable, and counts and acceptance pass. Unexplained caps or missing pages permit only Partial, not Complete or field-wide exhaustiveness. Do not change queries/eligibility to reach a count, clear pending or obtain favorable results.

v2 policy approval does not automatically authorize executing new sources; obtain corresponding authorization and freeze platform parameters first. Do not reassess current ACM v1. Record the policy version for subsequent v2 runs; evidence conclusions apply only to passages actually reviewed, not a comprehensive full-text review. [Original-byte snapshot preceding this version](archive/source-policy-v2-before-20261001T212521Z/workflow-template.md).
