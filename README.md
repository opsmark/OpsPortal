# CARK / OPS — Free CSV cleanup example and offline tool

Compare a small **fictional** before/after cleanup, run a free exact-row deduplication tool on your own **non-sensitive** CSV, or ask about a separately scoped paid cleanup service. No sign-in or payment is needed to inspect the examples or download the tool.

## 1. See what a conservative cleanup looks like — free

[Download the six-row fictional example (ZIP)](https://media.base44.com/files/public/6a89094776dbb07b37c5ae96/423c51ccf_CARK_CSV_QA_Fictional_Example_v1_20261028.zip) or inspect its [source CSV](samples/csv-qa/raw-fictional.csv), [reviewed CSV](samples/csv-qa/reviewed-fictional.csv), and [decision log](samples/csv-qa/README.txt).

The example removes one exact duplicate, demonstrates a manually reviewed whitespace edit, and flags missing or conflicting values rather than guessing. **This is invented educational data, not a past customer's file or proof of paid delivery.**

## 2. Run the free offline exact-row utility

**Known v5 receipt-cleanup limitation (confirmed in an isolated fault-injection test):** If the program fails while opening its newly published output for verification, it can leave a `.deduped.csv` file **without** the corresponding `.dedupe-receipt.json`. An output file without a matching receipt is **not a completed or approved result**. Run only on non-sensitive copies in a private, stable scratch folder, keep the original and a backup, and do not assume shared/synchronized-folder or Windows safety. If the receipt is missing, preserve the files for manual reconciliation; do not blindly rerun over existing paths or delete an output that another process may have changed. This is a documented v5 limitation; newer private repairs are not yet an accepted public replacement.

**[Download current CSV Dedupe v5 (ZIP)](https://media.base44.com/files/public/6a89094776dbb07b37c5ae96/4967c0755_CARK_Offline_Exact_CSV_Dedupe_v5.zip)** — Python 3.9+; standard library only; no cloud account, new package, or API credits.

To inspect before downloading, read the current [Python source](samples/csv-qa/offline-exact-v5/conservative_csv_dedupe.py), [12 automated tests](samples/csv-qa/offline-exact-v5/test_conservative_csv_dedupe.py), or [usage instructions](samples/csv-qa/offline-exact-v5/README.txt).

Run `python conservative_csv_dedupe.py yourfile.csv` from the extracted folder. It creates a new `yourfile.deduped.csv` and `yourfile.dedupe-receipt.json`, reporting rows and SHA-256 hashes; it refuses to overwrite existing output files. Tested limits: UTF-8 CSV with valid unique headers, up to **1,000,000 bytes and 10,000 data rows**.

**What it does not do:** trim or normalize cells, infer business-key duplicates, resolve conflicting records, repair XLSX formulas, import PDFs, guarantee business accuracy, or lock changing input files. CSV reserialization can alter quoting, line endings and BOM; formula-like values remain unchanged and may be unsafe when opened in spreadsheet applications. Keep a stable private source copy and inspect the results. The separate manually reviewed example is **not** produced identically by this exact-row-only tool.

**Earlier releases for provenance:** [v4](https://media.base44.com/files/public/6a89094776dbb07b37c5ae96/f02d375f7_CARK_Offline_Exact_CSV_Dedupe_v4.zip), [v3](https://media.base44.com/files/public/6a89094776dbb07b37c5ae96/94b03dc46_CARK_Offline_Exact_CSV_Dedupe_v3.zip), [v2](https://media.base44.com/files/public/6a89094776dbb07b37c5ae96/8099ac6aa_CARK_Offline_Exact_CSV_Dedupe_v2.zip), [v1](https://media.base44.com/files/public/6a89094776dbb07b37c5ae96/b880b1a6a_CARK_Offline_Exact_CSV_Dedupe_v1.zip); historical source and test directories remain in this repository. Current v5 adds bounded reads for oversized files; earlier versions addressed detected input changes, rollback identity and long CSV fields. This does not make the program an atomic filesystem transaction.

## 3. Need someone to review your CSV?

The separately offered **$59 conditional pilot** covers one agreed, non-sensitive CSV of up to 10,000 rows, with cleaned CSV, short QA/exception summary and one correction pass **only after a written scope, capacity and delivery-date fit check**. No automatic acceptance, XLSX/PDF processing, accounting approval, regulated records, arbitrary matching rules or guaranteed turnaround.

**Before paying**, [request a CSV cleanup scope check by email](mailto:rass991@gmail.com?subject=CSV%20cleanup%20scope%20check%20-%20GitHub%20example&body=Please%20check%20fit%20before%20payment.%0AInput%20type%20and%20approximate%20row%20count%3A%0AColumn%20names%20and%20duplicate%20key%20rules%3A%0AWhich%20changes%20are%20allowed%20and%20which%20must%20be%20flagged%3A%0ADesired%20output%3A%0ANeeded%20by%3A%0AI%20have%20authority%20to%20provide%20the%20data%3A%0APlease%20do%20not%20attach%20live%20or%20sensitive%20records%20until%20scope%20and%20the%20authorized%20transfer%20method%20are%20agreed.). Initially describe approximate rows, column names, permitted changes, output and deadline; **do not send customer records, credentials or sensitive files** before an approved transfer method is agreed.

Alternatively, the existing [CARK / OPS CSV cleanup service on Contra](https://contra.com/s/vkZZoFmM-csv-spreadsheet-cleanup-with-a-change-log) invites a **contact-for-pricing quote request**. Contra's quoted pricing and acceptance are separate from the website's conditional $59 pilot; neither route establishes a booking or a completed order.

Other available tools and educational demonstrations: [CARK / OPS Working Tools](https://ops-workflow-cost-calculator.rass991.chatgpt.site/).

**Found a reproducible tool defect or unclear instruction?** [Open a GitHub issue](https://github.com/opsmark/OpsPortal/issues/new) with the tool version, Python version, operating system, exact error and a **small invented CSV** that reproduces it. Do **not** attach customer data, credentials, medical or financial records. An issue is feedback, not a support SLA or an accepted paid task.

*Source examples and automated tests demonstrate bounded capabilities—not independent customer use, performance guarantees or revenue.*
