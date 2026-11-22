MOD = 998244353
_INV = [0, 1]  # _INV[i] = i の逆元（必要な分だけ伸ばす）

def _rates():
    # NTT の回転因子の表（原始根 3、MOD - 1 = 2^23 * 119）
    es, ies = [0] * 30, [0] * 30
    e = pow(3, (MOD - 1) >> 23, MOD)  # 1 の原始 2^23 乗根
    ie = pow(e, MOD - 2, MOD)
    for i in range(23, 1, -1):
        es[i - 2], ies[i - 2] = e, ie
        e, ie = e * e % MOD, ie * ie % MOD
    se, sie = [0] * 30, [0] * 30
    now = inow = 1
    for i in range(21):
        se[i] = es[i] * now % MOD
        now = now * ies[i] % MOD
        sie[i] = ies[i] * inow % MOD
        inow = inow * es[i] % MOD
    return se, sie

_SUM_E, _SUM_IE = _rates()

def _butterfly(a):
    # NTT（長さは 2 べき。結果はビットを逆にした順に並ぶ）
    mod = MOD
    h = len(a).bit_length() - 1
    for ph in range(1, h + 1):
        p = 1 << (h - ph)
        now = 1
        for s in range(1 << (ph - 1)):
            off = s << (h - ph + 1)
            for i in range(off, off + p):
                l = a[i]
                r = a[i + p] * now % mod
                a[i] = (l + r) % mod
                a[i + p] = (l - r) % mod
            now = now * _SUM_E[(~s & (s + 1)).bit_length() - 1] % mod

def _butterfly_inv(a):
    # _butterfly の逆変換（長さ倍されたまま）
    mod = MOD
    h = len(a).bit_length() - 1
    for ph in range(h, 0, -1):
        p = 1 << (h - ph)
        inow = 1
        for s in range(1 << (ph - 1)):
            off = s << (h - ph + 1)
            for i in range(off, off + p):
                l = a[i]
                r = a[i + p]
                a[i] = (l + r) % mod
                a[i + p] = (l - r) * inow % mod
            inow = inow * _SUM_IE[(~s & (s + 1)).bit_length() - 1] % mod

def _convolution(a, b):
    # a と b の畳み込み（mod 998244353）。短い方が 40 以下なら素朴に掛ける
    n, m = len(a), len(b)
    if n == 0 or m == 0:
        return []
    if min(n, m) <= 40:
        if n < m:
            a, b, n, m = b, a, m, n
        res = [0] * (n + m - 1)
        for j in range(m):
            y = b[j]
            for i in range(n):
                res[i + j] = (res[i + j] + a[i] * y) % MOD
        return res
    z = 1 << (n + m - 2).bit_length()
    a = [x % MOD for x in a] + [0] * (z - n)
    b = [x % MOD for x in b] + [0] * (z - m)
    _butterfly(a)
    _butterfly(b)
    a = [x * y % MOD for x, y in zip(a, b)]
    _butterfly_inv(a)
    iz = pow(z, MOD - 2, MOD)
    return [a[i] * iz % MOD for i in range(n + m - 1)]

def fps_diff(f):
    # 微分 f'
    return [f[i] * i % MOD for i in range(1, len(f))]

def fps_integral(f):
    # 積分（定数項は 0）
    while len(_INV) <= len(f):
        i = len(_INV)
        _INV.append(-(MOD // i) * _INV[MOD % i] % MOD)
    return [0] + [f[i] * _INV[i + 1] % MOD for i in range(len(f))]

def fps_inv(f, n):
    # 1 / f の最初の n 項（f[0] は 0 でない）
    g = [pow(f[0], MOD - 2, MOD)]
    m = 1
    while m < n:
        m2 = min(2 * m, n)
        # f g は m 次未満が 1, 0, 0, ... なので、m 次から m2 - 1 次だけを使って g を直す
        h = _convolution(f[:m2], g)[m:m2]
        h = _convolution(g[:m2 - m], h)[:m2 - m]
        g += [-x % MOD for x in h] + [0] * (m2 - m - len(h))
        m = m2
    return g[:n]

def fps_log(f, n):
    # log f の最初の n 項（f[0] = 1）
    if n <= 1:
        return [0] * n
    g = _convolution(fps_diff(f[:n]), fps_inv(f, n - 1))[:n - 1]
    return fps_integral(g + [0] * (n - 1 - len(g)))

def fps_exp(f, n):
    # exp f の最初の n 項（f[0] = 0）
    f = list(f[:n]) + [0] * (n - len(f))
    g = [1]
    m = 1
    while m < n:
        m2 = min(2 * m, n)
        # g (1 + f - log g)。f - log g は m 次未満が 0 なので、m 次以上の項だけ掛ける
        h = fps_log(g, m2)
        h = [(f[i] - h[i]) % MOD for i in range(m, m2)]
        h = _convolution(g[:m2 - m], h)[:m2 - m]
        g += h + [0] * (m2 - m - len(h))
        m = m2
    return g[:n]

def fps_pow(f, k, n):
    # f^k の最初の n 項（k >= 0。k = 0 なら 1）
    if k == 0:
        return [1] + [0] * (n - 1) if n > 0 else []
    d = 0  # f の 0 でない最初の項の次数
    while d < len(f) and d < n and f[d] % MOD == 0:
        d += 1
    if d == len(f) or d * k >= n:
        return [0] * n
    # f = c x^d g（g[0] = 1）として、f^k = c^k x^(dk) exp(k log g)
    m = n - d * k
    c = f[d] % MOD
    ic = pow(c, MOD - 2, MOD)
    g = fps_log([x * ic % MOD for x in f[d:d + m]], m)
    g = fps_exp([x * (k % MOD) % MOD for x in g], m)
    ck = pow(c, k, MOD)
    return [0] * (d * k) + [x * ck % MOD for x in g]

def fps_sqrt(f, n):
    # f[0] = 1 のとき、定数項が 1 の f^(1/2) の最初の n 項
    return fps_exp([x * ((MOD + 1) // 2) % MOD for x in fps_log(f, n)], n)
