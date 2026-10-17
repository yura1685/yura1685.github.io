def bipartite_matching(n, m, edges):
    # 左 n 頂点・右 m 頂点の二部グラフ、edges = [(u, v), ...]（0 <= u < n, 0 <= v < m）
    # 最大マッチングの辺 (u, v) のリストを u の昇順で返す
    g = [[] for _ in range(n)]
    for u, v in edges:
        g[u].append(v)
    ml = [-1] * n  # ml[u] = 左の u とマッチしている右の頂点
    mr = [-1] * m  # mr[v] = 右の v とマッチしている左の頂点
    while True:
        dist = [-1] * n
        q = [u for u in range(n) if ml[u] == -1]
        for u in q:
            dist[u] = 0
        found = False
        for u in q:
            for v in g[u]:
                w = mr[v]
                if w == -1:
                    found = True
                elif dist[w] == -1:
                    dist[w] = dist[u] + 1
                    q.append(w)
        if not found:
            break
        it = [0] * n
        for s in range(n):
            if ml[s] != -1:
                continue
            st = [s]
            while st:
                u = st[-1]
                if it[u] == len(g[u]):
                    dist[u] = -1
                    st.pop()
                    continue
                v = g[u][it[u]]
                it[u] += 1
                w = mr[v]
                if w == -1:
                    for x in st:
                        y = g[x][it[x] - 1]
                        ml[x] = y
                        mr[y] = x
                    break
                if dist[w] == dist[u] + 1:
                    st.append(w)
    return [(u, ml[u]) for u in range(n) if ml[u] != -1]
