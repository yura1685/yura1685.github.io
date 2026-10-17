def inversion_count(a):
    # i < j かつ a[i] > a[j] となる組 (i, j) の個数
    vals = sorted(set(a))
    idx = {x: i + 1 for i, x in enumerate(vals)}
    m = len(vals)
    bit = [0] * (m + 1)
    res = 0
    for i, x in enumerate(a):
        k = idx[x]
        # これまでに出てきた x 以下の値の個数を数え、残りを足す
        j = k
        s = 0
        while j:
            s += bit[j]
            j -= j & -j
        res += i - s
        while k <= m:
            bit[k] += 1
            k += k & -k
    return res
