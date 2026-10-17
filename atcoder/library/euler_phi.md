---
title: オイラーの φ 関数
category: 整数論
description: $1$ 以上 $N$ 以下で $N$ と互いに素な整数の個数 $\varphi(N)$ を、1 つなら $O(\sqrt{N})$、表なら $O(N \log \log N)$ で求める
order: 5
---

$N$ を割り切る素数を $p_1, \ldots, p_k$ とすると $\varphi(N) = N (1 - 1/p_1) \cdots (1 - 1/p_k)$ であることを使います。

- `euler_phi(N)`: $\varphi(N)$（ $N \ge 1$）。試し割りで素因数を求める。 $O(\sqrt{N})$
- `phi_table(N)`: `phi[x]` が $\varphi(x)$ になるリスト（ $0 \le x \le N$、`phi[0]` は $0$）を返す。篩で、素数 $p$ の倍数をまとめて処理する。 $O(N \log \log N)$

$a$ と $N$ が互いに素なとき $a^{\varphi(N)} \equiv 1 \pmod{N}$ が成り立ちます（オイラーの定理）。また、分母が $N$ の既約分数で $0$ より大きく $1$ 以下のものは $\varphi(N)$ 個あります。
