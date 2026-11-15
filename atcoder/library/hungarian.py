def hungarian(A):
    # N×M のコスト行列 A（N <= M、負でもよい）で、各行に違う列を 1 つずつ割り当てるときの
    # (コストの和の最小値, p) を返す。行 i には列 p[i] を割り当てる
    n = len(A)
    m = len(A[0]) if n else 0
    INF = float("inf")
    u = [0] * n  # 行のポテンシャル
    v = [0] * m  # 列のポテンシャル
    row = [-1] * m  # row[j] = 列 j に割り当てた行（-1 は空き）
    for i in range(n):
        # 行 i を加える。被約費用 A[r][j] - u[r] - v[j] を辺の重みにして、
        # 行 i から空いている列までの最短路を Dijkstra 法で求める
        Ai = A[i]
        d = [Ai[j] - v[j] for j in range(m)]  # 行 i から列 j までの距離
        way = [-1] * m  # 最短路で列 j の 1 つ前の列（-1 なら行 i から直接）
        done = [False] * m
        used = []  # 距離が確定した列
        j = 0
        for k in range(1, m):
            if d[k] < d[j]:
                j = k
        while row[j] != -1:
            done[j] = True
            used.append(j)
            r = row[j]
            Ar = A[r]
            base = d[j] - u[r]
            best = INF
            nj = -1
            for k in range(m):
                if not done[k]:
                    x = base + Ar[k] - v[k]
                    if x < d[k]:
                        d[k] = x
                        way[k] = j
                    else:
                        x = d[k]
                    if x < best:
                        best = x
                        nj = k
            j = nj
        # ポテンシャルを更新して、最短路に沿って割り当てを付け替える
        D = d[j]
        u[i] += D
        for k in used:
            t = D - d[k]
            v[k] -= t
            u[row[k]] += t
        while way[j] != -1:
            k = way[j]
            row[j] = row[k]
            j = k
        row[j] = i
    p = [0] * n
    for j in range(m):
        if row[j] != -1:
            p[row[j]] = j
    return sum(A[i][p[i]] for i in range(n)), p
