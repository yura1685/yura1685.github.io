from math import isqrt


def prime_count(n):
    # n 以下の素数の個数 π(n)（Lucy DP）
    if n < 2:
        return 0
    r = isqrt(n)
    small = [v - 1 for v in range(r + 1)]  # 最後に small[v] = π(v)（v <= r）
    large = [0] + [n // i - 1 for i in range(1, r + 1)]  # 最後に large[i] = π(n // i)
    for p in range(2, r + 1):
        if small[p] == small[p - 1]:
            continue  # p は合成数
        c = small[p - 1]  # p 未満の素数の個数
        m = min(r, n // (p * p))  # n // i >= p^2 となる i の上限
        b = min(m, r // p)  # i * p <= r なら large を、そうでなければ small を見る
        large[1:b + 1] = [large[i] - large[i * p] + c for i in range(1, b + 1)]
        large[b + 1:m + 1] = [large[i] - small[n // (i * p)] + c for i in range(b + 1, m + 1)]
        small[p * p:] = [small[v] - small[v // p] + c for v in range(p * p, r + 1)]
    return large[1]


def prime_sum(n):
    # n 以下の素数の和（prime_count と同じ DP で、個数の代わりに和を持つ）
    if n < 2:
        return 0
    r = isqrt(n)
    small = [v * (v + 1) // 2 - 1 for v in range(r + 1)]
    large = [0] + [(n // i) * (n // i + 1) // 2 - 1 for i in range(1, r + 1)]
    for p in range(2, r + 1):
        if small[p] == small[p - 1]:
            continue
        c = small[p - 1]  # p 未満の素数の和
        m = min(r, n // (p * p))
        b = min(m, r // p)
        large[1:b + 1] = [large[i] - p * (large[i * p] - c) for i in range(1, b + 1)]
        large[b + 1:m + 1] = [large[i] - p * (small[n // (i * p)] - c) for i in range(b + 1, m + 1)]
        small[p * p:] = [small[v] - p * (small[v // p] - c) for v in range(p * p, r + 1)]
    return large[1]
