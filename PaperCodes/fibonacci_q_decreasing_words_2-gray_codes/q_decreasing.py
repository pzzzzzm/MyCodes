# generate 2-Gray codes for q-decreasing words and q-run constrained words
# https://doi.org/10.1007/978-981-97-0566-5_8

import math

def qrun(n, q):
    R = []
    p = 1
    for i in range(0, n-(math.floor(1/q)+2)+1):
        if (i+1)%2: j_range = (1, n-i-(math.floor((n - i)/(q + 1))+1)+1, 1)
        else: j_range = (n-i-(math.floor((n-i)/(q+1))+1), 0, -1)

        for j in range(*j_range):
            if p%2:
                R += ["0"*(n-i-j) + "1"*j + s for s in reversed(qrun(i, q))]
            else:
                R += ["0"*(n-i-j) + "1"*j + s for s in qrun(i, q)]
            p = 1 - int(R[-1][-1])
                
    R.append("0"*n)
    return R

def qdecreasing(n, q):
    Q = []
    p = 1
    for r in range(n, -1, -2):
        if p%2: Q += ["1"*r + s for s in reversed(qrun(n-r, q))]
        else: Q += ["1"*r + s for s in qrun(n - r, q)]
        p = 1 - int(Q[-1][-1])
        
    _Q = []
    p = 1
    for r in range(n-1, -1, -2):
        if p%2: _Q += ["1"*r + s for s in reversed(qrun(n-r, q))]
        else: _Q += ["1"*r + s for s in qrun(n - r, q)]
        p = 1 - int(_Q[-1][-1])
        
    return Q + list(reversed(_Q))

print('  =========================================')
print('  1.  q-decreasing words')
print('  2.  q-run constrained words\n')
print('  =========================================')
print(' Enter selection #: ')
this_type = int(input())
print('Enter n:')
this_n = int(input())
print('Enter q:')
this_p = float(input())

if this_type == 1: qr = qdecreasing(this_n, this_p)
else: qr = qrun(this_n, this_p)

for curr in qr: print(curr)
print('total: {}'.format(len(qr)))