---
title: Li Chao Tree
category: データ構造
description: 直線 $y = ax + b$ の追加と、ある $x$ での最小値を $O(\log N)$ で求める（Convex Hull Trick）
order: 8
---

調べる $x$ を前もってすべて受け取り、それらを葉に持つ完全二分木を作ります。各ノードには、そのノードの区間の真ん中で値が最も小さい直線を 1 本だけ持たせ、負けた方の直線は、勝てる可能性がある方の子に送ります。直線の傾きや加える順番に条件はありません。

- `LiChaoTree(xs)`: 調べる $x$ のリスト `xs`（空でないこと）で初期化。 $O(N \log N)$
- `add_line(a, b)`: 直線 $y = ax + b$ を加える。 $O(\log N)$
- `add_segment(a, b, lo, hi)`: $\mathrm{lo} \le x < \mathrm{hi}$ の範囲だけに線分 $y = ax + b$ を加える。 $O(\log^2 N)$
- `query(x)`: $x$ でのすべての直線（線分）の値の最小値。 $x$ は `xs` に含まれる値で、 $x$ を通るものがなければ `None`。 $O(\log N)$

最大値を求めるときは、 $y = -ax - b$ を加えて、`query` の結果の符号を反転します。

例（ $\mathrm{dp}[j] = \min_{i < j} (\mathrm{dp}[i] + (x[j] - x[i])^2)$）:

```python
t = LiChaoTree(x)
dp = [0] * n
t.add_line(-2 * x[0], x[0] ** 2)
for j in range(1, n):
    dp[j] = t.query(x[j]) + x[j] ** 2
    t.add_line(-2 * x[j], dp[j] + x[j] ** 2)
```
