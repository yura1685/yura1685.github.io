---
title: 線形漸化式（Bostan–Mori・Berlekamp–Massey）
category: 数学
description: $d$ 項間の線形漸化式の第 $N$ 項を $O(d^2 \log N)$ で求め、数列の最初の $2d$ 項から漸化式そのものを $O(d^2)$ で求める
order: 7
---

$a_i = c_0 a_{i - 1} + c_1 a_{i - 2} + \cdots + c_{d - 1} a_{i - d}$ を満たす数列の母関数は、 $Q(x) = 1 - c_0 x - \cdots - c_{d - 1} x^d$ と $d - 1$ 次以下の $P(x)$ で $P(x) / Q(x)$ と書けます。Bostan–Mori 法は、分母分子に $Q(-x)$ を掛けて分母を偶関数にし、 $N$ の偶奇で分子の偶数次・奇数次の項だけを残すことで $N$ を半分にしていきます。行列累乗（ $O(d^3 \log N)$）より速いです。

Berlekamp–Massey 法は、数列を満たす最短の線形漸化式を求めます。漸化式が $d$ 項間なら、最初の $2d$ 項があれば正しく求まります。

- `linear_recurrence(a, c, n, mod)`: $a_i = \sum_j c_j a_{i - 1 - j}$（ $i \ge d$）を満たす数列の第 $n$ 項（0-indexed）。`a` は最初の $d$ 項（ $d$ は $c$ の長さ）。 $O(d^2 \log n)$
- `bostan_mori(P, Q, n, mod)`: 形式的冪級数 $P(x) / Q(x)$ の $x^n$ の係数（ $Q_0$ は mod で逆元を持つ）。 $O(d^2 \log n)$
- `berlekamp_massey(a, mod)`: 数列 `a` を満たす最短の漸化式の係数 `c`（`linear_recurrence` にそのまま渡せる形）。mod は素数。 $O(\mathrm{len}(a)^2)$

多項式の掛け算は素朴に $O(d^2)$ でしています。 $d$ が数千を超えるときは、`_mul` を NTT などの畳み込みに替えると $O(d \log d \log n)$ になります。

例（漸化式がわからないが、線形漸化式になると予想できる数列の第 $n$ 項）:

```python
mod = 998244353
a = [...]  # 愚直に求めた最初の数十項
c = berlekamp_massey(a, mod)
print(linear_recurrence(a, c, n, mod))
```
