from heapq import heapify, heappush, heappop


def topological_sort(g):
    # 閉路があれば None
    n = len(g)
    indeg = [0] * n
    for v in range(n):
        for to in g[v]:
            indeg[to] += 1
    order = [v for v in range(n) if indeg[v] == 0]
    for v in order:
        for to in g[v]:
            indeg[to] -= 1
            if indeg[to] == 0:
                order.append(to)
    return order if len(order) == n else None


def topological_sort_lex(g):
    # 辞書順最小のトポロジカル順序。閉路があれば None
    n = len(g)
    indeg = [0] * n
    for v in range(n):
        for to in g[v]:
            indeg[to] += 1
    hq = [v for v in range(n) if indeg[v] == 0]
    heapify(hq)
    order = []
    while hq:
        v = heappop(hq)
        order.append(v)
        for to in g[v]:
            indeg[to] -= 1
            if indeg[to] == 0:
                heappush(hq, to)
    return order if len(order) == n else None
