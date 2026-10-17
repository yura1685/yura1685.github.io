---
title: 2次元セグ木
category: データ構造
description: 前もって与えた点に値を置き、長方形の中にある点の値の和や最大値を $O(\log^2 N)$ で求める
order: 10
---

$x$ 座標についてのセグ木の各ノードに、そのノードが受け持つ点の $y$ 座標を並べた、 $y$ 方向のセグ木を持たせます。値を置く点を先にすべて渡すので（オフライン）、座標が大きくても使えます。演算 `op` は結合的かつ可換なもの（和・最大値・最小値・xor など）で、`e` はその単位元です。

- `SegTree2D(points, op, e, vals)`: 値を置く点のリスト `points = [(x, y), ...]` と、それぞれの初期値 `vals`（省略するとすべて `e`）から構築。同じ座標の点の値は `op` でまとめる。 $O(N \log N)$
- `set(x, y, v)`: 点 $(x, y)$（`points` にある点）の値を $v$ にする。 $O(\log^2 N)$
- `get(x, y)`: 点 $(x, y)$ の値（`points` にない点なら `e`）。 $O(\log N)$
- `prod(xl, xr, yl, yr)`: $\mathrm{xl} \le x < \mathrm{xr}$ かつ $\mathrm{yl} \le y < \mathrm{yr}$ を満たす点の値を `op` でまとめたもの（そのような点がなければ `e`）。 $O(\log^2 N)$

$N$ は点の個数で、メモリは $O(N \log N)$ です。値を足したいときは `set(x, y, get(x, y) + v)` とします。 $H \times W$ のマス目全体で使うときは、すべてのマスを `points` に入れます。

例（長方形の中にある点の個数）:

```python
st = SegTree2D(points, lambda a, b: a + b, 0, [1] * len(points))
cnt = st.prod(xl, xr, yl, yr)
```
