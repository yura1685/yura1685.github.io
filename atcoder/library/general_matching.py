def general_matching(n, edges):
    # 頂点 0..n-1、無向辺 edges = [(u, v), ...] のグラフの最大マッチング（Edmonds の花のアルゴリズムを Gabow の方法で）
    # マッチングの辺 (u, v)（u < v）のリストを u の昇順で返す。自己ループは無視し、多重辺はあってもよい
    # 中では頂点を 1..n とし、0 を番兵にする
    K = n + 1
    g = [[] for _ in range(K)]
    for u, v in edges:
        if u != v:
            g[u + 1].append(v + 1)
            g[v + 1].append(u + 1)
    mate = [0] * K  # mate[v] = v とマッチしている頂点（0 ならマッチしていない）
    for x in range(1, K):  # 最初に貪欲にマッチさせておく
        if mate[x] == 0:
            for y in g[x]:
                if mate[y] == 0:
                    mate[x] = y
                    mate[y] = x
                    break
    # label[v]: 負なら外点でない（-1 か、花を探すときの印）、0 は根、1..n は頂点ラベル、K 以上は辺ラベル
    # 外点 v の first[v] は、v から根への交互路で最初の外点でない頂点（外点を指していたら find でたどる）
    label = [-1] * K
    first = [0] * K

    def find(x):
        y = x
        while label[first[y]] >= 0:
            y = first[y]
        r = first[y]
        while label[first[x]] >= 0:  # 経路圧縮
            nx = first[x]
            first[x] = r
            x = nx
        return r

    for root in range(1, K):
        if mate[root]:
            continue
        label[root] = 0
        first[root] = 0
        q = [root]
        found = False
        for x in q:
            for y in g[x]:
                if mate[y] == 0 and y != root:
                    # 増加パスが見つかったので、根から x を通って y までの辺を付け替える
                    mate[y] = x
                    st = [x, y]
                    while st:
                        w = st.pop()
                        v = st.pop()
                        t = mate[v]
                        mate[v] = w
                        if mate[t] != v:
                            continue
                        lv = label[v]
                        if lv < K:  # 頂点ラベル
                            mate[t] = lv
                            st.append(lv)
                            st.append(t)
                        else:  # 辺ラベル (a, b): a 側を付け替えてから b 側を付け替える
                            a = lv // K - 1
                            b = lv % K
                            st.append(b)
                            st.append(a)
                            st.append(a)
                            st.append(b)
                    found = True
                    break
                if label[y] >= 0:
                    # x と y がともに外点で、奇閉路（花）ができた
                    r = find(x)
                    s = find(y)
                    if r == s:
                        continue
                    e = K * (x + 1) + y  # 辺ラベル
                    label[r] = label[s] = -e
                    # 2 つの交互路を交互にたどり、最初に合流する外点でない頂点 join を探す
                    while True:
                        if s:
                            r, s = s, r
                        r = find(label[mate[r]])
                        if label[r] == -e:
                            break
                        label[r] = -e
                    join = r
                    # join より手前の外点でない頂点に辺ラベルを付けて外点にする
                    for v in (first[x], first[y]):
                        while v != join:
                            q.append(v)
                            label[v] = e
                            first[v] = join
                            v = first[label[mate[v]]]
                else:
                    v = mate[y]
                    if label[v] < 0:
                        label[v] = x
                        first[v] = y
                        q.append(v)
            if found:
                break
        if found:
            for v in range(K):
                label[v] = -1
    return [(x - 1, mate[x] - 1) for x in range(1, K) if x < mate[x]]
