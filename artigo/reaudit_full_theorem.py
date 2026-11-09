"""Adversarial independent checks of the integrated theorem.

Primary check: exact Delannoy values from the three-term Legendre recurrence,
not the binomial-sum evaluators in the author's reproduction scripts.
Secondary check: truncated generalized-binomial interpolation for large and
negative indices, evaluated independently at the predicted precision.
"""
import json
from collections import Counter
from functools import lru_cache
from pathlib import Path


def v2(n):
    if n == 0:
        return None
    n = abs(n)
    return (n & -n).bit_length()-1


values = [1, 3]
for index in range(2, 8193):
    numerator = 3*(2*index-1)*values[-1] - (index-1)*values[-2]
    assert numerator % index == 0
    values.append(numerator // index)

counts = Counter()
failures = []
for b in range(-256, 257):
    for u in range(1, 32, 2):
        if b in (0, -1):
            n_min = 3
            t = None
        else:
            t = v2(b*(b+1))
            n_min = max(2, t)
        for n in range(n_min, 8):
            first = b + u*2**n
            second = b + u*2**(n+1)
            if first < 0:
                continue
            expected = 3*n if t is None else n+2*t
            actual = v2(values[second]-values[first])
            category = 'exceptional' if t is None else ('negative_shift' if b < 0 else 'positive_shift')
            counts[category] += 1
            counts['exact_integer_total'] += 1
            if actual != expected:
                failures.append(dict(method='exact', b=b, u=u, n=n, expected=expected, actual=actual))


@lru_cache(None)
def F_mod(index, precision):
    modulus = 2**precision
    choose = 1
    total = 1
    for k in range(1, precision):
        choose = choose*(index-k+1)//k
        total = (total + 2**k*choose*choose) % modulus
    return total


# High valuation near both critical shifts, including negative shifts and
# endpoints outside the classical domain for a separate F-interpolation check.
for t in range(3, 19):
    for odd_factor in (-9, -5, -1, 1, 5, 9):
        for shift_offset in (0, -1):
            b = odd_factor*2**t + shift_offset
            assert v2(b*(b+1)) == t
            for u in range(1, 16, 2):
                for n in (t, t+1, t+3):
                    expected = n+2*t
                    precision = expected+1
                    first = b+u*2**n
                    second = b+u*2**(n+1)
                    residue = (F_mod(second, precision)-F_mod(first, precision)) % 2**precision
                    counts['large_modular_F_total'] += 1
                    if first >= 0:
                        counts['large_modular_D_domain'] += 1
                    else:
                        counts['large_modular_negative_endpoint'] += 1
                    if residue != 2**expected:
                        failures.append(dict(method='modular', b=b, u=u, n=n, expected=expected, residue=residue))

# Exceptional shifts at larger scales.
for b in (0, -1):
    for n in range(8, 23):
        for u in range(1, 64, 2):
            expected = 3*n
            precision = expected+1
            first, second = b+u*2**n, b+u*2**(n+1)
            residue = (F_mod(second, precision)-F_mod(first, precision)) % 2**precision
            counts['large_exceptional_total'] += 1
            if residue != 2**expected:
                failures.append(dict(method='large_exceptional', b=b, u=u, n=n, expected=expected, residue=residue))

report = {
    'main_source': 'outputs/revisao_delannoy/artigo/main.tex',
    'method': 'Exact three-term Delannoy recurrence through index 8192; independent modular generalized-binomial recurrence for large/signed arguments',
    'counts': dict(counts),
    'failures': failures,
}
Path(__file__).with_suffix('.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
print(json.dumps(report, indent=2))
assert not failures
