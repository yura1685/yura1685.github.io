---
title: 二重辺連結成分分解・Block-Cut Tree
category: グラフ
description: 無向グラフを、橋で切った成分（二重辺連結成分）や、関節点で切ったブロック（二重頂点連結成分）に分け、木として扱えるようにする
order: 15
---

[lowlink](lowlink.html) を使って、DFS 木の辺ごとに「その辺で上下が切れるか」を判定し、上から順に成分を決めます。再帰は使いません。多重辺や自己ループ、非連結なグラフでも正しく動きます。

- `two_edge_connected_components(n, edges)`: 頂点数 $n$ と無向辺のリスト `edges = [(u, v), ...]` から、二重辺連結成分の個数 $k$ と、各頂点の成分番号のリスト `comp`（ $0$ 以上 $k$ 未満）の組を返す。 $O(N + M)$
- `block_cut_tree(n, edges)`: ブロックの頂点のリスト `blocks` と、Block-Cut Tree の隣接リスト `tree` の組を返す。 $O(N + M)$

二重辺連結成分は、どの辺を 1 本取り除いても連結なままの頂点の集まりです。成分を 1 つの頂点にまとめると、橋だけが残って森になります。

```python
k, comp = two_edge_connected_components(n, edges)
tree = [[] for _ in range(k)]
for u, v in edges:
    if comp[u] != comp[v]:  # 橋
        tree[comp[u]].append(comp[v])
        tree[comp[v]].append(comp[u])
```

ブロックは、どの頂点を 1 つ取り除いても連結なままの、辺の集まりの極大なものです（頂点 2 つと辺 1 本だけのものも含みます）。関節点は複数のブロックに入ります。Block-Cut Tree の頂点 $0, \ldots, n - 1$ は元の頂点、 $n + i$ は $i$ 番目のブロックで、頂点とそれを含むブロックを辺で結びます。森になり、元のグラフで $u$ から $v$ への道が必ず通る頂点は、木での $u$ - $v$ パス上の元の頂点です。関節点は、木での次数が $2$ 以上の元の頂点です。孤立点は頂点 1 つのブロックになります。
