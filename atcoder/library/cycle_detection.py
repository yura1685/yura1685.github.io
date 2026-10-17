def cycle_directed(g):
    # 有向グラフ g[v] = [to, ...] の閉路を 1 つ、頂点のリスト [v0, v1, ..., vk-1] で返す
    # （v0 -> v1 -> ... -> vk-1 -> v0）。閉路がなければ None
    n = len(g)
    state = [0] * n  # 0: 未訪問, 1: 探索中, 2: 探索済み
    it = [0] * n
    for s in range(n):
        if state[s]:
            continue
        state[s] = 1
        stack = [s]  # 根から今の頂点までのパス
        while stack:
            v = stack[-1]
            if it[v] < len(g[v]):
                to = g[v][it[v]]
                it[v] += 1
                if state[to] == 0:
                    state[to] = 1
                    stack.append(to)
                elif state[to] == 1:
                    return stack[stack.index(to):]
            else:
                state[v] = 2
                stack.pop()
    return None


def cycle_undirected(n, edges):
    # 無向グラフ edges = [(u, v), ...] の閉路を 1 つ、頂点のリストで返す。閉路がなければ None
    # 多重辺は長さ 2 の閉路、自己ループは長さ 1 の閉路とみなす
    g = [[] for _ in range(n)]
    for i, (u, v) in enumerate(edges):
        g[u].append((v, i))
        g[v].append((u, i))
    state = [0] * n
    pe = [-1] * n  # 親から来た辺の番号
    it = [0] * n
    for s in range(n):
        if state[s]:
            continue
        state[s] = 1
        stack = [s]
        while stack:
            v = stack[-1]
            if it[v] < len(g[v]):
                to, i = g[v][it[v]]
                it[v] += 1
                if i == pe[v]:
                    continue
                if state[to] == 0:
                    state[to] = 1
                    pe[to] = i
                    stack.append(to)
                elif state[to] == 1:
                    return stack[stack.index(to):]
            else:
                state[v] = 2
                stack.pop()
    return None
