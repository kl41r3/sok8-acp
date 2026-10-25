# Corpus Method

## Scope and retrieval

The academic-selection frame combines ACM Digital Library, IEEE Xplore, AAAI, and IJCAI records. AAMAS proceedings supply a separate bounded publication-relationship check. The public-availability cutoff is the end of 19 September 2026 in America/New_York, with no lower publication-year limit. The date belongs to the version represented by the identifier; conference event dates alone do not establish public availability.

[queries.csv](../02-source-evidence/queries.csv) records the full query expressions, actual search fields, observed counts, and source-specific counting scope. ACM used its Full-Text Collection with 27 Abstract and four AllField query/field pairs. The collection and search field are separate parameters. IEEE used abstract-field searches; its 1,000-row export limit required splitting the 1,744-result G03 search into 1985–2005, 2006–2016, and 2017–2026. AAAI and IJCAI used official proceedings metadata and author abstracts with the approved local Boolean matching procedure. Local matches are distinguished from native search-engine hits.

ACM retained 4,964 query appearances and 2,573 records. IEEE retained 4,346 appearances and 2,492 identifiers across 20 exports, including three standards outside the academic-selection denominator. The AAAI and IJCAI selection frames contain 96 and 59 records. Repeated query appearances and cross-source repetitions are retained through source memberships rather than treated as independent publications.

The AAMAS check considered 767 captured official HTML abstracts. Twenty-one matching cases produced 37 query appearances and 28 candidate relationship edges to ACM records. These cases add no confirmed inclusion or cross-identifier work/version merge. Missing abstracts, an inaccessible metadata page, and unchecked years bound this source check.

## Eligibility

Individual papers, surveys, posters, demonstrations, and extended abstracts qualify as publication units. Whole proceedings and books do not. Six separately authored IEEE chapters were approved as eligible units and still required relevance, date, identity, and evidence checks.

Inclusion requires one of two criteria:

1. **I1, direct commercial interaction.** The study establishes autonomous software agents, LLM agents, or an implemented or simulated software multi-agent system; explicit buying, selling, procurement, quotes or bids leading to transactions, orders, payment, delivery, refunds, or disputes; and substantive treatment of the participating roles, interaction rules, authorization, negotiation, allocation, payment mechanisms, or executable transaction process. Classical agents and software implementations of theoretical mechanisms qualify. Deployment is optional.
2. **I2, commercially relevant enabling protocols.** The study substantively investigates an identifiable agent protocol or standard and its mechanisms, such as messages, states, interoperability, tool calls, sessions, authorization, revocation, trust, attacks, defenses, or protocol costs, with an explicit commercial connection. A2A, AP2, and MCP use the study's fixed E001 commercial-link evidence where applicable; other protocols require a commercial connection established for that record.

General recommendation, prediction, marketing, logistics, code generation, economic strategy, security, blockchain performance, and broad agent frameworks qualify only when their evidence satisfies I1 or I2. Keywords and incidental protocol mentions are insufficient. Published versions are preferred; previously approved preprint-only exceptions address critical protocol gaps under the same eligibility criteria.

## Screening and review

Records retain the publication identity, source memberships, decision, rule, rationale, and evidence level. Screening begins with complete author abstracts. ACM's frozen abstract-only run did not use supplementary full text. IEEE, AAAI, and IJCAI allowed targeted full-text reading when a specific question could change inclusion. Such exceptions preserve the question, same-publication/version binding, passages or quotations, and actual reading scope.

Initial AI recommendations and central AI decisions are retained where available. Central review could see prior recommendations. It covered inclusions, targeted exceptions, uncertain or low-confidence records, and identity or version boundaries. Four recovered ACM abstracts went directly to central review; all 155 AAAI/IJCAI records received central review. The evidence and reviewer scope describe the actual saved run.

Final selection is binary. Records lacking required evidence are excluded with the specific reason. This accounts for 51 ACM, 170 IEEE, ten AAAI, and six IJCAI formerly unresolved records. Their original scientific assessments remain visible alongside the final selection, so an evidence gap is distinguishable from an affirmative finding of irrelevance.

## Consolidation and functional analysis

Exact identifiers define the merge operation. Any source inclusion retains the identifier. The full 5,241-record frame loses 33 repeated rows, yielding 5,208 identifiers. The 1,312 included academic records lose 11 repeated source rows, yielding 1,301 included typed identifiers. Similar titles or authors identify candidates for investigation; they do not establish cross-identifier work/version equivalence.

[Layer annotation](layer-annotation.md) classifies all 1,301 included identifiers from identical abstract packets supplied to two independent coders. Complete-label disagreements receive third-coder adjudication, with same-publication supplementary passages where required. The final analysis uses the 771 identifiers with at least one layer label. The other 530 are `not_evidenced`. Among the labeled records, 564 precede 2023 and 207 date from 2023 onward. Multilabel counts and period shares use the denominator stated in each table.

The released [source evidence](../02-source-evidence/README.md), [decisions](../03-screening-review/README.md), and [code](../05-code/README.md) reconstruct all saved-input-to-output computations. Search observations and scientific judgments are study inputs; independent retrieval or reannotation is a separate study operation.
