class BinaryTrie:
    # 0 以上 2^bit 未満の整数の多重集合
    def __init__(self, bit=30):
        self.bit = bit
        self.ch = [-1, -1]  # ch[2v + b] = ノード v の、次のビットが b の子（なければ -1）
        self.cnt = [0]      # cnt[v] = ノード v の下にある要素の個数
        self.lazy = 0       # 全要素に xor する値

    def __len__(self):
        return self.cnt[0]

    def xor_all(self, x):
        # すべての要素を (要素) xor x に変える
        self.lazy ^= x

    def add(self, x, k=1):
        # x を k 個加える
        x ^= self.lazy
        v = 0
        self.cnt[0] += k
        for i in range(self.bit - 1, -1, -1):
            j = 2 * v + (x >> i & 1)
            if self.ch[j] == -1:
                self.ch[j] = len(self.cnt)
                self.ch.append(-1)
                self.ch.append(-1)
                self.cnt.append(0)
            v = self.ch[j]
            self.cnt[v] += k

    def count(self, x):
        x ^= self.lazy
        v = 0
        for i in range(self.bit - 1, -1, -1):
            v = self.ch[2 * v + (x >> i & 1)]
            if v == -1:
                return 0
        return self.cnt[v]

    def discard(self, x, k=1):
        # x を k 個（入っている個数が少なければすべて）取り除き、取り除いた個数を返す
        k = min(k, self.count(x))
        if k == 0:
            return 0
        x ^= self.lazy
        v = 0
        self.cnt[0] -= k
        for i in range(self.bit - 1, -1, -1):
            v = self.ch[2 * v + (x >> i & 1)]
            self.cnt[v] -= k
        return k

    def kth(self, k, y=0):
        # (要素) xor y を小さい順に並べたときの k 番目（0-indexed）の値
        m = self.lazy ^ y
        v = 0
        res = 0
        for i in range(self.bit - 1, -1, -1):
            b = m >> i & 1
            c = self.ch[2 * v + b]
            if c != -1 and self.cnt[c] > k:
                v = c
            else:
                if c != -1:
                    k -= self.cnt[c]
                v = self.ch[2 * v + (b ^ 1)]
                res |= 1 << i
        return res

    def min_xor(self, y=0):
        # (要素) xor y の最小値
        return self.kth(0, y)

    def max_xor(self, y=0):
        # (要素) xor y の最大値
        return self.kth(self.cnt[0] - 1, y)

    def count_less(self, x, y=0):
        # (要素) xor y が x 未満の要素の個数
        if x <= 0:
            return 0
        if x >> self.bit:
            return self.cnt[0]
        m = self.lazy ^ y
        v = 0
        res = 0
        for i in range(self.bit - 1, -1, -1):
            b = m >> i & 1
            if x >> i & 1:
                c = self.ch[2 * v + b]
                if c != -1:
                    res += self.cnt[c]
                b ^= 1
            v = self.ch[2 * v + b]
            if v == -1:
                break
        return res
