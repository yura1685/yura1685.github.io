---
title: スパーステーブル
category: データ構造
description: 区間の最小値・最大値などを、前計算 $O(N \log N)$・クエリ $O(1)$ で求める
order: 4
---

長さ $2^k$ の区間の結果を前計算しておき、区間を重なりを許す 2 つの区間に分けて答えます。そのため演算は、同じ要素を何度まとめても結果が変わらないもの（min, max, gcd, bitwise or / and など）に限ります。値の更新はできません。

- `SparseTable(a, op)`: 列 $a$ と演算 `op`（既定は `min`）から前計算。 $O(N \log N)$
- `prod(l, r)`: `op(a[l], ..., a[r - 1])`（ $l < r$）。 $O(1)$
- `max_right(l, f)`: `f(prod(l, r))` が `True` となる最大の $r$（ $r = l$ のときは `True` とみなす）。 $O(\log N)$
- `min_left(r, f)`: `f(prod(l, r))` が `True` となる最小の $l$（ $l = r$ のときは `True` とみなす）。 $O(\log N)$

`max_right` と `min_left` に渡す `f` は、区間を広げると `True` から `False` に変わることはあっても、`False` から `True` には戻らないものとします（ACL のセグ木と同じです）。中では `prod` を使って二分探索しています。

例（ $\gcd$ が $1$ になる区間の個数）:

```python
from math import gcd

st = SparseTable(a, gcd)
ans = 0
for l in range(n):
    ans += n - st.max_right(l, lambda g: g > 1)
```
