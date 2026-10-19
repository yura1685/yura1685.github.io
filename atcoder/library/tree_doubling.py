class TreeDoubling:
    def __init__(self, n, edges, op, e, root=0):
        # edges = [(u, v, w), ...]。op は結合的かつ可換な演算、e はその単位元
        g = [[] for _ in range(n)]
        for u, v, w in edges:
            g[u].append((v, w))
            g[v].append((u, w))
        self.op = op
        self.e = e
        self.depth = [-1] * n
        self.depth[root] = 0
        par = [root] * n  # 根の親は根自身とする
        pw = [e] * n  # 親への辺の重み
        order = [root]
        for v in order:
            for to, w in g[v]:
                if self.depth[to] == -1:
                    self.depth[to] = self.depth[v] + 1
                    par[to] = v
                    pw[to] = w
                    order.append(to)
        self.log = max(1, (n - 1).bit_length())
        # up[k][v] = v の 2^k 個上の祖先、val[k][v] = そこまでの 2^k 本の辺の重みを op でまとめた値
        self.up = [par]
        self.val = [pw]
        for _ in range(self.log - 1):
            p, s = self.up[-1], self.val[-1]
            self.up.append([p[p[v]] for v in range(n)])
            self.val.append([op(s[v], s[p[v]]) for v in range(n)])

    def _climb(self, u, v):
        # (lca(u, v), u と v を結ぶパス上の辺の重みを op でまとめた値)
        op, up, val = self.op, self.up, self.val
        res = self.e
        if self.depth[u] < self.depth[v]:
            u, v = v, u
        k = self.depth[u] - self.depth[v]
        i = 0
        while k:
            if k & 1:
                res = op(res, val[i][u])
                u = up[i][u]
            k >>= 1
            i += 1
        if u == v:
            return u, res
        for i in range(self.log - 1, -1, -1):
            if up[i][u] != up[i][v]:
                res = op(res, op(val[i][u], val[i][v]))
                u = up[i][u]
                v = up[i][v]
        return up[0][u], op(res, op(val[0][u], val[0][v]))

    def lca(self, u, v):
        return self._climb(u, v)[0]

    def query(self, u, v):
        # u と v を結ぶパス上の辺の重みを op でまとめた値（u == v なら e）
        return self._climb(u, v)[1]
