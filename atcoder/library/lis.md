---
title: LIS
category: DP
description: 最長増加部分列を二分探索で $O(N \log N)$ で求める（復元付き）
order: 1
---

「長さ $k$ の増加部分列の末尾としてありうる最小の値」を配列で持ち、二分探索で更新します。

- `lis(a, strict=True)`: 最長増加部分列を 1 つ、値のリストで返す（長さは `len(lis(a))`）。`strict=False` にすると、等しい値を許す広義単調増加になる
- `lis_indices(a, strict=True)`: 最長増加部分列を 1 つ、添字の昇順のリストで返す
- `lis_lengths(a, strict=True)`: `res[i]` が「`a[i]` で終わる最長増加部分列の長さ」であるリストを返す
- 計算量: $O(N \log N)$

最長減少部分列は、各要素の符号を反転した列の LIS として求まります。

例（最長増加部分列のどれかに含まれる位置 $i$ をすべて求める）: `a[i]` から始まる最長増加部分列の長さは、反転して符号を変えた列の `lis_lengths` で求まります。

```python
left = lis_lengths(a)
right = lis_lengths([-x for x in reversed(a)])[::-1]  # right[i] = a[i] から始まる最長増加部分列の長さ
m = max(left, default=0)
ans = [i for i in range(len(a)) if left[i] + right[i] - 1 == m]
```
