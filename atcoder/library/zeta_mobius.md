---
title: 高速ゼータ変換・メビウス変換
category: 数学
description: 集合を添字とする $2^N$ 個の値について、部分集合や上位集合にわたる和と、その逆変換を $O(N 2^N)$ で求める
order: 4
---

集合 $S \subseteq \lbrace 0, 1, \ldots, N - 1 \rbrace$ をビットで表した整数を添字として、長さ $2^N$ のリスト `f` で $f(S)$ を表します。1 ビットずつ順に足し込むことで、すべての $S$ について和をまとめて求めます。

- `subset_zeta(f, mod)`: $g(S) = \sum_{T \subseteq S} f(T)$ のリストを返す
- `subset_mobius(g, mod)`: `subset_zeta` の逆変換
- `superset_zeta(f, mod)`: $g(S) = \sum_{T \supseteq S} f(T)$ のリストを返す
- `superset_mobius(g, mod)`: `superset_zeta` の逆変換
- 計算量: どれも $O(N 2^N)$

`mod` を渡すと、各値を `mod` で割った余りで返します（省略すると割らない）。渡したリストは書き換えません。

例（OR 畳み込み $h(S) = \sum_{T \cup U = S} f(T) g(U)$）:

```python
h = subset_mobius([x * y for x, y in zip(subset_zeta(f), subset_zeta(g))])
```

AND 畳み込み（ $T \cap U = S$ について足す）は、`superset_zeta` と `superset_mobius` で同じようにします。
