def manhattan_farthest(ps):
    # マンハッタン距離が最大の 2 点の (距離, i, j)（i, j は点の番号。点は 1 個以上）
    # |x1 - x2| + |y1 - y2| = max(|u1 - u2|, |v1 - v2|)（u = x + y, v = x - y）
    n = len(ps)
    best = (-1, 0, 0)
    for s in (1, -1):
        a = [x + s * y for x, y in ps]
        i = max(range(n), key=a.__getitem__)
        j = min(range(n), key=a.__getitem__)
        if a[i] - a[j] > best[0]:
            best = (a[i] - a[j], i, j)
    return best


def manhattan_mst(ps):
    # マンハッタン距離の最小全域木に使われうる辺 (w, i, j) のリスト（4N 本以下）
    n = len(ps)
    xs = [x for x, y in ps]
    ys = [y for x, y in ps]
    INF = float("inf")
    res = []
    for k in range(4):
        # X[j] >= X[i] かつ Y[j] - X[j] >= Y[i] - X[i] となる j（i から見て 45 度から 90 度の範囲）のうち、
        # X[j] + Y[j] が最小のものと i を結ぶ。X の大きい順に見て、Y - X の順の BIT で最小値を求める
        keys = sorted(set(y - x for x, y in zip(xs, ys)), reverse=True)
        rank = {v: r + 1 for r, v in enumerate(keys)}  # Y - X が大きいほど小さい番号
        m = len(keys)
        bv = [INF] * (m + 1)
        bi = [-1] * (m + 1)
        for i in sorted(range(n), key=lambda i: (xs[i], ys[i]), reverse=True):
            r = rank[ys[i] - xs[i]]
            s = xs[i] + ys[i]
            best, j = INF, -1
            t = r
            while t:
                if bv[t] < best:
                    best, j = bv[t], bi[t]
                t -= t & -t
            if j != -1:
                res.append((best - s, i, j))
            t = r
            while t <= m:
                if s < bv[t]:
                    bv[t], bi[t] = s, i
                t += t & -t
        # (x, y) -> (y, x) -> (-y, x) -> (x, -y) と変換して 4 つの範囲を見る
        if k % 2 == 0:
            xs, ys = ys, xs
        else:
            xs = [-x for x in xs]
    return res
