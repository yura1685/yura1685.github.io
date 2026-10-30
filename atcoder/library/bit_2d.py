class BIT2D:
    # 一点加算・長方形の和
    def __init__(self, h, w, a=None):
        # a: h×w の初期配列（省略時は全て0）。O(HW)で構築
        self.h = h
        self.w = w
        W = w + 1
        d = [0] * ((h + 1) * W)
        if a is not None:
            for i in range(h):
                row = a[i]
                base = (i + 1) * W
                for j in range(w):
                    d[base + j + 1] = row[j]
            for i in range(1, h + 1):
                base = i * W
                for j in range(1, w + 1):
                    k = j + (j & -j)
                    if k <= w:
                        d[base + k] += d[base + j]
            for i in range(1, h + 1):
                k = i + (i & -i)
                if k <= h:
                    bi = i * W
                    bk = k * W
                    for j in range(1, w + 1):
                        d[bk + j] += d[bi + j]
        self.d = d

    def add(self, x, y, v):
        # a[x][y] += v
        d = self.d
        h, w = self.h, self.w
        W = w + 1
        i = x + 1
        while i <= h:
            base = i * W
            j = y + 1
            while j <= w:
                d[base + j] += v
                j += j & -j
            i += i & -i

    def prefix(self, x, y):
        # [0, x) × [0, y) の和
        d = self.d
        W = self.w + 1
        s = 0
        i = x
        while i > 0:
            base = i * W
            j = y
            while j > 0:
                s += d[base + j]
                j -= j & -j
            i -= i & -i
        return s

    def sum(self, x1, y1, x2, y2):
        # [x1, x2) × [y1, y2) の和
        return (self.prefix(x2, y2) - self.prefix(x1, y2)
                - self.prefix(x2, y1) + self.prefix(x1, y1))

    def get(self, x, y):
        return self.sum(x, y, x + 1, y + 1)

    def set(self, x, y, v):
        self.add(x, y, v - self.get(x, y))


class RangeBIT2D:
    # 長方形加算・長方形の和
    def __init__(self, h, w):
        self.h = h
        self.w = w
        n = (h + 1) * (w + 1)
        self.b0 = [0] * n
        self.b1 = [0] * n
        self.b2 = [0] * n
        self.b3 = [0] * n

    def _add(self, x, y, v):
        # 1-indexedの差分点 (x, y) に v を加算
        h, w = self.h, self.w
        W = w + 1
        b0, b1, b2, b3 = self.b0, self.b1, self.b2, self.b3
        vy = v * y
        vx = v * x
        vxy = vx * y
        i = x
        while i <= h:
            base = i * W
            j = y
            while j <= w:
                k = base + j
                b0[k] += v
                b1[k] += vy
                b2[k] += vx
                b3[k] += vxy
                j += j & -j
            i += i & -i

    def add(self, x1, y1, x2, y2, v):
        # [x1, x2) × [y1, y2) の全要素に v を加算
        self._add(x1 + 1, y1 + 1, v)
        self._add(x1 + 1, y2 + 1, -v)
        self._add(x2 + 1, y1 + 1, -v)
        self._add(x2 + 1, y2 + 1, v)

    def prefix(self, x, y):
        # [0, x) × [0, y) の和
        W = self.w + 1
        b0, b1, b2, b3 = self.b0, self.b1, self.b2, self.b3
        q0 = q1 = q2 = q3 = 0
        i = x
        while i > 0:
            base = i * W
            j = y
            while j > 0:
                k = base + j
                q0 += b0[k]
                q1 += b1[k]
                q2 += b2[k]
                q3 += b3[k]
                j -= j & -j
            i -= i & -i
        return (x + 1) * (y + 1) * q0 - (x + 1) * q1 - (y + 1) * q2 + q3

    def sum(self, x1, y1, x2, y2):
        # [x1, x2) × [y1, y2) の和
        return (self.prefix(x2, y2) - self.prefix(x1, y2)
                - self.prefix(x2, y1) + self.prefix(x1, y1))

    def get(self, x, y):
        return self.sum(x, y, x + 1, y + 1)


class DualBIT2D:
    # 長方形加算・一点取得
    def __init__(self, h, w):
        self.h = h
        self.w = w
        self.d = [0] * ((h + 1) * (w + 1))

    def _add(self, x, y, v):
        # 1-indexedの差分点 (x, y) に v を加算
        d = self.d
        h, w = self.h, self.w
        W = w + 1
        i = x
        while i <= h:
            base = i * W
            j = y
            while j <= w:
                d[base + j] += v
                j += j & -j
            i += i & -i

    def add(self, x1, y1, x2, y2, v):
        # [x1, x2) × [y1, y2) の全要素に v を加算
        self._add(x1 + 1, y1 + 1, v)
        self._add(x1 + 1, y2 + 1, -v)
        self._add(x2 + 1, y1 + 1, -v)
        self._add(x2 + 1, y2 + 1, v)

    def get(self, x, y):
        # a[x][y]
        d = self.d
        W = self.w + 1
        s = 0
        i = x + 1
        while i > 0:
            base = i * W
            j = y + 1
            while j > 0:
                s += d[base + j]
                j -= j & -j
            i -= i & -i
        return s
