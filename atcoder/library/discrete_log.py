from math import gcd, isqrt


def discrete_log(a, b, m):
    # a^x ≡ b (mod m) となる最小の x >= 0（なければ None）。m は素数でなくてもよい
    a %= m
    b %= m
    k = 0
    t = 1 % m  # a^k をまだ割っていない部分の係数
    while True:
        if t == b:
            return k
        g = gcd(a, m)
        if g == 1:
            break
        if b % g:
            return None
        b //= g
        m //= g
        t = t * (a // g) % m
        k += 1
    # t * a^y ≡ b (mod m) を Baby-step Giant-step で解く（a と m は互いに素）
    n = isqrt(m) + 1
    baby = {}
    cur = b
    for j in range(n + 1):
        baby[cur] = j
        cur = cur * a % m
    an = pow(a, n, m)
    cur = t
    for i in range(1, n + 1):
        cur = cur * an % m
        if cur in baby:
            return k + n * i - baby[cur]
    return None
