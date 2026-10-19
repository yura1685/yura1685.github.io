class DualSegTree:
    # 区間に作用を適用し、1 点の値を求める（作用の渡し方は ACL の lazy_segtree と同じ）
    # mapping(f, x): f を x に作用させた値 / composition(f, g): g のあとに f をする作用
    def __init__(self, a, mapping, composition, id_):
        self.n = len(a)
        self.a = list(a)  # 値は葉に置いたまま
        self.mapping = mapping
        self.composition = composition
        self.id = id_
        self.log = 0
        while (1 << self.log) < self.n:
            self.log += 1
        self.size = 1 << self.log
        self.lz = [id_] * (2 * self.size)  # lz[k] = ノード k の区間にまだ配っていない作用

    def _push(self, k):
        # ノード k の作用を子に配る
        lz = self.lz
        f = lz[k]
        lz[2 * k] = self.composition(f, lz[2 * k])
        lz[2 * k + 1] = self.composition(f, lz[2 * k + 1])
        lz[k] = self.id

    def apply(self, l, r, f):
        # l <= i < r の各 a[i] に f を作用させる
        if l == r:
            return
        l += self.size
        r += self.size
        # 作用が可換でなくてもよいように、先に上のノードの作用を配っておく
        for i in range(self.log, 0, -1):
            if ((l >> i) << i) != l:
                self._push(l >> i)
            if ((r >> i) << i) != r:
                self._push((r - 1) >> i)
        lz = self.lz
        comp = self.composition
        while l < r:
            if l & 1:
                lz[l] = comp(f, lz[l])
                l += 1
            if r & 1:
                r -= 1
                lz[r] = comp(f, lz[r])
            l >>= 1
            r >>= 1

    def get(self, p):
        # a[p] の今の値（葉から根までの作用を合成して作用させる）
        lz = self.lz
        k = p + self.size
        f = lz[k]
        k >>= 1
        while k:
            f = self.composition(lz[k], f)
            k >>= 1
        return self.mapping(f, self.a[p])

    def set(self, p, x):
        # a[p] を x にする
        k = p + self.size
        for i in range(self.log, 0, -1):
            self._push(k >> i)
        self.lz[k] = self.id
        self.a[p] = x
