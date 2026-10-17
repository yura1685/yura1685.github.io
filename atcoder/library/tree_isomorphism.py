def subtree_ids(g, root=0, table=None):
    # 各頂点を根とする部分木の形に番号を振ったリスト（根付き木として同型なら同じ番号）
    # いくつかの木の番号を比べるときは、同じ辞書 table を渡す
    if table is None:
        table = {}
    n = len(g)
    par = [-1] * n
    order = [root]
    for v in order:
        for to in g[v]:
            if to != par[v]:
                par[to] = v
                order.append(to)
    ch = [[] for _ in range(n)]
    res = [0] * n
    for v in reversed(order):
        key = tuple(sorted(ch[v]))
        if key not in table:
            table[key] = len(table)
        res[v] = table[key]
        if v != root:
            ch[par[v]].append(res[v])
    return res


def centroids(g):
    # 木の重心（1 個か 2 個）のリスト
    n = len(g)
    par = [-1] * n
    order = [0]
    for v in order:
        for to in g[v]:
            if to != par[v]:
                par[to] = v
                order.append(to)
    size = [1] * n
    for v in reversed(order[1:]):
        size[par[v]] += size[v]
    res = []
    for v in range(n):
        mx = n - size[v]
        for to in g[v]:
            if to != par[v]:
                mx = max(mx, size[to])
        if 2 * mx <= n:
            res.append(v)
    return res


def isomorphic(g1, g2):
    # 根のない木 g1, g2 が同型か
    if len(g1) != len(g2):
        return False
    c1, c2 = centroids(g1), centroids(g2)
    if len(c1) != len(c2):
        return False
    table = {}
    x = subtree_ids(g1, c1[0], table)[c1[0]]
    return any(subtree_ids(g2, c, table)[c] == x for c in c2)
