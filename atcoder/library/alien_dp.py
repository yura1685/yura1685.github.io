def alien_dp(solve, k, lo, hi):
    # g(i) = ちょうど i 個選ぶときのコストの最小値 が i について凸のとき、g(k) を返す
    # solve(lam) = (1 個選ぶごとに lam を足したときのコストの最小値, その最小値をとる選び方での個数の最大値)
    # lam は [lo, hi) の整数から二分探索する
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if solve(mid)[1] >= k:
            lo = mid
        else:
            hi = mid
    return solve(lo)[0] - lo * k
