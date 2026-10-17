---
title: 座標圧縮
category: 基礎
description: 値を大小関係を保ったまま $0, 1, 2, \ldots$ に振り直す
order: 2
---

値の範囲が大きいとき、大小関係だけを残して小さい整数に置き換えます。BIT やセグ木の添字に使うときに便利です。

- `compress(a)`: `(b, vals)` を返す。`vals` は $a$ の値を重複なく昇順に並べたリストで、`b[i]` は `a[i]` が `vals` の何番目か（`vals[b[i]] == a[i]`）
- 計算量: $O(N \log N)$

$a$ に含まれない値 $x$ についても、`bisect_left(vals, x)` で「 $x$ 未満の値の種類数」が求まります。
