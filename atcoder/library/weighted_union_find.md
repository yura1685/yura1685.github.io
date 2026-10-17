---
title: 重み付きUnion-Find
category: データ構造
description: 「$b$ の値 $-$ $a$ の値 $= w$」という条件を管理し、矛盾の検出や差の計算を行う
order: 3
---

各頂点に値（ポテンシャル）があると考え、「 $b$ の値 $-$ $a$ の値 $= w$」という条件をまとめて管理します。経路圧縮と union by size を行い、再帰は使いません。

- `WeightedUnionFind(N)`: $N$ 頂点で初期化
- `merge(a, b, w)`: 「 $b$ の値 $-$ $a$ の値 $= w$」という条件を加える。今までの条件と矛盾するときだけ `False` を返す
- `diff(a, b)`: $b$ の値 $-$ $a$ の値（ $a$ と $b$ が同じ集合にあるときだけ使う）
- `weight(a)`: $a$ の値 $-$ $a$ の根の値
- `leader(a)`, `same(a, b)`, `size(a)`: 普通の Union-Find と同じ
- 計算量: ならし $O(\alpha(N))$
