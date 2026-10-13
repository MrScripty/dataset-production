import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest

HERE = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('recovery', HERE / 'recovery.py')
r = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r)

class RecoveryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def test_full_demo_restart_rollback_independent_restore(self):
        receipt = r.demo(self.root / 'exercise')
        self.assertEqual(receipt['restart']['status'], 'complete')
        self.assertEqual(receipt['restart_did_not_repair'], 'nested-negation regression failed')
        self.assertEqual(receipt['rollback']['release'], 'R1')
        self.assertTrue(receipt['working_tree_removed_before_restore'])
        self.assertTrue(receipt['restored_hashes_match'])
        self.assertFalse(receipt['restore']['refund_requested'])
        self.assertEqual(receipt['restore']['parser'], 'all-text-v1')

    def test_restart_idempotent_and_not_repair(self):
        work = self.root / 'work'; work.mkdir()
        r.make_bundle(work / 'R2', 'R2', 'direct-text-v2')
        (work / 'job.json').write_bytes(r.encode({'job':'toy-build-R2','status':'interrupted','resumes':0}))
        self.assertEqual(r.restart_job(work), r.restart_job(work))
        with self.assertRaises(ValueError): r.verify_bundle(work / 'R2')

    def test_hash_corruption_blocks_switch(self):
        work = self.root / 'work'; work.mkdir()
        r.make_bundle(work / 'R1', 'R1', 'all-text-v1')
        (work / 'R1/source.html').write_text('corrupt')
        with self.assertRaises(ValueError): r.select_bundle(work, 'R1')
        self.assertFalse((work / 'active.json').exists())

    def test_compatible_contract_required_even_with_updated_hash(self):
        bundle = self.root / 'bundle'
        r.make_bundle(bundle, 'R1', 'all-text-v1')
        contract = json.loads((bundle / 'contract.json').read_text())
        contract['consumer'] = 'unimplemented-consumer'
        data = r.encode(contract); (bundle / 'contract.json').write_bytes(data)
        manifest = json.loads((bundle / 'manifest.json').read_text())
        manifest['outputs']['contract.json'] = {'sha256':r.digest(data),'bytes':len(data)}
        (bundle / 'manifest.json').write_bytes(r.encode(manifest))
        with self.assertRaises(ValueError): r.verify_bundle(bundle)

    def test_independent_backup_survives_complete_work_loss(self):
        work, backup = self.root/'work', self.root/'backup'
        work.mkdir(); r.make_bundle(work/'R1','R1','all-text-v1')
        r.backup_bundle(work, backup)
        shutil.rmtree(work)
        self.assertFalse(work.exists())
        result = r.restore_bundle(backup, work)
        self.assertEqual(result['text'], r.EXPECTED_TEXT)
        self.assertFalse(result['refund_requested'])

    def test_missing_and_corrupt_backup_fail(self):
        with self.assertRaises(FileNotFoundError): r.restore_bundle(self.root/'absent', self.root/'work')
        bundle = self.root/'backup'/'R1'; r.make_bundle(bundle,'R1','all-text-v1')
        (bundle/'record.json').write_bytes(b'{}')
        with self.assertRaises(ValueError): r.restore_bundle(self.root/'backup',self.root/'work')
        self.assertFalse((self.root/'work').exists())

    def test_backup_inside_work_refused(self):
        work = self.root/'work'; work.mkdir(); r.make_bundle(work/'R1','R1','all-text-v1')
        with self.assertRaises(ValueError): r.backup_bundle(work, work/'backup')

    def test_nonempty_demo_root_not_deleted(self):
        sentinel = self.root/'user-file'; sentinel.write_text('keep')
        with self.assertRaises(ValueError): r.demo(self.root)
        self.assertEqual(sentinel.read_text(),'keep')

if __name__ == '__main__': unittest.main()
