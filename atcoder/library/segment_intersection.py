def cross(a, b, c):
    # ベクトル ab と ac の外積
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def on_segment(a, b, p):
    # 点 p が線分 ab 上（端点を含む）にあるか
    return (cross(a, b, p) == 0
            and min(a[0], b[0]) <= p[0] <= max(a[0], b[0])
            and min(a[1], b[1]) <= p[1] <= max(a[1], b[1]))


def segments_intersect(a, b, c, d):
    # 線分 ab と線分 cd が共有点を持つか（端点での接触や重なりも含む）
    d1, d2 = cross(a, b, c), cross(a, b, d)
    d3, d4 = cross(c, d, a), cross(c, d, b)
    if ((d1 > 0 > d2) or (d1 < 0 < d2)) and ((d3 > 0 > d4) or (d3 < 0 < d4)):
        return True
    return on_segment(a, b, c) or on_segment(a, b, d) or on_segment(c, d, a) or on_segment(c, d, b)


def line_intersection(a, b, c, d):
    # 直線 ab と直線 cd の交点（浮動小数点数）。平行なら None
    den = (b[0] - a[0]) * (d[1] - c[1]) - (b[1] - a[1]) * (d[0] - c[0])
    if den == 0:
        return None
    t = cross(a, c, d) / den
    return a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1])
