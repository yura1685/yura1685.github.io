class RangeSet:
    # 整数の集合を、互いに重ならず隣り合わない半開区間 [l, r) の集まりとして持つ
    # SortedMultiset を使う
    def __init__(self):
        self.ls = SortedMultiset()  # 区間の左端
        self.r = {}                 # r[l] = 左端が l の区間の右端
        self.total = 0              # 入っている整数の個数

    def __iter__(self):
        for l in self.ls:
            yield l, self.r[l]

    def __len__(self):
        return len(self.ls)

    def get(self, x):
        # x を含む区間 (l, r)。なければ None
        l = self.ls.le(x)
        if l is not None and x < self.r[l]:
            return l, self.r[l]
        return None

    def __contains__(self, x):
        return self.get(x) is not None

    def mex(self, x=0):
        # x 以上で、入っていない最小の整数
        iv = self.get(x)
        return x if iv is None else iv[1]

    def add(self, l, r):
        # [l, r) を加え、新しく加わった整数の個数を返す
        if l >= r:
            return 0
        p = self.ls.le(l)
        if p is not None and self.r[p] >= l:
            l = p
        removed = 0
        q = self.ls.ge(l)
        while q is not None and q <= r:
            rq = self.r.pop(q)
            self.ls.discard(q)
            removed += rq - q
            r = max(r, rq)
            q = self.ls.ge(q)
        self.ls.add(l)
        self.r[l] = r
        res = r - l - removed
        self.total += res
        return res

    def remove(self, l, r):
        # [l, r) を取り除き、取り除いた整数の個数を返す
        if l >= r:
            return 0
        res = 0
        p = self.ls.lt(l)
        if p is not None and self.r[p] > l:
            rp = self.r[p]
            self.r[p] = l
            if rp > r:
                self.ls.add(r)
                self.r[r] = rp
                self.total -= r - l
                return r - l
            res += rp - l
        q = self.ls.ge(l)
        while q is not None and q < r:
            rq = self.r.pop(q)
            self.ls.discard(q)
            if rq > r:
                self.ls.add(r)
                self.r[r] = rq
                res += r - q
                break
            res += rq - q
            q = self.ls.ge(q)
        self.total -= res
        return res
