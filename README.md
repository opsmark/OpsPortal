# CARK / OPS — Free CSV cleanup QA example

A small, inspectable example of conservative spreadsheet cleanup: compare invented source rows with reviewed output, see which duplicate was removed, and see why conflicting records remain flagged. The example is free. A separate $59 fixed-scope cleanup enquiry is optional and requires a fit check before payment.

## Download and inspect

[Download the fictional CSV cleanup and QA example (ZIP)](https://media.base44.com/files/public/6a89094776dbb07b37c5ae96/423c51ccf_CARK_CSV_QA_Fictional_Example_v1_20261028.zip)

Inspect the files directly: [raw CSV](samples/csv-qa/raw-fictional.csv), [reviewed CSV](samples/csv-qa/reviewed-fictional.csv), and [QA decision log](samples/csv-qa/README.txt).

This small public demonstration contains an invented raw CSV, a reviewed CSV and a plain-language decision log. It illustrates exact-duplicate review, whitespace cleanup, missing values and a conflicting-record hold. It is not real client work, a complete automation product, an accuracy guarantee or evidence of a paid customer. No purchase or sign-in is needed for this example.

For existing free tools and learning resources, visit [CARK / OPS Working Tools](https://ops-workflow-cost-calculator.rass991.chatgpt.site/).

### Try the free offline exact-row tool

[Download Offline Exact CSV Dedupe v5 — Python source, twelve tests and instructions (ZIP)](https://media.base44.com/files/public/6a89094776dbb07b37c5ae96/4967c0755_CARK_Offline_Exact_CSV_Dedupe_v5.zip)

**v2 verified correction:** a valid CSV field over 128 KiB previously failed under Python's default CSV parser limit, despite meeting the 1 MB overall pilot limit. Version 2 admits such fields within the existing size cap, restores the parser setting after success or failure, and clarifies that CSV quoting/line endings may change. **Inspect without downloading:** [v3 Python source](samples/csv-qa/offline-exact-v3/conservative_csv_dedupe.py), [eight regression tests](samples/csv-qa/offline-exact-v3/test_conservative_csv_dedupe.py), and [usage instructions](samples/csv-qa/offline-exact-v3/README.txt). These files were compared against the exact released v3 ZIP. Running the tool is optional; review its limits before using it on your own non-sensitive data.

**Current v5 inspection:** [Python source](samples/csv-qa/offline-exact-v5/conservative_csv_dedupe.py), [twelve tests](samples/csv-qa/offline-exact-v5/test_conservative_csv_dedupe.py), [instructions](samples/csv-qa/offline-exact-v5/README.txt). Version 5 rejects oversized CSV files before allocating the full source and caps rechecks if a concurrent writer grows the input. The [v4 ZIP remains available](https://media.base44.com/files/public/6a89094776dbb07b37c5ae96/f02d375f7_CARK_Offline_Exact_CSV_Dedupe_v4.zip). This is a bounded-input fix, not a full concurrency guarantee.

**Historical v4 inspection:** [source code](samples/csv-qa/offline-exact-v4/conservative_csv_dedupe.py), [ten tests](samples/csv-qa/offline-exact-v4/test_conservative_csv_dedupe.py), and [instructions](samples/csv-qa/offline-exact-v4/README.txt). Earlier [v3 source and tests](samples/csv-qa/offline-exact-v3/README.txt) are historical, not the current v4 implementation.

**v4 source-consistency repair:** A reproduced source edit during processing could leave stale output and a misleading approval receipt. Version 4 checks the input again before output publication and before receipt publication, rejecting detected changes and cleaning up only the output it owns. The input must still remain stable through the run; this is not a file lock or protection against modifications after the final check. The [v3 archive remains available](https://media.base44.com/files/public/6a89094776dbb07b37c5ae96/94b03dc46_CARK_Offline_Exact_CSV_Dedupe_v3.zip).\n\n**v3 verified repair:** when audit receipt creation fails after the CSV output was written, the utility now checks a retained open file handle before removing its own output. A separate process's replacement is preserved. This closes a reproduced rollback problem, not all concurrent filesystem races. The previous [v2 archive remains available](https://media.base44.com/files/public/6a89094776dbb07b37c5ae96/8099ac6aa_CARK_Offline_Exact_CSV_Dedupe_v2.zip).  

The original [v1 archive remains available](https://media.base44.com/files/public/6a89094776dbb07b37c5ae96/b880b1a6a_CARK_Offline_Exact_CSV_Dedupe_v1.zip) for provenance.

This is a **different, narrower capability** from the illustrative manually reviewed sample above: it removes only rows where **every CSV field matches exactly**, saves a new file without replacing the original, and writes an audit receipt with counts and source/output hashes. The v3 package includes eight regression tests. Requirements: Python 3.9+, UTF-8 CSV with valid unique headers, at most 1 MB and 10,000 data rows; no paid services or network required. It does **not** trim values, choose the newest conflicting record, resolve fuzzy matches, preserve XLSX formulas/styles, or certify data accuracy. Always inspect output before using it. Formula-like CSV values are not escaped, so treat untrusted source files cautiously in spreadsheet applications.


### Want help with a CSV you own?

CARK / OPS lists a **$59 fixed-scope spreadsheet cleanup and QA pilot** for **one agreed, non-sensitive CSV of up to 10,000 rows**, subject to an initial fit, available capacity and an agreed delivery date. The described output is a cleaned CSV, a short QA/exception summary and one correction pass. It does not include guaranteed Excel/XLSX processing, accounting approval, regulated data, open-ended enrichment or assumptions about conflicting records.

**Before paying**, [request a CSV cleanup scope check by email](mailto:rass991@gmail.com?subject=CSV%20cleanup%20scope%20check%20-%20GitHub%20example&body=Please%20check%20fit%20before%20payment.%0AInput%20type%20and%20approximate%20row%20count%3A%0AColumn%20names%20and%20duplicate%20key%20rules%3A%0AWhich%20changes%20are%20allowed%20and%20which%20must%20be%20flagged%3A%0ADesired%20output%3A%0ANeeded%20by%3A%0AI%20have%20authority%20to%20provide%20the%20data%3A%0APlease%20do%20not%20attach%20live%20or%20sensitive%20records%20until%20scope%20and%20the%20authorized%20transfer%20method%20are%20agreed.). Send only a short, non-sensitive description initially—not the dataset, patient details, credentials, private financial records or a payment.

A scope enquiry is **not** an accepted order. Price, specific rules, delivery feasibility and source transfer must be agreed in writing before purchasing. The fictional example above is free whether or not you request paid help.
