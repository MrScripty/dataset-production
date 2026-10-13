import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

HERE = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('contract', HERE / 'contract.py')
c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c)
ROOT = HERE.parents[1]
bspec = importlib.util.spec_from_file_location('first_release', ROOT / 'examples/first-release/build.py')
b = importlib.util.module_from_spec(bspec)
bspec.loader.exec_module(b)

class ConsumerContractTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.source, self.out = self.root / 'source', self.root / 'out'
        b.build(ROOT / 'examples/first-release/data/records.jsonl', ROOT / 'examples/first-release/data/gold.json', self.source)

    def adapt(self):
        return c.materialize(self.source, self.out)

    def rewrite_output(self, name, content):
        (self.out / name).write_bytes(content)
        manifest = c.strict_load((self.out / 'manifest.json').read_bytes())
        manifest['outputs'][name] = {'sha256': c.digest(content), 'bytes': len(content)}
        (self.out / 'manifest.json').write_bytes(c.encode(manifest))

    def test_exact_consumer_roundtrip(self):
        receipt = self.adapt()
        batch = c.load_batch(self.out)
        expected = {r['canonical_id']: r for r in c.rows((self.source / 'release.jsonl').read_bytes()) if r['label_status'] == 'labeled'}
        self.assertEqual(len(expected), receipt['accepted'])
        self.assertEqual(len(batch), receipt['accepted'])
        for row in batch:
            original = expected[row['id']]
            self.assertEqual(row['features'], [original['text']])
            self.assertEqual(row['target'], c.LABEL_IDS[original['weak_label']])
            self.assertEqual((row['group_id'], row['split']), (original['group_id'], original['split']))
        self.assertEqual(sum(len(c.load_batch(self.out, s)) for s in c.SCHEMA['splits']), len(batch))
        self.assertIn('no Training', receipt['compatibility'])

    def test_deterministic_and_relocatable(self):
        self.adapt()
        other = self.root / 'other'
        c.materialize(self.source, other)
        for file in self.out.iterdir():
            self.assertEqual(file.read_bytes(), (other / file.name).read_bytes())
        self.assertEqual(c.load_batch(self.out), c.load_batch(other))

    def test_detects_corrupt_bytes(self):
        self.adapt()
        (self.out / 'rows.jsonl').write_bytes(b'{}\n')
        with self.assertRaises(ValueError):
            c.load_batch(self.out)

    def test_rejects_changed_units_order_and_label_ids_even_with_updated_hash(self):
        self.adapt()
        for transform in ('units', 'order', 'labels'):
            schema = copy.deepcopy(c.SCHEMA)
            if transform == 'units': schema['features'][0]['unit'] = 'token IDs'
            elif transform == 'order': schema['features'].append({'name': 'id', 'type': 'string'})
            else: schema['target']['labels']['billing'] = 7
            self.rewrite_output('schema.json', c.encode(schema))
            with self.assertRaises(ValueError): c.load_batch(self.out)
        self.rewrite_output('schema.json', c.encode(c.SCHEMA))

    def test_rejects_bad_target_and_gold_feature(self):
        self.adapt()
        originals = c.rows((self.out / 'rows.jsonl').read_bytes())
        for change in ('target', 'gold'):
            altered = copy.deepcopy(originals)
            if change == 'target': altered[0]['target'] = True
            else: altered[0]['gold'] = 'billing'
            self.rewrite_output('rows.jsonl', b''.join((json.dumps(r)+'\n').encode() for r in altered))
            with self.assertRaises(ValueError): c.load_batch(self.out)

    def test_rejects_source_overlap_unknown_split_and_duplicate_ids(self):
        original = c.rows((self.source / 'release.jsonl').read_bytes())
        for fault in ('overlap', 'split', 'duplicate'):
            altered = copy.deepcopy(original)
            if fault == 'overlap':
                altered[1]['group_id'] = altered[0]['group_id']
                altered[1]['split'] = 'test' if altered[0]['split'] != 'test' else 'train'
            elif fault == 'split': altered[0]['split'] = 'calibration'
            else: altered[1]['canonical_id'] = altered[0]['canonical_id']
            data = b''.join((json.dumps(row)+'\n').encode() for row in altered)
            (self.source / 'release.jsonl').write_bytes(data)
            manifest = c.strict_load((self.source / 'manifest.json').read_bytes())
            manifest['outputs']['release.jsonl'] = {'sha256': c.digest(data), 'bytes': len(data)}
            (self.source / 'manifest.json').write_bytes(c.encode(manifest))
            with self.assertRaises(ValueError): self.adapt()
            self.assertFalse(self.out.exists())

    def test_refuses_overwrite(self):
        self.adapt()
        with self.assertRaises(ValueError): self.adapt()

    def test_duplicate_json_keys_rejected(self):
        with self.assertRaises(ValueError): c.strict_load(b'{"a":1,"a":2}')

if __name__ == '__main__': unittest.main()
