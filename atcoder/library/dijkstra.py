from heapq import heappush, heappop


def dijkstra(g, s):
    # g[v] = [(to, cost), ...]、cost は非負整数
    n = len(g)
    INF = 1 << 62
    dist = [INF] * n
    prev = [-1] * n
    dist[s] = 0
    hq = [s]
    while hq:
        dv = heappop(hq)
        d, v = divmod(dv, n)
        if d > dist[v]:
            continue
        for to, c in g[v]:
            nd = d + c
            if nd < dist[to]:
                dist[to] = nd
                prev[to] = v
                heappush(hq, nd * n + to)
    return dist, prev


def restore_path(prev, t):
    path = []
    while t != -1:
        path.append(t)
        t = prev[t]
    return path[::-1]
