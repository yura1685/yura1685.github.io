---
title: 2次元BIT
category: データ構造
description: H×W のマス目で、1 点加算または長方形加算と、長方形の和を $O(\log H \log W)$ で求める
order: 15
---

$H \times W$ のマス目の値について、加算と長方形の和をそれぞれ $O(\log H \log W)$ で行います。添字はすべて 0-indexed で、長方形は $\mathrm{x1} \le x < \mathrm{x2}$ かつ $\mathrm{y1} \le y < \mathrm{y2}$ の半開区間で指定します。使う方のクラスだけを貼れば動きます。メモリは $O(HW)$ です。

`BIT2D`（1 点加算・長方形の和）:

- `BIT2D(h, w, a)`: $H \times W$ の初期配列 `a`（省略するとすべて $0$）から構築。 $O(HW)$
- `add(x, y, v)`: `a[x][y]` に $v$ を足す
- `sum(x1, y1, x2, y2)`: 長方形の中の値の和
- `prefix(x, y)`: $[0, x) \times [0, y)$ の値の和
- `get(x, y)`: `a[x][y]`
- `set(x, y, v)`: `a[x][y]` を $v$ にする

`RangeBIT2D`（長方形加算・長方形の和）:

- `RangeBIT2D(h, w)`: すべて $0$ で構築
- `add(x1, y1, x2, y2, v)`: 長方形の中のすべての値に $v$ を足す
- `sum(x1, y1, x2, y2)`, `prefix(x, y)`, `get(x, y)`: `BIT2D` と同じ

`RangeBIT2D` は、2 次元の差分 $d$ に対して、 $[0, X) \times [0, Y)$ の和が $\sum d_{x,y} (X - x + 1)(Y - y + 1)$（ $x, y$ は 1-indexed）と書けることを使い、 $d,\ d \cdot y,\ d \cdot x,\ d \cdot xy$ の 4 つを BIT で持ちます。

例:

```python
b = BIT2D(3, 4)
b.add(1, 2, 5)
print(b.sum(0, 0, 2, 3))  # 5

r = RangeBIT2D(3, 4)
r.add(0, 0, 2, 2, 1)
print(r.sum(0, 0, 3, 4))  # 4
```
