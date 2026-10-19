---
title: 双対セグ木
category: データ構造
description: 区間に作用を一括で適用し、1 点の値を求めるセグ木。各操作 $O(\log N)$
order: 14
---

値は葉（元の列）に置いたままにして、各ノードには、そのノードの区間全体にまだ配っていない作用を持たせます。1 点の値は、葉から根までの作用を合成して、元の値に作用させたものです。区間に作用させる前に、上のノードの作用を子に配っておくので、区間更新や区間アフィン変換のように、作用の順番で結果が変わるもの（可換でないもの）にも使えます。

作用の渡し方は ACL の [遅延セグ木](lazy_segtree.html) と同じです。遅延セグ木でも同じことはできますが、区間の値をまとめる演算 `op` と単位元 `e` を用意して、作用がそれと両立するようにしなければなりません。1 点の値だけでよいときは、こちらの方が渡すものが少なく、速いです。

`DualSegTree(a, mapping, composition, id_)` に渡すもの:

- `a`: 初期の列
- `mapping(f, x)`: 作用 $f$ を値 $x$ に作用させた結果
- `composition(f, g)`: 作用 $g$ のあとに $f$ をすること（ $f \circ g$）を 1 つの作用にしたもの。 $f$ が新しく来た方
- `id_`: 何もしない作用

メソッド:

- `apply(l, r, f)`: $l \le i < r$ の各 $a_i$ に $f$ を作用させる。 $O(\log N)$
- `get(p)`: $a_p$ の今の値。 $O(\log N)$
- `set(p, x)`: $a_p$ を $x$ にする。 $O(\log N)$

例:

```python
# 区間加算・1 点取得
seg = DualSegTree(a, lambda f, x: f + x, lambda f, g: f + g, 0)
seg.apply(l, r, x)  # a[l:r] の各値に x を足す
y = seg.get(p)  # a[p]

# 区間 chmin・1 点取得
INF = 1 << 60
seg = DualSegTree(a, min, min, INF)
seg.apply(l, r, x)  # a[l:r] の各値を min(値, x) にする

# 区間更新・1 点取得（作用 None は何もしない）
mapping = lambda f, x: x if f is None else f
composition = lambda f, g: g if f is None else f
seg = DualSegTree(a, mapping, composition, None)
seg.apply(l, r, x)  # a[l:r] をすべて x にする
```
