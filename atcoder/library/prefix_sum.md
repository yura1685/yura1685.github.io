---
title: 累積和
category: 基礎
description: 1・2・3 次元の累積和で、区間・長方形・直方体の和を O(1) で求める
order: 1
---

前計算しておくことで、区間の和を $O(1)$ で求めます。添字はすべて 0-indexed で、区間は右端を含まない半開区間です。使う次元のクラスだけを貼れば動きます。

- `PrefixSum(a)`: 長さ $N$ の列から前計算。 $O(N)$
- `sum(l, r)`: $l \le i < r$ を満たす `a[i]` の和
- `PrefixSum2D(a)`: $H \times W$ の 2 次元配列から前計算。 $O(HW)$
- `sum(x1, y1, x2, y2)`: $x_1 \le i < x_2$, $y_1 \le j < y_2$ を満たす `a[i][j]` の和
- `PrefixSum3D(a)`: $X \times Y \times Z$ の 3 次元配列から前計算。 $O(XYZ)$
- `sum(x1, y1, z1, x2, y2, z2)`: $x_1 \le i < x_2$, $y_1 \le j < y_2$, $z_1 \le k < z_2$ を満たす `a[i][j][k]` の和
- 計算量: 各クエリ $O(1)$

1 次元だけなら、`itertools.accumulate(a, initial=0)` でも同じ表が作れます。
