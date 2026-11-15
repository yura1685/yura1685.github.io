---
title: エラトステネスの篩
category: 整数論
description: 最小素因数の表を作り、素数判定・素因数分解・約数列挙を高速に行う（区間篩付き）
order: 2
---

$n$ 以下の各整数の最小素因数（smallest prime factor）を篩で求めておきます。素数の一覧だけでなく、 $n$ 以下の整数を何度も素因数分解するときに便利です。

- `Sieve(n)`: 前計算。 $O(n \log \log n)$
- `primes`: $n$ 以下の素数の昇順リスト
- `spf[x]`: $x$ の最小素因数（ $x \ge 2$）
- `is_prime(x)`: $x$ が素数か（ $0 \le x \le n$）。 $O(1)$
- `factorize(x)`: `[(素因数, 指数), ...]` を素因数の昇順で返す（ $1 \le x \le n$）。 $O(\log x)$
- `divisors(x)`: 約数を昇順で返す（ $1 \le x \le n$）。 $O(d(x) \log d(x))$

`segment_sieve`（区間篩）:

$r$ が大きくても区間の幅 $r - l$ が小さい（ $10^6$ 程度）ときに、 $l$ 以上 $r$ 未満の素数を求めます。 $\sqrt{r}$ 以下の素数で区間 $[l, r)$ だけを篩います。

- `segment_sieve(l, r)`: $l \le x < r$ を満たす素数の昇順リストを返す（ $0 \le l$）。 $O(\sqrt{r} \log \log r + (r - l) \log \log r)$
