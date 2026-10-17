def cross(a, b, c):
    # ベクトル ab と ac の外積
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def convex_hull(ps):
    # 凸包の頂点を反時計回りに返す（辺上の点は含めない）
    ps = sorted(set(ps))
    if len(ps) <= 2:
        return ps
    lower = []
    for p in ps:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    upper = []
    for p in reversed(ps):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


def area2(ps):
    # 多角形の面積の 2 倍（反時計回りなら正）
    res = 0
    for i in range(len(ps)):
        x1, y1 = ps[i - 1]
        x2, y2 = ps[i]
        res += x1 * y2 - x2 * y1
    return res
