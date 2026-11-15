---
title: 形式的冪級数（FPS）
category: 数学
description: mod $998244353$ の形式的冪級数 $f$ について、 $1 / f$・ $\log f$・ $\exp f$・ $f^k$ の最初の $N$ 項をニュートン法で $O(N \log N)$ で求める
order: 8
---

係数のリスト `f`（ $f_i$ が $x^i$ の係数）で形式的冪級数を表し、mod $998244353$ で計算します。どれも、 $x^m$ 未満の項が正しい $g$ から $x^{2m}$ 未満の項が正しいものを作ることを繰り返すニュートン法です。 $1 / f$ は $g \leftarrow g (2 - f g)$、 $\log f$ は $\int f^\prime / f$、 $\exp f$ は $g \leftarrow g (1 + f - \log g)$ で求めます。 $f^k$ は $f = c x^d g$（ $g_0 = 1$）と表して、 $c^k x^{dk} \exp(k \log g)$ で求めます。畳み込みには、原始根 $3$ を使う NTT（数論変換）を中に書いています（ACL などは使いません）。

- `fps_inv(f, n)`: $1 / f$ の最初の $n$ 項。 $f_0 \ne 0$。 $O(n \log n)$
- `fps_log(f, n)`: $\log f$ の最初の $n$ 項。 $f_0 = 1$。 $O(n \log n)$
- `fps_exp(f, n)`: $\exp f$ の最初の $n$ 項。 $f_0 = 0$。 $O(n \log n)$
- `fps_pow(f, k, n)`: $f^k$ の最初の $n$ 項。 $f_0 = 0$ でもよく、 $k \ge 0$ は $10^{18}$ のように大きくてもよい（ $k = 0$ のときは $1$）。 $O(n \log n)$
- `fps_sqrt(f, n)`: $f_0 = 1$ のとき、定数項が $1$ の $\sqrt{f}$ の最初の $n$ 項。 $O(n \log n)$
- `fps_diff(f)`, `fps_integral(f)`: 微分 $f^\prime$ と、定数項を $0$ とする積分 $\int f$。 $O(\mathrm{len}(f))$
- `_convolution(a, b)`: 2 つの列の畳み込み $c_k = \sum_{i + j = k} a_i b_j$ を mod $998244353$ で求めたリスト。これだけを mod $998244353$ の畳み込みとして使ってもよい。 $O(L \log L)$（ $L = \mathrm{len}(a) + \mathrm{len}(b)$）

`n` をとる関数は長さ $n$ のリストを返します。`f` の長さは $n$ と違ってもよく、足りない項は $0$ とみなします。渡したリストは書き換えません。`fps_exp` と `fps_pow` は中で `fps_log` を何度も呼ぶので、`fps_inv` より数倍遅いです。

例（分割数とフィボナッチ数。 $\prod_{i \ge 1} 1 / (1 - x^i)$ の $\log$ は $\sum_{m \ge 1} \sigma(m) x^m / m$ で、 $\sigma(m)$ は $m$ の約数の和）:

```python
mod = 998244353
n = 10
s = [0] * n  # s[m] = m の約数の和
for i in range(1, n):
    for j in range(i, n, i):
        s[j] += i
a = [s[m] * pow(m, mod - 2, mod) % mod for m in range(n)]
print(fps_exp(a, n))  # [1, 1, 2, 3, 5, 7, 11, 15, 22, 30]
print(fps_inv([1, mod - 1, mod - 1], n))  # 1 / (1 - x - x^2) = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
```

分母と分子が多項式の $P(x) / Q(x)$ で、 $N$ が大きく第 $N$ 項だけが欲しいときは、[線形漸化式（Bostan–Mori・Berlekamp–Massey）](bostan_mori.html) を使います。
