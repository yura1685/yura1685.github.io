def dfs(g, s):
    n = len(g)
    seen = [False] * n
    par = [-1] * n
    pre = []
    post = []
    st = [s]
    while st:
        v = st.pop()
        if v >= 0:
            if seen[v]:
                continue
            seen[v] = True
            pre.append(v)
            # 行きがけの処理
            st.append(~v)
            for to in reversed(g[v]):
                if not seen[to]:
                    par[to] = v
                    st.append(to)
        else:
            v = ~v
            post.append(v)
            # 帰りがけの処理
    return pre, post, par
