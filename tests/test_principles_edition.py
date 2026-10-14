"""Structure, provenance and artifact regression gates for the revised edition."""
import hashlib
from html.parser import HTMLParser
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('principles', ROOT / 'scripts/build_principles_edition.py')
book = importlib.util.module_from_spec(spec)
spec.loader.exec_module(book)


class HTMLAudit(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.ids, self.fragments = [], []
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        if attrs.get('href', '').startswith('#'):
            self.fragments.append(attrs['href'][1:])


class PrinciplesTests(unittest.TestCase):
    def test_approved_structure_and_determinism(self):
        source, metadata = book.assemble()
        self.assertEqual(book.assemble(), (source, metadata))
        self.assertEqual(metadata['chapters'], 15)
        self.assertEqual(metadata['tracks'], 6)
        self.assertEqual(len(re.findall(r'^# \d+ ', source, re.M)), 15)
        self.assertEqual(len(re.findall(r'^# Part \d:', source, re.M)), 4)
        self.assertIn('Author: Puma', source)
        self.assertIn('No GPU, sensors, paid service, account or external dataset download is required', source)
        self.assertEqual(metadata['manuscript_sha256'], hashlib.sha256(source.encode()).hexdigest())
        for letter in 'ABCD':
            self.assertEqual(len(re.findall(r'^# Appendix '+letter+' ', source, re.M)), 1)

    def test_lessons_include_exercise_answer_and_gate(self):
        for path in sorted((ROOT / 'editions/principles/core').glob('[0-9][0-9]-*.md')):
            text = path.read_text().lower()
            for concept in ('principle', 'worked', 'exercise', 'acceptance', 'reviewer'):
                self.assertIn(concept, text, (path.name, concept))
        tracks = sorted((ROOT / 'editions/principles/tracks').glob('0[1-6]-*.md'))
        self.assertEqual(len(tracks), 6)
        for path in tracks:
            text = path.read_text().lower()
            for concept in ('exercise', 'answer', 'acceptance'):
                self.assertIn(concept, text, (path.name, concept))

    def test_original_edition_preserved_exactly(self):
        source = (ROOT / 'editions/research-2026-10-02/manuscript.md').read_bytes()
        self.assertEqual(hashlib.sha1(b'blob '+str(len(source)).encode()+b'\0'+source).hexdigest(), '8f10a4bc9adc5325974fa0e3cdba1a97127d3fdf')
        for name, expected in [('dataset-production-research-2026-10-02.pdf', 'be6f6df6124ca41cb613bfda9d7ce740e97c8e18'), ('dataset-production-research-2026-10-02-source.zip', '0ee5b6fdf3215cfd099ad54d9fb19194e51313de')]:
            content = (ROOT / 'docs/downloads' / name).read_bytes()
            self.assertEqual(hashlib.sha1(b'blob '+str(len(content)).encode()+b'\0'+content).hexdigest(), expected)

    def test_migration_covers_every_delivered_section(self):
        migration = json.loads((ROOT / 'editions/principles/migration.json').read_text())
        original = (ROOT / 'editions/research-2026-10-02/manuscript.md').read_text()
        expected = []
        for chunk in re.split(r'(?m)(?=^# )', original):
            match = re.match(r'# (\d+) [^\n]+\n', chunk)
            if match:
                expected.extend((int(match[1]), heading) for heading in re.findall(r'^## (.+)$', chunk, re.M))
        actual = {(item.get('source_chapter'), item['source_section']) for item in migration['sections']}
        self.assertFalse(set(expected)-actual)
        source, _ = book.assemble()
        anchors = set(re.findall(r'\{#([^}]+)\}', source))
        for item in migration['sections']:
            self.assertTrue(item['editorial_action'])
            self.assertFalse(set(item['destinations'])-anchors, item['source_section'])

    def test_reader_fragments_are_unique_and_resolvable(self):
        source, _ = book.assemble()
        rendered = subprocess.run(['pandoc', '-f', 'markdown', '-t', 'html5'], input=source, text=True, capture_output=True, check=True).stdout
        page = HTMLAudit(rendered)
        self.assertEqual(len(page.ids), len(set(page.ids)))
        self.assertFalse(set(page.fragments)-set(page.ids))

    def test_release_checksums_and_source_bundle(self):
        path = ROOT / 'docs/downloads/checksums.json'
        self.assertTrue(path.exists(), 'Generate the actual release before qualification')
        checks = json.loads(path.read_text())
        source = (ROOT / 'docs/book/manuscript.md').read_bytes()
        self.assertEqual(checks['manuscript_sha256'], hashlib.sha256(source).hexdigest())
        for name, value in checks['files'].items():
            content = (path.parent / name).read_bytes()
            self.assertEqual(value, {'bytes': len(content), 'sha256': hashlib.sha256(content).hexdigest()})
        with zipfile.ZipFile(path.parent / 'dataset-production-source.zip') as archive:
            self.assertEqual(archive.read('docs/book/manuscript.md'), source)
            hashes = json.loads(archive.read('file-hashes.json'))
            self.assertEqual(set(hashes), set(archive.namelist())-{'file-hashes.json'})
            for name, digest in hashes.items():
                self.assertEqual(hashlib.sha256(archive.read(name)).hexdigest(), digest)
            self.assertFalse(any('/evidence/' in name or '__pycache__' in name or '.git/' in name for name in archive.namelist()))


if __name__ == '__main__':
    unittest.main()
