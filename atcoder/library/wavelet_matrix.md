---
title: Wavelet Matrix
category: データ構造
description: 値の更新がない整数列について、区間で $k$ 番目に小さい値や、ある範囲にある値の個数・和を $O(\log A)$ で求める
order: 9
---

値を 2 進数で上の桁から見ていき、各桁で、その桁が $0$ のものを前に、 $1$ のものを後ろに（それぞれ元の順番のまま）並べ替えた列を、桁の数だけ作ります。各段で「先頭 $i$ 個のうち、その桁が $1$ のものの個数」を持っておくと、区間が次の段のどの区間に移るかがすぐにわかります。

列の値は $0$ 以上の整数とし、 $A$ を値の最大値とします。区間はすべて半開区間 $[l, r)$ です。

- `WaveletMatrix(a)`: 列 $a$ から前計算。 $O(N \log A)$
- `kth_smallest(l, r, k)`, `kth_largest(l, r, k)`: `a[l:r]` の小さい方・大きい方から $k$ 番目（0-indexed）の値
- `range_freq(l, r, lower, upper)`: `a[l:r]` のうち $\mathrm{lower}$ 以上 $\mathrm{upper}$ 未満の値の個数
- `range_sum(l, r, lower, upper)`: `a[l:r]` のうち $\mathrm{lower}$ 以上 $\mathrm{upper}$ 未満の値の和
- `prev_value(l, r, upper)`: `a[l:r]` のうち $\mathrm{upper}$ 未満の最大値（なければ `None`）
- `next_value(l, r, lower)`: `a[l:r]` のうち $\mathrm{lower}$ 以上の最小値（なければ `None`）
- `sum_smallest(l, r, k)`, `sum_largest(l, r, k)`: `a[l:r]` の小さい方・大きい方から $k$ 個の和（ $0 \le k \le r - l$）
- 計算量: 前計算以外はどれも $O(\log A)$

負の値があるときは、すべての値に同じ数を足して $0$ 以上にしてから使います。値の種類が少ないときは [座標圧縮](compress.html) すると段が減って速くなります（このとき和は圧縮したあとの値の和になります）。
