def rerooting(g, merge, e, add_root):
    # g[v] = [to, ...]（木）
    # merge(a, b): 子から来た値をまとめる演算（結合的かつ可換）、e: その単位元
    # add_root(x, v, p): 子の値をまとめた x に頂点 v を加えて p へ渡す値（p == -1 なら v の答え）
    n = len(g)
    par = [-1] * n
    order = [0]
    for v in order:
        for to in g[v]:
            if to != par[v]:
                par[to] = v
                order.append(to)
    down = [e] * n
    acc = [e] * n
    for v in reversed(order[1:]):
        down[v] = add_root(acc[v], v, par[v])
        acc[par[v]] = merge(acc[par[v]], down[v])
    up = [e] * n
    res = [e] * n
    for v in order:
        ch = [to for to in g[v] if to != par[v]]
        vals = [down[c] for c in ch]
        if v != 0:
            vals.append(up[v])
        k = len(vals)
        suf = [e] * (k + 1)
        for i in range(k - 1, -1, -1):
            suf[i] = merge(vals[i], suf[i + 1])
        res[v] = add_root(suf[0], v, -1)
        pre = e
        for i, c in enumerate(ch):
            up[c] = add_root(merge(pre, suf[i + 1]), v, c)
            pre = merge(pre, vals[i])
    return res
