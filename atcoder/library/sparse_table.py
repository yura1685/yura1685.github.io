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
