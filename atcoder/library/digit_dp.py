def digit_dp(n, init, step, accept, mod=None, base=10):
    # 0 以上 n 以下の整数 x のうち、上の桁から step で状態を進めた結果が accept を満たすものの個数
    # n は整数か、base 進数の数字の文字列。状態はタプルなど、辞書のキーにできる値
    # step(state, d): 状態 state で次の桁 d を読んだあとの状態（数えないなら None）
    # 先頭の 0 は読まない（x = 0 は init のまま）
    if isinstance(n, int):
        digits = []
        while n:
            digits.append(n % base)
            n //= base
        digits.reverse()
    else:
        digits = [int(c, base) for c in n]
    # キー (状態, ここまで n と同じか, 数が始まっているか)
    dp = {(init, True, False): 1}
    for lim in digits:
        ndp = {}
        for (st, tight, started), c in dp.items():
            top = lim if tight else base - 1
            for d in range(top + 1):
                nt = tight and d == top
                if not started and d == 0:
                    key = (st, nt, False)
                else:
                    ns = step(st, d)
                    if ns is None:
                        continue
                    key = (ns, nt, True)
                v = ndp.get(key, 0) + c
                ndp[key] = v % mod if mod else v
        dp = ndp
    res = 0
    for (st, tight, started), c in dp.items():
        if accept(st):
            res += c
    return res % mod if mod else res
