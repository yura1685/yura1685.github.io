def max_independent_set(n, edges):
    # 頂点 0..n-1、無向辺 edges = [(u, v), ...] のグラフの最大独立集合を 1 つ、昇順のリストで返す（n は 40 程度まで）
    # 自己ループのある頂点は選ばない
    adj = [0] * n
    ban = 0
    for u, v in edges:
        if u == v:
            ban |= 1 << u
        else:
            adj[u] |= 1 << v
            adj[v] |= 1 << u
    best = 0  # これまでに見つけた最大の独立集合
    st = [((1 << n) - 1) & ~ban, 0]  # (まだ決めていない頂点の集合, 選んだ頂点の集合) を積む
    while st:
        C = st.pop()
        S = st.pop()
        while S:
            # 次数 1 以下の頂点があれば選ぶ。次数がすべて 2 なら閉路だけなので、どれを選んでもよい
            T = S
            mv = md = -1
            while T:
                b = T & -T
                T ^= b
                v = b.bit_length() - 1
                d = (adj[v] & S).bit_count()
                if d <= 1:
                    mv = v
                    md = d
                    break
                if d > md:
                    mv = v
                    md = d
            if md >= 3:
                break
            C |= 1 << mv
            S &= ~(adj[mv] | 1 << mv)
        if S:
            # 次数が最大の頂点 mv を、選ばない場合と選ぶ場合に分ける
            st.append(S & ~(1 << mv))
            st.append(C)
            st.append(S & ~(adj[mv] | 1 << mv))
            st.append(C | 1 << mv)
        elif C.bit_count() > best.bit_count():
            best = C
    return [v for v in range(n) if best >> v & 1]
