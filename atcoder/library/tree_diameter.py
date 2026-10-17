def tree_diameter_weighted(g):
    # g[v] = [(to, w), ...]、w は非負
    n = len(g)

    def bfs(s):
        dist = [-1] * n
        par = [-1] * n
        dist[s] = 0
        order = [s]
        for v in order:
            for to, w in g[v]:
                if dist[to] == -1:
                    dist[to] = dist[v] + w
                    par[to] = v
                    order.append(to)
        return dist, par

    dist, _ = bfs(0)
    u = dist.index(max(dist))
    dist, par = bfs(u)
    v = dist.index(max(dist))
    path = [v]
    while path[-1] != u:
        path.append(par[path[-1]])
    return dist[v], path


def tree_diameter(g):
    # g[v] = [to, ...]（重みなし）
    return tree_diameter_weighted([[(to, 1) for to in gv] for gv in g])
