---
title: Miller–Rabin 素数判定
category: 整数論
description: $N < 2^{64}$ の素数判定を、底を固定した Miller–Rabin 法で確実に $O(\log N)$ で行う
order: 7
---

$n - 1 = 2^s d$（ $d$ は奇数）と表し、いくつかの底 $a$ について $a^d, a^{2d}, \ldots, a^{2^{s-1} d} \bmod n$ を調べます。 $n$ が素数なら、 $a^d \equiv 1$ になるか、どこかで $-1$ が現れます。 $n < 2^{64}$ なら、決まった 7 個の底（ $n < 4759123141$ なら 3 個）で調べれば、必ず正しく判定できます。

- `is_prime(n)`: $n$ が素数か（ $0 \le n < 2^{64}$）。 $O(\log n)$ 回の掛け算

$10^{12}$ 程度までなら [試し割り](trial_division.html) でも判定できますが、それより大きいときや、たくさんの数を判定するときに使います。素因数分解には [Pollard's rho 素因数分解](pollard_rho.html) を使います。
