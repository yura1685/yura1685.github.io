---
title: XOR・AND・OR 畳み込み
category: 数学
description: 長さ $2^N$ の 2 つの列について、添字の xor・and・or が $k$ になる組の積の和を $O(N 2^N)$ で求める
order: 5
---

xor 畳み込みはアダマール変換、and 畳み込みと or 畳み込みは上位集合・部分集合についてのゼータ変換を使い、要素ごとの積に直してから逆変換で戻します。

- `xor_convolution(f, g, mod)`: $h(k) = \sum_{i \oplus j = k} f(i) g(j)$ のリストを返す
- `and_convolution(f, g, mod)`: $h(k) = \sum_{i \mathbin{\mathrm{and}} j = k} f(i) g(j)$ のリストを返す
- `or_convolution(f, g, mod)`: $h(k) = \sum_{i \mathbin{\mathrm{or}} j = k} f(i) g(j)$ のリストを返す
- 計算量: どれも $O(N 2^N)$

`f` と `g` は同じ長さ（ $2$ のべき）にします。`mod` を渡すと、各値を `mod` で割った余りで返します（省略すると割らない）。xor 畳み込みで `mod` を渡すときは $2^N$ の逆元を使うので、`mod` は奇数にします。

部分集合や上位集合にわたる和だけが欲しいときは、[高速ゼータ変換・メビウス変換](zeta_mobius.html) を使います。
