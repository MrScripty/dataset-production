"""Check authored worked examples, without treating them as model experiments."""
from fractions import Fraction
from html.parser import HTMLParser
import json
import math
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
CHAPTERS = ROOT / 'editions/next/chapters'


def chapter(name):
    return (CHAPTERS / (name + '.md')).read_text()


def tilde_blocks(name, language):
    return re.findall(r'~~~' + language + r'\n(.*?)\n~~~', chapter(name), re.S)


class LessonExampleTests(unittest.TestCase):
    def test_pixel_move_and_crop_preserve_declared_coordinates(self):
        text = chapter('augmentation')
        fence = chr(96) * 3
        blocks = re.findall(fence + r'text\n(.*?)\n' + fence, text, re.S)
        pairs = [line.split() for line in blocks[0].splitlines()[1:]]
        original = [pair[0] for pair in pairs]
        moved = [pair[1] for pair in pairs]
        self.assertEqual(len(original), 5)
        self.assertTrue(all(len(row) == 5 for row in original + moved))
        def points(rows):
            return {(x, y) for y, row in enumerate(rows)
                    for x, value in enumerate(row) if value == '#'}
        self.assertEqual(points(original), {(1, 1), (2, 1), (1, 2), (2, 2)})
        self.assertEqual(points(moved), {(x + 1, y) for x, y in points(original)})
        cropped = blocks[1].splitlines()[1:]
        self.assertEqual(cropped, [row[:2] for row in original])

    def test_temperature_target_and_reversal_match_the_stated_rule(self):
        blocks = tilde_blocks('physical-systems', 'text')
        original = [[int(value) for value in row.split()]
                    for row in blocks[0].splitlines()]
        pairs = [[int(value) for value in row.split()]
                 for row in blocks[1].splitlines()[1:]]
        target = [row[2:] for row in pairs]
        self.assertEqual([row[:2] for row in pairs], original)
        self.assertEqual(target, [[value + 1 for value in row] for row in original])
        reversed_rows = [[int(value) for value in row.split()]
                         for row in blocks[2].splitlines()]
        self.assertEqual(reversed_rows, target[::-1])
        self.assertAlmostEqual(20 + 273.15, 293.15)

    def test_fraction_judgments_follow_the_explicit_format_and_value_contract(self):
        text = chapter('reasoning-trajectories')
        rows = [line.split('|')[1:-1] for line in text.splitlines()
                if line.startswith('| ') and line.count('|') == 5]
        candidates = [(row[0].strip(), row[3].strip()) for row in rows
                      if row[3].strip().startswith(('Accept', 'Reject'))]
        self.assertEqual(len(candidates), 7)
        def accepts(answer):
            answer = answer.strip()
            if not re.fullmatch(r'-?(?:0|[1-9][0-9]*)/[1-9][0-9]*', answer):
                return False
            numerator, denominator = map(int, answer.split('/'))
            return math.gcd(numerator, denominator) == 1 and Fraction(numerator, denominator) == Fraction(1, 2)
        for answer, judgment in candidates:
            self.assertEqual(accepts(answer), judgment.startswith('Accept'), answer)
        self.assertTrue(accepts(' 1/2 '))
        self.assertIn('without plus signs or leading zeros', text)

    def test_confidence_cutoff_selects_three_with_two_reference_matches(self):
        rows = []
        for line in chapter('weak-semisupervised').splitlines():
            if not line.startswith('| '):
                continue
            columns = [part.strip() for part in line.split('|')[1:-1]]
            if len(columns) == 4 and re.fullmatch(r'0\.\d+', columns[2]):
                rows.append(columns)
        self.assertEqual(len(rows), 4)
        selected = [row for row in rows if float(row[2]) >= .9]
        self.assertEqual(len(selected), 3)
        self.assertEqual(sum(row[1] == row[3] for row in selected), 2)

    def test_opening_reports_actual_coverage_and_scored_reference_denominators(self):
        audit = json.loads((ROOT / 'examples/first-release/expected/audit.json').read_text())
        weak = audit['weak_labels']
        text = chapter('first-release')
        self.assertIn(f"{weak['labeled']} of {audit['counts']['canonical_examples']}", text)
        self.assertIn(f"{weak['correct']} of {weak['evaluated_predictions']}", text)
        self.assertEqual(weak['labeled'] - weak['evaluated_predictions'], 1)
        self.assertIn('not an independent human annotation study', text)

    def test_augmentation_is_taught_before_consistency_training(self):
        config = json.loads((ROOT / 'editions/next/manifest.json').read_text())
        identities = [item['id'] for item in config['chapters']]
        self.assertLess(identities.index('augmentation'), identities.index('weak-semisupervised'))

    def test_monitoring_example_reproduces_the_described_nested_text_loss(self):
        source = tilde_blocks('monitoring', 'html')[0]
        class TextExtractor(HTMLParser):
            def __init__(self):
                super().__init__()
                self.stack, self.all_text, self.direct_text = [], [], []
            def handle_starttag(self, tag, attrs):
                self.stack.append(tag)
            def handle_endtag(self, tag):
                self.stack.pop()
            def handle_data(self, data):
                if 'p' in self.stack:
                    self.all_text.append(data)
                if self.stack and self.stack[-1] == 'p':
                    self.direct_text.append(data)
        parser = TextExtractor()
        parser.feed(source)
        clean = lambda parts: ' '.join(''.join(parts).split())
        self.assertEqual(clean(parser.all_text), 'Please do not refund this payment.')
        self.assertEqual(clean(parser.direct_text), 'Please do refund this payment.')


if __name__ == '__main__':
    unittest.main()
