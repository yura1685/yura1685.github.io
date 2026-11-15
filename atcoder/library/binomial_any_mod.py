class BinomialAnyMod:
    # 任意の m (>= 1) を法とする二項係数。m を割り切る素数べき p^e ごとに求めて、中国剰余定理でまとめる
    def __init__(self, m):
        self.m = m
        self.ps = []  # (p, e, q = p^e, 中国剰余定理の係数, 表)
        x = m
        p = 2
        while x > 1:
            if p * p > x:
                p = x  # 残りは素数
            if x % p == 0:
                e = 0
                q = 1
                while x % p == 0:
                    x //= p
                    e += 1
                    q *= p
                # fact[i] = (1 以上 i 以下で p の倍数でない整数の積) mod q
                fact = [1] * q
                for i in range(1, q):
                    fact[i] = fact[i - 1] if i % p == 0 else fact[i - 1] * i % q
                r = m // q
                coef = r * pow(r, -1, q) % m  # mod q で 1、mod m / q で 0
                self.ps.append((p, e, q, coef, fact))
            p += 1

    def C(self, n, k):
        # nCk mod m
        if k < 0 or k > n:
            return 0
        res = 0
        for p, e, q, coef, fact in self.ps:
            a, b, c = n, k, n - k
            num = den = 1
            v = 0  # nCk を割り切る p の指数（k と n - k を p 進数で足したときの繰り上がりの回数）
            s = 0  # e 桁目より上への繰り上がりの回数の偶奇（符号を決める）
            j = 0
            # n! から p を除いた部分 = (1 以上 q 以下で p の倍数でない整数の積)^(n // q) * fact[n % q] * (n // p)! から p を除いた部分
            # b か c が 0 で、下の桁からの繰り上がりもなければ、残りの桁は 1 を掛けるだけ
            while (b and c) or a > b + c:
                num = num * fact[a % q] % q
                den = den * fact[b % q] % q * fact[c % q] % q
                a //= p
                b //= p
                c //= p
                j += 1
                if a - b - c:
                    v += 1
                    if v == e:
                        break
                    if j >= e:
                        s ^= 1
            if v == e:
                continue  # mod q で 0
            x = num * pow(den, -1, q) % q * pow(p, v) % q
            if s:
                x = x * fact[q - 1] % q  # fact[q - 1] は ±1（p = 2, e >= 3 のときだけ 1）
            res += x * coef
        return res % self.m
