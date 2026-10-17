---
title: HL分解
category: 木
description: 木を heavy path に分けて頂点を並べ、パスや部分木に関するクエリを $O(\log N)$ 個の区間のクエリにする
order: 5
---

各頂点から部分木が最も大きい子への辺を heavy edge とし、heavy edge でつながった頂点が連続するように、DFS の行きがけ順で頂点を並べます。どのパスも $O(\log N)$ 本の heavy path にしかまたがらないので、パス上の頂点は列の $O(\log N)$ 個の区間に分かれます。部分木は 1 つの区間になります。再帰は使いません。

- `HLD(g, root)`: 木の隣接リスト `g[v] = [to, ...]` と根から前計算。 $O(N)$
- `pos[v]`, `order`: 列での $v$ の位置と、位置の順に並べた頂点のリスト（`order[pos[v]] == v`）
- `path(u, v, edge=False)`: $u$ と $v$ を結ぶパス上の頂点の位置を、半開区間 `(l, r)` のリストで返す（区間の順番はばらばら）。`edge=True` にすると LCA を除く。 $O(\log N)$
- `subtree(v)`: $v$ の部分木の頂点の位置を表す半開区間 `(l, r)`。 $O(1)$
- `lca(u, v)`, `dist(u, v)`: 最小共通祖先と距離（辺の本数）。 $O(\log N)$
- `kth_ancestor(v, k)`: $v$ の $k$ 個上の祖先（存在しなければ $-1$）。 $O(\log N)$
- `par[v]`, `depth[v]`, `size[v]`, `head[v]`: 親（根は $-1$）、深さ、部分木の頂点数、 $v$ を含む heavy path のうち最も根に近い頂点

辺に値があるときは、辺 $(\mathrm{par}[v], v)$ の値を位置 `pos[v]` に置き、`edge=True` で区間を求めます。`path` が返す区間は順番がばらばらなので、パス上の値をまとめる演算は可換なもの（和・最大値・xor など）に限ります。

例（頂点の値の更新と、パス上の頂点の値の和。ACL の Fenwick Tree を使う）:

```python
from atcoder.fenwicktree import FenwickTree

hld = HLD(g)
bit = FenwickTree(n)
for i in range(n):
    bit.add(hld.pos[i], a[i])
# 頂点 v の値に x を足す
bit.add(hld.pos[v], x)
# u と v を結ぶパス上の頂点の値の和
s = sum(bit.sum(l, r) for l, r in hld.path(u, v))
```
