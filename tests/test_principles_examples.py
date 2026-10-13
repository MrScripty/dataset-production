"""Recalculate the authored arithmetic; these checks are not model experiments."""
from fractions import Fraction
import json
import math
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
EDITION = ROOT / 'editions/principles'


def core(number):
    return next((EDITION / 'core').glob(f'{number:02}-*.md')).read_text()


class PaperExamplesTests(unittest.TestCase):
    def test_fixture_arithmetic_has_explicit_denominators(self):
        audit = json.loads((ROOT / 'examples/first-release/expected/audit.json').read_text())
        self.assertEqual(audit['counts']['input_lines'], 30)
        self.assertEqual(audit['counts']['accepted_raw_records']+audit['counts']['quarantined_lines'], 30)
        self.assertEqual(audit['counts']['canonical_examples'], 24)
        weak = audit['weak_labels']
        self.assertEqual(weak['labeled']+weak['abstain']+weak['conflict'], 24)
        self.assertEqual((weak['correct'], weak['evaluated_predictions']), (10, 13))
        self.assertIn('14 / 24', core(1))
        self.assertIn('10 / 13', core(1))

    def test_temperature_conversion_and_stated_rule(self):
        blocks = re.findall(r'~~~text\n(.*?)\n~~~', core(3), re.S)
        arrays = [block for block in blocks if re.fullmatch(r'\d+  \d+\n\d+  \d+', block)]
        self.assertEqual(len(arrays), 2)
        values = [[int(x) for x in array.split()] for array in arrays]
        self.assertEqual(values[1], [x+1 for x in values[0]])
        self.assertAlmostEqual(values[0][0]+273.15, 293.15)
        self.assertAlmostEqual(values[1][0]+273.15, 294.15)

    def test_pseudo_label_threshold_sensitivity(self):
        rows = []
        for line in core(11).splitlines():
            columns = [part.strip() for part in line.split('|')[1:-1]]
            if len(columns) == 4 and re.fullmatch(r'0\.\d+', columns[2]):
                rows.append(columns)
        self.assertEqual(len(rows), 4)
        for threshold, expected in [(0.60, (4,3)), (0.90,(3,2)), (0.95,(2,1)), (0.99,(0,0))]:
            selected = [row for row in rows if float(row[2]) >= threshold]
            self.assertEqual((len(selected), sum(row[1]==row[3] for row in selected)), expected)

    def test_fraction_judgments_are_exact_under_declared_contract(self):
        text = (EDITION / 'tracks/05-reasoning-trajectories.md').read_text()
        found = []
        for line in text.splitlines():
            columns = [part.strip() for part in line.split('|')[1:-1]]
            if len(columns)==4 and columns[3].startswith(('Accept','Reject')):
                answer, judgment = columns[0], columns[3]
                valid = bool(re.fullmatch(r'-?(?:0|[1-9][0-9]*)/[1-9][0-9]*', answer))
                if valid:
                    numerator, denominator = map(int, answer.split('/'))
                    valid = math.gcd(numerator,denominator)==1 and Fraction(numerator,denominator)==Fraction(1,2)
                self.assertEqual(valid, judgment.startswith('Accept'), answer)
                found.append(answer)
        self.assertEqual(len(found), 7)

    def test_tabular_availability_and_abstention(self):
        text = (EDITION / 'tracks/02-tabular-time-series.md').read_text()
        rows = []
        for line in text.splitlines():
            columns = [part.strip() for part in line.split('|')[1:-1]]
            if len(columns)==5 and columns[0] in ('A','B'):
                rows.append(columns)
        self.assertEqual(len(rows), 4)
        checked = []
        for _,_,feature,outcome,target in rows:
            self.assertEqual(int(outcome)>30, target=='yes')
            if feature!='missing':
                checked.append((int(feature)>27)==(target=='yes'))
        self.assertEqual((len(checked),sum(checked)), (3,3))

    def test_audio_duration_and_wer(self):
        text = (EDITION / 'tracks/04-audio.md').read_text()
        self.assertIn('[2,6)', text)
        self.assertEqual(Fraction(6-2,8),Fraction(1,2))
        self.assertEqual(Fraction(3,2)*100,150)
        self.assertIn('150%', text)


if __name__ == '__main__':
    unittest.main()
