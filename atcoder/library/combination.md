---
title: 二項係数 (nCr)
category: 整数論
description: 階乗テーブルを前計算して ${}_n\mathrm{C}_r$・${}_n\mathrm{P}_r$・${}_n\mathrm{H}_r$ を素数 $p$ を法として求める
order: 1
---

$0!$ から $N!$ までの階乗とその逆元を前計算します。 mod は $N$ より大きい素数である必要があります。

- `Combination(N, mod)`: 前計算。 mod の既定値は $998244353$。 $O(N)$
- `C(n, r)`: $\binom{n}{r}$。 $r < 0$ や $r > n$ のときは $0$
- `P(n, r)`: $\frac{n!}{(n-r)!}$
- `H(n, r)`: 重複組合せ $\binom{n+r-1}{r}$（ $n + r - 1 \le N$ の範囲で使う）
- `inv(n)`: $n^{-1}$（ $1 \le n \le N$）
- 計算量: 各クエリ $O(1)$
