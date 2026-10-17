class EulerTour:
    def __init__(self, g, root=0):
        n = len(g)
        par = [-1] * n
        depth = [0] * n
        tin = [0] * n
        tout = [0] * n
        order = []
        st = [root]
        while st:
            v = st.pop()
            if v >= 0:
                tin[v] = len(order)
                order.append(v)
                st.append(~v)
                for to in reversed(g[v]):
                    if to != par[v]:
                        par[to] = v
                        depth[to] = depth[v] + 1
                        st.append(to)
            else:
                tout[~v] = len(order)
        self.par = par
        self.depth = depth
        self.tin = tin
        self.tout = tout
        self.order = order

    def is_ancestor(self, u, v):
        # u が v の祖先か（u == v も含む）
        return self.tin[u] <= self.tin[v] < self.tout[u]
