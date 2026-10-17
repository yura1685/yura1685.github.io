---
title: 遅延セグ木（ACL）の使い方
category: データ構造
description: ACL の LazySegTree に渡す関数を、区間加算・区間更新・区間アフィン変換と、区間の最小値・最大値・和などの組み合わせごとにまとめる
order: 1
---

ACL（`atcoder.lazysegtree`）の遅延セグ木は、列の値をまとめる演算と、区間に一括で作用させる操作を自分で渡して使います。区間はすべて半開区間 $[l, r)$ で、各操作は $O(\log N)$ です。

`LazySegTree(op, e, mapping, composition, id_, v)` に渡すもの:

- `op(x, y)`: 値を 2 つまとめる結合的な演算。`e` はその単位元
- `mapping(f, x)`: 作用 $f$ を値 $x$ に作用させた結果
- `composition(f, g)`: 作用 $g$ のあとに $f$ をすること（ $f \circ g$）を 1 つの作用にしたもの。 $f$ が新しく来た方
- `id_`: 何もしない作用
- `v`: 初期の列（または長さ $N$ を渡すとすべて `e`）

おもなメソッドは `apply(l, r, f)`（区間に作用）、`apply(p, f)`（1 点に作用）、`prod(l, r)`、`all_prod()`、`get(p)`、`set(p, x)`、`max_right(l, g)`、`min_left(r, g)` です。

和を求めるときは、足す量が区間の長さに比例するので、値を (和, 区間の長さ) の組にして、初期の列を `[(x, 1) for x in a]` とします。区間更新では、何もしない作用を `None` で表します。

以下のコードは、列 `a` から `seg` を作るところまでです。

## 区間加算・区間最小値

{% include code.html file="lazy_segtree_add_min.py" %}

## 区間加算・区間最大値

{% include code.html file="lazy_segtree_add_max.py" %}

## 区間加算・区間和

{% include code.html file="lazy_segtree_add_sum.py" %}

## 区間更新・区間最小値

{% include code.html file="lazy_segtree_update_min.py" %}

## 区間更新・区間最大値

{% include code.html file="lazy_segtree_update_max.py" %}

## 区間更新・区間和

{% include code.html file="lazy_segtree_update_sum.py" %}

## 区間アフィン変換・区間和

作用 $(b, c)$ は、区間の各値 $x$ を $bx + c$ にします。2 つの作用の合成は、 $x \mapsto b_2 (b_1 x + c_1) + c_2 = b_1 b_2 x + (b_2 c_1 + c_2)$ です。区間加算は $(1, c)$、区間更新は $(0, c)$ で表せるので、加算と更新が混ざるときにも使えます。

{% include code.html file="lazy_segtree_affine_sum.py" %}

## 区間加算・区間最小値とその個数

すべての値が $0$ 以上のとき、区間の $0$ の個数（最小値が $0$ のときの個数）を求めるのに使えます。

{% include code.html file="lazy_segtree_add_min_count.py" %}

## 0/1 の列の区間反転・区間の 1 の個数

{% include code.html file="lazy_segtree_flip_sum.py" %}
