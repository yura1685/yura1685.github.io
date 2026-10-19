---
title: 素数の個数（Lucy DP）
category: 整数論
description: 整数 $N$ 以下の素数の個数 $\pi(N)$ を、 $\lfloor N / i \rfloor$ の形の値だけを持つ DP（Lucy DP）で $O(N^{3/4} / \log N)$ で求める
order: 12
---

$S(v, p)$ を「 $2$ 以上 $v$ 以下の整数のうち、素数であるか、最小素因数が $p$ より大きいものの個数」とします。 $S(v, 1) = v - 1$ から始めて $p$ を小さい順に増やすと、 $p$ が素数で $p^2 \le v$ のときだけ $S(v, p) = S(v, p - 1) - (S(\lfloor v / p \rfloor, p - 1) - S(p - 1, p - 1))$ と変わり、 $p^2 > v$ になったところで $S(v, p) = \pi(v)$ になります。 $\lfloor \lfloor N / i \rfloor / p \rfloor = \lfloor N / (ip) \rfloor$ なので、 $v$ は $\lfloor N / i \rfloor$ の形の $O(\sqrt{N})$ 個の値（[floor(N/i) の商列挙](floor_quotients.html) を参照）だけを持てば足ります。 $\sqrt{N}$ 以下の $v$ は $v$ を添字に、それより大きい $v = \lfloor N / i \rfloor$ は $i$ を添字にして、2 つのリストで持ちます。

- `prime_count(N)`: $N$ 以下の素数の個数 $\pi(N)$。 $O(N^{3/4} / \log N)$
- `prime_sum(N)`: $N$ 以下の素数の和。同じ DP で、個数の代わりに和を持つ。 $O(N^{3/4} / \log N)$

$N = 10^{11}$ 程度までが目安です。メモリは $O(\sqrt{N})$ です。 $N$ が大きいと `prime_sum` の値は $2^{63}$ を超えるので、PyPy では少し遅くなります（必要なら途中で mod を取ります）。

例:

```python
print(prime_count(pow(10, 10)))  # 455052511
```
