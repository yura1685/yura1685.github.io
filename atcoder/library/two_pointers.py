def two_pointers(n, can_add, add, remove):
    # 各 l について、区間 [l, r) が条件を満たす最大の r のリスト
    # can_add(r): 今の区間に位置 r を加えても条件を満たすか
    # add(r), remove(l): 位置を今の区間に加える・今の区間から除く
    res = [0] * n
    r = 0
    for l in range(n):
        if r < l:
            r = l
        while r < n and can_add(r):
            add(r)
            r += 1
        res[l] = r
        if r > l:
            remove(l)
    return res
