---
title: オイラーの φ 関数
category: 整数論
description: $\varphi(n)$ を 1 つなら $O(\sqrt{n})$ 、表なら $O(n \log \log n)$ で求める
order: 5
---

$n$ を割り切る素数を $p_1, \ldots, p_k$ とすると $\varphi(n) = n (1 - 1/p_1) \cdots (1 - 1/p_k)$ であることを使います。

- `euler_phi(n)`: $\varphi(n)$（ $n \ge 1$）。試し割りで素因数を求める。 $O(\sqrt{n})$
- `phi_table(n)`: `phi[x]` が $\varphi(x)$ になるリスト（ $0 \le x \le n$、`phi[0]` は $0$）を返す。篩で、素数 $p$ の倍数をまとめて処理する。 $O(n \log \log n)$

$a$ と $n$ が互いに素なとき $a^{\varphi(n)} \equiv 1 \pmod{n}$ が成り立ちます（オイラーの定理）。また、分母が $n$ の既約分数で $0$ より大きく $1$ 以下のものは $\varphi(n)$ 個あります。
