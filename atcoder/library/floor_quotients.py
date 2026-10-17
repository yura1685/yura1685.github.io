def floor_ranges(n):
    # [(l, r, q), ...]: l <= i < r の i について n // i == q（1 <= i <= n を q の値ごとに分ける）
    res = []
    l = 1
    while l <= n:
        q = n // l
        r = n // q + 1
        res.append((l, r, q))
        l = r
    return res
