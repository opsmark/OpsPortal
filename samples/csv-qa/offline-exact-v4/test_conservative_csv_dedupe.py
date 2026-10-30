import csv
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import conservative_csv_dedupe as tool
from conservative_csv_dedupe import process

class CsvToolChecks(unittest.TestCase):
    def run_fixture(self, data):
        t=tempfile.TemporaryDirectory();p=Path(t.name)/'input.csv';p.write_bytes(data)
        return t,p,p.with_name('input.deduped.csv'),p.with_name('input.dedupe-receipt.json')
    def test_exact_duplicate_and_conflicting_rows(self):
        data=b'id,name,date\nA,alpha,2026-01-01\nB,beta,\nB,beta,\nC,gamma,2026-01-02\nC,gamma,2026-01-03\n'
        t,p,out,receipt=self.run_fixture(data)
        with t:
            result=process(p,out,receipt)
            self.assertEqual((result['source_rows'],result['kept_rows'],result['duplicate_rows_removed']),(5,4,1))
            self.assertEqual(result['duplicate_data_row_numbers_1_based'],[3]);self.assertEqual(p.read_bytes(),data)
            with out.open() as f: rows=list(csv.DictReader(f))
            self.assertEqual(sum(x['id']=='C' for x in rows),2)
            self.assertEqual(rows[1]['date'],'');self.assertEqual(hashlib.sha256(out.read_bytes()).hexdigest(),json.loads(receipt.read_text())['output_sha256'])
            with self.assertRaises(FileExistsError):process(p,out,receipt)
    def test_reject_invalid_duplicate_headers_without_writes(self):
        for text in [b'a,a\n1,2\n',b'a,b\n1\n',b'']:
            t,p,out,receipt=self.run_fixture(text)
            with t:
                with self.assertRaises(ValueError):process(p,out,receipt)
                self.assertFalse(out.exists());self.assertFalse(receipt.exists())
    def test_reject_oversized(self):
        t,p,out,receipt=self.run_fixture(b'a\n'+b'x'*1_000_001)
        with t:
            with self.assertRaises(ValueError):process(p,out,receipt)
    def test_long_valid_field_within_published_byte_cap(self):
        # This failed on v1 because Python's CSV field limit is about 128 KiB.
        data=('id,notes\n1,' + 'X'*140_000 + '\n1,' + 'X'*140_000 + '\n').encode()
        t,p,out,receipt=self.run_fixture(data)
        with t:
            prior=csv.field_size_limit()
            r=process(p,out,receipt)
            self.assertEqual((r['source_rows'],r['kept_rows'],r['duplicate_rows_removed']),(2,1,1))
            self.assertEqual(csv.field_size_limit(),prior)
            self.assertIn(('X'*140_000).encode(),out.read_bytes())
            self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),r['input_sha256'])

    def test_csv_field_limit_restored_when_validation_fails(self):
        data=('id,notes\n1,' + 'X'*140_000 + '\n2\n').encode()
        t,p,out,receipt=self.run_fixture(data)
        with t:
            prior=csv.field_size_limit()
            with self.assertRaises(ValueError):process(p,out,receipt)
            self.assertEqual(csv.field_size_limit(),prior)
            self.assertFalse(out.exists())
            self.assertFalse(receipt.exists())

    def test_failed_receipt_removes_own_output_only(self):
        t,p,out,receipt=self.run_fixture(b'id,name\n1,A\n1,A\n')
        with t:
            original=tool.write_exclusive
            def fail_receipt(path,payload):
                if path==receipt:
                    raise OSError('simulated receipt failure')
                return original(path,payload)
            with patch.object(tool,'write_exclusive',side_effect=fail_receipt):
                with self.assertRaisesRegex(OSError,'simulated'):
                    process(p,out,receipt)
            self.assertFalse(out.exists())
            self.assertFalse(receipt.exists())
            self.assertTrue(p.exists())

    def test_failed_receipt_never_removes_replaced_output(self):
        t,p,out,receipt=self.run_fixture(b'id,name\n1,A\n1,A\n')
        with t:
            original=tool.write_exclusive
            def foreign_replace_before_receipt(path,payload):
                if path==receipt:
                    out.unlink()
                    out.write_bytes(b'FOREIGN PROCESS OUTPUT')
                    raise OSError('receipt rejected')
                return original(path,payload)
            with patch.object(tool,'write_exclusive',side_effect=foreign_replace_before_receipt):
                with self.assertRaisesRegex(OSError,'receipt rejected'):
                    process(p,out,receipt)
            self.assertEqual(out.read_bytes(),b'FOREIGN PROCESS OUTPUT')
            self.assertFalse(receipt.exists())
            self.assertEqual(p.read_bytes(),b'id,name\n1,A\n1,A\n')

    def test_changed_input_during_output_publish_rejects_and_cleans_owned_output(self):
        t,p,out,receipt=self.run_fixture(b'id,name\n1,A\n1,A\n')
        with t:
            original=tool.write_exclusive
            def mutate_source_at_output(path,payload):
                if path==out:
                    p.write_bytes(b'id,name\n1,CHANGED\n')
                return original(path,payload)
            with patch.object(tool,'write_exclusive',side_effect=mutate_source_at_output):
                with self.assertRaisesRegex(ValueError,'Input changed'):
                    process(p,out,receipt)
            self.assertFalse(out.exists())
            self.assertFalse(receipt.exists())
            self.assertIn(b'CHANGED',p.read_bytes())

    def test_changed_input_before_output_publish_has_no_side_effects(self):
        t,p,out,receipt=self.run_fixture(b'id,name\n1,A\n1,A\n')
        with t:
            # Input modification immediately after initial parse, before the first source guard.
            original_process=tool._process_decoded
            def changed_before_processing(src, out, receipt, raw, text):
                src.write_bytes(b'id,name\n1,EDITED\n')
                return original_process(src,out,receipt,raw,text)
            with patch.object(tool,'_process_decoded',side_effect=changed_before_processing):
                with self.assertRaisesRegex(ValueError,'Input changed'):
                    process(p,out,receipt)
            self.assertFalse(out.exists());self.assertFalse(receipt.exists())

    def test_quoted_newline_and_bom(self):
        t,p,out,receipt=self.run_fixture(b'\xef\xbb\xbfkey,note\n1,"hi\nthere"\n1,"hi\nthere"\n')
        with t:
            r=process(p,out,receipt)
            self.assertEqual(r['duplicate_rows_removed'],1)
            with out.open() as f: self.assertEqual(list(csv.reader(f))[1][1],'hi\nthere')

if __name__=='__main__':unittest.main()
