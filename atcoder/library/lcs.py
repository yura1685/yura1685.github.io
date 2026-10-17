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
