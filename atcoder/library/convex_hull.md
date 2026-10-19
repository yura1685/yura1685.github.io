---
title: 凸包
category: 幾何
description: Andrew のアルゴリズム（Monotone Chain）で凸包を求める（外積・面積・格子点の数付き）
order: 1
---

点を $x$ 座標（同じなら $y$ 座標）の順に並べ、外積で向きを判定しながら下側と上側の凸包を作ります。座標が整数なら、すべて整数のまま計算できます。

- `cross(a, b, c)`: ベクトル $\overrightarrow{ab}$ と $\overrightarrow{ac}$ の外積。正なら $a \to b \to c$ が反時計回り、負なら時計回り、 $0$ なら一直線上
- `convex_hull(ps, include_collinear=False)`: 点（タプル `(x, y)`）のリストの凸包の頂点を反時計回りに返す。`include_collinear=True` にすると、凸包の辺上にある点も含めて返す。重複する点は 1 つにまとめる。 $O(N \log N)$
- `area2(ps)`: 頂点を順に並べた多角形の面積の 2 倍。反時計回りなら正、時計回りなら負。 $O(N)$
- `lattice_points(ps)`: 頂点が格子点の多角形（頂点を順に並べたもの、自己交差なし）について、`(内部の格子点の数, 周上の格子点の数)` を返す。`convex_hull` が返す 1 点や 2 点を渡してもよい。 $O(N \log C)$（ $C$ は座標の大きさ）

すべての点が一直線上にあるときは、`include_collinear=False` なら両端の 2 点を、`True` ならすべての点を端から順に返します。

周上の格子点の数 $B$ は各辺の $\gcd(\lvert \Delta x \rvert, \lvert \Delta y \rvert)$ の和です。内部の格子点の数 $I$ は、面積を $S$ としたピックの定理 $S = I + B / 2 - 1$ から求めます。
