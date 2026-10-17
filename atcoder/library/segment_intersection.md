---
title: 線分の交差判定
category: 幾何
description: 2 つの線分が交わるかを外積で判定し、2 直線の交点を求める
order: 3
---

線分 $ab$ と線分 $cd$ は、 $c, d$ が直線 $ab$ の両側にあり、 $a, b$ も直線 $cd$ の両側にあるときに交わります。そうでないときは、どれかの端点がもう一方の線分上にあるかで判定します。座標が整数なら、交点を求める以外は整数のまま計算できます。

- `cross(a, b, c)`: ベクトル $\overrightarrow{ab}$ と $\overrightarrow{ac}$ の外積
- `on_segment(a, b, p)`: 点 $p$ が線分 $ab$ 上（端点を含む）にあるか
- `segments_intersect(a, b, c, d)`: 線分 $ab$ と線分 $cd$ が共有点を持つか。端点で接する場合や、一直線上で重なる場合も `True`
- `line_intersection(a, b, c, d)`: 直線 $ab$ と直線 $cd$ の交点（浮動小数点数）。平行なら `None`

点はタプル `(x, y)` で表し、計算量はどれも $O(1)$ です。
