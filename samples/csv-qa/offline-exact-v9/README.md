# CARK / OPS — Free offline exact-row CSV dedupe v9

**Free educational utility · November 6, 2026.** No sign-in, data upload, API fees or checkout. Exact original source tested on local Windows 11/NTFS (20/20 tests) and Linux scratch. **No paid-client delivery or spreadsheet correctness guarantee.** The $59 cleanup service is a separate, currently paused, scope-first offer.

## What it does

Removes duplicate CSV data rows only when **every parsed cell value** matches; it preserves differing spaces, conflicting amounts, and formula-like text. CSV quoting, BOM or line endings may be serialized differently. It does **not** normalize whitespace, merge customer records, infer identities, handle XLSX, inspect live business sources, or make accounting decisions.

Input: strict UTF-8 CSV, unique nonblank header names, at most 1,000,000 bytes and 10,000 data rows. Requires Python 3.9 or newer, standard library only. Run **only on copies of non-sensitive files** in a private **local non-synchronized** folder, preferably NTFS on Windows. Do not run directly on cloud-sync directories, SMB/network shares or customer-sensitive originals; these environments were not qualified.

```sh
python conservative_csv_dedupe.py mycopy.csv
python -m unittest discover -v
```

On success it creates `mycopy.deduped.csv` and `mycopy.dedupe-receipt.json` beside the input, without overwriting existing files; keep the source and verify receipt hashes. Missing receipt, error, or orphan output means **do not use the result**. Preserve artifacts for manual investigation; do not blindly rerun, overwrite, or delete a file another process could have changed.

**Security:** It does not neutralize spreadsheet formulas. Cells beginning with `=`, `+`, `-`, or `@` may be interpreted as formulas when you subsequently open untrusted CSV in Excel or similar spreadsheet software. Review text safely and avoid opening untrusted output in software that evaluates CSV cells. Do not share credentials, regulated data or real customer records for testing.

## Repair and evidence

v9 closes its own output handle before a guarded receipt-failure rollback, avoiding the demonstrated v8 Windows-style open-handle cleanup error. When external deletion still fails it surfaces `ROLLBACK_INCOMPLETE` rather than certifying a mismatched output. Tested private native Windows 11 (build 26200), Python 3.13.15, NTFS: **20/20 tests passed**, with happy path, receipt-write failure cleanup, no-overwrite and input preservation. This does **not** prove hard-power-loss atomicity, hostile concurrency, antivirus interference, SMB or Dropbox/OneDrive synchronization behavior. Linux acceptance used synthetic fixtures only, not real customer files.

Source SHA-256: `a2c48d6543e312b62c5cb6c92248019b497f21c3c6059e222ee92cb7792fb792`.

This public distribution is original Cark/OPS work. No private OPS operating notes, device credentials, client files, company secrets or private QA packet are included. Report reproducible defects using invented non-sensitive data only. Historical public v5 remains available separately for provenance; v9 does not imply that customers or paid services have been accepted.
