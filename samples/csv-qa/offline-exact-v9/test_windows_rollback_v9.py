"""Synthetic Windows-sharing regression checks; NOT native Windows execution."""
import unittest
import tempfile
from pathlib import Path
from unittest.mock import patch
import csv
import hashlib
import json
from contextlib import contextmanager
import conservative_csv_dedupe as tool

class WindowsLikeRollbackV9(unittest.TestCase):
    def make(self):
        d=tempfile.TemporaryDirectory(prefix='cark_v9_rollback_')
        root=Path(d.name)
        src=root/'input.csv'
        src.write_bytes(b'id,value\n1,A\n1,A\n2,B\n')
        return d,src,root/'input.deduped.csv',root/'input.dedupe-receipt.json'

    def test_receipt_fails_but_own_handle_closed_before_output_unlink(self):
        d,src,out,receipt=self.make()
        with d:
            handles=[]
            original_owned=tool.write_exclusive_owned
            original_unlink=Path.unlink
            @contextmanager
            def capture_owned(path,payload):
                with original_owned(path,payload) as f:
                    handles.append(f)
                    yield f
            def windows_refusal_if_open(path,*args,**kwargs):
                if path==out and handles and not handles[-1].closed:
                    raise PermissionError('simulated Windows sharing violation while own handle remains open')
                return original_unlink(path,*args,**kwargs)
            def receipt_fail(path,payload):
                if path==receipt:
                    raise OSError('INJECTED_PRIMARY_RECEIPT_FAILURE')
                raise AssertionError('unexpected publisher')
            with patch.object(tool,'write_exclusive_owned',side_effect=capture_owned),patch.object(tool,'write_exclusive',side_effect=receipt_fail),patch.object(Path,'unlink',windows_refusal_if_open):
                with self.assertRaisesRegex(OSError,'INJECTED_PRIMARY_RECEIPT_FAILURE'):
                    tool.process(src,out,receipt)
            self.assertTrue(handles[0].closed)
            self.assertFalse(out.exists())
            self.assertFalse(receipt.exists())
            self.assertEqual(list(src.parent.glob('.*')),[])

    def test_permanent_delete_refusal_reported_as_explicit_orphan(self):
        d,src,out,receipt=self.make()
        with d:
            original_unlink=Path.unlink
            def deny_own_output(path,*a,**kw):
                if path==out: raise PermissionError('INJECTED_OTHER_WINDOWS_LOCK')
                return original_unlink(path,*a,**kw)
            def fail_receipt(path,payload):
                if path==receipt: raise OSError('INJECTED_PRIMARY_RECEIPT_FAILURE')
                raise AssertionError('unexpected publisher')
            with patch.object(Path,'unlink',deny_own_output),patch.object(tool,'write_exclusive',side_effect=fail_receipt):
                with self.assertRaisesRegex(OSError,'ROLLBACK_INCOMPLETE') as ctx:
                    tool.process(src,out,receipt)
            self.assertIsInstance(ctx.exception.__cause__,OSError)
            self.assertIn('INJECTED_PRIMARY_RECEIPT_FAILURE',str(ctx.exception.__cause__))
            self.assertTrue(out.exists())
            self.assertFalse(receipt.exists())
            self.assertEqual(src.read_bytes(),b'id,value\n1,A\n1,A\n2,B\n')

    def test_receipt_success_output_integrity(self):
        d,src,out,receipt=self.make()
        with d:
            res=tool.process(src,out,receipt)
            self.assertEqual(res['tool'],'CARK conservative CSV dedupe v9')
            self.assertEqual((res['source_rows'],res['kept_rows'],res['duplicate_rows_removed']),(3,2,1))
            self.assertEqual(hashlib.sha256(out.read_bytes()).hexdigest(),json.loads(receipt.read_text())['output_sha256'])
            self.assertEqual(list(src.parent.glob('.*')),[])

if __name__=='__main__':unittest.main()