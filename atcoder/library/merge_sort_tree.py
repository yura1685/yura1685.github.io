from bisect import bisect_left


class MergeSortTree:
    # 値の更新のない列 a に対する、区間の中の値についてのクエリ
    def __init__(self, a):
        n = len(a)
        sz = 1
        while sz < n:
            sz *= 2
        self.sz = sz
        self.dat = [[] for _ in range(2 * sz)]  # dat[k] = ノード k が受け持つ値（昇順）
        for i, x in enumerate(a):
            self.dat[sz + i] = [x]
        for k in range(sz - 1, 0, -1):
            self.dat[k] = sorted(self.dat[2 * k] + self.dat[2 * k + 1])
        self.acc = []  # acc[k][i] = dat[k] の先頭 i 個の和
        for d in self.dat:
            s = [0] * (len(d) + 1)
            for i, x in enumerate(d):
                s[i + 1] = s[i] + x
            self.acc.append(s)

    def _nodes(self, l, r):
        # 区間 [l, r) をちょうど覆うノードのリスト
        res = []
        l += self.sz
        r += self.sz
        while l < r:
            if l & 1:
                res.append(l)
                l += 1
            if r & 1:
                r -= 1
                res.append(r)
            l >>= 1
            r >>= 1
        return res

    def range_freq(self, l, r, lower, upper):
        # a[l:r] のうち lower 以上 upper 未満の値の個数
        if lower >= upper:
            return 0
        res = 0
        for k in self._nodes(l, r):
            d = self.dat[k]
            res += bisect_left(d, upper) - bisect_left(d, lower)
        return res

    def range_sum(self, l, r, lower, upper):
        # a[l:r] のうち lower 以上 upper 未満の値の和
        if lower >= upper:
            return 0
        res = 0
        for k in self._nodes(l, r):
            d = self.dat[k]
            res += self.acc[k][bisect_left(d, upper)] - self.acc[k][bisect_left(d, lower)]
        return res

    def prev_value(self, l, r, upper):
        # a[l:r] のうち upper 未満の最大値（なければ None）
        res = None
        for k in self._nodes(l, r):
            d = self.dat[k]
            i = bisect_left(d, upper)
            if i and (res is None or d[i - 1] > res):
                res = d[i - 1]
        return res

    def next_value(self, l, r, lower):
        # a[l:r] のうち lower 以上の最小値（なければ None）
        res = None
        for k in self._nodes(l, r):
            d = self.dat[k]
            i = bisect_left(d, lower)
            if i < len(d) and (res is None or d[i] < res):
                res = d[i]
        return res
