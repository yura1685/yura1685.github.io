def ext_gcd(a, b):
    # a x + b y = g（g = gcd(a, b) >= 0）となる (g, x, y)
    x0, y0, x1, y1 = 1, 0, 0, 1
    while b:
        q = a // b
        a, b = b, a - q * b
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    if a < 0:
        return -a, -x0, -y0
    return a, x0, y0


def linear_congruence(a, b, m):
    # a x ≡ b (mod m) の解を x ≡ x0 (mod m') として (x0, m') で返す。解がなければ None
    g, x, _ = ext_gcd(a % m, m)
    if b % g:
        return None
    m //= g
    return x * (b // g) % m, m
