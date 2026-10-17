---
title: エラトステネスの篩
category: 整数論
description: 最小素因数の表を作り、素数判定・素因数分解・約数列挙を高速に行う（区間篩付き）
order: 2
---

$N$ 以下の各整数の最小素因数（smallest prime factor）を篩で求めておきます。素数の一覧だけでなく、 $N$ 以下の整数を何度も素因数分解するときに便利です。

- `Sieve(N)`: 前計算。 $O(N \log \log N)$
- `primes`: $N$ 以下の素数の昇順リスト
- `spf[x]`: $x$ の最小素因数（ $x \ge 2$）
- `is_prime(x)`: $x$ が素数か（ $0 \le x \le N$）。 $O(1)$
- `factorize(x)`: `[(素因数, 指数), ...]` を素因数の昇順で返す（ $1 \le x \le N$）。 $O(\log x)$
- `divisors(x)`: 約数を昇順で返す（ $1 \le x \le N$）。 $O(d(x) \log d(x))$

## 区間篩

$R$ が大きくても区間の幅 $R - L$ が小さい（ $10^6$ 程度）ときに、 $L$ 以上 $R$ 未満の素数を求めます。 $\sqrt{R}$ 以下の素数で区間 $[L, R)$ だけを篩います。

- `segment_sieve(L, R)`: $L \le x < R$ を満たす素数の昇順リストを返す（ $0 \le L$）。 $O(\sqrt{R} \log \log R + (R - L) \log \log R)$
