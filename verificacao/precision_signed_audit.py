"""Exact independent modular audit using generalized binomial coefficients.

Negative arguments are evaluated directly, rather than through reflection.
The calculation corroborates the written cutoff proof; it is not that proof.
"""
from pathlib import Path
from fractions import Fraction
import json

def v2(n):
    if not n:
        return float('inf')
    n = abs(n)
    return (n & -n).bit_length()-1

def rational_mod(x, bits):
    assert x.denominator % 2
    modulus = 1 << bits
    return x.numerator * pow(x.denominator, -1, modulus) % modulus

def F_mod(n, bits):
    modulus = 1 << bits
    binomial = 1
    value = 1
    for k in range(1, bits):
        dividend = binomial * (n-k+1)
        binomial, remainder = divmod(dividend, k)
        assert remainder == 0
        value = (value + (1 << k)*binomial*binomial) % modulus
    return value

H = H2 = nu = mu = Fraction(0)
mu8 = None
for k in range(1, 257):
    weight = Fraction(1 << k, k*k)
    nu -= 2*weight*H
    mu += weight*(2*H*H-H2)
    if k == 8:
        mu8 = mu
    H += Fraction(1, k)
    H2 += Fraction(1, k*k)
assert mu8 == Fraction(4352977,39690)
assert v2(mu.numerator)-v2(mu.denominator) == -1

bits = 80
nu_mod = rational_mod(nu,bits)
mu2_mod = rational_mod(2*mu,bits)
checks = []
failures = []
sharp = []
for t in range(3,13):
    q = 1 << t
    values = {x:F_mod(q*x,bits) for x in range(-9,10)}
    for x in values:
        for y in values:
            if x >= y:
                continue
            c = v2(y-x)
            diff = values[y]-values[x]
            cubic = nu_mod*q**3*(y**3-x**3)
            quartic = mu2_mod*(1 << (4*t-1))*(y**4-x**4)
            cubic_val = v2((diff-cubic) % (1 << bits))
            quartic_val = v2((diff-cubic-quartic) % (1 << bits))
            if cubic_val < 4*t+c-1 or quartic_val < 5*t+c-4:
                failures.append({'t':t,'x':x,'y':y,'c':c,
                                 'cubic_v':cubic_val,'quartic_v':quartic_val})
            checks.append((t,x,y))
    if t >= 4:
        observed = v2((values[1]-values[0]-nu_mod*q**3) % (1 << bits))
        assert observed == 4*t-1
        sharp.append({'t':t,'x':0,'y':1,'error_valuation':observed})

assert not failures
result = {'tests':len(checks),'failures':failures,'t_range':[3,12],
          'x_y_range':[-9,9],'evaluation':'direct generalized binomial sum modulo 2^80',
          'mu_sum_through_8':str(mu8),'mu_valuation':-1,
          'sharpness_checks':sharp,
          'tail_note':'Coefficient truncation k<=256 has tails beyond 80 bits by the dyadic lower bounds.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))
