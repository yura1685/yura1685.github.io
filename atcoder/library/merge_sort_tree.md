---
title: Merge Sort Tree
category: データ構造
description: 値の更新がない列について、区間の中である範囲に入る値の個数・和や、ある値の直前・直後の値を $O(\log^2 N)$ で求める
order: 11
---

セグ木の各ノードに、そのノードが受け持つ区間の値をソートしたリスト（とその累積和）を持たせます。区間 $[l, r)$ を $O(\log N)$ 個のノードに分け、それぞれで二分探索します。 [Wavelet Matrix](wavelet_matrix.html) と同じ形のクエリに答えますが、値が負でも大きくてもそのまま使え、コードも短いです（ $k$ 番目の値は Wavelet Matrix の方が速いです）。

区間はすべて半開区間 $[l, r)$ です。

- `MergeSortTree(a)`: 列 $a$ から前計算。 $O(N \log N)$ 時間・メモリ
- `range_freq(l, r, lower, upper)`: `a[l:r]` のうち $\mathrm{lower}$ 以上 $\mathrm{upper}$ 未満の値の個数
- `range_sum(l, r, lower, upper)`: `a[l:r]` のうち $\mathrm{lower}$ 以上 $\mathrm{upper}$ 未満の値の和
- `prev_value(l, r, upper)`: `a[l:r]` のうち $\mathrm{upper}$ 未満の最大値（なければ `None`）
- `next_value(l, r, lower)`: `a[l:r]` のうち $\mathrm{lower}$ 以上の最小値（なければ `None`）
- 計算量: 前計算以外はどれも $O(\log^2 N)$

$x$ 以下の値の個数は `range_freq(l, r, -INF, x + 1)` のように求めます。
