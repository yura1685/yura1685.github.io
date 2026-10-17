---
title: Binary Trie
category: データ構造
description: $2^B$ 未満の整数を上の桁から Trie に入れ、xor した値の最小値・最大値や $k$ 番目に小さい値を $O(B)$ で求める
order: 6
---

$0$ 以上 $2^B$ 未満の整数を $B$ 桁の 2 進数で表し、上の桁から順に Trie の辺としてたどって入れます。同じ値を何個でも入れられ（多重集合）、すべての要素をまとめて xor することもできます。以下、入っている要素を $a$ とします。

- `BinaryTrie(B)`: 空の集合で初期化（既定は $B = 30$。値が $10^{18}$ 程度までなら $B = 60$）
- `add(x, k)`: $x$ を $k$ 個加える（既定は $k = 1$）
- `discard(x, k)`: $x$ を $k$ 個取り除き、取り除いた個数を返す（既定は $k = 1$。入っている個数が少なければすべて取り除く）
- `count(x)`: $x$ の個数
- `xor_all(x)`: すべての要素 $a$ を $a \oplus x$ に変える。 $O(1)$
- `kth(k, y)`: $a \oplus y$ を小さい順に並べたときの $k$ 番目（0-indexed）の値（既定は $y = 0$ で、 $k$ 番目に小さい要素）
- `min_xor(y)`, `max_xor(y)`: $a \oplus y$ の最小値・最大値（空でないときだけ使う）
- `count_less(x, y)`: $a \oplus y < x$ となる要素の個数（既定は $y = 0$ で、 $x$ 未満の要素の個数）
- `len(t)`: 要素の個数
- 計算量: `xor_all` と `len` 以外は $O(B)$

`kth` などは $a \oplus y$ の値を返すので、要素 $a$ そのものが欲しいときは、返り値と $y$ の xor を取ります。ノードは取り除いても消さないので、メモリは加えた値の種類数 $\times B$ に比例します。

例（列から 2 つ選んだときの xor の最大値）:

```python
t = BinaryTrie(30)
ans = 0
for x in a:
    if len(t):
        ans = max(ans, t.max_xor(x))
    t.add(x)
```
