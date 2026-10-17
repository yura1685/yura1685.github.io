def monotone_minima(n, m, f):
    # n 行 m 列の行列（i 行 j 列が f(i, j)）について、各行で最小値をとる列のうち最も左のもの
    # 最も左の最小値の列が、行が下がるにつれて右に（同じか大きく）なることが条件
    res = [0] * n
    st = [(0, n, 0, m)]  # (行の範囲 [l, r), 列の範囲 [lo, hi))
    while st:
        l, r, lo, hi = st.pop()
        if l >= r:
            continue
        i = (l + r) // 2
        best = lo
        bv = f(i, lo)
        for j in range(lo + 1, hi):
            x = f(i, j)
            if x < bv:
                bv = x
                best = j
        res[i] = best
        st.append((l, i, lo, best + 1))
        st.append((i + 1, r, best, hi))
    return res
