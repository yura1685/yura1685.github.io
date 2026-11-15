---
title: Subset Convolution
category: 数学
description: 集合を添字とする長さ $2^N$ の 2 つの列について、 $h(S) = \sum_{T \subseteq S} f(T) g(S \setminus T)$ をすべての $S$ について $O(N^2 2^N)$ で求める
order: 9
---

集合 $S \subseteq \lbrace 0, 1, \ldots, N - 1 \rbrace$ をビットで表した整数を添字として、長さ $2^N$ のリストで表します。 $h(S)$ は、 $T \cup U = S$ となる組を足す OR 畳み込みのうち、 $T \cap U = \emptyset$ となる組だけを足したものです。 $T \cup U = S$ のとき、 $T \cap U = \emptyset$ は $\lvert T \rvert + \lvert U \rvert = \lvert S \rvert$ と同じなので、要素数ごとに分けて考えます。要素数が $i$ の集合での値だけを残した $f_i$, $g_i$ をゼータ変換して $F_i$, $G_i$ とし、 $S$ ごとに $H_k(S) = \sum_{i + j = k} F_i(S) G_j(S)$ を求めます。 $H_k$ をメビウス変換したものの $S$ での値が、 $k = \lvert S \rvert$ のとき $h(S)$ です（ランク付きゼータ変換）。

- `subset_convolution(f, g, mod)`: $h(S) = \sum_{T \subseteq S} f(T) g(S \setminus T)$ のリストを返す。 $O(N^2 2^N)$

`f` と `g` は同じ長さ（ $2$ のべき）にします。各値を `mod`（既定値は $998244353$）で割った余りで返します。逆元を使わないので、`mod` は素数でなくてもかまいません。渡したリストは書き換えません。メモリは $O(N 2^N)$ です。

例（頂点の集合 $S$ を 2 つの独立集合 $T$, $S \setminus T$ に分ける方法の数。 $S$ が誘導する部分グラフを 2 色で塗り分ける方法の数です）:

```python
N = 3
edges = [(0, 1), (1, 2)]
ind = [1] * (1 << N)  # ind[T] = (T が独立集合なら 1、そうでなければ 0)
for T in range(1 << N):
    for u, v in edges:
        if T >> u & 1 and T >> v & 1:
            ind[T] = 0
print(subset_convolution(ind, ind))  # [1, 2, 2, 2, 2, 4, 2, 2]
```

$T$ と $U$ が交わってもよい OR 畳み込みは [XOR・AND・OR 畳み込み](bitwise_convolution.html) で、部分集合にわたる和だけが欲しいときは [高速ゼータ変換・メビウス変換](zeta_mobius.html) で求められます。
