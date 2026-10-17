def mo(n, queries, add, remove, get, add_left=None, remove_left=None):
    # queries = [(l, r), ...]（半開区間 [l, r)、0 <= l <= r <= n）
    # add(i), remove(i): 位置 i を今の区間に加える・今の区間から除く
    # get(k): 今の区間を k 番目のクエリの区間としたときの答え
    # 左端での出し入れを右端と分けたいときは add_left, remove_left も渡す
    if add_left is None:
        add_left = add
    if remove_left is None:
        remove_left = remove
    q = len(queries)
    b = max(1, int(n / max(1, q) ** 0.5))
    key = []
    for l, r in queries:
        k = l // b
        key.append(k * (n + 1) + (r if k % 2 == 0 else n - r))
    res = [None] * q
    l = r = 0
    for k in sorted(range(q), key=key.__getitem__):
        ql, qr = queries[k]
        while l > ql:
            l -= 1
            add_left(l)
        while r < qr:
            add(r)
            r += 1
        while l < ql:
            remove_left(l)
            l += 1
        while r > qr:
            r -= 1
            remove(r)
        res[k] = get(k)
    return res
