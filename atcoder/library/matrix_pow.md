---
title: 行列累乗
category: 数学
description: 行列の積と累乗を mod で計算し、線形漸化式の第 $N$ 項を求める
order: 1
---

- `mat_mul(A, B, mod)`: 行列の積 $AB$ を mod で求める。 $A$ が $N \times M$、 $B$ が $M \times K$ のとき $O(NMK)$
- `mat_pow(A, k, mod)`: 正方行列 $A$ の $k$ 乗（ $k \ge 0$）を求める。 $A$ が $K \times K$ のとき $O(K^3 \log k)$
- mod の既定値は $998244353$

$K$ 項間の線形漸化式は、 $K \times K$ の行列の累乗で第 $N$ 項を $O(K^3 \log N)$ で求められます。

例（フィボナッチ数列の第 $n$ 項。 $F_0 = 0$, $F_1 = 1$）:

```python
A = [[1, 1], [1, 0]]
f = mat_pow(A, n, 10**9 + 7)[0][1]
```
