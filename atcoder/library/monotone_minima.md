---
title: Monotone Minima
category: DP
description: 各行の最小値の位置が下の行ほど右にある行列について、すべての行の最小値の位置を $O((N + M) \log N)$ 回の評価で求める
order: 6
---

真ん中の行の最小値の位置を全部の列を見て求めると、それより上の行はその位置から左だけ、下の行は右だけを見ればよくなります。これを分割統治で繰り返します（再帰は使いません）。行列は関数 `f(i, j)` で与えるので、全部の値を作っておく必要はありません。

- `monotone_minima(n, m, f)`: $n$ 行 $m$ 列の行列（ $i$ 行 $j$ 列が `f(i, j)`）について、各行で最小値をとる列のうち最も左のもののリストを返す。`f` を呼ぶ回数は $O((n + m) \log n)$

条件は「各行で最小値をとる最も左の列が、下の行ほど右（同じでもよい）にある」ことです。行列が Monge（ $f(i, j) + f(i + 1, j + 1) \le f(i, j + 1) + f(i + 1, j)$）なら、この条件を満たします。

例（ $b$ が凸のときの min-plus 畳み込み $c[k] = \min_i (a[i] + b[k - i])$）:

```python
INF = float("inf")


def f(k, i):
    return a[i] + b[k - i] if 0 <= k - i < len(b) else INF


idx = monotone_minima(len(a) + len(b) - 1, len(a), f)
c = [f(k, i) for k, i in enumerate(idx)]
```
