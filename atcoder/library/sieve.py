from math import isqrt


class Sieve:
    def __init__(self, n):
        spf = list(range(n + 1))
        for i in range(2, isqrt(n) + 1):
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


def segment_sieve(l, r):
    # l <= x < r の素数のリスト
    if r <= l:
        return []
    k = isqrt(r - 1)
    small = bytearray([1]) * (k + 1)
    is_p = bytearray([1]) * (r - l)
    for x in range(l, min(r, 2)):
        is_p[x - l] = 0
    for i in range(2, k + 1):
        if small[i]:
            small[i * i::i] = bytearray(len(range(i * i, k + 1, i)))
            start = max(i * i, (l + i - 1) // i * i) - l
            is_p[start::i] = bytearray(len(range(start, r - l, i)))
    return [l + i for i in range(r - l) if is_p[i]]
