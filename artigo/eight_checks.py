"""Four exact derivative residues and four exact transition residues."""
from math import comb
import json
from pathlib import Path

def D(n):
    return sum((1 << k)*comb(n,k)**2 for k in range(n+1))

derivatives = []
for t, bases in ((1,(1,2)), (2,(3,4))):
    H, M = 1 << (2*t), 1 << (2*t+1)
    for b in bases:
        numerator = D(b+2*H)-D(b+H)
        assert numerator % H == 0
        residue = (numerator//H) % M
        assert residue == 1 << (2*t)
        derivatives.append(dict(t=t,b=b,H=H,modulus=M,residue=residue))

transitions = []
for n in (2,3):
    for b in (3,4):
        modulus = 1 << (n+5)
        residue = (D(b+(2<<n))-D(b+(1<<n))) % modulus
        assert residue == 1 << (n+4)
        transitions.append(dict(t=2,n=n,b=b,u=1,modulus=modulus,residue=residue))

report = dict(derivative_checks=derivatives, transition_checks=transitions,
              exact_checks=8, failures=0, maximum_D_argument=36)
Path(__file__).with_name('eight_checks.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
