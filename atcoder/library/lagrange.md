---
title: Lagrange 補間
category: 数学
description: $d + 1$ 点を通る $d$ 次以下の多項式 $f$ について、係数を求めずに $f(x)$ を求める。点が $x = 0, 1, \ldots, d$ なら $O(d)$
order: 6
---

$x_0, \ldots, x_d$ が互いに異なるとき、点 $(x_i, y_i)$ をすべて通る $d$ 次以下の多項式は $f(x) = \sum_i y_i \prod_{j \ne i} \frac{x - x_j}{x_i - x_j}$ で、これを mod で計算します。 $x_i = i$ のときは、分子を左右からの累積積、分母を階乗で表せるので $O(d)$ になります。式の導き方は [多項式補間についての記事](../../articles/details.html?file=003_lagrange_interpolation.md) に書いています。

mod は素数で、 $x$ は大きくても負でもかまいません。

- `lagrange(xs, ys, x, mod)`: 点 $(x_i, y_i)$ を通る多項式の $f(x)$。 $x_i$ は mod で互いに異なる。 $O(d^2 + d \log \mathrm{mod})$
- `lagrange_iota(ys, x, mod)`: 点 $(i, y_i)$（ $i = 0, 1, \ldots, d$）を通る多項式の $f(x)$。 $d < \mathrm{mod}$。 $O(d + \log \mathrm{mod})$

答えが $n$ についての $d$ 次多項式になるとわかっているときに、 $n = 0, 1, \ldots, d$ の答えを愚直に求めておき、大きい $n$ での値を求めるのによく使います。

例（ $1^k + 2^k + \cdots + n^k$ は $n$ の $k + 1$ 次多項式）:

```python
mod = 998244353
ys = [0]
for i in range(1, k + 2):
    ys.append((ys[-1] + pow(i, k, mod)) % mod)
print(lagrange_iota(ys, n, mod))
```
