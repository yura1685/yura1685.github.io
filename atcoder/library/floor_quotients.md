---
title: floor(n/i) の商列挙
category: 整数論
description: $\lfloor n / i \rfloor$ の値ごとの区間を、 $O(\sqrt{n})$ 個列挙する
order: 6
---

$\lfloor n / i \rfloor$ がとる値は $O(\sqrt{n})$ 種類しかなく、値が $q$ になる $i$ は $\lfloor n / (q + 1) \rfloor < i \le \lfloor n / q \rfloor$ の範囲にまとまります。

- `floor_ranges(n)`: $l \le i < r$ のとき $\lfloor n / i \rfloor = q$ となる組 $(l, r, q)$ のリストを、 $l$ の小さい順に返す。区間は $1 \le i \le n$ をちょうど覆う。 $O(\sqrt{n})$

例（ $\sum_{i=1}^{n} \lfloor n / i \rfloor$）:

```python
ans = sum((r - l) * q for l, r, q in floor_ranges(n))
```
