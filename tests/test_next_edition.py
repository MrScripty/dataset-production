"""Check the review assembly without modifying the published edition."""
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('next_edition', ROOT / 'scripts/build_next_edition.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class NextEditionTests(unittest.TestCase):
    def test_retained_source_is_exact_audited_blob(self):
        source = (ROOT / 'docs/book/manuscript.md').read_bytes()
        blob = hashlib.sha1(b'blob ' + str(len(source)).encode() + b'\0' + source).hexdigest()
        self.assertEqual(blob, '8f10a4bc9adc5325974fa0e3cdba1a97127d3fdf')

    def test_assembly_is_deterministic_and_credited(self):
        manuscript, metadata = module.assemble()
        self.assertEqual(module.assemble(), (manuscript, metadata))
        self.assertIn('Author: Puma', manuscript)
        self.assertIn('# Reader paths and data acquisition', manuscript)
        self.assertIn('## Exact beginner acquisition paths', manuscript)
        self.assertIn('### B Small open tabular data', manuscript)
        self.assertIn('examples/first-release/README.md)', manuscript)
        self.assertIn('Initial next-edition draft', manuscript)
        self.assertEqual(metadata['manuscript_sha256'], hashlib.sha256(manuscript.encode()).hexdigest())
        self.assertEqual(metadata['retained_chapters'], list(range(1, 17)))
        self.assertEqual(len(re.findall(r'^# \d+ ', manuscript, re.M)), metadata['chapters'])
        for letter in 'ABCD':
            self.assertEqual(len(re.findall(r'^# Appendix ' + letter + ' ', manuscript, re.M)), 1)

    def test_all_legacy_citations_have_entries(self):
        manuscript, _ = module.assemble()
        citations = set(re.findall(r'\[([RTB]\d+)\]', manuscript))
        entries = set(re.findall(r'\*\*\[([RTB]\d+)\]', manuscript))
        self.assertEqual(citations - entries, set())

    def test_every_figure_exists(self):
        manuscript, _ = module.assemble()
        figures = re.findall(r'!\[[^\]]*\]\(figures/([^)]*)\)', manuscript)
        self.assertTrue(figures)
        for name in figures:
            self.assertTrue((ROOT / 'docs/book/figures' / name).is_file(), name)
            self.assertTrue(name.endswith('.svg'))

    def test_build_emits_reader_and_refuses_overwrite(self):
        source_hash = hashlib.sha256((ROOT / 'docs/book/manuscript.md').read_bytes()).hexdigest()
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / 'review'
            command = [sys.executable, str(ROOT / 'scripts/build_next_edition.py'), '--out', str(output)]
            result = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            metadata = json.loads((output / 'metadata.json').read_text())
            self.assertEqual(metadata['retained_source_sha256'], source_hash)
            self.assertIn('<html lang="en">', (output / 'index.html').read_text())
            self.assertEqual(subprocess.run(command, capture_output=True).returncode, 2)
        self.assertEqual(hashlib.sha256((ROOT / 'docs/book/manuscript.md').read_bytes()).hexdigest(), source_hash)

    def test_refuses_published_output(self):
        for target in (ROOT, ROOT / 'docs', ROOT / 'docs/book/unpublished-preview'):
            result = subprocess.run([sys.executable, str(ROOT / 'scripts/build_next_edition.py'), '--out', str(target)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 2)
            self.assertIn('outside the published docs tree', result.stderr)


if __name__ == '__main__':
    unittest.main()
