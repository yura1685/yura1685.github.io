def centroid_decomposition(g):
    # 木の隣接リスト g から (cpar, level) を返す
    # cpar[v] = 重心分解の木での v の親（根は -1）、level[v] = その木での v の深さ
    n = len(g)
    cpar = [-1] * n
    level = [-1] * n  # -1 はまだ取り除いていない頂点
    bpar = [-1] * n
    size = [1] * n
    st = [(0, -1, 0)]  # (成分の頂点, 親になる重心, 深さ)
    while st:
        s, p, d = st.pop()
        bpar[s] = -1
        comp = [s]
        for v in comp:
            size[v] = 1
            for to in g[v]:
                if to != bpar[v] and level[to] == -1:
                    bpar[to] = v
                    comp.append(to)
        for v in reversed(comp[1:]):
            size[bpar[v]] += size[v]
        c = s
        while True:
            for to in g[c]:
                if to != bpar[c] and level[to] == -1 and 2 * size[to] > len(comp):
                    c = to
                    break
            else:
                break
        cpar[c] = p
        level[c] = d
        for to in g[c]:
            if level[to] == -1:
                st.append((to, c, d + 1))
    return cpar, level
