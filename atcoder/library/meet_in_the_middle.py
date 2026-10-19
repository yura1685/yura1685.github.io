def _merge(a, b):
    # 昇順のリスト a, b を合わせて昇順にする
    res = []
    i = j = 0
    n, m = len(a), len(b)
    while i < n and j < m:
        if a[i] <= b[j]:
            res.append(a[i])
            i += 1
        else:
            res.append(b[j])
            j += 1
    res += a[i:]
    res += b[j:]
    return res


def all_subset_sums(a):
    # a の部分集合 2^N 個それぞれの和を昇順に並べたリスト（同じ値も重ねて含む）
    res = [0]
    for x in a:
        res = _merge(res, [y + x for y in res])  # x を足しても昇順のまま
    return res


def count_subset_sum_le(a, s):
    # 和が s 以下になる部分集合（空集合も含む）の個数
    m = len(a) // 2
    L = all_subset_sums(a[:m])
    R = all_subset_sums(a[m:])
    res = 0
    j = len(R)
    for x in L:
        while j and x + R[j - 1] > s:
            j -= 1
        res += j
    return res


def knapsack_mitm(items, W):
    # items = [(重さ, 価値), ...]（各品物 1 個まで、重さと W は 0 以上）
    # 重さの合計 W 以下での価値の合計の最大値
    m = len(items) // 2
    halves = []
    for its in (items[:m], items[m:]):
        ps = [(0, 0)]  # (重さの和, 価値の和) を重さの昇順に
        for w, v in its:
            ps = _merge(ps, [(x + w, y + v) for x, y in ps])
        halves.append(ps)
    L, R = halves
    best = []  # best[j] = R[0], ..., R[j] の価値の最大値
    mx = R[0][1]
    for _, v in R:
        if v > mx:
            mx = v
        best.append(mx)
    res = 0
    j = len(R) - 1
    for w, v in L:
        while j >= 0 and w + R[j][0] > W:
            j -= 1
        if j < 0:
            break
        if v + best[j] > res:
            res = v + best[j]
    return res
