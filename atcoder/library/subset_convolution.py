def subset_convolution(f, g, mod=998244353):
    # h[S] = (T ⊆ S についての f[T] g[S - T] の和)。f と g の長さは同じ 2 べき
    size = len(f)
    n = size.bit_length() - 1
    pc = [0] * size  # pc[S] = S の要素数
    for s in range(1, size):
        pc[s] = pc[s >> 1] + (s & 1)
    # F[i][S] = (S の部分集合 T で要素数が i のものについての f[T] の和)。G も同じ
    F = [[0] * size for _ in range(n + 1)]
    G = [[0] * size for _ in range(n + 1)]
    for s in range(size):
        F[pc[s]][s] = f[s] % mod
        G[pc[s]][s] = g[s] % mod
    for A in F + G:
        w = 1
        while w < size:
            for i in range(0, size, 2 * w):
                for j in range(i, i + w):
                    A[j + w] += A[j]
            w *= 2
        for s in range(size):
            A[s] %= mod
    # S ごとに要素数についての畳み込みをして F に上書きする
    # （あとで使うのは要素数 k が S の要素数 c 以上のところだけで、k > 2c なら 0 のまま）
    for s in range(size):
        c = pc[s]
        a = [F[i][s] for i in range(c + 1)]
        b = [G[i][s] for i in range(c + 1)]
        for k in range(c, min(2 * c, n) + 1):
            t = 0
            for i in range(k - c, c + 1):
                t = (t + a[i] * b[k - i]) % mod
            F[k][s] = t
    for A in F:
        w = 1
        while w < size:
            for i in range(0, size, 2 * w):
                for j in range(i, i + w):
                    A[j + w] -= A[j]
            w *= 2
    return [F[pc[s]][s] % mod for s in range(size)]
