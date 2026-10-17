class FunctionalGraph:
    def __init__(self, f):
        # 各頂点 v から辺が 1 本だけ出ているグラフ（v -> f[v]、0 <= f[v] < N）
        n = len(f)
        self.f = f
        self.cycles = []          # 閉路のリスト。各閉路は [v, f[v], f[f[v]], ...]
        self.cycle_id = [-1] * n  # v から進むとたどり着く閉路の番号
        self.pos = [-1] * n       # 閉路上の頂点の、閉路の中での位置（閉路上になければ -1）
        self.depth = [0] * n      # 閉路にたどり着くまでの辺の本数（閉路上なら 0）
        self.root = [-1] * n      # 最初にたどり着く閉路上の頂点
        state = [0] * n
        for s in range(n):
            if state[s]:
                continue
            path = []
            v = s
            while state[v] == 0:
                state[v] = 1
                path.append(v)
                v = f[v]
            if state[v] == 1:
                i = path.index(v)
                cyc = path[i:]
                cid = len(self.cycles)
                self.cycles.append(cyc)
                for j, u in enumerate(cyc):
                    self.cycle_id[u] = cid
                    self.pos[u] = j
                    self.root[u] = u
                    state[u] = 2
                del path[i:]
            for u in reversed(path):
                w = f[u]
                self.cycle_id[u] = self.cycle_id[w]
                self.depth[u] = self.depth[w] + 1
                self.root[u] = self.root[w]
                state[u] = 2

    def cycle_len(self, v):
        # v から進むとたどり着く閉路の長さ
        return len(self.cycles[self.cycle_id[v]])

    def kth(self, v, k):
        # v から k 回進んだ頂点
        d = self.depth[v]
        if k < d:
            for _ in range(k):
                v = self.f[v]
            return v
        cyc = self.cycles[self.cycle_id[v]]
        return cyc[(self.pos[self.root[v]] + k - d) % len(cyc)]
