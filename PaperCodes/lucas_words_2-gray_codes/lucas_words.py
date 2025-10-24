# generate 2-Gray codes for Lucas words, Fibonacci words, and Fibonacci words that start with a 0
# https://doi.org/10.4230/LIPIcs.CPM.2025.22

fib_run_dp_table = {}

def construct_fib_run_table(n, p):

    for m in range(1, n+1):
        R = []
        j = 1

        for i in range(0, m-1):
            j = 1 if i == 2 else j

            for k in range(*(1, min(p-1, m-i-1)+1, 1) if (i+1)%2 else (min(p-1, m-i-1), 0, -1)):
                R += [(m-i-k, k, j%2, i)]
                j = 1 - j

        R += [(m, 0, 0, 0)]
        fib_run_dp_table[m] = R


def fib_run_dp(n, j=0, prev=None, tail=None):

    if n == 0:
        yield prev if not tail else prev + tail
        return

    prev = [] if prev is None else prev

    for (r1, r2, r3, r4) in reversed(fib_run_dp_table[n]) if j else fib_run_dp_table[n]:
        yield from fib_run_dp(r4, (j+r3)%2, prev + [0]*r1 + [1]*r2, tail)


def fib_run(n, p):
    construct_fib_run_table(n, p)
    yield from fib_run_dp(n)


def fib_string(n, p):
    construct_fib_run_table(n, p)

    j = 0
    for r in range(p-1, -1, -2):
        yield from fib_run_dp(n-r, j, [1]*r)
        j = 1 - j

    # calculate the direction of the last Z
    j = ((p + 1) // 2) % 2
    for r in reversed(range(p-2, -1, -2)):
        yield from fib_run_dp(n-r, j, [1]*r)
        j = 1 - j


def lucas_string(n, p):

    if p > n: p = n
    construct_fib_run_table(n, p)

    yield from fib_run_dp(n, 1) if p > 2 else fib_run_dp(n, 0)

    # left side
    j = 0
    for t in range(1, p-1):  # t = s - r: len of 1s in the front
        for s in reversed(range(t+1, p)) if j else range(t+1, p):
            yield from fib_run_dp(n-s-1, j, [1]*t, [0]+[1]*(s-t))
        j = 1 - j

    # right side
    if p == 2:
        yield from fib_run_dp(n-2, 0, [1], [0])
    elif p == 3:
        yield from fib_run_dp(n-3, 1, [1]*2, [0])
        yield from fib_run_dp(n-2, 0, [1], [0])
    elif p > 3:
        # M^n_{p, s, r} -> fRun(n-s-1, j, 1^s-r, 01^r)
        yield from fib_run_dp(n-p+1, 1-j, [1]*(p-2), [0])
        yield from fib_run_dp(n-p, 0, [1]*(p-1), [0])
        for s in range(p-3, 0, -1):
            yield from fib_run_dp(n-s-1, 1, [1]*s, [0])


if __name__ == '__main__':
    print("================================================")
    print("1. Fibonacci words that start with a 0")
    print("2. Fibonacci words")
    print("3. Lucas words")
    print("================================================")
    print("Enter selection #: ")

    this_type = [fib_run, fib_string, lucas_string][int(input())-1]

    print("Enter n: ")
    this_n = int(input())
    print("Enter p: ")
    this_p = int(input())

    cnt = 0
    for perm in this_type(this_n, this_p):
        cnt += 1
        print(*perm)

    print("Total: " + str(cnt))