---
title: マンハッタン距離
category: 幾何
description: 座標を 45 度回転して、マンハッタン距離が最大の 2 点を $O(N)$ で、最小全域木の辺の候補を $O(N \log N)$ で求める
order: 8
---

$u = x + y$, $v = x - y$ と変換する（45 度回転して $\sqrt{2}$ 倍する）と、 $\lvert a \rvert + \lvert b \rvert = \max(\lvert a + b \rvert, \lvert a - b \rvert)$ から $\lvert x_1 - x_2 \rvert + \lvert y_1 - y_2 \rvert = \max(\lvert u_1 - u_2 \rvert, \lvert v_1 - v_2 \rvert)$ が成り立ちます。マンハッタン距離が $u$ の差と $v$ の差の大きい方になるので、 $u$ と $v$ を別々に扱えます。たとえば最も遠い 2 点の距離は、 $u$ の最大値と最小値の差と、 $v$ の最大値と最小値の差のうち大きい方です。

最小全域木は、各点 $i$ から見て 45 度ずつに区切った 8 つの範囲それぞれで、 $i$ に最も近い点と $i$ を結んだ辺だけから作れます。同じ範囲にある 2 点 $j$, $k$ の距離は、 $i$ から $j$ への距離と $i$ から $k$ への距離の大きい方以下になるからです。辺に向きはないので 4 つの範囲を見れば足ります。座標を入れ替えたり符号を反転したりして同じ形の範囲にし、 $x$ 座標の大きい順に見ながら Fenwick Tree で最も近い点を探します。

- `manhattan_farthest(ps)`: 点（タプル `(x, y)`）のリスト（1 個以上）のうちマンハッタン距離が最も大きい 2 点について、`(距離, i, j)` を返す（ $i$, $j$ は点の番号）。 $O(N)$
- `manhattan_mst(ps)`: 点のリストについて、マンハッタン距離の最小全域木に使われうる辺の候補を `(w, i, j)`（ $w$ は点 $i$ と点 $j$ の距離）のリストで返す。辺は $4N$ 本以下。 $O(N \log N)$

`manhattan_mst` が返した辺だけで最小全域木を求めると、すべての 2 点の間に辺がある完全グラフの最小全域木になります。 $O(N^2)$ の Prim 法より速いです。

例（[最小全域木（Kruskal・Prim）](mst.html) の `kruskal` を使う）:

```python
ps = [(0, 0), (3, 1), (1, 4), (5, 5)]
print(manhattan_farthest(ps))  # (10, 3, 0)
es = manhattan_mst(ps)
cost, used = kruskal(len(ps), [(i, j, w) for w, i, j in es])
print(cost)  # 14
tree = [es[k] for k in used]  # 最小全域木の辺 (w, i, j)
```
