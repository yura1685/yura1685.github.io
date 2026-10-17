from bisect import bisect_left, bisect_right


def lis(a, strict=True):
    # 最長増加部分列を 1 つ返す（strict=False なら広義単調増加）
    bis = bisect_left if strict else bisect_right
    tail = []
    tail_idx = []
    prev = [-1] * len(a)
    for i, x in enumerate(a):
        k = bis(tail, x)
        if k == len(tail):
            tail.append(x)
            tail_idx.append(i)
        else:
            tail[k] = x
            tail_idx[k] = i
        if k:
            prev[i] = tail_idx[k - 1]
    res = []
    i = tail_idx[-1] if tail_idx else -1
    while i != -1:
        res.append(a[i])
        i = prev[i]
    return res[::-1]


def lis_lengths(a, strict=True):
    # res[i] = a[i] で終わる最長増加部分列の長さ
    bis = bisect_left if strict else bisect_right
    tail = []
    res = [0] * len(a)
    for i, x in enumerate(a):
        k = bis(tail, x)
        if k == len(tail):
            tail.append(x)
        else:
            tail[k] = x
        res[i] = k + 1
    return res
