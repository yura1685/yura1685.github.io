class Lucas:
    # 小さい素数 p を法とする二項係数（n, r は大きくてよい）
    def __init__(self, p):
        self.p = p
        self.fact = [1] * p
        for i in range(1, p):
            self.fact[i] = self.fact[i - 1] * i % p
        self.inv = [1] * p
        self.inv[p - 1] = pow(self.fact[p - 1], p - 2, p)
        for i in range(p - 1, 0, -1):
            self.inv[i - 1] = self.inv[i] * i % p

    def C(self, n, r):
        if r < 0 or r > n:
            return 0
        p = self.p
        res = 1
        while n:
            a, b = n % p, r % p
            if b > a:
                return 0
            res = res * self.fact[a] * self.inv[b] * self.inv[a - b] % p
            n //= p
            r //= p
        return res
