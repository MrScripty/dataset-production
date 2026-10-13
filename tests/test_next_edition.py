"""Check the review assembly without modifying the published edition."""
import hashlib
from html.parser import HTMLParser
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('next_edition', ROOT / 'scripts/build_next_edition.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class HTMLAudit(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.ids, self.links, self.text = [], [], []
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        if tag == 'a':
            self.links.append(attrs)

    def handle_data(self, data):
        self.text.append(data)


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
            page = (output / 'index.html').read_text()
            self.assertIn('<html lang="en">', page)
            self.assertIn('a{color:#1257a4;overflow-wrap:anywhere}', page)
            self.assertRegex(page, r'body\{[^}]*overflow-wrap:anywhere')
            self.assertEqual(subprocess.run(command, capture_output=True).returncode, 2)
        self.assertEqual(hashlib.sha256((ROOT / 'docs/book/manuscript.md').read_bytes()).hexdigest(), source_hash)

    def test_preformatted_scroller_preserves_text_attributes_and_keyboard_access(self):
        source = ('<p>Inline <code>keep wrapping</code>.</p>'
                  '<pre class="text"><code>Input     Target\n20  22    21  23\n'
                  '18  21    19  22\n&amp; [R01]\n</code></pre>'
                  '<pre tabindex="0" role="region" aria-label="Existing label">x</pre>')
        output = module.make_pre_scrollable(source)
        self.assertEqual(''.join(HTMLAudit(source).text), ''.join(HTMLAudit(output).text))
        self.assertIn('Input     Target\n20  22    21  23\n18  21    19  22\n', output)
        self.assertIn('<pre class="text" tabindex="0" role="region"', output)
        self.assertIn('aria-label="Code or text diagram; scroll horizontally when needed"', output)
        self.assertIn('<pre tabindex="0" role="region" aria-label="Existing label">x</pre>', output)
        self.assertIn('&amp; [R01]', output)
        self.assertEqual(module.make_pre_scrollable(output), output)

    def test_reader_preserves_diagram_rows_with_contained_scrolling(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / 'review'
            subprocess.run([sys.executable, str(ROOT / 'scripts/build_next_edition.py'),
                            '--out', str(output)], check=True, capture_output=True)
            page = (output / 'index.html').read_text()
        style = re.search(r'<style>(.*?)</style>', page, re.S)[1]
        pre = re.search(r'(?:^|})pre\{([^}]+)}', style)[1]
        properties = dict(item.split(':', 1) for item in pre.split(';'))
        for name, value in {'white-space': 'pre', 'overflow-wrap': 'normal',
                            'word-break': 'normal', 'overflow-x': 'auto',
                            'max-width': '100%', 'box-sizing': 'border-box'}.items():
            self.assertEqual(properties[name], value)
        self.assertIn('pre code{white-space:inherit;overflow-wrap:normal;word-break:normal}', style)
        self.assertIn('pre:focus-visible{outline:', style)
        self.assertRegex(style, r'body\{[^}]*overflow-wrap:anywhere')
        self.assertIn('a{color:#1257a4;overflow-wrap:anywhere}', style)
        diagrams = [match[1] for match in re.finditer(r'<pre[^>]*><code[^>]*>(.*?)</code></pre>', page, re.S)]
        self.assertIn('Input at 0 seconds      Target at 1 second\n'
                      '20  22                  21  23\n18  21                  19  22', diagrams)
        self.assertIn('Original            Moved one column right\n'
                      '.....               .....\n.##..               ..##.\n'
                      '.##..               ..##.\n.....               .....\n'
                      '.....               .....', diagrams)
        for tag in re.findall(r'<pre(?:\s[^>]*)?>', page):
            self.assertIn('tabindex="0"', tag)
            self.assertIn('aria-label=', tag)

    def test_citation_groups_ranges_and_unknowns_preserve_text(self):
        source = ('<p>[R01] [T02, B04] [T02-T06] [R01, R999] [R404]</p>'
                  '<h1 id="references-and-evidence-notes">References</h1>'
                  '<p><strong>[R01] Real title.</strong> Evidence &amp; limits.</p>'
                  '<p><strong>[T02] Two.</strong></p><p><strong>[T06] Six.</strong></p>'
                  '<p><strong>[B04] Four.</strong></p>')
        linked = module.link_citations(source)
        audit = HTMLAudit(linked)
        self.assertEqual(''.join(audit.text), ''.join(HTMLAudit(source).text))
        self.assertEqual(set(audit.ids), {'references-and-evidence-notes', 'reference-r01', 'reference-t02', 'reference-t06', 'reference-b04'})
        self.assertEqual(len(audit.links), 6)
        self.assertNotIn('href="#reference-r999"', linked)
        self.assertNotIn('href="#reference-r404"', linked)
        self.assertIn('[R404]', linked)
        self.assertEqual(module.link_citations(linked), linked)

    def test_citation_linker_does_not_mutate_code_attributes_or_existing_links(self):
        protected = ('<a href="https://example.org/[R01]">[R01]</a>'
                     '<code>[R01]</code><pre><code>[R01]</code></pre>'
                     '<span data-example="[R01]">plain</span><!-- [R01] -->')
        source = protected + '<p>[R01]</p><h1 id="references-and-evidence-notes">References</h1><p><strong>[R01] Title.</strong></p>'
        linked = module.link_citations(source)
        self.assertIn(protected, linked)
        self.assertEqual(linked.count('class="citation"'), 1)
        self.assertEqual(''.join(HTMLAudit(linked).text), ''.join(HTMLAudit(source).text))

    def test_reference_discovery_ignores_script_code_and_unrelated_bold_prose(self):
        source = ('<script>const x="<p><strong>[R99]</strong></p>";</script>'
                  '<p><strong>[R01] Prose.</strong><strong>[R98] Prose.</strong> [R99] [R98] [R01]</p>'
                  '<h1 id="references-and-evidence-notes">References</h1>'
                  '<pre><code><strong>[R97]</strong></code></pre>'
                  '<p><strong><code>[R94]</code></strong></p>'
                  '<p><strong>&amp;[R93]</strong></p>'
                  '<p><strong>&#38;[R92]</strong></p>'
                  '<p>&amp;<strong>[R91]</strong></p>'
                  '<p>Not an entry: <strong>[R96]</strong></p>'
                  '<p><strong>[R01] Real entry.</strong></p>'
                  '<h1 id="next-edition-research-register">Next section</h1>'
                  '<p><strong>[R95] Not an entry.</strong> [R95]</p>')
        linked = module.link_citations(source)
        self.assertEqual(''.join(HTMLAudit(source).text), ''.join(HTMLAudit(linked).text))
        self.assertEqual(linked.count('class="citation"'), 1)
        self.assertIn('id="reference-r01"', linked)
        for label in ('r91', 'r92', 'r93', 'r94', 'r95', 'r96', 'r97', 'r98', 'r99'):
            self.assertNotIn('reference-' + label, linked)
        self.assertIn('<script>const x="<p><strong>[R99]</strong></p>";</script>', linked)

    def test_duplicate_reference_destinations_fail(self):
        with self.assertRaisesRegex(ValueError, 'duplicate bibliography label'):
            module.link_citations('<h1 id="references-and-evidence-notes">Refs</h1><p><strong>[R01] First</strong></p><p><strong>[R01] Second</strong></p>')

    def test_chapter_anchors_survive_reordering(self):
        _, original = module.assemble()
        config = json.loads(module.MANIFEST.read_text())
        config['chapters'] = list(reversed(config['chapters']))
        with tempfile.TemporaryDirectory() as temporary:
            manifest = Path(temporary) / 'manifest.json'
            manifest.write_text(json.dumps(config))
            with patch.object(module, 'MANIFEST', manifest):
                manuscript, reordered = module.assemble()
        self.assertEqual(reordered['chapter_anchors'], list(reversed(original['chapter_anchors'])))
        self.assertIn('[21 Build your first release from supplied data](#chapter-first-release)', manuscript)
        self.assertIn('# 21 Build your first release from supplied data {#chapter-first-release}', manuscript)

    def test_duplicate_chapter_ids_fail(self):
        config = json.loads(module.MANIFEST.read_text())
        config['chapters'][1]['id'] = config['chapters'][0]['id']
        with tempfile.TemporaryDirectory() as temporary:
            manifest = Path(temporary) / 'manifest.json'
            manifest.write_text(json.dumps(config))
            with patch.object(module, 'MANIFEST', manifest):
                with self.assertRaisesRegex(ValueError, 'unique stable'):
                    module.assemble()

    def test_reader_navigation_and_reference_links_have_unique_destinations(self):
        manuscript, metadata = module.assemble()
        source = subprocess.run(['pandoc', '-f', 'markdown', '-t', 'html5', '--wrap=none'],
                                input=manuscript, text=True, capture_output=True, check=True).stdout
        linked = module.link_citations(source)
        audit = HTMLAudit(linked)
        self.assertEqual(len(audit.ids), len(set(audit.ids)))
        links = [link['href'][1:] for link in audit.links if link.get('href', '').startswith('#')]
        self.assertEqual(set(links) - set(audit.ids), set())
        for anchor in metadata['chapter_anchors']:
            self.assertIn(anchor, links)
        for anchor in ('reader-paths', 'contents', 'appendix-a', 'appendix-b', 'appendix-c',
                       'appendix-d', 'references-and-evidence-notes', 'next-edition-research-register'):
            self.assertIn(anchor, links)
        entries = set(re.findall(r'\*\*\[([RTB]\d+)\]', manuscript))
        reference_ids = {identity for identity in audit.ids if identity.startswith('reference-')}
        self.assertEqual(reference_ids, {'reference-' + entry.lower() for entry in entries})
        self.assertGreater(len([link for link in audit.links if link.get('class') == 'citation']), 80)
        self.assertEqual(''.join(audit.text), ''.join(HTMLAudit(source).text))

    def test_refuses_published_output(self):
        for target in (ROOT, ROOT / 'docs', ROOT / 'docs/book/unpublished-preview'):
            result = subprocess.run([sys.executable, str(ROOT / 'scripts/build_next_edition.py'), '--out', str(target)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 2)
            self.assertIn('outside the published docs tree', result.stderr)


if __name__ == '__main__':
    unittest.main()
