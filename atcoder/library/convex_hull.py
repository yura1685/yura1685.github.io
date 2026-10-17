def cross(a, b, c):
    # ベクトル ab と ac の外積
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def convex_hull(ps, include_collinear=False):
    # 凸包の頂点を反時計回りに返す（include_collinear=True なら辺上の点も含める）
    ps = sorted(set(ps))
    if len(ps) <= 2:
        return ps
    if include_collinear and all(cross(ps[0], ps[-1], p) == 0 for p in ps):
        return ps

    def chain(qs):
        res = []
        for p in qs:
            while len(res) >= 2:
                c = cross(res[-2], res[-1], p)
                if c > 0 or (c == 0 and include_collinear):
                    break
                res.pop()
            res.append(p)
        return res

    lower = chain(ps)
    upper = chain(reversed(ps))
    return lower[:-1] + upper[:-1]


def area2(ps):
    # 多角形の面積の 2 倍（反時計回りなら正）
    res = 0
    for i in range(len(ps)):
        x1, y1 = ps[i - 1]
        x2, y2 = ps[i]
        res += x1 * y2 - x2 * y1
    return res
