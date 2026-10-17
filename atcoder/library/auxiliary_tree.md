---
title: Auxiliary Tree
category: 木
description: 木の頂点の集合 $S$ について、 $S$ の頂点とそれらの LCA だけからなる、頂点数 $O(\lvert S \rvert)$ の木を作る
order: 8
---

指定された頂点を DFS の行きがけ順に並べ、隣り合う 2 頂点の LCA を加えると、どの 2 頂点の LCA もその中に含まれます。それらを行きがけ順にスタックで親子づけすると、元の木の祖先と子孫の関係を保った小さな木（Auxiliary Tree）ができます。頂点の集合ごとの木 DP を、集合の大きさの合計に比例する時間で行えます。再帰は使いません。

- `AuxiliaryTree(g, root)`: 木の隣接リスト `g[v] = [to, ...]` と根から前計算。 $O(N \log N)$
- `build(vs)`: 頂点のリスト `vs` から Auxiliary Tree を作り、`(頂点のリスト, 親のリスト)` を返す。頂点は行きがけ順に並び、親のリストの $i$ 番目は $i$ 番目の頂点の親（Auxiliary Tree の根は $-1$）。 $O(K \log N)$（ $K$ は `vs` の長さ）
- `lca(u, v)`: 最小共通祖先。 $O(\log N)$
- `is_ancestor(u, v)`: $u$ が $v$ の祖先か（ $u = v$ のときも `True`）。 $O(1)$
- `depth[v]`, `tin[v]`: 根からの深さと、行きがけ順での番号

Auxiliary Tree の辺 $(p, v)$ は、元の木の長さ $\mathrm{depth}[v] - \mathrm{depth}[p]$ のパスに当たります。辺に重みがあるときは、根からの重み付きの距離を別に求めておき、その差を使います。頂点のリストを後ろから見ると子が親より先に来るので、そのまま木 DP ができます。

例（`vs` の頂点をすべて含む最小の部分木の辺の本数）:

```python
at = AuxiliaryTree(g)
nodes, par = at.build(vs)
ans = sum(at.depth[v] - at.depth[p] for v, p in zip(nodes, par) if p != -1)
```
