def range_count_distinct(a, queries):
    # queries = [(l, r), ...]（半開区間 [l, r)、0 <= l <= r <= len(a)）
    # a[l:r] に含まれる値の種類数を、クエリの順に並べたリストで返す（オフライン）
    n = len(a)
    q = len(queries)
    # 右端が r のクエリを head[r] から nxt でたどれるようにまとめる
    head = [-1] * (n + 1)
    nxt = [-1] * q
    for k in range(q):
        r = queries[k][1]
        nxt[k] = head[r]
        head[r] = k
    # 各値の、今までで最後に出てきた位置にだけ 1 を置いた列の BIT（位置は 1-indexed）
    bit = [0] * (n + 1)
    last = {}
    kinds = 0  # 今までに出てきた値の種類数
    res = [0] * q  # r = 0 のクエリの答えは 0 のまま
    for r in range(1, n + 1):
        x = a[r - 1]
        j = last.get(x, 0)
        if j:
            # 前に出てきた位置の 1 を消す
            while j <= n:
                bit[j] -= 1
                j += j & -j
        else:
            kinds += 1
        last[x] = r
        j = r
        while j <= n:
            bit[j] += 1
            j += j & -j
        # a[l:r] の種類数 = BIT の位置 l + 1 から r にある 1 の個数 = kinds - (位置 1 から l の和)
        k = head[r]
        while k != -1:
            j = queries[k][0]
            s = kinds
            while j:
                s -= bit[j]
                j -= j & -j
            res[k] = s
            k = nxt[k]
    return res
