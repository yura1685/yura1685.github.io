---
title: Lucas の定理
category: 整数論
description: 小さい素数 $p$ を法とする二項係数 ${}_n\mathrm{C}_r$ を、 $n$ と $r$ を $p$ 進数で表して求める
order: 10
---

$n$ と $r$ を $p$ 進数で表したときの各桁を $n_i$, $r_i$ とすると、 $\binom{n}{r} \equiv \prod_i \binom{n_i}{r_i} \pmod{p}$ が成り立ちます（Lucas の定理）。 $p$ 未満の階乗とその逆元を前計算しておけば、 $n$ や $r$ が $p$ より大きくても求められます。

- `Lucas(p)`: 素数 $p$ を法として前計算。 $O(p)$
- `C(n, r)`: ${}_n\mathrm{C}_r \bmod p$（ $r < 0$ や $r > n$ のときは $0$）。 $O(\log_p n)$

$p$ が $N$ より大きいときは、普通の [二項係数](combination.html) で十分です。 $p = 2$ のときは、「 ${}_n\mathrm{C}_r$ が奇数になるのは、 $r$ のビットがすべて $n$ のビットに含まれる（`(n & r) == r`）ときに限る」という形でもよく使います。
