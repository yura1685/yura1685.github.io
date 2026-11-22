from bisect import bisect_left

class StaticTopTree:
    # 根付き木の DP を、頂点のデータを変えるたびに O(log N) で計算し直す
    # heavy path を compress で、light な子の部分木を rake でまとめた、深さ O(log N) の二分木を作る
    def __init__(self, n, edges, root, vertex, compress, rake, add_edge, add_vertex):
        self.vertex = vertex
        self.compress = compress
        self.rake = rake
        self.add_edge = add_edge
        self.add_vertex = add_vertex
        g = [[] for _ in range(n)]
        for u, v in edges:
            g[u].append(v)
            g[v].append(u)
        par = [-1] * n
        order = [root]
        for v in order:
            for to in g[v]:
                if to != par[v]:
                    par[to] = v
                    order.append(to)
        size = [1] * n
        for v in reversed(order):
            if v != root:
                size[par[v]] += size[v]
        heavy = [-1] * n  # 部分木が最も大きい子
        for v in order:
            p = par[v]
            if p != -1 and (heavy[p] == -1 or size[v] > size[heavy[p]]):
                heavy[p] = v
        # ノード x の子 L[x], R[x]、親 P[x]、種類 T[x]、クラスタの値 val[x]
        # ノード v (< n) は頂点 v（T = 0: vertex, 4: add_vertex）
        # n 以降は T = 1: compress, 2: rake, 3: add_edge
        self.L = [-1] * n
        self.R = [-1] * n
        self.P = [-1] * n
        self.T = [0] * n
        self.val = [None] * n
        edge_node = [-1] * n  # light な子 c の部分木を表す点クラスタ（add_edge）のノード
        # 下の heavy path から順に作る（light な子の部分木は先にできている）
        for t in reversed(order):
            if t != root and heavy[par[t]] == t:
                continue
            path = []
            ws = []
            v = t
            while v != -1:
                cs = [c for c in g[v] if c != par[v] and c != heavy[v]]
                if cs:
                    x = self._merge([edge_node[c] for c in cs], [size[c] for c in cs], 2)
                    self.L[v] = x
                    self.P[x] = v
                    self.T[v] = 4
                    self.val[v] = add_vertex(self.val[x], v)
                else:
                    self.val[v] = vertex(v)
                path.append(v)
                h = heavy[v]
                ws.append(size[v] - size[h] if h != -1 else 1)
                v = h
            x = self._merge(path, ws, 1)
            if t == root:
                self.root = x
            else:
                y = self._new(3)
                self.L[y] = x
                self.P[x] = y
                self.val[y] = add_edge(self.val[x])
                edge_node[t] = y

    def _new(self, t):
        self.L.append(-1)
        self.R.append(-1)
        self.P.append(-1)
        self.T.append(t)
        self.val.append(None)
        return len(self.L) - 1

    def _merge(self, xs, ws, t):
        # ノード xs をこの順に、重み ws で釣り合うように種類 t のノードでまとめ、根を返す
        k = len(xs)
        if k == 1:
            return xs[0]
        L, R, P = self.L, self.R, self.P
        pre = [0] * (k + 1)
        for i in range(k):
            pre[i + 1] = pre[i] + ws[i]
        q = [pre[i] + pre[i + 1] for i in range(k)]
        start = self._new(t)
        st = [(0, k, start)]
        while st:
            lo, hi, x = st.pop()
            # [lo, m) の重みがおよそ半分になる m で分ける（lo < m < hi）
            m = bisect_left(q, pre[lo] + pre[hi], lo + 1, hi - 1)
            if m - lo == 1:
                y = xs[lo]
            else:
                y = self._new(t)
                st.append((lo, m, y))
            L[x] = y
            P[y] = x
            if hi - m == 1:
                y = xs[m]
            else:
                y = self._new(t)
                st.append((m, hi, y))
            R[x] = y
            P[y] = x
        # 子は親より後に作ったので、後ろから値を計算する
        f = self.compress if t == 1 else self.rake
        val = self.val
        for x in range(len(L) - 1, start - 1, -1):
            val[x] = f(val[L[x]], val[R[x]])
        return start

    def update(self, v):
        # 頂点 v のデータを変えたあとに呼ぶ（v から根までのノードを計算し直す）
        L, R, P, T, val = self.L, self.R, self.P, self.T, self.val
        compress, rake, add_edge, add_vertex = self.compress, self.rake, self.add_edge, self.add_vertex
        if T[v] == 0:
            val[v] = self.vertex(v)
        else:
            val[v] = add_vertex(val[L[v]], v)
        x = P[v]
        while x != -1:
            t = T[x]
            if t == 1:
                val[x] = compress(val[L[x]], val[R[x]])
            elif t == 2:
                val[x] = rake(val[L[x]], val[R[x]])
            elif t == 3:
                val[x] = add_edge(val[L[x]])
            else:
                val[x] = add_vertex(val[L[x]], x)
            x = P[x]

    def get(self):
        # 木全体のパスクラスタ（根を含む heavy path 全体）
        return self.val[self.root]
