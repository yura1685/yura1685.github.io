from math import hypot


def cross(a, b, c):
    # ベクトル ab と ac の外積
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def dot(a, b, c):
    # ベクトル ab と ac の内積
    return (b[0] - a[0]) * (c[0] - a[0]) + (b[1] - a[1]) * (c[1] - a[1])


def dist_point_line(p, a, b):
    # 点 p と直線 ab（a != b）の距離
    return abs(cross(a, b, p)) / hypot(b[0] - a[0], b[1] - a[1])


def dist_point_segment(p, a, b):
    # 点 p と線分 ab の距離
    if a == b or dot(a, b, p) <= 0:
        return hypot(p[0] - a[0], p[1] - a[1])
    if dot(b, a, p) <= 0:
        return hypot(p[0] - b[0], p[1] - b[1])
    return dist_point_line(p, a, b)


def dist_segment_segment(a, b, c, d):
    # 線分 ab と線分 cd の距離（交わるなら 0）
    d1, d2 = cross(a, b, c), cross(a, b, d)
    d3, d4 = cross(c, d, a), cross(c, d, b)
    if ((d1 > 0 > d2) or (d1 < 0 < d2)) and ((d3 > 0 > d4) or (d3 < 0 < d4)):
        return 0.0
    return min(dist_point_segment(c, a, b), dist_point_segment(d, a, b),
               dist_point_segment(a, c, d), dist_point_segment(b, c, d))
