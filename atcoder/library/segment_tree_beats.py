class SegmentTreeBeats:
    # 区間 chmin・chmax・加算と、区間の和・最大値・最小値（区間はすべて半開区間 [l, r)）
    # 値の絶対値は INF 未満とする（INF を番兵に使う）
    INF = 1 << 62

    def __init__(self, a):
        n = len(a)
        log = 0
        while (1 << log) < n:
            log += 1
        size = 1 << log
        self.n = n
        self.log = log
        self.size = size
        inf = self.INF
        m = 2 * size
        # ノード k の子は 2k と 2k + 1 で、葉 size + i が a[i]（i >= n の葉は要素なし）
        self.mx1 = [-inf] * m  # 最大値
        self.mx2 = [-inf] * m  # 2 番目に大きい値（値が 1 種類なら -INF）
        self.mxc = [0] * m  # 最大値の個数
        self.mn1 = [inf] * m  # 最小値
        self.mn2 = [inf] * m  # 2 番目に小さい値（値が 1 種類なら INF）
        self.mnc = [0] * m  # 最小値の個数
        self.sm = [0] * m  # 和
        self.ln = [0] * m  # 要素数
        self.lz = [0] * m  # 子にまだ足していない値
        self.mx1[size:size + n] = a
        self.mn1[size:size + n] = a
        self.sm[size:size + n] = a
        self.mxc[size:size + n] = [1] * n
        self.mnc[size:size + n] = [1] * n
        self.ln[size:size + n] = [1] * n
        ln = self.ln
        for k in range(size - 1, 0, -1):
            ln[k] = ln[2 * k] + ln[2 * k + 1]
            self._pull(k)

    def _add_node(self, k, x):
        # ノード k の区間の各値に x を足す
        mx1, mn1 = self.mx1, self.mn1
        mx1[k] += x
        mn1[k] += x
        if mx1[k] != mn1[k]:  # 値が 2 種類以上のときだけ 2 番目の値がある
            self.mx2[k] += x
            self.mn2[k] += x
        self.sm[k] += x * self.ln[k]
        self.lz[k] += x

    def _chmin_node(self, k, x):
        # ノード k の最大値を x にする（2 番目に大きい値 < x < 最大値 のとき）
        mx1 = self.mx1
        self.sm[k] += (x - mx1[k]) * self.mxc[k]
        if mx1[k] == self.mn1[k]:  # 値が 1 種類なら最小値も変わる
            self.mn1[k] = x
        elif mx1[k] == self.mn2[k]:  # 値が 2 種類なら 2 番目に小さい値も変わる
            self.mn2[k] = x
        mx1[k] = x

    def _chmax_node(self, k, x):
        # ノード k の最小値を x にする（最小値 < x < 2 番目に小さい値 のとき）
        mn1 = self.mn1
        self.sm[k] += (x - mn1[k]) * self.mnc[k]
        if mn1[k] == self.mx1[k]:
            self.mx1[k] = x
        elif mn1[k] == self.mx2[k]:
            self.mx2[k] = x
        mn1[k] = x

    def _push(self, k):
        # ノード k にたまっている加算・chmin・chmax を子に配る
        a = 2 * k
        b = a + 1
        x = self.lz[k]
        if x:
            self._add_node(a, x)
            self._add_node(b, x)
            self.lz[k] = 0
        mx1, mn1 = self.mx1, self.mn1
        x = mx1[k]
        if mx1[a] > x:
            self._chmin_node(a, x)
        if mx1[b] > x:
            self._chmin_node(b, x)
        x = mn1[k]
        if mn1[a] < x:
            self._chmax_node(a, x)
        if mn1[b] < x:
            self._chmax_node(b, x)

    def _pull(self, k):
        # ノード k の値を子から計算し直す
        mx1, mx2, mxc = self.mx1, self.mx2, self.mxc
        mn1, mn2, mnc = self.mn1, self.mn2, self.mnc
        a = 2 * k
        b = a + 1
        self.sm[k] = self.sm[a] + self.sm[b]
        x, y = mx1[a], mx1[b]
        if x > y:
            mx1[k], mxc[k] = x, mxc[a]
            z = mx2[a]
            mx2[k] = z if z > y else y
        elif x < y:
            mx1[k], mxc[k] = y, mxc[b]
            z = mx2[b]
            mx2[k] = z if z > x else x
        else:
            mx1[k], mxc[k] = x, mxc[a] + mxc[b]
            z, w = mx2[a], mx2[b]
            mx2[k] = z if z > w else w
        x, y = mn1[a], mn1[b]
        if x < y:
            mn1[k], mnc[k] = x, mnc[a]
            z = mn2[a]
            mn2[k] = z if z < y else y
        elif x > y:
            mn1[k], mnc[k] = y, mnc[b]
            z = mn2[b]
            mn2[k] = z if z < x else x
        else:
            mn1[k], mnc[k] = x, mnc[a] + mnc[b]
            z, w = mn2[a], mn2[b]
            mn2[k] = z if z < w else w

    def _cover(self, l, r):
        # [l, r) をちょうど覆うノードを返す（先に、その祖先にたまっている作用を配る）
        if l >= r:
            return []
        l += self.size
        r += self.size
        for i in range(self.log, 0, -1):
            if ((l >> i) << i) != l:
                self._push(l >> i)
            if ((r >> i) << i) != r:
                self._push((r - 1) >> i)
        res = []
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

    def _update(self, l, r, x, t):
        # t = 0: chmin、t = 1: chmax、t = 2: 加算
        if l >= r:
            return
        st = self._cover(l, r)
        if t == 2:
            for k in st:
                self._add_node(k, x)
        else:
            mx1, mx2, mn1, mn2 = self.mx1, self.mx2, self.mn1, self.mn2
            order = []  # 子に降りたノード（あとで下から計算し直す）
            while st:
                k = st.pop()
                if t == 0:
                    if mx1[k] <= x:  # 何も変わらない
                        continue
                    if mx2[k] < x:  # 最大値だけが変わる
                        self._chmin_node(k, x)
                        continue
                else:
                    if mn1[k] >= x:
                        continue
                    if mn2[k] > x:
                        self._chmax_node(k, x)
                        continue
                self._push(k)
                order.append(k)
                st.append(2 * k)
                st.append(2 * k + 1)
            for k in reversed(order):
                self._pull(k)
        # 覆ったノードの祖先を下から計算し直す
        l += self.size
        r += self.size
        for i in range(1, self.log + 1):
            if ((l >> i) << i) != l:
                self._pull(l >> i)
            if ((r >> i) << i) != r:
                self._pull((r - 1) >> i)

    def chmin(self, l, r, x):
        # l <= i < r の各 a[i] を min(a[i], x) にする
        self._update(l, r, x, 0)

    def chmax(self, l, r, x):
        # l <= i < r の各 a[i] を max(a[i], x) にする
        self._update(l, r, x, 1)

    def add(self, l, r, x):
        # l <= i < r の各 a[i] に x を足す
        self._update(l, r, x, 2)

    def sum(self, l, r):
        # a[l] + ... + a[r - 1]（l == r なら 0）
        sm = self.sm
        s = 0
        for k in self._cover(l, r):
            s += sm[k]
        return s

    def max(self, l, r):
        # max(a[l], ..., a[r - 1])（l == r なら -INF）
        mx1 = self.mx1
        s = -self.INF
        for k in self._cover(l, r):
            if mx1[k] > s:
                s = mx1[k]
        return s

    def min(self, l, r):
        # min(a[l], ..., a[r - 1])（l == r なら INF）
        mn1 = self.mn1
        s = self.INF
        for k in self._cover(l, r):
            if mn1[k] < s:
                s = mn1[k]
        return s
