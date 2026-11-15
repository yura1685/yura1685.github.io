def cartesian_tree(a):
    # a の最小値を根とする Cartesian Tree の親のリスト par（根は par[root] = -1）
    # 同じ値どうしでは左にあるものが祖先になる
    n = len(a)
    par = [-1] * n
    st = []  # 根から右の子だけをたどった道の頂点
    for i in range(n):
        x = a[i]
        last = -1
        while st and a[st[-1]] > x:
            last = st.pop()
        if last != -1:
            par[last] = i  # 取り除いた部分は i の左の部分木になる
        if st:
            par[i] = st[-1]  # i は残った道の最後の頂点の右の子になる
        st.append(i)
    return par
