---
title: スパーステーブル
category: データ構造
description: 区間の最小値・最大値などを、前計算 O(N log N)・クエリ O(1) で求める
order: 4
---

長さ $2^k$ の区間の結果を前計算しておき、区間を重なりを許す 2 つの区間に分けて答えます。そのため演算は、同じ要素を何度まとめても結果が変わらないもの（min, max, gcd, bitwise or / and など）に限ります。値の更新はできません。

- `SparseTable(a, op)`: 列 $a$ と演算 `op`（既定は `min`）から前計算。 $O(N \log N)$
- `prod(l, r)`: `op(a[l], ..., a[r - 1])`（ $l < r$）。 $O(1)$
