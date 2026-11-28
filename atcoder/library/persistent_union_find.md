---
title: 完全永続 Union-Find
category: データ構造
description: どの版からでも unite して新しい版を作れる Union-Find。各操作 $O(\log^2 N)$
order: 19
---

各頂点の親（根なら集合の大きさに $-1$ を掛けた値）を並べた配列を、 [永続配列](persistent_array.html) と同じ考え方で持ちます。配列を二分木で表し、書き換えるときは根からその要素までの道のノードだけを複製するので、書き換える前の版もそのまま残ります。このファイルに永続配列（`_get` と `_set`）も入れてあるので、これだけで動きます。

経路圧縮をせず union by size だけを行うので、根にたどり着くまでに配列を読むのは $O(\log N)$ 回で、1 回読むのに $O(\log N)$ かかります。

版は番号で表し、初期状態が版 $0$ です。`unite` で新しい版ができるたびに、1 から順に番号を振ります。

- `PersistentUnionFind(n)`: $n$ 頂点で初期化。何もつないでいない状態が版 $0$。 $O(\log N)$（初めはすべての要素が同じなので、木の各段のノードを 1 つにまとめられる）
- `unite(ver, a, b)`: 版 $\mathrm{ver}$ で $a$ と $b$ をつないだ新しい版の番号を返す。版 $\mathrm{ver}$ は変わらない。すでに同じ集合なら新しい版は作らず、`ver` をそのまま返す（なので、返り値が `ver` と等しいかで、つないだかがわかる）。 $O(\log^2 N)$ で、メモリが $O(\log N)$ 増える
- `find(ver, x)`: 版 $\mathrm{ver}$ での $x$ の根。 $O(\log^2 N)$
- `same(ver, a, b)`: 版 $\mathrm{ver}$ で $a$ と $b$ が同じ集合にあるか。 $O(\log^2 N)$
- `size(ver, x)`: 版 $\mathrm{ver}$ での $x$ を含む集合の大きさ。 $O(\log^2 N)$

クエリをすべて先読みできる問題なら、版を頂点、`unite` を辺とする木（版の木）を作って根から DFS し、辺を下るときにつなぎ、戻るときに取り消すようにすると、 [ロールバック付き Union-Find](rollback_union_find.html) で同じことができます。そちらの方が速く、メモリも少なくて済みます。

例:

```python
uf = PersistentUnionFind(4)
v1 = uf.unite(0, 0, 1)  # 版 0 で 0 と 1 をつなぐ
v2 = uf.unite(v1, 2, 3)  # 版 v1 で 2 と 3 をつなぐ
v3 = uf.unite(v1, 1, 2)  # 版 v1 から枝分かれして 1 と 2 をつなぐ
print(uf.same(v2, 0, 3), uf.same(v3, 0, 2), uf.same(v3, 2, 3))  # False True False
print(uf.size(v2, 2), uf.size(v3, 0), uf.size(0, 0))  # 2 3 1
print(uf.unite(v3, 0, 2) == v3)  # True（すでに連結なので版は変わらない）

# i 番目のクエリ (k, a, b): ver[k] の版で a と b をつないだものを ver[i] とする（ver[0] は初期状態）
uf = PersistentUnionFind(n)
ver = [0] * (len(queries) + 1)
for i, (k, a, b) in enumerate(queries, 1):
    ver[i] = uf.unite(ver[k], a, b)
```
