from random import random


class Treap:
    # 列を持つ平衡二分木（位置で分割・結合する）。区間の op での積と区間反転ができる
    def __init__(self, op, e, a=()):
        self.op = op
        self.e = e
        # ノード 0 は空の木を表す番兵
        self.lch = [0]
        self.rch = [0]
        self.pri = [0.0]
        self.size = [0]
        self.val = [e]
        self.sum = [e]   # 部分木の値を左から順に op でまとめたもの
        self.rsum = [e]  # 右から順にまとめたもの（op が可換でないときの反転用）
        self.rev = [False]  # 子の部分木を反転する予定があるか
        # Cartesian tree として O(N) で作る
        st = []
        for x in a:
            v = self._new(x)
            last = 0
            while st and self.pri[st[-1]] < self.pri[v]:
                last = st.pop()
            self.lch[v] = last
            if st:
                self.rch[st[-1]] = v
            st.append(v)
        self.root = st[0] if st else 0
        for v in sorted(range(1, len(self.pri)), key=self.pri.__getitem__):
            self._update(v)

    def _new(self, x):
        self.lch.append(0)
        self.rch.append(0)
        self.pri.append(random())
        self.size.append(1)
        self.val.append(x)
        self.sum.append(x)
        self.rsum.append(x)
        self.rev.append(False)
        return len(self.val) - 1

    def _update(self, t):
        l, r = self.lch[t], self.rch[t]
        self.size[t] = self.size[l] + self.size[r] + 1
        self.sum[t] = self.op(self.op(self.sum[l], self.val[t]), self.sum[r])
        self.rsum[t] = self.op(self.op(self.rsum[r], self.val[t]), self.rsum[l])

    def _toggle(self, t):
        if t:
            self.lch[t], self.rch[t] = self.rch[t], self.lch[t]
            self.sum[t], self.rsum[t] = self.rsum[t], self.sum[t]
            self.rev[t] = not self.rev[t]

    def _push(self, t):
        if self.rev[t]:
            self._toggle(self.lch[t])
            self._toggle(self.rch[t])
            self.rev[t] = False

    def split(self, t, k):
        # 木 t を、先頭 k 個の木と残りの木に分ける
        if t == 0:
            return 0, 0
        self._push(t)
        if self.size[self.lch[t]] >= k:
            a, b = self.split(self.lch[t], k)
            self.lch[t] = b
            self._update(t)
            return a, t
        a, b = self.split(self.rch[t], k - self.size[self.lch[t]] - 1)
        self.rch[t] = a
        self._update(t)
        return t, b

    def merge(self, a, b):
        # 木 a のうしろに木 b をつなげた木
        if a == 0 or b == 0:
            return a or b
        if self.pri[a] > self.pri[b]:
            self._push(a)
            self.rch[a] = self.merge(self.rch[a], b)
            self._update(a)
            return a
        self._push(b)
        self.lch[b] = self.merge(a, self.lch[b])
        self._update(b)
        return b

    def __len__(self):
        return self.size[self.root]

    def insert(self, i, x):
        # 位置 i に x を挿入する
        a, b = self.split(self.root, i)
        self.root = self.merge(self.merge(a, self._new(x)), b)

    def pop(self, i):
        # 位置 i の値を取り除いて返す
        a, b = self.split(self.root, i)
        m, b = self.split(b, 1)
        self.root = self.merge(a, b)
        return self.val[m]

    def get(self, i):
        t = self.root
        while True:
            self._push(t)
            s = self.size[self.lch[t]]
            if i < s:
                t = self.lch[t]
            elif i == s:
                return self.val[t]
            else:
                i -= s + 1
                t = self.rch[t]

    def set(self, i, x):
        a, b = self.split(self.root, i)
        m, b = self.split(b, 1)
        self.val[m] = x
        self._update(m)
        self.root = self.merge(self.merge(a, m), b)

    def prod(self, l, r):
        # 区間 [l, r) の値を op でまとめたもの
        a, b = self.split(self.root, l)
        m, b = self.split(b, r - l)
        res = self.sum[m]
        self.root = self.merge(self.merge(a, m), b)
        return res

    def reverse(self, l, r):
        # 区間 [l, r) を反転する
        a, b = self.split(self.root, l)
        m, b = self.split(b, r - l)
        self._toggle(m)
        self.root = self.merge(self.merge(a, m), b)

    def to_list(self):
        res = []
        st = []
        t = self.root
        while st or t:
            while t:
                self._push(t)
                st.append(t)
                t = self.lch[t]
            t = st.pop()
            res.append(self.val[t])
            t = self.rch[t]
        return res
