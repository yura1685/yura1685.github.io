INF = 1 << 60


def warshall_floyd(n, edges):
    # edges = [(u, v, w), ...]（有向）
    d = [[INF] * n for _ in range(n)]
    for i in range(n):
        d[i][i] = 0
    for u, v, w in edges:
        if w < d[u][v]:
            d[u][v] = w
    for k in range(n):
        dk = d[k]
        for i in range(n):
            di = d[i]
            dik = di[k]
            if dik == INF:
                continue
            for j in range(n):
                if dk[j] != INF and dik + dk[j] < di[j]:
                    di[j] = dik + dk[j]
    return d


def add_edge(d, u, v, w):
    # warshall_floyd の結果 d に有向辺 (u, v, w) を加えたときの更新（負閉路ができないとき）
    # 無向辺なら add_edge(d, u, v, w) と add_edge(d, v, u, w) の両方を呼ぶ
    if w >= d[u][v]:
        return
    n = len(d)
    dv = d[v]
    for i in range(n):
        di = d[i]
        diu = di[u]
        if diu == INF:
            continue
        x = diu + w
        for j in range(n):
            if dv[j] != INF and x + dv[j] < di[j]:
                di[j] = x + dv[j]
