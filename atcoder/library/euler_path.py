def euler_path_directed(n, edges, s=None):
    # 有向グラフ edges = [(u, v), ...] のすべての辺を 1 回ずつ通る路を (頂点の列, 辺の番号の列) で返す
    # 始点 s を指定しなければ自動で選ぶ。存在しなければ None
    g = [[] for _ in range(n)]
    deg = [0] * n  # 出次数 - 入次数
    for i, (u, v) in enumerate(edges):
        g[u].append((v, i))
        deg[u] += 1
        deg[v] -= 1
    plus = [v for v in range(n) if deg[v] > 0]
    minus = [v for v in range(n) if deg[v] < 0]
    if plus or minus:
        if len(plus) != 1 or len(minus) != 1 or deg[plus[0]] != 1 or deg[minus[0]] != -1:
            return None
        if s is None:
            s = plus[0]
        elif s != plus[0]:
            return None
    elif s is None:
        s = next((v for v in range(n) if g[v]), 0)
    it = [0] * n
    vs, es = [], []
    stack = [(s, -1)]
    while stack:
        v, e = stack[-1]
        if it[v] < len(g[v]):
            to, i = g[v][it[v]]
            it[v] += 1
            stack.append((to, i))
        else:
            stack.pop()
            vs.append(v)
            es.append(e)
    if len(vs) != len(edges) + 1:
        return None
    return vs[::-1], es[-2::-1]


def euler_path_undirected(n, edges, s=None):
    # 無向グラフ版。返り値は euler_path_directed と同じ
    g = [[] for _ in range(n)]
    deg = [0] * n
    for i, (u, v) in enumerate(edges):
        g[u].append((v, i))
        g[v].append((u, i))
        deg[u] += 1
        deg[v] += 1
    odd = [v for v in range(n) if deg[v] % 2]
    if len(odd) > 2:
        return None
    if s is None:
        s = odd[0] if odd else next((v for v in range(n) if g[v]), 0)
    elif odd and deg[s] % 2 == 0:
        return None
    used = [False] * len(edges)
    it = [0] * n
    vs, es = [], []
    stack = [(s, -1)]
    while stack:
        v, e = stack[-1]
        while it[v] < len(g[v]) and used[g[v][it[v]][1]]:
            it[v] += 1
        if it[v] < len(g[v]):
            to, i = g[v][it[v]]
            it[v] += 1
            used[i] = True
            stack.append((to, i))
        else:
            stack.pop()
            vs.append(v)
            es.append(e)
    if len(vs) != len(edges) + 1:
        return None
    return vs[::-1], es[-2::-1]
