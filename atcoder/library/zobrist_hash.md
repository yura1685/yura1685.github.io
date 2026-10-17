---
title: Zobrist ハッシュ
category: 基礎
description: 値ごとに乱数を割り当て、集合や多重集合が等しいかをハッシュで $O(1)$ で判定する
order: 5
---

値 $x$ ごとにランダムな整数 $h(x)$ を割り当て、集合のハッシュを $h(x)$ の XOR、多重集合のハッシュを $h(x)$ の和（ $2^{61} - 1$ で割った余り）で表します。異なる集合のハッシュが一致する確率は、1 回の比較でおよそ $2^{-61}$ です。

- `ZobristHash()`: 空の表で初期化
- `get(x)`: 値 $x$ に割り当てた乱数（初めて使う値には新しく割り当てる）。 $O(1)$
- `prefix_set(a)`: `res[i]` が $a_0, \ldots, a_{i-1}$ に現れる値の集合のハッシュになるリストを返す。 $O(N)$
- `prefix_multiset(a)`: 累積和 `res` を返す。 $a_l, \ldots, a_{r-1}$ の多重集合のハッシュは `(res[r] - res[l]) % MOD`。 $O(N)$

比べたい列どうしには、同じ `ZobristHash` を使います。

例（ $a$ の先頭 $x$ 個と $b$ の先頭 $y$ 個で、現れる値の集合が等しいか）:

```python
Z = ZobristHash()
ha, hb = Z.prefix_set(a), Z.prefix_set(b)
# ha[x] == hb[y] なら等しい
```
