---
title: 拡張ユークリッドの互除法
category: 整数論
description: $ax + by = \gcd(a, b)$ となる整数 $x, y$ や、 $m$ を法とする 1 次合同式の解を求める
order: 4
---

ユークリッドの互除法の商を使って、 $ax + by = \gcd(a, b)$ を満たす $(x, y)$ を再帰を使わずに求めます。

- `ext_gcd(a, b)`: $ax + by = g$ を満たす $(g, x, y)$ を返す。 $g = \gcd(a, b) \ge 0$ で、 $a, b$ は負でもよい。 $O(\log \max(\lvert a \rvert, \lvert b \rvert))$
- `linear_congruence(a, b, m)`: $ax \equiv b \pmod{m}$ の解全体を $x \equiv x_0 \pmod{m'}$ と表して $(x_0, m')$ を返す（ $0 \le x_0 < m'$、 $m' = m / \gcd(a, m)$）。解がなければ `None`。 $O(\log m)$

$ax + by = c$ の整数解は、 $c$ が $g$ の倍数のときだけあります。`ext_gcd` の $(x, y)$ を $c / g$ 倍したものが 1 つの解で、すべての解は整数 $t$ を使って $(x c / g + t b / g, y c / g - t a / g)$ と表せます。

$a$ と $m$ が互いに素なときの $a$ の逆元は、Python 3.8 以降なら `pow(a, -1, m)` でも求められます。
