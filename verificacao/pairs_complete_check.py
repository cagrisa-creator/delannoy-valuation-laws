"""Exploratory exact check; no submitted manuscript is modified."""
from pathlib import Path
from collections import Counter
import json

def v2(x):
    x=abs(x)
    return None if x==0 else (x & -x).bit_length()-1

limit=1024
D=[1,3]
for n in range(2,limit+1):
    numerator=3*(2*n-1)*D[-1]-(n-1)*D[-2]
    assert numerator % n == 0
    D.append(numerator//n)

counts=Counter()
failures=[]
for m in range(limit+1):
    for n in range(m):
        k=v2(m-n)
        if k <= 1:
            expected=k+1
            case=f'k={k}'
        else:
            tm=v2(m*(m+1))
            tn=v2(n*(n+1))
            a=min(t for t in (tm,tn) if t is not None)
            expected=k+2*a
            case='k>=2'
        actual=v2(D[m]-D[n])
        counts[case]+=1
        if expected!=actual:
            failures.append({'m':m,'n':n,'expected':expected,'actual':actual})
            if len(failures)>=20: break
    if len(failures)>=20: break

report={'limit':limit,'pairs':sum(counts.values()),'cases':dict(counts),'failures':failures,
'formula':'k=v2(M-N), t_X=v2(X(X+1)), t_0=infinity; v2(D(M)-D(N))=k+1 for k<=1, otherwise k+2 min(t_M,t_N)',
'status':'Computational corroboration. A deduction from existing manuscript results is provided separately.'}
out=Path(__file__).with_suffix('.json')
out.write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report))
