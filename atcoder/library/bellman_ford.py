INF = 1 << 60


def bellman_ford(n, edges, s):
    # edges = [(u, v, w), ...]（有向）
    # 到達できない頂点は INF、負閉路を通っていくらでも小さくできる頂点は -INF
    dist = [INF] * n
    dist[s] = 0
    for _ in range(n - 1):
        updated = False
        for u, v, w in edges:
            if dist[u] != INF and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                updated = True
        if not updated:
            return dist
    for _ in range(n):
        for u, v, w in edges:
            if dist[u] != INF and dist[u] + w < dist[v]:
                dist[v] = -INF
    return dist
