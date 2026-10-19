class SparseTable:
    def __init__(self, a, op=min):
        # op は min, max, gcd のように、同じ要素を何度まとめても結果が変わらない演算
        self.op = op
        self.table = [list(a)]
        k = 1
        while 2 * k <= len(a):
            prev = self.table[-1]
            self.table.append([op(prev[i], prev[i + k]) for i in range(len(prev) - k)])
            k *= 2

    def prod(self, l, r):
        # op(a[l], ..., a[r - 1])（l < r）
        k = (r - l).bit_length() - 1
        t = self.table[k]
        return self.op(t[l], t[r - (1 << k)])

    def max_right(self, l, f):
        # f(prod(l, r)) が True となる最大の r（f は単調で、r = l のときは True とみなす）
        lo, hi = l, len(self.table[0]) + 1
        while hi - lo > 1:
            m = (lo + hi) // 2
            if f(self.prod(l, m)):
                lo = m
            else:
                hi = m
        return lo

    def min_left(self, r, f):
        # f(prod(l, r)) が True となる最小の l（f は単調で、l = r のときは True とみなす）
        lo, hi = -1, r
        while hi - lo > 1:
            m = (lo + hi) // 2
            if f(self.prod(m, r)):
                hi = m
            else:
                lo = m
        return hi
