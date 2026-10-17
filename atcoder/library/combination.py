class Combination:
    def __init__(self, n, mod=998244353):
        self.mod = mod
        self.fact = [1] * (n + 1)
        for i in range(1, n + 1):
            self.fact[i] = self.fact[i - 1] * i % mod
        self.inv_fact = [1] * (n + 1)
        self.inv_fact[n] = pow(self.fact[n], mod - 2, mod)
        for i in range(n, 0, -1):
            self.inv_fact[i - 1] = self.inv_fact[i] * i % mod

    def C(self, n, r):
        if r < 0 or r > n or n < 0:
            return 0
        return self.fact[n] * self.inv_fact[r] % self.mod * self.inv_fact[n - r] % self.mod

    def P(self, n, r):
        if r < 0 or r > n or n < 0:
            return 0
        return self.fact[n] * self.inv_fact[n - r] % self.mod

    def H(self, n, r):
        if n == 0 and r == 0:
            return 1
        return self.C(n + r - 1, r)

    def inv(self, n):
        return self.inv_fact[n] * self.fact[n - 1] % self.mod
