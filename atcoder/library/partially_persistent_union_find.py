from bisect import bisect_right

class PartiallyPersistentUnionFind:
    # unite を t 回呼んだ直後を時刻 t とする（初期状態は時刻 0）
    # union by size で経路圧縮をしないので、根でなくなった頂点の親はその後変わらない
    def __init__(self, n):
        self.t = 0  # 今の時刻
        self.par = [-1] * n  # 根でなくなったときにつないだ先
        self.tm = [1 << 60] * n  # tm[x] = x が根でなくなった時刻（根のままなら大きな値）
        self.st = [[0] for _ in range(n)]  # 根 x の大きさの履歴: 時刻 st[x][i] から大きさ sz[x][i]
        self.sz = [[1] for _ in range(n)]

    def now(self):
        # 今の時刻（unite を呼んだ回数）
        return self.t

    def find(self, t, x):
        # 時刻 t での x の根
        tm, par = self.tm, self.par
        while tm[x] <= t:
            x = par[x]
        return x

    def unite(self, a, b):
        # 時刻を 1 進めて a と b をつなぐ。すでに同じ集合なら False（このときも時刻は進む）
        a = self.find(self.t, a)
        b = self.find(self.t, b)
        self.t += 1
        if a == b:
            return False
        sa, sb = self.sz[a][-1], self.sz[b][-1]
        if sa < sb:
            a, b = b, a
        self.par[b] = a
        self.tm[b] = self.t
        self.st[a].append(self.t)
        self.sz[a].append(sa + sb)
        return True

    def same(self, t, a, b):
        # 時刻 t で a と b が同じ集合にあるか
        return self.find(t, a) == self.find(t, b)

    def size(self, t, x):
        # 時刻 t での x を含む集合の大きさ（履歴を二分探索する）
        x = self.find(t, x)
        return self.sz[x][bisect_right(self.st[x], t) - 1]
