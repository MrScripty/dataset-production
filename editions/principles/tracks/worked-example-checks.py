"""Check the six authored paper examples using only the Python standard library.

These checks verify example arithmetic and declared semantics. They do not run
an ML model, a project consumer, a simulator or a production release recovery.
Run: python editions/principles/tracks/worked-example-checks.py
"""
from fractions import Fraction
from math import gcd
import json
import re


def main():
    checks = []
    def check(name, condition):
        if not condition:
            raise AssertionError(name)
        checks.append(name)

    # Retrieval sufficiency is the explicitly authored guide, not a learned score.
    sufficient = lambda chunks: {'D1-a', 'D1-b'}.issubset(chunks)
    check('text missing exception fails sufficient evidence', not sufficient(['D1-a', 'D2']))
    check('text neighboring context supplies scope and exception', sufficient(['D1-a', 'D1-b']))
    morning = [24, 29, 25, None]
    later = [28, 32, 27, 31]
    target = [False, True, False, True]
    prediction = [None if x is None else x > 27 for x in morning]
    check('tabular later values reproduce labels but are unavailable features', [x > 30 for x in later] == target)
    check('tabular baseline coverage is three of four', sum(x is not None for x in prediction) == 3)
    check('tabular conditional agreement is three of three', sum(p == y for p,y in zip(prediction,target) if p is not None) == 3)
    foreground = {(1,1), (2,1)}
    shifted = {(x+1,y) for x,y in foreground}
    check('vision shifted foreground reaches last column', shifted == {(2,1), (3,1)})
    check('vision image-only transform has IoU one third', Fraction(len(foreground & shifted),len(foreground | shifted)) == Fraction(1,3))
    check('vision exclusive maximum reaches width four', max(x for x,y in shifted)+1 == 4)
    waveform = [0,0,1,-1,1,-1,0,0]
    check('audio half-open interval contains four samples', waveform[2:6] == [1,-1,1,-1])
    check('audio interval lasts half a second', Fraction(6-2,8) == Fraction(1,2))
    check('audio insertion-only WER is 150 percent', Fraction(3,2)*100 == 150)
    def narrow_fraction(answer):
        answer = answer.strip()
        if not re.fullmatch(r'(?:0|[1-9][0-9]*)/[1-9][0-9]*', answer):
            return False
        numerator, denominator = map(int, answer.split('/'))
        return gcd(numerator,denominator) == 1 and Fraction(numerator,denominator) == Fraction(1,2)
    check('reasoning exact reduced fraction accepted', narrow_fraction(' 1/2 '))
    for answer in ['2/4','0.5','1/3','1/2 or 2/3','The answer is not 1/2.','1/2 because 1 + 1 = 3']:
        check('reasoning rejects '+answer, not narrow_fraction(answer))
    field = [[20,22],[18,21]]
    warmed = [[x+1 for x in row] for row in field]
    check('physical four-cell arithmetic target', warmed == [[21,23],[19,22]])
    check('physical Kelvin conversion changes numerical value', Fraction(20)+Fraction(27315,100) == Fraction(29315,100))
    check('physical horizontal face count is six', (2+1)*2 == 6)
    check('modal two-observation gain is three', Fraction(1*3+2*6,1*1+2*2) == 3)
    check('mixture equal example target-token proportion', Fraction(400,420) == Fraction(20,21))
    check('verifier single accepted precision', Fraction(5700,6100) == Fraction(57,61))
    check('verifier conditional-independent accepted precision', Fraction(5415,5455) > Fraction(99,100))
    print(json.dumps({'status':'passed','evidence':'executed arithmetic checks on authored examples only','checks':checks},indent=2))


if __name__ == '__main__':
    main()
