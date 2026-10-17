class OfflineDynamicConnectivity:
    # 辺の追加・削除と連結性の質問を先にすべて受け取り、run() でまとめて答える
    def __init__(self, n):
        self.n = n
        self.ops = []  # (種類, u, v)。種類は 0: 追加, 1: 削除, 2: same, 3: 連結成分の個数

    def add_edge(self, u, v):
        self.ops.append((0, u, v))

    def remove_edge(self, u, v):
        # 今ある辺 (u, v) を 1 本取り除く
        self.ops.append((1, u, v))

    def same(self, u, v):
        # この時点で u と v が連結か（答えは run() の返り値に、質問した順に入る）
        self.ops.append((2, u, v))

    def count(self):
        # この時点の連結成分の個数
        self.ops.append((3, 0, 0))

    def run(self):
        T = len(self.ops)
        sz = 1
        while sz < T:
            sz *= 2
        edges = [[] for _ in range(2 * sz)]  # セグ木のノードごとの、その時間の区間でずっとある辺

        def add_interval(l, r, e):
            l += sz
            r += sz
            while l < r:
                if l & 1:
                    edges[l].append(e)
                    l += 1
                if r & 1:
                    r -= 1
                    edges[r].append(e)
                l >>= 1
                r >>= 1

        start = {}  # 辺 -> 追加された時刻のリスト
        for t, (k, u, v) in enumerate(self.ops):
            if u > v:
                u, v = v, u
            if k == 0:
                start.setdefault((u, v), []).append(t)
            elif k == 1:
                add_interval(start[(u, v)].pop(), t, (u, v))
        for e, ts in start.items():
            for s in ts:
                add_interval(s, T, e)

        # ロールバック付き Union-Find
        p = [-1] * self.n
        history = []  # つないだ側の根と、その元の p

        def leader(a):
            while p[a] >= 0:
                a = p[a]
            return a

        res = []
        save = [0] * (2 * sz)
        st = [1]
        while st:
            k = st.pop()
            if k < 0:
                # ノード ~k を抜けるので、そこでつないだ辺を取り消す
                while len(history) > save[~k]:
                    v, pv = history.pop()
                    p[p[v]] -= pv
                    p[v] = pv
                continue
            save[k] = len(history)
            st.append(~k)
            for u, v in edges[k]:
                u, v = leader(u), leader(v)
                if u == v:
                    continue
                if p[u] > p[v]:
                    u, v = v, u
                history.append((v, p[v]))
                p[u] += p[v]
                p[v] = u
            if k >= sz:
                t = k - sz
                if t < T:
                    kind, u, v = self.ops[t]
                    if kind == 2:
                        res.append(leader(u) == leader(v))
                    elif kind == 3:
                        res.append(self.n - len(history))  # つないだ回数だけ成分が減る
            else:
                st.append(2 * k + 1)
                st.append(2 * k)
        return res
