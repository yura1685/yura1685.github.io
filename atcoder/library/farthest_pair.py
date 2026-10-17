def cross(a, b, c):
    # ベクトル ab と ac の外積
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def convex_hull(ps):
    # 凸包の頂点を反時計回りに返す（辺上の点は含めない）
    ps = sorted(set(ps))
    if len(ps) <= 2:
        return ps

    def chain(qs):
        res = []
        for p in qs:
            while len(res) >= 2 and cross(res[-2], res[-1], p) <= 0:
                res.pop()
            res.append(p)
        return res

    return chain(ps)[:-1] + chain(reversed(ps))[:-1]


def farthest_pair(ps):
    # 最も遠い 2 点の (距離の 2 乗, 点, 点)
    hull = convex_hull(ps)
    n = len(hull)
    if n == 1:
        return 0, hull[0], hull[0]

    def d2(p, q):
        return (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2

    best = (-1, None, None)
    j = 1
    for i in range(n):
        a, b = hull[i], hull[(i + 1) % n]
        while cross(a, b, hull[(j + 1) % n]) > cross(a, b, hull[j]):
            j = (j + 1) % n
        for p in (a, b):
            d = d2(p, hull[j])
            if d > best[0]:
                best = (d, p, hull[j])
    return best
