def chromatic_number(n, edges):
    # 頂点 0..n-1、無向辺 edges = [(u, v), ...] のグラフの彩色数（自己ループなし）
    if n == 0:
        return 0
    adj = [0] * n
    for u, v in edges:
        adj[u] |= 1 << v
        adj[v] |= 1 << u
    # ind[S] = S の部分集合のうち独立集合であるものの個数（空集合を含む）
    ind = [1] * (1 << n)
    pc = [0] * (1 << n)
    for S in range(1, 1 << n):
        b = S & -S
        v = b.bit_length() - 1
        # v を使わないものと、v を使う（v とその隣を除いた中から選ぶ）もの
        ind[S] = ind[S ^ b] + ind[S & ~(adj[v] | b)]
        pc[S] = pc[S ^ b] + 1
    # k 色で塗れるのは sum((-1)^(n - |S|) * ind[S]^k) が 0 でないとき
    pos = [ind[S] for S in range(1 << n) if (n - pc[S]) % 2 == 0]
    neg = [ind[S] for S in range(1 << n) if (n - pc[S]) % 2 == 1]
    res = n
    # 2 つの素数を法として計算し、どちらかで 0 でなければ塗れるとする
    for p in (998244353, 1000000007):
        a, b = pos[:], neg[:]
        for k in range(1, res):
            if (sum(a) - sum(b)) % p:
                res = k
                break
            a = [x * y % p for x, y in zip(a, pos)]
            b = [x * y % p for x, y in zip(b, neg)]
    return res
