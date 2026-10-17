def subset_zeta(f, mod=0):
    # g[S] = (S の部分集合 T すべてについての f[T] の和)
    f = [x % mod for x in f] if mod else list(f)
    n = len(f)
    b = 1
    while b < n:
        for i in range(0, n, 2 * b):
            for j in range(i, i + b):
                f[j + b] += f[j]
        if mod:
            f = [x % mod for x in f]
        b *= 2
    return f


def subset_mobius(g, mod=0):
    # subset_zeta の逆変換
    g = [x % mod for x in g] if mod else list(g)
    n = len(g)
    b = 1
    while b < n:
        for i in range(0, n, 2 * b):
            for j in range(i, i + b):
                g[j + b] -= g[j]
        if mod:
            g = [x % mod for x in g]
        b *= 2
    return g


def superset_zeta(f, mod=0):
    # g[S] = (S を含む集合 T すべてについての f[T] の和)
    f = [x % mod for x in f] if mod else list(f)
    n = len(f)
    b = 1
    while b < n:
        for i in range(0, n, 2 * b):
            for j in range(i, i + b):
                f[j] += f[j + b]
        if mod:
            f = [x % mod for x in f]
        b *= 2
    return f


def superset_mobius(g, mod=0):
    # superset_zeta の逆変換
    g = [x % mod for x in g] if mod else list(g)
    n = len(g)
    b = 1
    while b < n:
        for i in range(0, n, 2 * b):
            for j in range(i, i + b):
                g[j] -= g[j + b]
        if mod:
            g = [x % mod for x in g]
        b *= 2
    return g
