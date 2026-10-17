from collections import deque


def knapsack_01(items, W):
    # items = [(重さ, 価値), ...]（各品物 1 個まで）。dp[j] = 重さの合計 j 以下での価値の最大値
    dp = [0] * (W + 1)
    for w, v in items:
        for j in range(W, w - 1, -1):
            if dp[j - w] + v > dp[j]:
                dp[j] = dp[j - w] + v
    return dp


def knapsack_unbounded(items, W):
    # items = [(重さ, 価値), ...]（各品物いくつでも、重さは 1 以上）
    dp = [0] * (W + 1)
    for w, v in items:
        for j in range(w, W + 1):
            if dp[j - w] + v > dp[j]:
                dp[j] = dp[j - w] + v
    return dp


def knapsack_bounded(items, W):
    # items = [(重さ, 価値, 個数), ...]（各品物を個数まで、重さは 1 以上）
    # 重さ w で割った余りごとに、スライド最大値で遷移する
    dp = [0] * (W + 1)
    for w, v, c in items:
        ndp = dp[:]
        for r in range(min(w, W + 1)):
            q = deque()  # (t, dp[r + t * w] - t * v)。値が減少するように並べる
            t = 0
            for j in range(r, W + 1, w):
                x = dp[j] - t * v
                while q and q[-1][1] <= x:
                    q.pop()
                q.append((t, x))
                if q[0][0] < t - c:
                    q.popleft()
                ndp[j] = q[0][1] + t * v
                t += 1
        dp = ndp
    return dp


def knapsack_01_by_value(items, W):
    # items = [(重さ, 価値), ...]（各品物 1 個まで）。重さが大きく価値が小さいとき用
    # 重さの合計 W 以下での価値の最大値を返す
    V = sum(v for _, v in items)
    inf = float("inf")
    dp = [inf] * (V + 1)  # dp[x] = 価値の合計が x になるときの重さの最小値
    dp[0] = 0
    for w, v in items:
        for x in range(V, v - 1, -1):
            if dp[x - v] + w < dp[x]:
                dp[x] = dp[x - v] + w
    return max(x for x in range(V + 1) if dp[x] <= W)
