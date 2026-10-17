def kruskal(n, edges):
    # edges = [(u, v, w), ...]（無向）。(重みの和, 使った辺の番号のリスト) を返す
    # 連結でないときは最小全域森になる（len(used) < n - 1）
    par = list(range(n))

    def find(x):
        while par[x] != x:
            par[x] = par[par[x]]
            x = par[x]
        return x

    cost = 0
    used = []
    for i in sorted(range(len(edges)), key=lambda i: edges[i][2]):
        u, v, w = edges[i]
        u, v = find(u), find(v)
        if u != v:
            par[u] = v
            cost += w
            used.append(i)
    return cost, used


def prim(n, cost):
    # 完全グラフ（u と v を結ぶ辺の重みが cost(u, v)）の最小全域木
    # (重みの和, par) を返す。par[v] は木で v とつながる頂点（par[0] = -1）
    dist = [cost(0, v) for v in range(n)]
    par = [0] * n
    par[0] = -1
    used = [False] * n
    used[0] = True
    total = 0
    for _ in range(n - 1):
        u = -1
        for v in range(n):
            if not used[v] and (u == -1 or dist[v] < dist[u]):
                u = v
        used[u] = True
        total += dist[u]
        for v in range(n):
            if not used[v]:
                c = cost(u, v)
                if c < dist[v]:
                    dist[v] = c
                    par[v] = u
    return total, par
