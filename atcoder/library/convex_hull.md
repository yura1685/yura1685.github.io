---
title: 凸包
category: 幾何
description: Andrew のアルゴリズム（Monotone Chain）で凸包を求める（外積・面積付き）
order: 1
---

点を $x$ 座標（同じなら $y$ 座標）の順に並べ、外積で向きを判定しながら下側と上側の凸包を作ります。座標が整数なら、すべて整数のまま計算できます。

- `cross(a, b, c)`: ベクトル $\overrightarrow{ab}$ と $\overrightarrow{ac}$ の外積。正なら $a \to b \to c$ が反時計回り、負なら時計回り、 $0$ なら一直線上
- `convex_hull(ps)`: 点（タプル `(x, y)`）のリストの凸包の頂点を反時計回りに返す。辺上の点や重複する点は含めない。 $O(N \log N)$
- `area2(ps)`: 頂点を順に並べた多角形の面積の 2 倍。反時計回りなら正、時計回りなら負。 $O(N)$
