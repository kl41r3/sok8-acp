# Source Evidence

| File | Contents |
|---|---|
| [records.json](records.json) | 5,241 source records with identifiers, titles, URLs, saved abstract text, public dates, query memberships, and publication-unit information |
| [queries.csv](queries.csv) | 155 source/query accounting rows with full expressions, actual fields, observed hits and appearances, and counting scope |
| [annotation-population.json](annotation-population.json) | Stable IDs, source bindings, and URLs for the 1,301 included identifiers |
| [supplements.json](supplements.json) | 25 records' additional same-publication passages, organized by adjudication job and record ID |

`records.json` separates the academic-selection frame from three IEEE standards and 21 AAMAS relationship cases. A missing saved abstract is represented by an empty string and `abstract_available: false`. The abstracts used for layer coding preserve the exact text read by both initial coders. `public_dates` supplies the eligibility-screening date or dates; the earliest recorded year defines the analysis year.

The reconstruction program joins `annotation-population.json` to `records.json` using source and source-record ID, confirms identifier agreement, and builds both coders' identical evidence packets. Supplement entries retain their publication identity, question, passage, section or reading scope, and retrieval metadata. Source URLs identify the scholarly publication; generated evidence tables point into these distributed files using JSON pointers.

Query hit counts and retrieval appearances describe saved observations, including source-specific caps and local matching. They are distinct from the inclusion counts reconstructed from scientific decisions. Publisher PDFs, duplicate captures, and HTTP transport dumps are outside the package; the saved abstracts and relevant quoted passages support the distributed judgments.
