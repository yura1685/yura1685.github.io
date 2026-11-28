---
title: 任意 mod の二項係数
category: 整数論
description: 素数とは限らない $m$ を法とする $\binom{n}{k}$ を求める（ $n \le 10^{18}$ ）
order: 14
---

$m = p_1^{e_1} p_2^{e_2} \cdots$ と素因数分解し、 $q = p^e$ ごとに $\binom{n}{k} \bmod q$ を求めてから中国剰余定理でまとめます。 $\binom{n}{k}$ を割り切る $p$ の指数 $v$ は、 $k$ と $n - k$ を $p$ 進数で足したときの繰り上がりの回数です（Kummer の定理）。 $v \ge e$ なら $\binom{n}{k} \equiv 0 \pmod{q}$ です。

$n!$ を $p$ で割れるだけ割ったものを $F(n)$、 $1$ 以上 $i$ 以下で $p$ の倍数でない整数の積を $q$ で割った余りを $T(i)$ とすると、 $F(n) \equiv T(q - 1)^{\lfloor n / q \rfloor} T(n \bmod q) F(\lfloor n / p \rfloor) \pmod{q}$ が成り立ちます。 $T(q - 1)$ は $p = 2$, $e \ge 3$ のときだけ $1$ で、それ以外は $-1$ です。 $q$ 未満の $T$ の表を前計算しておけば、 $\binom{n}{k} \equiv p^v F(n) / (F(k) F(n - k)) \pmod{q}$ を、 $n$ を $p$ で割っていきながら求められます（Granville による Lucas の定理の拡張）。

- `BinomialAnyMod(m)`: $m \ge 1$ を法として前計算する。 $m$ を割り切る素数べき $q$ ごとに長さ $q$ の表を作る。 $O(m)$
- `C(n, k)`: $\binom{n}{k} \bmod m$（ $k < 0$ や $k > n$ のときは $0$）。 $0 \le n \le 10^{18}$ でよい。 $O(\omega(m) \log n)$（ $\omega(m)$ は $m$ の素因数の種類数）

表の大きさの合計は $m$ 以下なので、 $m$ は $10^7$ 程度までが目安です。 $m$ が $998244353$ のような大きい素数で $n$ が小さいときは [二項係数 (nCr)](combination.html) を、 $m$ が小さい素数なら [Lucas の定理](lucas.html) を使っても求められます。

例:

```python
B = BinomialAnyMod(pow(10, 6))
print(B.C(100, 50))  # 497256
print(B.C(pow(10, 18) - 1, 12345))  # 499999
```
