#!/usr/bin/env python3
"""Offline, exact-row CSV deduplication with no overwrite and a JSON audit receipt.

Safety: never assumes two conflicting rows are equivalent; does not infer dates,
keys, or normalize business facts. Standard-library only, zero network access.
"""
import argparse
import csv
import hashlib
import io
import json
import os
from pathlib import Path
import tempfile

MAX_BYTES = 1_000_000
MAX_ROWS = 10_000


def write_exclusive(path: Path, payload: bytes) -> None:
    """Publish a complete new file without silently replacing an existing one."""
    fd, tmp = tempfile.mkstemp(prefix=f'.{path.name}.', dir=path.parent)
    try:
        with os.fdopen(fd, 'wb') as f:
            f.write(payload)
            f.flush()
            os.fsync(f.fileno())
        os.link(tmp, path)  # Fails if final path already exists (including symlinks).
    finally:
        os.unlink(tmp)


def process(src: Path, out: Path, receipt: Path) -> dict:
    src, out, receipt = (p.absolute() for p in (src, out, receipt))
    if len({src, out, receipt}) != 3:
        raise ValueError('Input, output, and receipt must be different paths')
    if not src.is_file():
        raise ValueError('Input must be an existing regular file')
    if out.exists() or receipt.exists():
        raise FileExistsError('Refusing to overwrite an output or receipt')
    if out.parent != src.parent or receipt.parent != src.parent:
        raise ValueError('Output and receipt must be alongside input for this pilot')
    raw = src.read_bytes()
    if len(raw) > MAX_BYTES:
        raise ValueError('CSV exceeds the 1,000,000-byte pilot limit')
    # utf-8-sig discards only the BOM marker; cell values remain unmodified.
    text = raw.decode('utf-8-sig')
    # Python's default field limit (~128 KiB) is smaller than the documented
    # one-megabyte source cap. Admit a valid long field within that source cap.
    previous_field_limit = csv.field_size_limit()
    csv.field_size_limit(MAX_BYTES)
    try:
        return _process_decoded(src, out, receipt, raw, text)
    finally:
        csv.field_size_limit(previous_field_limit)


def _process_decoded(src: Path, out: Path, receipt: Path, raw: bytes, text: str) -> dict:
    reader = csv.reader(io.StringIO(text, newline=''), strict=True)
    try:
        header = next(reader)
    except StopIteration:
        raise ValueError('CSV has no header')
    if not header or any(not col.strip() for col in header) or len(set(header)) != len(header):
        raise ValueError('CSV header contains missing or repeated column names')
    seen = set()
    kept = []
    duplicates = []
    total = 0
    for row in reader:
        total += 1
        if total > MAX_ROWS:
            raise ValueError('CSV exceeds the 10,000-row pilot limit')
        if len(row) != len(header):
            raise ValueError(f'Row {total} has {len(row)} fields; expected {len(header)}')
        key = tuple(row)
        if key in seen:
            duplicates.append(total)
        else:
            seen.add(key)
            kept.append(row)
    stream = io.StringIO(newline='')
    writer = csv.writer(stream, lineterminator='\n')
    writer.writerow(header)
    writer.writerows(kept)
    output_bytes = stream.getvalue().encode('utf-8')
    result = {
        'tool': 'CARK conservative CSV dedupe v4',
        'mode': 'exact_all_columns_only',
        'normalization': 'field values unchanged; CSV serialization may alter quoting, line endings and BOM',
        'input_sha256': hashlib.sha256(raw).hexdigest(),
        'output_sha256': hashlib.sha256(output_bytes).hexdigest(),
        'source_rows': total,
        'kept_rows': len(kept),
        'duplicate_rows_removed': len(duplicates),
        'duplicate_data_row_numbers_1_based': duplicates,
        'input_columns': header,
        'caution': 'Conflicting or near-matching records are preserved. Review keys, authority and business rules before any non-exact deletions.',
    }
    receipt_bytes = (json.dumps(result, indent=2, ensure_ascii=False) + '\n').encode('utf-8')
    # Reject an input edited while parsing. This is a snapshot guard, not a
    # filesystem lock; callers must keep their input stable during the run.
    if src.read_bytes() != raw:
        raise ValueError('Input changed during CSV processing; no output published')
    # Publish the report last; never replace inputs or existing output files.
    write_exclusive(out, output_bytes)
    # Keep our output inode open while publishing the receipt. An unlinked
    # inode may be immediately recycled, making a bare inode-number comparison
    # insufficient to distinguish an external replacement.
    flags = os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0)
    with os.fdopen(os.open(out, flags), 'rb') as owned_output:
        identity = os.fstat(owned_output.fileno())
        try:
            # A synchronized/shared-folder writer can modify the source
            # during our output publication. Do not issue an approving receipt
            # for stale content detected at this boundary.
            if src.read_bytes() != raw:
                raise ValueError('Input changed before receipt publication; no valid result')
            write_exclusive(receipt, receipt_bytes)
        except Exception:
            try:
                current = os.stat(out, follow_symlinks=False)
            except FileNotFoundError:
                pass
            else:
                if os.path.samestat(identity, current):
                    out.unlink()
            raise
    return result


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('input_csv', type=Path, help='UTF-8 CSV; up to 1 MB / 10,000 data rows')
    args = ap.parse_args()
    src = args.input_csv
    if src.suffix.lower() != '.csv':
        ap.error('Input filename must end in .csv')
    try:
        result = process(src, src.with_name(src.stem + '.deduped.csv'), src.with_name(src.stem + '.dedupe-receipt.json'))
    except (OSError, UnicodeError, ValueError, csv.Error) as e:
        ap.exit(2, f'NOT PROCESSED: {e}\n')
    print(f"Done: {result['source_rows']} rows -> {result['kept_rows']} kept; {result['duplicate_rows_removed']} exact duplicates removed")


if __name__ == '__main__':
    main()
