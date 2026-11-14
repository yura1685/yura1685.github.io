class PersistentSegTree:
    # 経路コピーで永続化したセグ木（op は結合的、e はその単位元）。版の番号は 0, 1, 2, ...
    def __init__(self, a, op, e):
        n = len(a)
        self.n = n
        self.op = op
        self.e = e
        log = 0
        while (1 << log) < n:
            log += 1
        self.log = log
        size = 1 << log
        # 版 0 はヒープと同じ番号付け（ノード k の子は 2k と 2k + 1、葉 size + i が a[i]）
        self.lch = list(range(0, 2 * size, 2)) + [0] * size
        self.rch = list(range(1, 2 * size, 2)) + [0] * size
        d = [e] * (2 * size)  # d[t] = ノード t の区間の値を op でまとめたもの
        d[size:size + n] = a
        for k in range(size - 1, 0, -1):
            d[k] = op(d[2 * k], d[2 * k + 1])
        self.d = d
        self.root = [1]  # root[v] = 版 v の根

    def set(self, ver, p, x):
        # 版 ver の a[p] を x にした新しい版を作り、その番号を返す（版 ver は変わらない）
        lch, rch, d = self.lch, self.rch, self.d
        t = self.root[ver]
        k = c = len(d)  # 根から順に、通るノードをコピーしたノード k, k + 1, ... を作る
        for j in range(self.log - 1, -1, -1):
            c += 1
            if p >> j & 1:
                lch.append(lch[t])
                rch.append(c)
                t = rch[t]
            else:
                lch.append(c)
                rch.append(rch[t])
                t = lch[t]
            d.append(x)  # 値はあとで計算し直す
        lch.append(0)
        rch.append(0)
        d.append(x)
        # 葉の親から根に向かって、区間の値を計算し直す
        op = self.op
        for u in range(c - 1, k - 1, -1):
            d[u] = op(d[lch[u]], d[rch[u]])
        self.root.append(k)
        return len(self.root) - 1

    def get(self, ver, p):
        # 版 ver の a[p]
        lch, rch = self.lch, self.rch
        t = self.root[ver]
        for j in range(self.log - 1, -1, -1):
            t = rch[t] if p >> j & 1 else lch[t]
        return self.d[t]

    def prod(self, ver, l, r):
        # 版 ver の op(a[l], ..., a[r - 1])（l == r なら e）
        if l >= r:
            return self.e
        lch, rch, d, op = self.lch, self.rch, self.d, self.op
        r -= 1  # 両端を含む [l, r] にする
        j = (l ^ r).bit_length() - 1  # l と r が分かれる桁
        t = self.root[ver]
        for i in range(self.log - 1, j, -1):  # l と r が同じ子に入る間はそちらに進む
            t = rch[t] if l >> i & 1 else lch[t]
        if j < 0:
            return d[t]
        # l は左の子から、r は右の子から葉まで降りながら、間にある部分木の値をまとめる
        sl = sr = self.e
        u = lch[t]
        v = rch[t]
        for i in range(j - 1, -1, -1):
            if l >> i & 1:
                u = rch[u]
            else:
                sl = op(d[rch[u]], sl)
                u = lch[u]
            if r >> i & 1:
                sr = op(sr, d[lch[v]])
                v = rch[v]
            else:
                v = lch[v]
        return op(op(d[u], sl), op(sr, d[v]))


class RangeKth:
    # a[l:r] の小さい方から k 番目の値を求める
    # 版 i が a[:i] の各値（座標圧縮したもの）の個数を持つ永続セグ木を使う
    def __init__(self, a):
        self.vals = sorted(set(a))
        idx = {x: i for i, x in enumerate(self.vals)}
        log = 0
        while (1 << log) < len(self.vals):
            log += 1
        self.log = log
        # 降りるときに見るのは左の子の個数だけなので、各ノードにはそれを持たせる
        # ノード 0 は個数がすべて 0 の木（子も自分自身）
        lch = [0]
        rch = [0]
        lc = [0]  # lc[t] = ノード t の左の子の区間に入る値の個数（葉は 0）
        root = [0]  # root[i] = 版 i の根
        for x in a:
            p = idx[x]
            t = root[-1]
            c = len(lc)  # 根から順に、通るノードをコピーしたノード c, c + 1, ... を作る
            root.append(c)
            for j in range(log - 1, -1, -1):
                c += 1
                if p >> j & 1:
                    lc.append(lc[t])
                    lch.append(lch[t])
                    rch.append(c)
                    t = rch[t]
                else:
                    lc.append(lc[t] + 1)
                    lch.append(c)
                    rch.append(rch[t])
                    t = lch[t]
            lc.append(0)
            lch.append(0)
            rch.append(0)
        self.lch = lch
        self.rch = rch
        self.lc = lc
        self.root = root

    def kth(self, l, r, k):
        # a[l:r] の小さい方から k 番目（0-indexed）の値
        # 版 r と版 l の根から同時に降り、左の子の個数の差で進む向きを決める
        lch, rch, lc = self.lch, self.rch, self.lc
        u = self.root[l]
        v = self.root[r]
        p = 0
        for j in range(self.log - 1, -1, -1):
            c = lc[v] - lc[u]  # a[l:r] のうち左の子に入る値の個数
            if k < c:
                u = lch[u]
                v = lch[v]
            else:
                k -= c
                u = rch[u]
                v = rch[v]
                p += 1 << j
        return self.vals[p]
