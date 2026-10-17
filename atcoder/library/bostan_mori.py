def _mul(f, g, mod):
    # 多項式の積（素朴に O(len(f) len(g))）
    if not f or not g:
        return []
    res = [0] * (len(f) + len(g) - 1)
    for i, x in enumerate(f):
        if x:
            for j, y in enumerate(g):
                res[i + j] = (res[i + j] + x * y) % mod
    return res


def bostan_mori(P, Q, n, mod):
    # 形式的冪級数 P(x) / Q(x) の x^n の係数（Q[0] は mod で逆元を持つ）
    while n:
        R = [q if i % 2 == 0 else -q % mod for i, q in enumerate(Q)]  # Q(-x)
        P = _mul(P, R, mod)[n & 1::2]
        Q = _mul(Q, R, mod)[::2]
        n >>= 1
    return P[0] * pow(Q[0], -1, mod) % mod if P else 0


def linear_recurrence(a, c, n, mod):
    # a[i] = c[0] a[i - 1] + c[1] a[i - 2] + ... + c[d - 1] a[i - d]（i >= d）を満たす数列の第 n 項
    # a は最初の d 項（d = len(c)）
    d = len(c)
    if d == 0:
        return 0
    Q = [1] + [-x % mod for x in c]
    P = _mul(a[:d], Q, mod)[:d]
    return bostan_mori(P, Q, n, mod)


def berlekamp_massey(a, mod):
    # 数列 a を満たす最短の線形漸化式の係数 c（a[i] = c[0] a[i - 1] + ... + c[d - 1] a[i - d]）。mod は素数
    C = [1]  # 今の漸化式 1 - c[0] x - c[1] x^2 - ...
    B = [1]  # 最後に長さが変わる前の漸化式
    L = 0
    m = 1
    b = 1
    for i in range(len(a)):
        d = a[i]  # 今の漸化式で a[i] を予測したときのずれ
        for j in range(1, L + 1):
            d = (d + C[j] * a[i - j]) % mod
        if d == 0:
            m += 1
            continue
        coef = d * pow(b, mod - 2, mod) % mod
        T = C[:]
        if len(C) < len(B) + m:
            C += [0] * (len(B) + m - len(C))
        for j, x in enumerate(B):
            C[j + m] = (C[j + m] - coef * x) % mod
        if 2 * L <= i:
            L = i + 1 - L
            B = T
            b = d
            m = 1
        else:
            m += 1
    return [-x % mod for x in C[1:L + 1]]
