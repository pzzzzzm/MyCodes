# 2-Gray codes for k-ary/mixed-radix words

def k_ary(k_list, alpha):

    n = len(k_list)
    d = [1 if a != 1 else -1 for a in alpha]
    idx = []
    s = [sum(alpha)]

    order = [i for i in range(n)]
    for i in range(n-1, -1, -1):
        if k_list[i] > 1:
            order[n-1], order[i] = i, n-1
            break

    def _next(i):
        i_ = order[i]

        for r in range(k_list[i_] + 1):

            if i == n-1:
                if s[0] != 0:
                    if len(idx) > 1 and idx[0] == idx[1]:
                        idx.pop()
                    yield alpha, idx
                    idx[:] = []
            else:
                i_next = order[i + 1]
                yield from _next(i + 1)
                d[i_next] = 1 if alpha[i_next] == k_list[i_next] else -d[i_next]

            if r < k_list[i_]:
                a_b = alpha[i_]
                a_a = (alpha[i_] + d[i_] + k_list[i_] + 1) % (k_list[i_] + 1)
                s[0] += a_a - a_b
                alpha[i_] = a_a
                idx.append(i_)

    yield from _next(0)
