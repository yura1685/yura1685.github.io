from bisect import bisect_left


class LiChaoTree:
    # 直線 y = ax + b を加え、ある x での最小値を求める（x として使う値はすべて前もって渡す）
    def __init__(self, xs):
        xs = sorted(set(xs))
        self.idx = {x: i for i, x in enumerate(xs)}
        n = 1
        while n < len(xs):
            n *= 2
        self.n = n
        self.xs = xs + [xs[-1]] * (n - len(xs))
        self.a = [0] * (2 * n)
        self.b = [0] * (2 * n)
        self.empty = [True] * (2 * n)

    def _add(self, a, b, k, l, r):
        # ノード k（xs の添字 [l, r) を受け持つ）以下に直線を加える
        xs = self.xs
        while True:
            if self.empty[k]:
                self.empty[k] = False
                self.a[k] = a
                self.b[k] = b
                return
            m = (l + r) // 2
            x = xs[m]
            if a * x + b < self.a[k] * x + self.b[k]:
                self.a[k], a = a, self.a[k]
                self.b[k], b = b, self.b[k]
            if r - l == 1:
                return
            x = xs[l]
            if a * x + b < self.a[k] * x + self.b[k]:
                k, r = 2 * k, m
                continue
            x = xs[r - 1]
            if a * x + b < self.a[k] * x + self.b[k]:
                k, l = 2 * k + 1, m
                continue
            return

    def add_line(self, a, b):
        # 直線 y = ax + b を加える
        self._add(a, b, 1, 0, self.n)

    def add_segment(self, a, b, lo, hi):
        # lo <= x < hi の範囲だけに、線分 y = ax + b を加える
        l = bisect_left(self.xs, lo, 0, len(self.idx)) + self.n
        r = bisect_left(self.xs, hi, 0, len(self.idx)) + self.n
        h = 0
        while l < r:
            if l & 1:
                self._add(a, b, l, (l << h) - self.n, ((l + 1) << h) - self.n)
                l += 1
            if r & 1:
                r -= 1
                self._add(a, b, r, (r << h) - self.n, ((r + 1) << h) - self.n)
            l >>= 1
            r >>= 1
            h += 1

    def query(self, x):
        # x での最小値（x を通る直線がなければ None）
        k = self.idx[x] + self.n
        res = None
        while k:
            if not self.empty[k]:
                y = self.a[k] * x + self.b[k]
                if res is None or y < res:
                    res = y
            k >>= 1
        return res
