---
title: LCA
category: 木
description: ダブリングで最小共通祖先・2 頂点間の距離・$k$ 個上の祖先・パス上の $k$ 番目の頂点を求める
order: 1
---

根からの BFS で深さと親を求め（再帰なし）、 $2^i$ 個上の祖先の表を作ります。

- `LCA(g, root)`: 木の隣接リスト `g[v] = [to, ...]` と根から前計算。 $O(N \log N)$
- `lca(u, v)`: $u$ と $v$ の最小共通祖先。 $O(\log N)$
- `dist(u, v)`: $u$ と $v$ の距離（辺の本数）。 $O(\log N)$
- `kth_ancestor(v, k)`: $v$ の $k$ 個上の祖先（存在しなければ $-1$）。 $O(\log N)$
- `jump(u, v, k)`: $u$ から $v$ へのパス上で、 $u$ から $k$ 番目（0-indexed）の頂点（ $k$ が $u$ と $v$ の距離より大きければ $-1$）。 $O(\log N)$
- `depth[v]`: 根からの深さ

辺に重みがある場合は、BFS のときに根からの重み付き距離 `wd` も求めておけば、 $\mathrm{wd}[u] + \mathrm{wd}[v] - 2\,\mathrm{wd}[\mathrm{lca}(u, v)]$ で距離が求まります。
