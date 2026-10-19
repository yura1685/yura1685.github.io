---
title: SWAG
category: データ構造
description: 結合的な演算（可換でなくてよい）で全体をまとめた値を求められるキュー。各操作ならし $O(1)$
order: 13
---

Sliding Window Aggregation の略で、キューを 2 つのスタックで作ります。先頭側のスタックには、各値とあわせて、そこから底までをまとめた値も積んでおき、先頭側が空のときに末尾側をすべて移します。演算 `op` は結合的であればよく、可換でなくても、先頭から末尾の順にまとめます。`e` はその単位元です。

- `SWAG(op, e)`: 空のキューを作る
- `push(x)`: 末尾に $x$ を加える。 $O(1)$
- `pop()`: 先頭の値を取り除いて返す（空でないときだけ使う）。ならし $O(1)$
- `fold()`: `op(先頭, ..., 末尾)`（空なら `e`）。 $O(1)$
- `len(q)`: 要素数

スライド最小値は単調な deque でも求められますが、SWAG なら `op` を取り替えるだけで、gcd や 1 次関数の合成のような演算にも使えます。

例（長さ $k$ の区間の最小値）:

```python
q = SWAG(min, 1 << 60)
res = []
for i in range(n):
    q.push(a[i])
    if len(q) > k:
        q.pop()
    if len(q) == k:
        res.append(q.fold())  # min(a[i - k + 1:i + 1])
```

例（1 次関数の列 $f_i(x) = b_i x + c_i$ で、長さ $k$ の区間の関数を前から順に通したもの）:

```python
mod = 998244353
# 関数 (b, c) は x を b x + c にする。op(f, g) は f のあとに g をする関数
op = lambda f, g: (f[0] * g[0] % mod, (g[0] * f[1] + g[1]) % mod)
q = SWAG(op, (1, 0))
res = []
for i in range(n):
    q.push(fs[i])
    if len(q) > k:
        q.pop()
    if len(q) == k:
        b, c = q.fold()
        res.append((b * x + c) % mod)  # fs[i - k + 1], ..., fs[i] の順に x を通した値
```
