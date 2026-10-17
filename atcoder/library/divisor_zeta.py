def _primes(n):
    # n 以下の素数のリスト
    s = [True] * (n + 1)
    res = []
    for i in range(2, n + 1):
        if s[i]:
            res.append(i)
            for j in range(i * i, n + 1, i):
                s[j] = False
    return res


def divisor_zeta(f, mod=0):
    # g[n] = (n の約数 d すべてについての f[d] の和)。添字は 1 から N（f[0] は使わない）
    f = [x % mod for x in f] if mod else list(f)
    n = len(f) - 1
    for p in _primes(n):
        for i in range(1, n // p + 1):
            f[i * p] += f[i]
    return [x % mod for x in f] if mod else f


def divisor_mobius(g, mod=0):
    # divisor_zeta の逆変換
    g = [x % mod for x in g] if mod else list(g)
    n = len(g) - 1
    for p in _primes(n):
        for i in range(n // p, 0, -1):
            g[i * p] -= g[i]
    return [x % mod for x in g] if mod else g


def multiple_zeta(f, mod=0):
    # g[n] = (N 以下の n の倍数 m すべてについての f[m] の和)。添字は 1 から N（f[0] は使わない）
    f = [x % mod for x in f] if mod else list(f)
    n = len(f) - 1
    for p in _primes(n):
        for i in range(n // p, 0, -1):
            f[i] += f[i * p]
    return [x % mod for x in f] if mod else f


def multiple_mobius(g, mod=0):
    # multiple_zeta の逆変換
    g = [x % mod for x in g] if mod else list(g)
    n = len(g) - 1
    for p in _primes(n):
        for i in range(1, n // p + 1):
            g[i] -= g[i * p]
    return [x % mod for x in g] if mod else g
