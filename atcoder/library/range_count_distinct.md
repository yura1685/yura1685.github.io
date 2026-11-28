---
title: 区間の種類数
category: データ構造
description: 区間に含まれる値の種類数を、オフラインで $O((N + Q) \log N)$ で求める
order: 23
---

クエリを右端 $r$ の小さい順に処理します。列を左から 1 つずつ見ていき、各値について、それまでで最後に出てきた位置にだけ $1$ を置いた列を BIT（Fenwick Tree）で持ちます。 $a_{r-1}$ まで見たとき、 $a_l, \ldots, a_{r-1}$ に含まれる値の種類数は、位置 $l$ 以上に置かれた $1$ の個数です。値 $x$ が区間に含まれることと、 $a_0, \ldots, a_{r-1}$ で $x$ が最後に出てきた位置が $l$ 以上であることは同じだからです。クエリを先にすべて読んでおく必要があります（オフライン）。

- `range_count_distinct(a, queries)`: 列 $a$ と区間のリスト `queries = [(l, r), ...]`（半開区間 $[l, r)$、 $0 \le l \le r \le N$）について、`a[l:r]` に含まれる値の種類数をクエリの順に並べたリストで返す。値はハッシュできれば何でもよい。 $O((N + Q) \log N)$

クエリを先読みできない（オンライン）ときは [永続セグ木](persistent_segtree.html) を使うと、1 クエリ $O(\log N)$ で答えられます。 $a_i$ を 1 つ見るごとに上の列を新しい版として残しておけば、区間 $[l, r)$ の答えは $a_{r-1}$ まで見た版の $[l, r)$ の和です（下の 2 つ目の例）。または、 $a_i$ と同じ値が $i$ より前に最後に出てきた位置を $p_i$（なければ $-1$）とすると、種類数は $l \le i < r$ かつ $p_i < l$ となる $i$ の個数なので、版 $i$ に $p_0, \ldots, p_{i-1}$ の値ごとの個数を持たせて（`RangeKth` と同じ形）、版 $r$ と版 $l$ の差から求めることもできます。

[Mo's algorithm](mo.html) のページの例と同じ問題で、そちらでも（オフラインで）求められますが、こちらの方が速いです。

例:

```python
a = [1, 2, 1, 3, 2, 2]
print(range_count_distinct(a, [(0, 6), (1, 3), (2, 2), (3, 6), (5, 6)]))  # [3, 2, 0, 2, 1]
```

例（[永続セグ木](persistent_segtree.html) の `PersistentSegTree` を使って、オンラインで答える）:

```python
seg = PersistentSegTree([0] * len(a), lambda x, y: x + y, 0)
ver = [0]  # ver[r] = a[r - 1] まで見た版
last = {}
for i, x in enumerate(a):
    v = ver[-1]
    if x in last:
        v = seg.set(v, last[x], 0)  # 前に出てきた位置の 1 を消す
    last[x] = i
    ver.append(seg.set(v, i, 1))
print(seg.prod(ver[6], 0, 6), seg.prod(ver[3], 1, 3))  # 3 2
```
