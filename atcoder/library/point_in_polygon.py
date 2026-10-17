def cross(a, b, c):
    # ベクトル ab と ac の外積
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def point_in_polygon(ps, p):
    # 多角形 ps（頂点を順に並べたもの）に対して、点 p が内部なら 2、辺上なら 1、外部なら 0
    x, y = p
    inside = False
    for i in range(len(ps)):
        a, b = ps[i - 1], ps[i]
        c = cross(a, b, p)
        if (c == 0 and min(a[0], b[0]) <= x <= max(a[0], b[0])
                and min(a[1], b[1]) <= y <= max(a[1], b[1])):
            return 1
        if (a[1] > y) != (b[1] > y) and (c > 0) == (b[1] > a[1]):
            inside = not inside
    return 2 if inside else 0


def point_in_convex(ps, p):
    # 反時計回りに頂点を並べた凸多角形 ps（3 頂点以上、どの 3 頂点も一直線上にない）に対して、内部なら 2、辺上なら 1、外部なら 0
    n = len(ps)
    a = ps[0]
    c1 = cross(a, ps[1], p)
    c2 = cross(a, ps[-1], p)
    if c1 < 0 or c2 > 0:
        return 0
    lo, hi = 1, n - 1
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if cross(a, ps[mid], p) >= 0:
            lo = mid
        else:
            hi = mid
    c = cross(ps[lo], ps[hi], p)
    if c < 0:
        return 0
    if c == 0 or (lo == 1 and c1 == 0) or (hi == n - 1 and c2 == 0):
        return 1
    return 2
