from math import gcd
from random import randrange


def is_prime(n):
    # 決定的 Miller–Rabin（n < 2^64 で正しい）
    if n < 2:
        return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % p == 0:
            return n == p
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
    if n < 4759123141:
        bases = (2, 7, 61)
    else:
        bases = (2, 325, 9375, 28178, 450775, 9780504, 1795265022)
    for a in bases:
        if a % n == 0:
            continue
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def pollard_rho(n):
    # 合成数 n の、1 と n 以外の約数を 1 つ返す
    if n % 2 == 0:
        return 2
    m = int(n ** 0.125) + 1
    while True:
        c = randrange(1, n)
        y = randrange(n)
        g = q = r = 1
        while g == 1:
            x = y
            for _ in range(r):
                y = (y * y + c) % n
            k = 0
            while k < r and g == 1:
                ys = y
                for _ in range(min(m, r - k)):
                    y = (y * y + c) % n
                    q = q * abs(x - y) % n
                g = gcd(q, n)
                k += m
            r *= 2
        if g == n:
            g = 1
            while g == 1:
                ys = (ys * ys + c) % n
                g = gcd(abs(x - ys), n)
        if g != n:
            return g


def factorize(n):
    # [(素因数, 指数), ...] を素因数の昇順で返す（n >= 1）
    cnt = {}
    for p in range(2, 50):
        while n % p == 0:
            n //= p
            cnt[p] = cnt.get(p, 0) + 1
    st = [n] if n > 1 else []
    while st:
        m = st.pop()
        if is_prime(m):
            cnt[m] = cnt.get(m, 0) + 1
        else:
            d = pollard_rho(m)
            st.append(d)
            st.append(m // d)
    return sorted(cnt.items())


def divisors(n):
    # n の約数を昇順で返す（n >= 1）
    res = [1]
    for p, e in factorize(n):
        res = [d * p ** i for d in res for i in range(e + 1)]
    return sorted(res)
