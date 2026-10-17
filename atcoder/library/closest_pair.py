def closest_pair(ps):
    # 最も近い 2 点の (距離の 2 乗, 点, 点)（点は 2 個以上）
    # x 座標で並べた列を、短い区間から順に y 座標でマージしていく分割統治（再帰なし）
    ps = sorted(ps)
    n = len(ps)
    best = None
    cur = ps[:]  # 長さ w ごとの区間の中が y 座標順に並んでいる
    w = 1
    while w < n:
        nxt = []
        for l in range(0, n, 2 * w):
            m = min(l + w, n)
            r = min(l + 2 * w, n)
            a, b = cur[l:m], cur[m:r]
            i = j = 0
            merged = []
            while i < len(a) or j < len(b):
                if j == len(b) or (i < len(a) and a[i][1] <= b[j][1]):
                    merged.append(a[i])
                    i += 1
                else:
                    merged.append(b[j])
                    j += 1
            nxt += merged
            if m == r:
                continue
            mx = ps[m][0]
            strip = [p for p in merged if best is None or (p[0] - mx) ** 2 < best[0]]
            for i in range(len(strip)):
                p = strip[i]
                for j in range(i + 1, len(strip)):
                    q = strip[j]
                    if best is not None and (q[1] - p[1]) ** 2 >= best[0]:
                        break
                    d = (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2
                    if best is None or d < best[0]:
                        best = (d, p, q)
        cur = nxt
        w *= 2
    return best
