# Data dictionary and projection boundary

All CSV files use UTF-8, a header row and LF. Lists in generated identifier CSV cells are compact JSON. The source-record key is `(source, recordID)` and is unique within the frame. `recordID` is a source-local audit key; it is never a global work key.

| Table | Unit / rows | Preserved fields and interpretation |
|---|---|---|
| data/records.csv | source record / 5241 | source; recordID; normalized_identifier; union_identifier_key; track; scientific_disposition; scientific_clause; evidence_level. These are frozen upstream classifications and keys. |
| data/selection-overlay.csv | administrative disposition / 237 | source; recordID; typed key; prior_status; scientific_disposition; final_selection; reason. Pending stays pending; final_selection becomes not_included. |
| data/query-counts.csv | source/concept / 155 | exact_query; actual_field; expression_id; Hq/Oq or local match and original scientific disposition counts; original count scope/status. 31 concepts per source; v2 aliases 27 expressions. |
| data/gate-matrix.csv | scoped gate assertion / 40 | source; gate; status; exact scope. Partial and NotRun wording is preserved; no whole-project Pass is asserted. |
| data/process-receipt.json | saved receipt summary | bounded IEEE D2/review processing and AA/IJ targeted-read quantities. This package does not rerun these processes. |
| expected/final-selection-records.csv | source record / 5241 | data/records fields plus independently reconstructed final_selection and selection_basis. |
| expected/source-counts.csv | source / 5 | source-row, selection, preserved pending, standard and relation counts; AAMAS selection-pending blank is not a zero-science claim. |
| expected/identifier-selection.csv | typed key / 5208 | source members, source-record members, original scientific dispositions, final selection and overlay member count; global verdict Unassigned; W/V blank. |
| expected/included-identifiers.csv | included typed key / 1301 | exact subset of identifier-selection with at least one included source member. |

`union_identifier_key` is a typed DOI, platform identifier or exact primary URL inherited from the upstream union; source namespaces remain distinct. `scientific_disposition` uses include/exclude/pending and is not rewritten by the administrative overlay. `scientific_clause` is the preserved original rule reference, including type/date/access qualifications. `evidence_level` keeps the original source-specific wording; ACM v1 has no retrospective v2 mutually exclusive assignment. Original source exclusions must be interpreted with their retained local control/evidence records.

`native_Hq` is the saved native query hit count; `observed_Oq` is the returned native appearance count when applicable. AAAI/IJCAI/AAMAS numbers are local primary-author-Abstract matches, with native totals Unknown. `pending_record_IDs` in the query table is original scientific evidence uncertainty, not the now-closed final selection pending quantity. Empty input cells retain the original producer's unavailable/not-applicable encoding; explicit Unknown/Not applicable strings are retained. CSV row counts and schemas are machine listed in MANIFEST.json.

No abstracts, body text, quotations, screenshots, titles, reasons containing source excerpts, author lists, private paths, internal messages, access credentials or native service envelopes are included. Original unredacted decision/evidence records are retained locally. No rows are deleted from the scientific source record frame. This corpus has no experimentally assigned train/validation/test split or derived taxonomy coding labels in this scoped package.

The [eight-function analytical codebook](analytical-codebook.md) supplies manuscript-authored comparison definitions. It is documentation, not a per-record taxonomy dataset. No corpus function labels, measured frequencies, saturation or coding agreement are distributed. Eligibility decision codes remain a separate frozen scheme.
