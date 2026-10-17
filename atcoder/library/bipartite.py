def bipartite(g):
    # 二部グラフなら各頂点の色（0 か 1）のリスト、そうでなければ None
    n = len(g)
    color = [-1] * n
    for s in range(n):
        if color[s] != -1:
            continue
        color[s] = 0
        q = [s]
        for v in q:
            for to in g[v]:
                if color[to] == -1:
                    color[to] = color[v] ^ 1
                    q.append(to)
                elif color[to] == color[v]:
                    return None
    return color
