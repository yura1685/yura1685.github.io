def _lowlink(n, edges):
    # DFS の訪問順 ord、lowlink、DFS 木の親 par、行きがけ順 order（再帰なし、多重辺可）
    g = [[] for _ in range(n)]
    for i, (u, v) in enumerate(edges):
        g[u].append((v, i))
        g[v].append((u, i))
    ord_ = [-1] * n
    low = [0] * n
    par = [-1] * n
    par_edge = [-1] * n
    it = [0] * n
    order = []
    for root in range(n):
        if ord_[root] != -1:
            continue
        ord_[root] = low[root] = len(order)
        order.append(root)
        st = [root]
        while st:
            v = st[-1]
            if it[v] < len(g[v]):
                to, ei = g[v][it[v]]
                it[v] += 1
                if ei == par_edge[v]:
                    continue
                if ord_[to] == -1:
                    ord_[to] = low[to] = len(order)
                    order.append(to)
                    par[to] = v
                    par_edge[to] = ei
                    st.append(to)
                elif ord_[to] < low[v]:
                    low[v] = ord_[to]
            else:
                st.pop()
                p = par[v]
                if p != -1 and low[v] < low[p]:
                    low[p] = low[v]
    return ord_, low, par, order


def two_edge_connected_components(n, edges):
    # 橋を取り除いたときの連結成分（二重辺連結成分）。(成分の個数, 各頂点の成分番号) を返す
    ord_, low, par, order = _lowlink(n, edges)
    comp = [-1] * n
    k = 0
    for v in order:
        p = par[v]
        if p != -1 and low[v] <= ord_[p]:  # 辺 (p, v) は橋でないので同じ成分
            comp[v] = comp[p]
        else:
            comp[v] = k
            k += 1
    return k, comp


def block_cut_tree(n, edges):
    # 二重頂点連結成分（ブロック）のリストと、Block-Cut Tree の隣接リストを返す
    # 木の頂点 0..n-1 は元の頂点、n + i は i 番目のブロックで、頂点とそれを含むブロックを辺で結ぶ
    ord_, low, par, order = _lowlink(n, edges)
    blocks = []
    eb = [-1] * n  # DFS 木の辺 (par[v], v) が入るブロック
    has_child = [False] * n
    for v in order:
        p = par[v]
        if p == -1:
            continue
        has_child[p] = True
        if low[v] >= ord_[p]:  # p を取り除くと v の側が切れるので、ここから新しいブロック
            eb[v] = len(blocks)
            blocks.append([p, v])
        else:
            eb[v] = eb[p]
            blocks[eb[v]].append(v)
    for v in range(n):
        if par[v] == -1 and not has_child[v]:  # 孤立点は 1 頂点のブロック
            blocks.append([v])
    tree = [[] for _ in range(n + len(blocks))]
    for i, b in enumerate(blocks):
        for v in b:
            tree[v].append(n + i)
            tree[n + i].append(v)
    return blocks, tree
