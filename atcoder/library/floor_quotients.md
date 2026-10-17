---
title: floor(N/i) の商列挙
category: 整数論
description: $i = 1, \ldots, N$ を $\lfloor N / i \rfloor$ の値ごとに区間に分け、 $O(\sqrt{N})$ 個の区間として列挙する
order: 6
---

$\lfloor N / i \rfloor$ がとる値は $O(\sqrt{N})$ 種類しかなく、値が $q$ になる $i$ は $\lfloor N / (q + 1) \rfloor < i \le \lfloor N / q \rfloor$ の範囲にまとまります。

- `floor_ranges(N)`: $l \le i < r$ のとき $\lfloor N / i \rfloor = q$ となる組 $(l, r, q)$ のリストを、 $l$ の小さい順に返す。区間は $1 \le i \le N$ をちょうど覆う。 $O(\sqrt{N})$

例（ $\sum_{i=1}^{N} \lfloor N / i \rfloor$）:

```python
ans = sum((r - l) * q for l, r, q in floor_ranges(n))
```
