---
title: 拡張ユークリッドの互除法・中国剰余定理
category: 整数論
description: $ax + by = \gcd(a, b)$ となる整数 $x, y$ や、 $m$ を法とする 1 次合同式の解、中国剰余定理で連立合同式の解を求める
order: 4
---

ユークリッドの互除法の商を使って、 $ax + by = \gcd(a, b)$ を満たす $(x, y)$ を再帰を使わずに求めます。

- `ext_gcd(a, b)`: $ax + by = g$ を満たす $(g, x, y)$ を返す。 $g = \gcd(a, b) \ge 0$ で、 $a, b$ は負でもよい。 $O(\log \max(\lvert a \rvert, \lvert b \rvert))$
- `linear_congruence(a, b, m)`: $ax \equiv b \pmod{m}$ の解全体を $x \equiv x_0 \pmod{m^\prime}$ と表して $(x_0, m^\prime)$ を返す（ $0 \le x_0 < m^\prime$、 $m^\prime = m / \gcd(a, m)$）。解がなければ `None`。 $O(\log m)$
- `crt(r, m)`: 中国剰余定理。 $x \equiv r_i \pmod{m_i}$（ $i = 0, \ldots, K - 1$）をすべて満たす $x$ 全体を $x \equiv x_0 \pmod{M}$ と表して $(x_0, M)$ を返す（ $0 \le x_0 < M$、 $M = \mathrm{lcm}(m_0, \ldots, m_{K-1})$）。 $m_i \ge 1$ は互いに素でなくてもよい。解がなければ `None`。 $O(K \log M)$

$ax + by = c$ の整数解は、 $c$ が $g$ の倍数のときだけあります。`ext_gcd` の $(x, y)$ を $c / g$ 倍したものが 1 つの解で、すべての解は整数 $t$ を使って $(x c / g + t b / g, y c / g - t a / g)$ と表せます。

$a$ と $m$ が互いに素なときの $a$ の逆元は、Python 3.8 以降なら `pow(a, -1, m)` でも求められます。

例（ $x \equiv 2 \pmod{3}$、 $x \equiv 3 \pmod{5}$、 $x \equiv 2 \pmod{7}$）:

```python
print(crt([2, 3, 2], [3, 5, 7]))  # (23, 105)
```
