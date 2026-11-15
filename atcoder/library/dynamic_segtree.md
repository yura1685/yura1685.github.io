---
title: 動的セグ木
category: データ構造
description: 添字が $10^{18}$ 程度まで大きくても使えるセグ木。使うノードだけを作り、1 点更新と区間の積を $O(\log n)$ で求める
order: 21
---

列の長さ $n$ が大きく（ $10^{18}$ 程度まで）、普通のセグ木では配列を用意できないときに使います。高さ $\lceil \log_2 n \rceil$ の完全二分木を考え、`set` で値を置くときに、根からその葉までの道にあるノードのうち、まだないものだけを作ります。まだ作っていない部分木の値はすべて `e` なので、ノード $0$ を「値が `e` の空の部分木」として、子がないところはノード $0$ を指すようにしています。ノードはオブジェクトにせず、子の番号と値をリスト `lch`, `rch`, `d` に持たせ、再帰は使いません。

`op` と `e` は ACL のセグ木と同じで、`op` は結合的な演算（可換でなくてよい）、`e` はその単位元です。最初はすべての値が `e` です。区間はすべて半開区間 $[l, r)$ です。

- `DynamicSegTree(n, op, e)`: 長さ $n$ の列（値はすべて `e`）を作る。 $O(\log n)$
- `set(p, x)`: $a_p$ を $x$ にする。ノードは高々 $\lceil \log_2 n \rceil$ 個増える。 $O(\log n)$
- `get(p)`: $a_p$。 $O(\log n)$
- `prod(l, r)`: `op(a[l], ..., a[r - 1])`（ $l = r$ なら `e`）。 $O(\log n)$
- `max_right(l, f)`: `f(op(a[l], ..., a[r - 1]))` が `True` になる最大の $r$（ $l \le r \le n$）。 $O(\log n)$

`max_right` に渡す `f` は、`f(e)` が `True` で、区間を広げると `True` から `False` に変わることはあっても、`False` から `True` には戻らないものとします（ACL のセグ木と同じです）。

`set` を $Q$ 回呼んだときのメモリは $O(Q \log n)$ です。クエリがすべて前もってわかっているときは、使う添字を [座標圧縮](compress.html) して普通のセグ木（ACL の `SegTree`）を使う方が、速くてメモリも少なく済みます。

例:

```python
n = pow(10, 18)
seg = DynamicSegTree(n, lambda x, y: x + y, 0)
seg.set(3, 5)
seg.set(pow(10, 17), 2)
seg.set(n - 1, 7)
print(seg.prod(0, n), seg.prod(4, n - 1), seg.get(3), seg.get(4))  # 14 2 5 0
```

例（ $0$ 以上 $10^{18}$ 未満の整数の多重集合で、小さい方から $k$ 番目の値）:

```python
cnt = DynamicSegTree(pow(10, 18), lambda x, y: x + y, 0)  # cnt[v] = v の個数
for v in [5, pow(10, 17), 5, 42]:
    cnt.set(v, cnt.get(v) + 1)
k = 2  # 0-indexed
print(cnt.max_right(0, lambda s: s <= k))  # 42（v 以下の個数が k より多くなる最小の v）
```
