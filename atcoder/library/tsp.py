def tsp(d, start=0):
    # dp[S][v] = start から出発して集合 S の頂点をすべて訪れ、いま v にいるときの最小コスト
    n = len(d)
    INF = 1 << 60
    dp = [[INF] * n for _ in range(1 << n)]
    dp[1 << start][start] = 0
    for S in range(1 << n):
        dpS = dp[S]
        for v in range(n):
            if dpS[v] == INF:
                continue
            dv = d[v]
            for to in range(n):
                if S >> to & 1:
                    continue
                nd = dpS[v] + dv[to]
                if nd < dp[S | 1 << to][to]:
                    dp[S | 1 << to][to] = nd
    return dp
