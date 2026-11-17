from fractions import Fraction
from pathlib import Path
import json

OUT = Path(__file__).parent

def v2(n):
    if n == 0:
        return 1000000
    n = abs(n)
    return (n & -n).bit_length() - 1

def residue(f, bits):
    a = v2(f.numerator) - v2(f.denominator)
    assert a >= 0
    return (f.numerator * pow(f.denominator, -1, 1 << bits)) % (1 << bits)

# The displayed tail bounds in the manuscript give > 60 bits for k>256.
H = Fraction(0)
H2 = Fraction(0)
nu = Fraction(0)
mu = Fraction(0)
for k in range(1, 257):
    weight = Fraction(1 << k, k*k)
    nu += -2 * weight * H
    mu += weight * (2*H*H-H2)
    H += Fraction(1,k)
    H2 += Fraction(1,k*k)

bits = 60
nu60 = residue(nu, bits)
# mu may not be integral; report its valuation separately.
mu_v = v2(mu.numerator)-v2(mu.denominator)
mu_scaled = mu * (1 << max(0,-mu_v))
mu_residue = residue(mu_scaled,bits)

# Exact central Delannoy recurrence.
NMAX = 4096
D = [1,3]
for n in range(2,NMAX+1):
    q,r = divmod(3*(2*n-1)*D[-1]-(n-1)*D[-2],n)
    assert r == 0
    D.append(q)

tests = 0
failures = []
quartic_failures = []
excess = {}
for t in range(3,10):
    q = 1 << t
    mn = None
    for x in range(0, min(8,NMAX//q)+1):
        for y in range(x+1,min(8,NMAX//q)+1):
            c = v2(y-x)
            exponent = 4*t+c-1
            diff = D[q*y]-D[q*x]
            cubic = (1 << (3*t))*(y**3-x**3)
            rem = diff - nu60*cubic
            val = v2(rem)
            tests += 1
            if val < exponent:
                failures.append([t,x,y,exponent,val])
            quartic = mu_residue*(1 << (4*t-1))*(y**4-x**4)
            qval = v2(rem-quartic)
            if qval < 5*t+c-4:
                quartic_failures.append([t,x,y,5*t+c-4,qval])
            mn = min(mn,val-exponent) if mn is not None else val-exponent
    excess[str(t)] = mn

result = {
 'nu_mod_2_60':nu60,
 'nu_hex':hex(nu60),
 'quartic_coefficient_partial_sum_v2':mu_v,
 'quartic_coefficient_scaled_mod_2_60':mu_residue,
 'scaled_by':1<<max(0,-mu_v),
 'improved_cubic_modulus':'2^(4t+v2(y-x)-1), t>=3',
 'quartic_modulus':'2^(5t+v2(y-x)-4), t>=3',
 'mathematical_status':'proved by retaining the quartic term in the existing proof; proof outline in precision_proof.txt',
 'tests':tests,'failures':failures,'quartic_failures':quartic_failures,'minimum_excess_valuation':excess,
 'range':{'t':[3,9],'x_y':[0,8],'max_index':NMAX},
 'coefficient_tail':'For nu the manuscript bound k+1-2v2(k)-floor(log2(k-1)) exceeds 60 for every k>=257. For mu the bound k-2v2(k)-2floor(log2(k-1)) does likewise. Dyadic minima increase thereafter.'
}
(OUT/'precision_results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))
