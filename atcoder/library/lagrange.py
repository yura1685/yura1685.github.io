def lagrange(xs, ys, x, mod):
    # 点 (xs[i], ys[i]) をすべて通る len(xs) - 1 次以下の多項式 f について f(x) を mod で求める
    # xs は mod で互いに異なり、mod は素数
    n = len(xs)
    res = 0
    for i in range(n):
        num = 1
        den = 1
        for j in range(n):
            if i == j:
                continue
            num = num * (x - xs[j]) % mod
            den = den * (xs[i] - xs[j]) % mod
        res += ys[i] * num * pow(den, mod - 2, mod)
    return res % mod


def lagrange_iota(ys, x, mod):
    # xs = 0, 1, ..., d のとき（ys[i] = f(i)）。mod は d より大きい素数
    d = len(ys) - 1
    x %= mod
    if x <= d:
        return ys[x] % mod
    pre = [1] * (d + 2)  # pre[i] = (x - 0)(x - 1)...(x - (i - 1))
    for i in range(d + 1):
        pre[i + 1] = pre[i] * (x - i) % mod
    suf = [1] * (d + 2)  # suf[i] = (x - i)(x - (i + 1))...(x - d)
    for i in range(d, -1, -1):
        suf[i] = suf[i + 1] * (x - i) % mod
    fact = [1] * (d + 1)
    for i in range(1, d + 1):
        fact[i] = fact[i - 1] * i % mod
    inv_fact = [1] * (d + 1)
    inv_fact[d] = pow(fact[d], mod - 2, mod)
    for i in range(d, 0, -1):
        inv_fact[i - 1] = inv_fact[i] * i % mod
    res = 0
    for i in range(d + 1):
        t = ys[i] * pre[i] % mod * suf[i + 1] % mod * inv_fact[i] % mod * inv_fact[d - i] % mod
        res += -t if (d - i) & 1 else t
    return res % mod
