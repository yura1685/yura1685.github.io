class DynamicSegTree:
    # 添字 0 <= i < n（n は 10^18 程度まででよい）の列で、触ったノードだけを作るセグ木
    # op は結合的な演算（可換でなくてよい）、e はその単位元。最初はすべて e
    def __init__(self, n, op, e):
        self.n = n
        self.op = op
        self.e = e
        log = 0
        while (1 << log) < n:
            log += 1
        self.log = log
        # 高さ log の完全二分木で、根はノード 1、根から p の桁を上から見て降りた葉が a[p]
        # ノード 0 は「まだ作っていない部分木」（値は e で、子も 0）
        self.lch = [0, 0]  # 左の子（なければ 0）
        self.rch = [0, 0]  # 右の子（なければ 0）
        self.d = [e, e]  # d[t] = ノード t の区間の値を op でまとめたもの

    def set(self, p, x):
        # a[p] を x にする（通るノードがなければ作る）
        lch, rch, d = self.lch, self.rch, self.d
        path = []
        t = 1
        for j in range(self.log - 1, -1, -1):
            path.append(t)
            ch = rch if p >> j & 1 else lch
            c = ch[t]
            if not c:
                c = ch[t] = len(d)
                lch.append(0)
                rch.append(0)
                d.append(self.e)
            t = c
        d[t] = x
        # 葉の親から根に向かって計算し直す
        op = self.op
        for t in reversed(path):
            d[t] = op(d[lch[t]], d[rch[t]])

    def get(self, p):
        # a[p] の値（ノードがなければ e）
        lch, rch = self.lch, self.rch
        t = 1
        for j in range(self.log - 1, -1, -1):
            t = rch[t] if p >> j & 1 else lch[t]
        return self.d[t]

    def prod(self, l, r):
        # op(a[l], ..., a[r - 1])（l == r なら e）
        if l >= r:
            return self.e
        lch, rch, d, op = self.lch, self.rch, self.d, self.op
        r -= 1  # 両端を含む [l, r] にする
        j = (l ^ r).bit_length() - 1  # l と r が分かれる桁
        t = 1
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
                c = rch[u]
                if c:
                    sl = op(d[c], sl)
                u = lch[u]
            if r >> i & 1:
                c = lch[v]
                if c:
                    sr = op(sr, d[c])
                v = rch[v]
            else:
                v = lch[v]
        return op(op(d[u], sl), op(sr, d[v]))

    def max_right(self, l, f):
        # f(op(a[l], ..., a[r - 1])) が True になる最大の r（f(e) は True で、ACL と同じ）
        if l >= self.n:
            return self.n
        lch, rch, d, op = self.lch, self.rch, self.d, self.op
        # 根から葉 l へ降りながら、右側にある部分木とその高さを集める
        nodes = []
        hs = []
        t = 1
        for i in range(self.log - 1, -1, -1):
            if l >> i & 1:
                t = rch[t]
            else:
                nodes.append(rch[t])
                hs.append(i)
                t = lch[t]
        nodes.append(t)
        hs.append(0)
        # 葉 l から右へ、部分木を順に足していく
        s = self.e
        p = l
        for k in range(len(nodes) - 1, -1, -1):
            t = nodes[k]
            x = op(s, d[t])
            if f(x):
                s = x
                p += 1 << hs[k]
                continue
            # この部分木の中で、f が False になる最初の葉を探す
            for i in range(hs[k] - 1, -1, -1):
                x = op(s, d[lch[t]])
                if f(x):
                    s = x
                    p += 1 << i
                    t = rch[t]
                else:
                    t = lch[t]
            return p
        return self.n
