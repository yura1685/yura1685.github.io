from random import randrange

MOD = (1 << 61) - 1


class ZobristHash:
    def __init__(self):
        self.table = {}

    def get(self, x):
        # 値 x に割り当てた乱数（1 以上 MOD 未満）
        h = self.table.get(x)
        if h is None:
            h = self.table[x] = randrange(1, MOD)
        return h

    def prefix_set(self, a):
        # res[i] = a[:i] に現れる値の集合のハッシュ（XOR）
        res = [0] * (len(a) + 1)
        seen = set()
        h = 0
        for i, x in enumerate(a):
            if x not in seen:
                seen.add(x)
                h ^= self.get(x)
            res[i + 1] = h
        return res

    def prefix_multiset(self, a):
        # (res[r] - res[l]) % MOD が a[l:r] の多重集合のハッシュ
        res = [0] * (len(a) + 1)
        h = 0
        for i, x in enumerate(a):
            h = (h + self.get(x)) % MOD
            res[i + 1] = h
        return res
