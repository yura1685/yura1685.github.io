def euler_phi(n):
    # 1 以上 n 以下で n と互いに素な整数の個数
    res = n
    p = 2
    while p * p <= n:
        if n % p == 0:
            res -= res // p
            while n % p == 0:
                n //= p
        p += 1
    if n > 1:
        res -= res // n
    return res


def phi_table(n):
    # phi[x] = φ(x)（0 <= x <= n、phi[0] = 0）
    phi = list(range(n + 1))
    for p in range(2, n + 1):
        if phi[p] == p:  # p は素数
            for x in range(p, n + 1, p):
                phi[x] -= phi[x] // p
    return phi
