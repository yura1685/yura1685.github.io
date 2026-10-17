class HLD:
    def __init__(self, g, root=0):
        n = len(g)
        par = [-1] * n
        depth = [0] * n
        bfs = [root]
        for v in bfs:
            for to in g[v]:
                if to != par[v]:
                    par[to] = v
                    depth[to] = depth[v] + 1
                    bfs.append(to)
        size = [1] * n
        for v in reversed(bfs[1:]):
            size[par[v]] += size[v]
        heavy = [-1] * n  # 部分木が最も大きい子
        for v in bfs:
            for to in g[v]:
                if to != par[v] and (heavy[v] == -1 or size[to] > size[heavy[v]]):
                    heavy[v] = to
        head = [root] * n  # v を含む heavy path の、根に最も近い頂点
        pos = [0] * n      # 列での v の位置
        order = []         # order[pos[v]] = v
        st = [root]
        while st:
            v = st.pop()
            pos[v] = len(order)
            order.append(v)
            for to in g[v]:
                if to != par[v] and to != heavy[v]:
                    head[to] = to
                    st.append(to)
            if heavy[v] != -1:
                head[heavy[v]] = head[v]
                st.append(heavy[v])
        self.par = par
        self.depth = depth
        self.size = size
        self.head = head
        self.pos = pos
        self.order = order

    def lca(self, u, v):
        pos, head = self.pos, self.head
        while True:
            if pos[u] > pos[v]:
                u, v = v, u
            if head[u] == head[v]:
                return u
            v = self.par[head[v]]

    def dist(self, u, v):
        return self.depth[u] + self.depth[v] - 2 * self.depth[self.lca(u, v)]

    def kth_ancestor(self, v, k):
        # v の k 個上の祖先（存在しなければ -1）
        if k > self.depth[v]:
            return -1
        while True:
            h = self.head[v]
            if self.pos[v] - self.pos[h] >= k:
                return self.order[self.pos[v] - k]
            k -= self.pos[v] - self.pos[h] + 1
            v = self.par[h]

    def path(self, u, v, edge=False):
        # u-v パス上の頂点の位置を、半開区間 [l, r) のリストで返す（区間の順番はばらばら）
        # edge=True なら LCA を除く（辺 (par[x], x) を位置 pos[x] に置いたときの、パス上の辺）
        pos, head = self.pos, self.head
        res = []
        while True:
            if pos[u] > pos[v]:
                u, v = v, u
            if head[u] == head[v]:
                l = pos[u] + 1 if edge else pos[u]
                if l <= pos[v]:
                    res.append((l, pos[v] + 1))
                return res
            res.append((pos[head[v]], pos[v] + 1))
            v = self.par[head[v]]

    def subtree(self, v):
        # v の部分木の頂点の位置の半開区間 [l, r)
        return self.pos[v], self.pos[v] + self.size[v]
