---
title: Alien DP
category: DP
description: ちょうど $K$ 個選ぶときの最小値 $g(K)$ を、1 個選ぶごとにペナルティ $\lambda$ を足した問題を $\lambda$ について二分探索して解くことで求める
order: 8
---

$g(i)$ を「ちょうど $i$ 個選ぶときのコストの最小値」とし、 $g$ が $i$ について凸（ $g(i + 1) - g(i)$ が広義単調増加）であるとします。個数の制約を外し、1 個選ぶごとにコスト $\lambda$ を足した問題 $h(\lambda) = \min_i (g(i) + \lambda i)$ を解くと、 $\lambda$ が大きいほど選ぶ個数が減るので、ちょうど $K$ 個選ぶのが最適になる $\lambda$ を二分探索で見つけられます。そのとき $g(K) = h(\lambda) - \lambda K$ です。個数の次元を DP から消せるので、 $O(NK)$ の DP が $O(N \log C)$ などになります。

- `alien_dp(solve, k, lo, hi)`: $g(k)$ を返す。`solve(lam)` は、1 個選ぶごとに $\lambda$ を足したときのコストの最小値と、その最小値をとる選び方での個数の最大値の組を返す関数。 $\lambda$ は整数で、 $[\mathrm{lo}, \mathrm{hi})$ から探す。`solve` を $O(\log(\mathrm{hi} - \mathrm{lo}))$ 回呼ぶ

コストは整数とします。 $\lvert g(i + 1) - g(i) \rvert$ の最大値を $D$ とすると、`lo = -D - 1`, `hi = D + 1` とすれば十分です。最小値が同じ選び方が複数あるときに個数の最大値を返すのが大事で、DP の値を (コスト, $-$個数) の組にしてタプルの比較で最小をとると簡単です。最大化の問題は、符号を反転させて最小化にします。

例（長さ $N$ の数列から、隣り合わないようにちょうど $K$ 個選ぶときの和の最大値）:

```python
INF = 1 << 60


def solve(lam):
    # 1 個選ぶごとにコスト -a[i] + lam。状態は (コスト, -個数)
    no, yes = (0, 0), (INF, 0)  # 直前を選んでいない・選んだ
    for x in a:
        no, yes = min(no, yes), (no[0] - x + lam, no[1] - 1)
    v, c = min(no, yes)
    return v, -c


D = 2 * sum(abs(x) for x in a) + 1
print(-alien_dp(solve, K, -D - 1, D + 1))
```
