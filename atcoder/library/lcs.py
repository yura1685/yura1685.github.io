def lcs_length(s, t):
    # s と t の最長共通部分列の長さ
    m = len(t)
    dp = [0] * (m + 1)
    for a in s:
        ndp = [0] * (m + 1)
        for j in range(m):
            if a == t[j]:
                ndp[j + 1] = dp[j] + 1
            elif ndp[j] >= dp[j + 1]:
                ndp[j + 1] = ndp[j]
            else:
                ndp[j + 1] = dp[j + 1]
        dp = ndp
    return dp[m]

def edit_distance(s, t):
    # 挿入・削除・置換をそれぞれコスト 1 として、s を t に変える最小コスト
    m = len(t)
    dp = list(range(m + 1))
    for i, a in enumerate(s, 1):
        ndp = [i] * (m + 1)
        for j in range(m):
            x = dp[j] if a == t[j] else dp[j] + 1
            y = dp[j + 1] + 1
            if y < x:
                x = y
            y = ndp[j] + 1
            ndp[j + 1] = y if y < x else x
        dp = ndp
    return dp[m]

def edit_distance_bit(s, t):
    # edit_distance と同じ値を、t の位置を 1 ビットずつに対応させたビット並列（Myers の方法）で求める
    m = len(t)
    if m == 0:
        return len(s)
    peq = {}
    for j, c in enumerate(t):
        peq[c] = peq.get(c, 0) | (1 << j)
    mask = (1 << m) - 1
    top = 1 << (m - 1)
    pv, mv, score = mask, 0, m  # 縦の差分が +1 の位置・-1 の位置、最後の行の値
    for c in s:
        eq = peq.get(c, 0)
        xv = eq | mv
        xh = (((eq & pv) + pv) ^ pv) | eq
        ph = mv | (~(xh | pv) & mask)  # 横の差分が +1 の位置
        mh = pv & xh  # 横の差分が -1 の位置
        if ph & top:
            score += 1
        elif mh & top:
            score -= 1
        ph = ((ph << 1) | 1) & mask
        mh = (mh << 1) & mask
        pv = mh | (~(xv | ph) & mask)
        mv = ph & xv
    return score

def lcs(s, t):
    # s と t の最長共通部分列を 1 つ返す（s が文字列なら文字列、そうでなければリスト）
    n, m = len(s), len(t)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n):
        a = s[i]
        cur, nxt = dp[i], dp[i + 1]
        for j in range(m):
            if a == t[j]:
                nxt[j + 1] = cur[j] + 1
            elif nxt[j] >= cur[j + 1]:
                nxt[j + 1] = nxt[j]
            else:
                nxt[j + 1] = cur[j + 1]
    res = []
    i, j = n, m
    while i and j:
        if s[i - 1] == t[j - 1]:
            res.append(s[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1
    res.reverse()
    return "".join(res) if isinstance(s, str) else res
