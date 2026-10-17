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
