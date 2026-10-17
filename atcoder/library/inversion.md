---
title: 転倒数
category: 基礎
description: $i < j$ かつ $a_i > a_j$ となる組の個数を、BIT を使って $O(N \log N)$ で求める
order: 4
---

値を座標圧縮し、左から順に「それより前にある、自分より大きい値の個数」を BIT（Fenwick Tree）で数えて足します。

- `inversion_count(a)`: 列 $a$ の転倒数（ $i < j$ かつ $a_i > a_j$ となる組 $(i, j)$ の個数）。値は大小を比べられれば何でもよい。 $O(N \log N)$

隣り合う 2 つの要素の交換をくり返して $a$ を昇順に並べるとき、交換の最小回数は転倒数に等しくなります。
