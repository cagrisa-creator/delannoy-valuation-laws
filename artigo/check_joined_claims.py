"""Exact checks of the new consequences; finite evidence, not a universal proof."""
from pathlib import Path
from collections import Counter
import json

def v2(x):
    if x == 0: return None
    x=abs(x)
    return (x & -x).bit_length()-1

values=[1,3]
for i in range(2,8193):
    numerator=3*(2*i-1)*values[-1]-(i-1)*values[-2]
    assert numerator % i == 0
    values.append(numerator//i)

counts=Counter()
failures=[]
def check(group,actual,expected,parameters):
    counts[group]+=1
    if actual!=expected: failures.append([group,parameters,actual,expected])

for m in range(4,8193,4):
    check('basepoint_zero',v2(values[m]-1),3*v2(m),m)
    check('basepoint_minus_one',v2(values[m-1]+1),3*v2(m),m)
for m in range(2048):
    check('conjecture_2',v2(values[4*m+3]+1),3*(v2(m+1)+2),m)
for m in range(2,4097,2):
    check('conjecture_3',v2(values[2*m]-1),3*v2(2*m),m)
for exponent in range(2,12):
    for u in range(1,32,2):
        upper=u*(1 << (exponent+1))
        lower=u*(1 << exponent)
        if upper>8192: continue
        for b in [0,-1]:
            check('exceptional_C4_including_scale_four',v2(values[upper+b]-values[lower+b]),3*exponent,[exponent,u,b])
for n in range(2,257,2):
    for p in range(3,64,2):
        if p*n<=8192:
            check('multiplier_exact',v2(values[p*n]-values[n]),v2(p-1)+3*v2(n),[p,n])
for n in range(2,129,2):
    for m in range(n+2,257,2):
        if v2(m)==v2(n):
            check('two_point_exact',v2(values[m]-values[n]),v2(m-n)+2*v2(n),[m,n])

def dmod(n,bits):
    modulus=1<<bits
    total=coefficient=1
    for k in range(1,bits):
        coefficient=coefficient*(n-k+1)//k
        total=(total+(1<<k)*coefficient*coefficient)%modulus
    return total

for a in [1,2,3,7,16,32,64]:
    for s in [1,2,5,12]:
        for q in [1,3,255]:
            for u in [1,3,127]:
                n=(1<<a)*u
                p=1+(1<<s)*q
                w=s+3*a
                residue=(dmod(p*n,w+1)-dmod(n,w+1)) % (1<<(w+1))
                check('multiplier_large_modular',residue,1<<w,[a,s,q,u])

report={'method':'Exact three-term Delannoy recurrence to index 8192; truncated integer binomial sums for large parameters',
        'checks_by_group':dict(counts),'checks_total':sum(counts.values()),'failures_count':len(failures),
        'failures':failures,'status':'PASS' if not failures else 'FAIL',
        'scope_warning':'Finite corroboration only. Does not regenerate NEG terms, ladders, or tail estimates.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
assert not failures
