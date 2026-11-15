def _det_mod(M, mod):
    # 正方行列 M の行列式 mod（mod は素数、M の成分は 0 以上 mod 未満。M を書き換える）
    n = len(M)
    det = 1
    for c in range(n):
        piv = -1
        for i in range(c, n):
            if M[i][c]:
                piv = i
                break
        if piv == -1:
            return 0
        if piv != c:
            M[c], M[piv] = M[piv], M[c]
            det = -det
        row = M[c]
        det = det * row[c] % mod
        inv = pow(row[c], mod - 2, mod)
        for i in range(c + 1, n):
            Mi = M[i]
            if Mi[c]:
                f = Mi[c] * inv % mod
                for k in range(c, n):
                    Mi[k] = (Mi[k] - f * row[k]) % mod
    return det % mod


def count_spanning_trees(n, edges, mod):
    # 頂点 0..n-1（n >= 1）、無向辺 edges = [(u, v), ...] のグラフの全域木の個数 mod（mod は素数）
    # 自己ループは無視し、多重辺は別々の辺として数える
    L = [[0] * n for _ in range(n)]
    for u, v in edges:
        if u != v:
            L[u][u] += 1
            L[v][v] += 1
            L[u][v] -= 1
            L[v][u] -= 1
    # ラプラシアン行列から頂点 0 の行と列を除いた行列の行列式
    return _det_mod([[x % mod for x in L[i][1:]] for i in range(1, n)], mod)


def count_arborescences(n, edges, root, mod):
    # 頂点 0..n-1、有向辺 edges = [(u, v), ...]（u から v への辺）のグラフで、
    # root から外向きの全域木（すべての辺が根から離れる向き）の個数 mod（mod は素数）
    L = [[0] * n for _ in range(n)]
    for u, v in edges:
        if u != v:
            L[v][v] += 1  # v に入る辺の本数
            L[u][v] -= 1
    # root の行と列を除いた行列の行列式
    idx = [i for i in range(n) if i != root]
    return _det_mod([[L[i][j] % mod for j in idx] for i in idx], mod)
