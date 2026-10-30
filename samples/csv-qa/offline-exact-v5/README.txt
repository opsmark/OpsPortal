CARK / OPS — Free offline exact-row CSV deduplication tool, v5

Purpose: handle only byte-equivalent decoded CSV rows (same values in all columns),
not fuzzy matching, business-key merges, 'newest record' decisions, whitespace
normalization or manual source repair. This deliberately narrower tool DOES NOT
reproduce the separate reviewed fictional example's whitespace transformation.

Requires: Python 3.9+ on a machine you control. No additional Python packages,
cloud account, API credits or Internet access. Reads and writes locally only.

Usage:
  python conservative_csv_dedupe.py yourfile.csv

On success, in the same folder, generates two NEW files:
  yourfile.deduped.csv
  yourfile.dedupe-receipt.json
The original CSV is not modified. The receipt includes source/output SHA-256,
rows in/out and duplicate data-row numbers (not the underlying record contents).
Both outputs refuse to overwrite existing files. If anything fails, stop and
review the error; do not assume a complete output exists without the receipt.
A failed receipt may leave a replacement file created by another process; do
not assume it is this tool's output.

Limits: maximum source CSV size 1,000,000 bytes; maximum 10,000 data rows;
strict UTF-8 CSV with a header; supports long single fields within the total 1MB cap; no duplicate/missing header names and no jagged
rows. UTF-8 BOM may be consumed, and line endings/re-quoting may change.
Version 5 also rejects oversized files before loading content into memory,
and caps source rechecks if another process grows the input. This prevents
the demonstrated oversize-file allocation failure within the pilot limit.
Version 4 rejects an input edit detected before output creation or before the
receipt is published; it rolls back only its own output. This is not an atomic
source lock, and changes after the final check can still occur. Copy files to
a stable, private directory before processing synchronized/shared sources.
Version 2 corrected the default 128-KiB field-size rejection; version 3
prevents a failed-receipt rollback from deleting a file another process
replaced after this run created its output.
The parser field-size setting is restored after each run, including failures.
Formula-looking cells are preserved as-is: avoid opening untrusted CSV in a
spreadsheet tool that evaluates formulas. Do not send sensitive files to CARK.
This is a free educational local utility, not an accepted paid job, guarantee
of business-data correctness, capacity SLA or method to handle regulated data.

Self-test:
  python -m unittest -v test_conservative_csv_dedupe.py

Source/example: https://github.com/opsmark/OpsPortal/blob/main/README.md
