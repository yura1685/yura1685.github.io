class AuxiliaryTree:
    def __init__(self, g, root=0):
        n = len(g)
        par = [-1] * n
        self.depth = depth = [0] * n
        self.tin = tin = [0] * n    # 行きがけ順での番号
        self.tout = tout = [0] * n  # v の部分木の頂点は tin が tin[v] 以上 tout[v] 未満
        t = 0
        st = [root]
        while st:
            v = st.pop()
            if v >= 0:
                tin[v] = t
                t += 1
                st.append(~v)
                for to in g[v]:
                    if to != par[v]:
                        par[to] = v
                        depth[to] = depth[v] + 1
                        st.append(to)
            else:
                tout[~v] = t
        par[root] = root
        self.up = [par]  # up[i][v] = v の 2^i 個上の祖先（根より上は根）
        for _ in range(max(1, (n - 1).bit_length()) - 1):
            p = self.up[-1]
            self.up.append([p[p[v]] for v in range(n)])

    def is_ancestor(self, u, v):
        # u が v の祖先か（u == v も含む）
        return self.tin[u] <= self.tin[v] < self.tout[u]

    def lca(self, u, v):
        if self.is_ancestor(u, v):
            return u
        for p in reversed(self.up):
            if not self.is_ancestor(p[u], v):
                u = p[u]
        return self.up[0][u]

    def build(self, vs):
        # vs と、その中の 2 頂点の LCA からなる木を作る
        # 戻り値: (頂点のリスト（行きがけ順）, 各頂点の親のリスト（根は -1）)
        tin = self.tin
        vs = sorted(set(vs), key=tin.__getitem__)
        for i in range(len(vs) - 1):
            vs.append(self.lca(vs[i], vs[i + 1]))
        vs = sorted(set(vs), key=tin.__getitem__)
        par = []
        st = []
        for v in vs:
            while st and not self.is_ancestor(st[-1], v):
                st.pop()
            par.append(st[-1] if st else -1)
            st.append(v)
        return vs, par
