def rectangle_union_area(rects):
    # rects = [(l, d, r, u), ...]: l <= x < r かつ d <= y < u の長方形（座標は整数）
    # 長方形の和集合の面積を返す
    rects = [t for t in rects if t[0] < t[2] and t[1] < t[3]]  # 面積 0 の長方形は除く
    n = len(rects)
    if n == 0:
        return 0
    ys = sorted(set([t[1] for t in rects] + [t[3] for t in rects]))
    idx = {y: i for i, y in enumerate(ys)}
    m = len(ys) - 1  # y 方向の区間 [ys[j], ys[j + 1]) の個数
    size = 1
    while size < m:
        size *= 2
    # mn[k]: ノード k の区間で、覆っている長方形の個数の最小値（k とその下に足した分だけ）
    # ct[k]: その区間のうち、個数が最小値になる部分の長さ。ad[k]: ノード k の区間全体に足した値
    mn = [0] * (2 * size)
    ct = [0] * (2 * size)
    ad = [0] * (2 * size)
    for j in range(m):
        ct[size + j] = ys[j + 1] - ys[j]
    for k in range(size - 1, 0, -1):
        ct[k] = ct[2 * k] + ct[2 * k + 1]
    total = ys[-1] - ys[0]
    # 長方形 i の左端をイベント 2i（+1）、右端をイベント 2i + 1（-1）とする
    xs = []
    for l, d, r, u in rects:
        xs.append(l)
        xs.append(r)
    lo_y = [idx[t[1]] for t in rects]
    hi_y = [idx[t[3]] for t in rects]
    order = sorted(range(2 * n), key=xs.__getitem__)
    res = 0
    px = xs[order[0]]
    for e in order:
        x = xs[e]
        if x != px:
            # 前のイベントから x までの間、y 方向に覆われている長さは total - (個数が 0 の部分の長さ)
            res += (total - (ct[1] if mn[1] == 0 else 0)) * (x - px)
            px = x
        w = -1 if e & 1 else 1
        l = lo_y[e >> 1] + size
        r = hi_y[e >> 1] + size
        lk = l >> 1
        rk = (r - 1) >> 1
        # [l, r) をノードに分けて w を足す
        while l < r:
            if l & 1:
                mn[l] += w
                ad[l] += w
                l += 1
            if r & 1:
                r -= 1
                mn[r] += w
                ad[r] += w
            l >>= 1
            r >>= 1
        # 両端の葉の祖先 lk, rk を下から計算し直す（合流したら lk だけ）
        while lk:
            c = 2 * lk
            a = mn[c]
            b = mn[c + 1]
            if a < b:
                mn[lk] = a + ad[lk]
                ct[lk] = ct[c]
            elif a > b:
                mn[lk] = b + ad[lk]
                ct[lk] = ct[c + 1]
            else:
                mn[lk] = a + ad[lk]
                ct[lk] = ct[c] + ct[c + 1]
            if rk != lk:
                c = 2 * rk
                a = mn[c]
                b = mn[c + 1]
                if a < b:
                    mn[rk] = a + ad[rk]
                    ct[rk] = ct[c]
                elif a > b:
                    mn[rk] = b + ad[rk]
                    ct[rk] = ct[c + 1]
                else:
                    mn[rk] = a + ad[rk]
                    ct[rk] = ct[c] + ct[c + 1]
            lk >>= 1
            rk >>= 1
    return res
