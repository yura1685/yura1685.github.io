class WaveletMatrix:
    # 0 以上の整数の列 a に対する区間のクエリ（値の更新はできない）
    def __init__(self, a):
        n = len(a)
        self.log = log = max(max(a, default=0).bit_length(), 1)
        self.pre = [0] * (n + 1)  # a の累積和
        for i, x in enumerate(a):
            self.pre[i + 1] = self.pre[i] + x
        self.ones = []   # ones[j][i] = 段 j の先頭 i 個のうち、見ているビットが 1 のものの個数
        self.zeros = []  # zeros[j] = 段 j で見ているビットが 0 のものの個数
        self.sums = []   # sums[j][i] = 段 j で並べ替えたあとの先頭 i 個の和
        cur = list(a)
        for d in range(log - 1, -1, -1):
            o = [0] * (n + 1)
            zero = []
            one = []
            for i, x in enumerate(cur):
                if x >> d & 1:
                    o[i + 1] = o[i] + 1
                    one.append(x)
                else:
                    o[i + 1] = o[i]
                    zero.append(x)
            cur = zero + one
            s = [0] * (n + 1)
            for i, x in enumerate(cur):
                s[i + 1] = s[i] + x
            self.ones.append(o)
            self.zeros.append(len(zero))
            self.sums.append(s)

    def kth_smallest(self, l, r, k):
        # a[l:r] の小さい方から k 番目（0-indexed）
        res = 0
        for j in range(self.log):
            o = self.ones[j]
            zl, zr = l - o[l], r - o[r]
            if k < zr - zl:
                l, r = zl, zr
            else:
                k -= zr - zl
                res |= 1 << (self.log - 1 - j)
                l, r = self.zeros[j] + o[l], self.zeros[j] + o[r]
        return res

    def kth_largest(self, l, r, k):
        # a[l:r] の大きい方から k 番目（0-indexed）
        return self.kth_smallest(l, r, r - l - 1 - k)

    def sum_smallest(self, l, r, k):
        # a[l:r] の小さい方から k 個の和
        if k == 0:
            return 0
        k -= 1
        res = 0
        val = 0
        for j in range(self.log):
            o = self.ones[j]
            zl, zr = l - o[l], r - o[r]
            if k < zr - zl:
                l, r = zl, zr
            else:
                k -= zr - zl
                res += self.sums[j][zr] - self.sums[j][zl]
                val |= 1 << (self.log - 1 - j)
                l, r = self.zeros[j] + o[l], self.zeros[j] + o[r]
        return res + (k + 1) * val

    def sum_largest(self, l, r, k):
        # a[l:r] の大きい方から k 個の和
        return self.pre[r] - self.pre[l] - self.sum_smallest(l, r, r - l - k)

    def _less(self, l, r, upper):
        # a[l:r] のうち upper 未満の値の (個数, 和)
        if upper <= 0:
            return 0, 0
        if upper >> self.log:
            return r - l, self.pre[r] - self.pre[l]
        cnt = 0
        s = 0
        for j in range(self.log):
            o = self.ones[j]
            zl, zr = l - o[l], r - o[r]
            if upper >> (self.log - 1 - j) & 1:
                cnt += zr - zl
                s += self.sums[j][zr] - self.sums[j][zl]
                l, r = self.zeros[j] + o[l], self.zeros[j] + o[r]
            else:
                l, r = zl, zr
        return cnt, s

    def range_freq(self, l, r, lower, upper):
        # a[l:r] のうち lower 以上 upper 未満の値の個数
        if lower >= upper:
            return 0
        return self._less(l, r, upper)[0] - self._less(l, r, lower)[0]

    def range_sum(self, l, r, lower, upper):
        # a[l:r] のうち lower 以上 upper 未満の値の和
        if lower >= upper:
            return 0
        return self._less(l, r, upper)[1] - self._less(l, r, lower)[1]

    def prev_value(self, l, r, upper):
        # a[l:r] のうち upper 未満の最大値（なければ None）
        c = self._less(l, r, upper)[0]
        return None if c == 0 else self.kth_smallest(l, r, c - 1)

    def next_value(self, l, r, lower):
        # a[l:r] のうち lower 以上の最小値（なければ None）
        c = self._less(l, r, lower)[0]
        return None if c == r - l else self.kth_smallest(l, r, c)
