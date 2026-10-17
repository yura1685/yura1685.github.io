from bisect import bisect_left


class SegTree2D:
    # 前もって与えた点 (x, y) に値を置き、長方形の中の点の値を op でまとめる（op は結合的かつ可換）
    def __init__(self, points, op, e, vals=None):
        if vals is None:
            vals = [e] * len(points)
        self.op = op
        self.e = e
        cell = {}  # 同じ座標の点の値は op でまとめる
        for p, v in zip(points, vals):
            cell[p] = op(cell[p], v) if p in cell else v
        self.xs = sorted(set(x for x, _ in cell))
        sz = 1
        while sz < len(self.xs):
            sz *= 2
        self.sz = sz
        ys = [[] for _ in range(2 * sz)]  # ys[k] = ノード k が受け持つ点の y 座標（昇順、重複なし）
        val = [[] for _ in range(2 * sz)]
        for (x, y), v in sorted(cell.items()):
            k = sz + bisect_left(self.xs, x)
            ys[k].append(y)
            val[k].append(v)
        for k in range(sz - 1, 0, -1):
            ay, av, by, bv = ys[2 * k], val[2 * k], ys[2 * k + 1], val[2 * k + 1]
            i = j = 0
            ry, rv = ys[k], val[k]
            while i < len(ay) or j < len(by):
                if j == len(by) or (i < len(ay) and ay[i] < by[j]):
                    ry.append(ay[i])
                    rv.append(av[i])
                    i += 1
                elif i == len(ay) or by[j] < ay[i]:
                    ry.append(by[j])
                    rv.append(bv[j])
                    j += 1
                else:
                    ry.append(ay[i])
                    rv.append(op(av[i], bv[j]))
                    i += 1
                    j += 1
        self.ys = ys
        self.tree = []  # tree[k] = ノード k の y 方向のセグ木（長さ 2 * len(ys[k])）
        for k in range(2 * sz):
            m = len(ys[k])
            t = [e] * m + val[k]
            for i in range(m - 1, 0, -1):
                t[i] = op(t[2 * i], t[2 * i + 1])
            self.tree.append(t)

    def _get(self, k, y):
        # ノード k の y での値（その y の点がなければ e）
        a = self.ys[k]
        i = bisect_left(a, y)
        if i < len(a) and a[i] == y:
            return self.tree[k][len(a) + i]
        return self.e

    def _set(self, k, y, v):
        a = self.ys[k]
        t = self.tree[k]
        op = self.op
        i = bisect_left(a, y) + len(a)
        t[i] = v
        while i > 1:
            i >>= 1
            t[i] = op(t[2 * i], t[2 * i + 1])

    def get(self, x, y):
        # 点 (x, y) の値（与えた点でなければ e）
        i = bisect_left(self.xs, x)
        if i == len(self.xs) or self.xs[i] != x:
            return self.e
        return self._get(self.sz + i, y)

    def set(self, x, y, v):
        # 点 (x, y)（最初に与えた点のどれか）の値を v にする
        k = self.sz + bisect_left(self.xs, x)
        self._set(k, y, v)
        while k > 1:
            v = self.op(v, self._get(k ^ 1, y))  # 兄弟のノードの y での値とまとめる
            k >>= 1
            self._set(k, y, v)

    def prod(self, xl, xr, yl, yr):
        # xl <= x < xr かつ yl <= y < yr を満たす点の値を op でまとめたもの
        res = self.e
        l = self.sz + bisect_left(self.xs, xl)
        r = self.sz + bisect_left(self.xs, xr)
        while l < r:
            if l & 1:
                res = self.op(res, self._prod(l, yl, yr))
                l += 1
            if r & 1:
                r -= 1
                res = self.op(res, self._prod(r, yl, yr))
            l >>= 1
            r >>= 1
        return res

    def _prod(self, k, yl, yr):
        # ノード k で yl <= y < yr の値をまとめたもの
        a = self.ys[k]
        t = self.tree[k]
        op = self.op
        l = bisect_left(a, yl) + len(a)
        r = bisect_left(a, yr) + len(a)
        res = self.e
        while l < r:
            if l & 1:
                res = op(res, t[l])
                l += 1
            if r & 1:
                r -= 1
                res = op(res, t[r])
            l >>= 1
            r >>= 1
        return res
