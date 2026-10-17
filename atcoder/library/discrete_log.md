---
title: 離散対数
category: 整数論
description: $a^x \equiv b \pmod{m}$ となる最小の $x$ を、Baby-step Giant-step で $O(\sqrt{m})$ で求める
order: 9
---

$n = \lfloor \sqrt{m} \rfloor + 1$ として $x = i n - j$（ $0 \le j \le n$）と表し、 $b a^j$ を辞書に入れておいてから、 $a^{i n}$ を $i = 1, 2, \ldots$ の順に調べます（Baby-step Giant-step）。 $a$ と $m$ が互いに素でないときは、 $\gcd(a, m)$ で両辺と $m$ を割ることを繰り返して、互いに素な場合に直します。

- `discrete_log(a, b, m)`: $a^x \equiv b \pmod{m}$ を満たす最小の $x \ge 0$。なければ `None`。 $m$ は素数でなくてもよい。 $O(\sqrt{m})$

$0^0 = 1$ として扱います。辞書に $\sqrt{m}$ 個ほど入れるので、 $m$ は $10^{12}$ 程度までが目安です。
