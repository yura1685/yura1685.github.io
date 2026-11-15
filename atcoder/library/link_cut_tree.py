class LinkCutTree:
    # 頂点に値を持つ森。根から下る各パスを、根に近い頂点ほど左に来る splay 木で持つ
    # op は結合的な演算（可換でなくてよい）、e はその単位元
    def __init__(self, n, op, e, a=None):
        self.op = op
        self.e = e
        self.L = [-1] * n  # splay 木の左の子（根に近い側）
        self.R = [-1] * n  # splay 木の右の子（根から遠い側）
        # splay 木の親。splay 木の根では、そのパスの一番上の頂点の親（木の根なら -1）
        self.P = [-1] * n
        self.val = [e] * n if a is None else list(a)
        self.sum = self.val[:]   # splay 木の部分木の値を左から順に op でまとめたもの
        self.rsum = self.val[:]  # 右から順にまとめたもの（反転したとき用）
        self.rev = [False] * n   # 子の部分木を反転する予定があるか

    def _update(self, x):
        l = self.L[x]
        r = self.R[x]
        s = t = self.val[x]
        if l != -1:
            s = self.op(self.sum[l], s)
            t = self.op(t, self.rsum[l])
        if r != -1:
            s = self.op(s, self.sum[r])
            t = self.op(self.rsum[r], t)
        self.sum[x] = s
        self.rsum[x] = t

    def _toggle(self, x):
        # x の部分木を反転する（x の子の部分木にはあとで配る）
        self.L[x], self.R[x] = self.R[x], self.L[x]
        self.sum[x], self.rsum[x] = self.rsum[x], self.sum[x]
        self.rev[x] = not self.rev[x]

    def _push(self, x):
        if self.L[x] != -1:
            self._toggle(self.L[x])
        if self.R[x] != -1:
            self._toggle(self.R[x])
        self.rev[x] = False

    def _splay(self, x):
        # x をその splay 木の根にする（x の値は呼び出し側で計算し直す）
        L, R, P, rev = self.L, self.R, self.P, self.rev
        val, sm, rsm, op = self.val, self.sum, self.rsum, self.op
        if rev[x]:
            self._push(x)
        while True:
            p = P[x]
            if p == -1 or (L[p] != x and R[p] != x):
                break
            g = P[p]
            # 反転は上から配る（上にまだ配っていない反転があっても、回し方は変わらない）
            if g != -1 and (L[g] == p or R[g] == p):
                if rev[g]:
                    self._push(g)
                if rev[p]:
                    self._push(p)
                if rev[x]:
                    self._push(x)
                # 同じ向きなら p を、違う向きなら x を先に回す
                ys = (p, x) if (L[g] == p) == (L[p] == x) else (x, x)
            else:
                if rev[p]:
                    self._push(p)
                if rev[x]:
                    self._push(x)
                ys = (x,)
            for y in ys:
                # y を親 q の位置に上げ、q の値を計算し直す
                q = P[y]
                r = P[q]
                if L[q] == y:
                    c = R[y]
                    L[q] = c
                    R[y] = q
                else:
                    c = L[y]
                    R[q] = c
                    L[y] = q
                if c != -1:
                    P[c] = q
                P[q] = y
                P[y] = r
                if r != -1:
                    if L[r] == q:
                        L[r] = y
                    elif R[r] == q:
                        R[r] = y
                l = L[q]
                c = R[q]
                s = t = val[q]
                if l != -1:
                    s = op(sm[l], s)
                    t = op(t, rsm[l])
                if c != -1:
                    s = op(s, sm[c])
                    t = op(rsm[c], t)
                sm[q] = s
                rsm[q] = t

    def _expose(self, x):
        # 根から x までのパスを 1 つの splay 木にし、x をその根にする
        # 最後に乗り移ったパスの頂点を返す（lca に使う）
        R, P = self.R, self.P
        last = -1
        y = x
        while y != -1:
            self._splay(y)
            R[y] = last
            self._update(y)
            last = y
            y = P[y]
        if last != x:
            self._splay(x)
            self._update(x)
        return last

    def evert(self, v):
        # v を木の根にする（根から v までのパスを反転する）
        self._expose(v)
        self._toggle(v)

    def link(self, u, v):
        # 辺 (u, v) を加える（u と v は別の木にあること）
        self.evert(u)
        self.P[u] = v

    def cut(self, u, v):
        # 辺 (u, v) を取り除く（辺 (u, v) があること）
        self.evert(u)
        self._expose(v)
        # v の splay 木は u と v の 2 頂点だけで、u は v の左の子
        self.P[self.L[v]] = -1
        self.L[v] = -1
        self._update(v)

    def connected(self, u, v):
        if u == v:
            return True
        self._expose(u)
        self._expose(v)
        # 同じ木なら u は v の splay 木の中に入り、根ではなくなる
        return self.P[u] != -1

    def get(self, v):
        return self.val[v]

    def set(self, v, x):
        # v を splay 木の根にすれば、v の値を含むのは v の splay 木だけ
        self._splay(v)
        self.val[v] = x
        self._update(v)

    def prod(self, u, v):
        # u から v へのパス上の頂点の値を、u の側から順に op でまとめたもの（同じ木にあること）
        self.evert(u)
        self._expose(v)
        return self.sum[v]

    def lca(self, root, u, v):
        # root を根としたときの u と v の最小共通祖先（root, u, v は同じ木にあること）
        self.evert(root)
        self._expose(u)
        return self._expose(v)

    def parent(self, root, v):
        # root を根としたときの v の親（v == root なら -1）
        self.evert(root)
        self._expose(v)
        x = self.L[v]
        if x == -1:
            return -1
        # v の 1 つ上は、左の部分木で一番右の頂点
        while True:
            if self.rev[x]:
                self._push(x)
            if self.R[x] == -1:
                break
            x = self.R[x]
        self._splay(x)
        self._update(x)
        return x
