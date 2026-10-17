class LCA:
    def __init__(self, g, root=0):
        n = len(g)
        self.depth = [-1] * n
        self.depth[root] = 0
        par = [-1] * n
        order = [root]
        for v in order:
            for to in g[v]:
                if self.depth[to] == -1:
                    self.depth[to] = self.depth[v] + 1
                    par[to] = v
                    order.append(to)
        self.log = max(1, (n - 1).bit_length())
        self.up = [par]
        for _ in range(self.log - 1):
            p = self.up[-1]
            self.up.append([-1 if p[v] == -1 else p[p[v]] for v in range(n)])

    def kth_ancestor(self, v, k):
        if k > self.depth[v]:
            return -1
        i = 0
        while k:
            if k & 1:
                v = self.up[i][v]
            k >>= 1
            i += 1
        return v

    def lca(self, u, v):
        if self.depth[u] < self.depth[v]:
            u, v = v, u
        u = self.kth_ancestor(u, self.depth[u] - self.depth[v])
        if u == v:
            return u
        for i in range(self.log - 1, -1, -1):
            if self.up[i][u] != self.up[i][v]:
                u = self.up[i][u]
                v = self.up[i][v]
        return self.up[0][u]

    def dist(self, u, v):
        return self.depth[u] + self.depth[v] - 2 * self.depth[self.lca(u, v)]
