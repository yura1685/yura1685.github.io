---
title: mod 平方根
category: 整数論
description: 素数 $p$ を法として $x^2 \equiv a \pmod{p}$ となる $x$ を、Tonelli–Shanks のアルゴリズムで $O(\log^2 p)$ で求める
order: 13
---

$a \not\equiv 0$ のとき、 $x^2 \equiv a \pmod{p}$ に解があるのは $a^{(p-1)/2} \equiv 1 \pmod{p}$ のときに限ります（オイラーの規準）。 $p - 1 = 2^s q$（ $q$ は奇数）と表し、平方非剰余 $z$ を 1 つ見つけておきます。 $x = a^{(q+1)/2}$, $t = a^q$ から始めると $x^2 \equiv a t$ で、 $t$ の位数は $2$ の冪です。 $z^q$ の冪を掛けて $x^2 \equiv a t$ を保ったまま $t$ の位数を小さくしていき、 $t = 1$ になったときの $x$ が答えです（Tonelli–Shanks のアルゴリズム）。

- `mod_sqrt(a, p)`: $x^2 \equiv a \pmod{p}$ を満たす $x$（ $0 \le x < p$）を 1 つ返す。なければ `-1`。 $p$ は素数（ $p = 2$ でもよい）。 $O(\log^2 p)$（ $z$ を探す部分は期待値）

もう 1 つの解は $p - x$ です（ $a \equiv 0$ のときは $x = 0$ だけ）。 $p \equiv 3 \pmod{4}$ なら $s = 1$ で、 $x = a^{(p+1)/4}$ がそのまま答えになります。
