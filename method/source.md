# Source plan v2: confirmed

**Policy status: Approved; version: cross-source-v2-20261001.** The user confirmation was recorded at 2026-10-01 17:25:21 America/New_York. This version applies to subsequent runs; this task only confirmed the documents. Pilots, searches and retrieval outside ACM were NotRun at that point.

ACM Full-Text Collection and IEEE Xplore are confirmed as the main academic search entry points; AAAI/IJCAI provide targeted checks of formal proceedings; AAMAS prioritizes coverage checking and gap filling; arXiv is a limited auxiliary source; OpenAlex/DBLP are optional. This is a user-confirmed work plan, not evidence that these sources are universally considered the most relevant or cover the entire field. The local record is authoritative; Library holds a copy.

## Confirmed entry points and boundaries

| Entry point and role | Coverage, overlap and execution limits |
|---|---|
| **ACM Digital Library: core** | The current collection is Full-Text Collection, not Guide; platform indexing does not imply ACM publication. Future runs default to the Abstract field. Native hits and RSS returns are reported separately; RSS does not establish complete retrieval. [Official guide](https://libraries.acm.org/binaries/content/assets/libraries/new_acm-digital-library-user-guide.pdf) |
| **IEEE Xplore: core** | A complementary entry point for networking, communication, systems and security research; check overlap with ACM and the publication entity at the work level. Future runs use the Abstract field; the default metadata scope is broader and must not be described as abstract-only search. Verify pagination and export caps during execution. [Search guide](https://ieeexplore.ieee.org/Xplorehelp/downloads/user-guides/IEEE_Xplore_Searching_and_Saving_Searches.pdf) |
| **AAAI: targeted check** | [Official portal](https://ojs.aaai.org/) and [search entry](https://ojs.aaai.org/index.php/AAAI/search); individual records provide RIS/BibTeX. Field semantics and bulk export remain to be verified; complete abstract-query support is not claimed. |
| **IJCAI: targeted check** | [Past conferences](https://www.ijcai.org/past_conferences) and [2025 proceedings](https://www.ijcai.org/proceedings/2025/); self-published since 2017. Year/volume title/author filters and individual abstract, DOI, PDF and BibTeX access do not constitute cross-year abstract Boolean search. |
| **AAMAS: check coverage first, then fill gaps** | The [call for papers](https://aamas2025.org/index.php/conference/calls/call-for-papers-main-technical-track/) covers interoperability, commercial protocols, interaction protocols, auctions and negotiation. The [2025 proceedings information](https://aamas2025.org/index.php/proceedings/) identifies IFAAMAS publication and ACM DL indexing; use the [proceedings by year](https://www.ifaamas.org/proceedings.html) to check existing query and retrieval evidence for each year/volume and fill only identifiable gaps. Indexing does not establish complete coverage. |
| **arXiv: limited auxiliary source** | Use only for key protocol gaps, author versions and correspondence with formal publication, not an additional broad core search. The [API manual](https://info.arxiv.org/help/api/user-manual.html) supports abs:; retain ID/version, initial and updated dates, DOI/journal-ref and unknowns. |
| **OpenAlex/DBLP: optional checks** | Use for specific metadata, identity, venue and recall-gap checks; neither is a mandatory core step. [OpenAlex default search](https://help.openalex.org/api/searching/) can span title, abstract and indexable full text; [DBLP](https://dblp.org/faq/How%2Bto%2Buse%2Bthe%2Bdblp%2Bsearch%2BAPI.html) is a bibliographic checking entry point, not a complete abstract database. |

A venue is a coverage object; do not count platforms, publication entities and venues repeatedly as extra sources or independent works. If a platform lacks an equivalent Abstract field, record the closest actual scope and make an **explicit deviation decision**. Before that decision, do not substitute metadata, AllField or full-text scope for abstract-topic discovery.

## Confirmed common standards

Future academic runs default to **Abstract-field discovery and abstract-first screening**. Targeted reading of relevant full text is permitted only when a specific record's inclusion, mechanism or relationship is genuinely uncertain. Record the reason, question, source/version/text location, extent read, result and reviewer. This exception authorizes neither database-wide full-text search nor general use of AllField, and it does not require reading every paper in full. Label each content judgment as `abstract` or `fulltext-exception` and count them separately; distinguish missing abstracts, unavailable full text and out-of-scope content. [Workflow v2](workflow-template.md) specifies the operational rules and A0/X2 adaptation; [acceptance v2](acceptance.md) checks them.

Other standards inherit ACM: I1/I2 scientific scope, document types, cutoff and languages, identity/version, deduplication, complete retrieval, evidence preservation and counting. Prefer formal published versions. The accepted preprint-only exception fills only key protocol gaps, with a per-item reason and separate marking, and still requires the same scientific scope and eligibility conditions. Once correspondence with a later formal publication is confirmed, associate it with the same work, retain versions, and do not add an independent work or retroactively change cutoff eligibility. Further restrictions on publication types require a separate decision.

A total of 150 to 200 candidates across all entry points is only a workload reference, not a per-source quota, inclusion target or stopping rule. Distinguish records, independent works and versions. Normalize DOI/platform IDs first; cross-ID relationships require primary correspondence evidence, while title/author similarity generates candidates only. Unconfirmed independent-work counts remain Unknown.

## Official specifications and version boundaries

Official specifications/implementations are a separate evidence track, for example [A2A](https://github.com/a2aproject/A2A/blob/main/docs/specification.md) and [x402](https://github.com/x402-foundation/x402). Pin the issuing entity, specification/code category, tag/commit/version, access date and clause location; keep a separate ledger and exclude these from academic-work counts. The abstract-field default applies to academic discovery; specification clauses remain primary evidence for protocol mechanisms and do not automatically extend I2 commercial associations.

The current [31 frozen ACM queries](acm-completion-20261001/query-manifest.json) comprise 27 Abstract and 4 AllField queries; Full-Text Collection is a collection name. This run and its [protocol](acm-completion-20261001/protocol.json), golden rule, inputs and existing judgments are not automatically changed or reassessed by v2. Its original [workflow](archive/source-policy-v2-before-20261001T212521Z/workflow-template.md) and [acceptance](archive/source-policy-v2-before-20261001T212521Z/acceptance.md) have been preserved byte-for-byte.

## Basis in user decisions

Entry points, roles and the preprint-only exception were confirmed in message `Sentinel_f6b3d4a77a0c819181bcd1902c3521c9`; inheritance of ACM standards was confirmed in `Sentinel_ceeab56bd7b08191a6c436d15f40c8e4`. The final search/reading revision follows the user statement translated into English below. The timestamp above is the local recording time, not a claimed message-sending time.

> Translated user decision: Good. From now on, keep all standards consistent with ACM, except that searches should normally use abstracts only; full text may be consulted when there is substantial uncertainty. Put all of this into the documents, then deliver the confirmed source, workflow and acceptance documents to me.

[Original-byte source.md snapshot preceding this version](archive/source-policy-v2-before-20261001T212521Z/source.md). A new run requires corresponding execution authorization and frozen platform parameters; confirming these documents does not initiate other sources.
