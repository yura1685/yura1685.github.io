class LowLink:
    def __init__(self, n, edges):
        # edges = [(u, v), ...]（無向）
        g = [[] for _ in range(n)]
        for i, (u, v) in enumerate(edges):
            g[u].append((v, i))
            g[v].append((u, i))
        ord_ = [-1] * n
        low = [0] * n
        par = [-1] * n
        par_edge = [-1] * n
        it = [0] * n
        is_art = [False] * n
        self.bridges = []
        cnt = 0
        for root in range(n):
            if ord_[root] != -1:
                continue
            ord_[root] = low[root] = cnt
            cnt += 1
            children = 0
            st = [root]
            while st:
                v = st[-1]
                if it[v] < len(g[v]):
                    to, ei = g[v][it[v]]
                    it[v] += 1
                    if ei == par_edge[v]:
                        continue
                    if ord_[to] == -1:
                        ord_[to] = low[to] = cnt
                        cnt += 1
                        par[to] = v
                        par_edge[to] = ei
                        st.append(to)
                    elif ord_[to] < low[v]:
                        low[v] = ord_[to]
                else:
                    st.pop()
                    p = par[v]
                    if p == -1:
                        continue
                    if low[v] < low[p]:
                        low[p] = low[v]
                    if ord_[p] < low[v]:
                        self.bridges.append(par_edge[v])
                    if p == root:
                        children += 1
                    elif ord_[p] <= low[v]:
                        is_art[p] = True
            if children >= 2:
                is_art[root] = True
        self.ord = ord_
        self.low = low
        self.articulation = [v for v in range(n) if is_art[v]]
