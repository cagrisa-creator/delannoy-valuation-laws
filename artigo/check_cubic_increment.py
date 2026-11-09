"""Independent modular checks of M4, including new scales t=3,4.

No imports from the manuscript's reproducing scripts.  Generalized binomial
coefficients are evaluated by their integer recurrence.  This is evidence,
not a replacement for the uniform estimates in the accompanying proof.
"""
from fractions import Fraction
from functools import lru_cache
import json
from pathlib import Path


def v2(n):
    if n == 0:
        return 10**9
    n = abs(n)
    return (n & -n).bit_length() - 1


harmonic = Fraction(0)
nu = Fraction(0)
for k in range(1, 256):
    nu -= Fraction(2 ** (k + 1), k * k) * harmonic
    harmonic += Fraction(1, k)
assert nu.denominator % 2
assert nu.numerator % 2


@lru_cache(None)
def interpolated_mod(n, precision):
    modulus = 2**precision
    coefficient = 1
    total = 1
    for k in range(1, precision):
        coefficient = coefficient * (n - k + 1) // k
        total = (total + (1 << k) * coefficient * coefficient) % modulus
    return total


counts = {}
failures = []
for t in range(3, 9):
    q = 2**t
    counts[str(t)] = 0
    for r in range(-11, 12):
        for s in list(range(-32, 0)) + list(range(1, 33)):
            c = v2(s)
            precision = 3*t + c + 1
            modulus = 2**precision
            nu_mod = nu.numerator * pow(nu.denominator, -1, modulus) % modulus
            x = r+s
            y = r+2*s
            difference = (interpolated_mod(q*y, precision) - interpolated_mod(q*x, precision)) % modulus
            main = nu_mod*q**3*(y**3-x**3) % modulus
            counts[str(t)] += 1
            if difference != main:
                failures.append([t, r, s, precision, difference, main])
            if r % 2 and v2(difference) != 3*t+c:
                failures.append(['odd valuation', t, r, s])

# Direct exhaustive checks of the numerical inequality, beyond the proof.
inequality_checks = 0
for t in range(3, 14):
    for k in range(2, 2**(t+1)):
        ell = (k-1).bit_length()-1
        assert t + k - 2*v2(k) - 2*ell >= 1
        inequality_checks += 1

report = {
    'method': 'Independent integer binomial recurrence, modular F series, exact rational nu partial sum',
    'nu_cutoff_exclusive': 256,
    'nu_tail_justification': 'For k>=256, k+1-2*v2(k)-floor(log2(k-1))>=233; all tested precisions <=30.',
    'increment_cases_by_t': counts,
    'increment_cases_total': sum(counts.values()),
    'numerical_inequality_checks': inequality_checks,
    'failures': failures,
}
Path(__file__).with_suffix('.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
print(json.dumps(report, indent=2))
assert not failures
