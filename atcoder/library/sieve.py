class Sieve:
    def __init__(self, n):
        spf = list(range(n + 1))
        for i in range(2, int(n ** 0.5) + 1):
            if spf[i] == i:
                for j in range(i * i, n + 1, i):
                    if spf[j] == j:
                        spf[j] = i
        self.spf = spf
        self.primes = [i for i in range(2, n + 1) if spf[i] == i]

    def is_prime(self, x):
        return x >= 2 and self.spf[x] == x

    def factorize(self, x):
        # [(素因数, 指数), ...]
        res = []
        while x > 1:
            p = self.spf[x]
            e = 0
            while x % p == 0:
                x //= p
                e += 1
            res.append((p, e))
        return res

    def divisors(self, x):
        res = [1]
        for p, e in self.factorize(x):
            m = len(res)
            q = 1
            for _ in range(e):
                q *= p
                for i in range(m):
                    res.append(res[i] * q)
        res.sort()
        return res
