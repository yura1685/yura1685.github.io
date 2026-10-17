def subset_sums(a, s):
    # a のいくつかを選んだ和として作れる s 以下の値を、ビットの集合（整数）で返す
    # 和 x を作れる <=> (res >> x) & 1
    mask = (1 << (s + 1)) - 1
    bits = 1
    for x in a:
        bits = (bits | bits << x) & mask
    return bits


def subset_sum_restore(a, s):
    # 和がちょうど s になる部分集合を、添字のリストで 1 つ返す。作れなければ None
    mask = (1 << (s + 1)) - 1
    dp = [1]
    for x in a:
        dp.append((dp[-1] | dp[-1] << x) & mask)
    if not dp[-1] >> s & 1:
        return None
    res = []
    for i in range(len(a) - 1, -1, -1):
        if not dp[i] >> s & 1:
            res.append(i)
            s -= a[i]
    res.reverse()
    return res
