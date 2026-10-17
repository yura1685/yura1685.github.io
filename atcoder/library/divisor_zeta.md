---
title: 約数系ゼータ変換・メビウス変換
category: 整数論
description: $1$ から $N$ を添字とする値について、約数や倍数にわたる和と、その逆変換を $O(N \log \log N)$ で求める
order: 11
---

素数 $p$ ごとに「 $f(i)$ を $f(ip)$ に足す」ことを繰り返すと、約数にわたる和になります。[高速ゼータ変換](zeta_mobius.html) でビットを 1 つずつ見るところを、素因数の指数を 1 つずつ見るのに変えたものです。リストの添字は $1$ から $N$ までを使い、 $0$ 番目は使いません。

- `divisor_zeta(f, mod)`: $g(n) = \sum_{d \mid n} f(d)$ のリストを返す
- `divisor_mobius(g, mod)`: `divisor_zeta` の逆変換
- `multiple_zeta(f, mod)`: $g(n) = \sum_{n \mid m} f(m)$（ $m \le N$）のリストを返す
- `multiple_mobius(g, mod)`: `multiple_zeta` の逆変換
- 計算量: どれも $O(N \log \log N)$

`mod` を渡すと、各値を `mod` で割った余りで返します（省略すると割らない）。渡したリストは書き換えません。 $f(1) = 1$ でそれ以外が $0$ のリストに `divisor_mobius` を使うと、メビウス関数 $\mu(n)$ の表になります。

例（gcd 畳み込み $h(k) = \sum_{\gcd(i, j) = k} f(i) g(j)$）:

```python
F, G = multiple_zeta(f), multiple_zeta(g)
h = multiple_mobius([x * y for x, y in zip(F, G)])
```

lcm 畳み込み（ $\mathrm{lcm}(i, j) = k \le N$ となる組について足す）は、`divisor_zeta` と `divisor_mobius` で同じようにします。
