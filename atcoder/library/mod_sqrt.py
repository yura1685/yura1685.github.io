def mod_sqrt(a, p):
    # x^2 ≡ a (mod p) となる x を 1 つ（p は素数、なければ -1）。もう 1 つの解は p - x
    a %= p
    if a < 2 or p == 2:
        return a
    if pow(a, (p - 1) // 2, p) != 1:
        return -1  # 平方非剰余（オイラーの規準）
    q, s = p - 1, 0
    while q % 2 == 0:
        q //= 2
        s += 1
    z = 2
    while pow(z, (p - 1) // 2, p) == 1:
        z += 1  # 平方非剰余 z を探す
    c = pow(z, q, p)  # 位数がちょうど 2^s
    x = pow(a, (q + 1) // 2, p)
    t = pow(a, q, p)  # x^2 ≡ a t を保ち、t を 1 にする（Tonelli–Shanks）
    while t != 1:
        i, u = 0, t
        while u != 1:
            u = u * u % p
            i += 1  # t の位数は 2^i
        b = pow(c, 1 << (s - i - 1), p)
        s = i
        c = b * b % p
        x = x * b % p
        t = t * c % p
    return x
