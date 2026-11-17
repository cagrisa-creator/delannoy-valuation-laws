from pathlib import Path
import json

def v2(n):
    return (abs(n)&-abs(n)).bit_length()-1 if n else 10**9

limit=3000
d=[1,3]
for k in range(1,limit):
    numer=3*(2*k+1)*d[k]-k*d[k-1]
    assert numer%(k+1)==0
    d.append(numer//(k+1))
checked=0
failures=[]
checks_by_n={}
for b in range(-1000,1001):
    t=v2(b*(b+1))
    for u in range(1,32,2):
        for n in range(10):
            lo=b+u*2**n
            hi=b+u*2**(n+1)
            if not(0<=lo<hi<=limit):
                continue
            observed=v2(d[hi]-d[lo])
            expected=1 if n==0 else 2 if n==1 else n+2*min(n,t)
            checked+=1
            checks_by_n[n]=checks_by_n.get(n,0)+1
            if expected!=observed:
                failures.append([b,u,n,t,expected,observed])

examples=[]
for b,u,n in [(16,1,2),(32,1,3),(-17,3,2),(1,1,1),(1,1,2),(0,1,2)]:
    lo=b+u*2**n
    hi=b+u*2**(n+1)
    if 0<=lo<hi<=limit:
        examples.append({'b':b,'u':u,'n':n,'t':None if b in(0,-1) else v2(b*(b+1)),
                         'lo':lo,'hi':hi,'observed_v2':v2(d[hi]-d[lo]),
                         'old_linear_prediction':None if b in(0,-1) else n+2*v2(b*(b+1))})
result={'test':'exact-integer check of strengthened saturated formula',
        'number_of_cases':checked,'cases_by_n':checks_by_n,'failures':failures,
        'examples':examples,'status':'finite confirmation; general proof follows from submitted basepoint theorem and main theorem'}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))
