---
title: 木のパス上の値の集約（ダブリング）
category: 木
description: 辺に重みがある木で、2 頂点を結ぶパス上の重みの最大値・最小値・和などをダブリングで $O(\log N)$ で求める
order: 9
---

[LCA](lca.html) と同じく根からの BFS で親と深さを求め（再帰なし）、 $v$ の $2^k$ 個上の祖先と、そこまでの $2^k$ 本の辺の重みを `op` でまとめた値の表を作ります。 $u$ と $v$ を LCA まで持ち上げるときに飛んだ区間の値をまとめると、パス上の辺の重みをまとめた値になります。

`op` は結合的で可換な演算（最大値・最小値・和・gcd など）に限ります。パスの $u$ 側と $v$ 側を、向きや順番を気にせずにまとめるためです。

- `TreeDoubling(n, edges, op, e, root=0)`: 頂点数 $n$、木の辺のリスト `edges = [(u, v, w), ...]`、演算 `op` とその単位元 `e`、根から前計算。 $O(N \log N)$
- `query(u, v)`: $u$ と $v$ を結ぶパス上の辺の重みを `op` でまとめた値（ $u = v$ なら `e`）。 $O(\log N)$
- `lca(u, v)`: $u$ と $v$ の最小共通祖先。 $O(\log N)$
- `up[k][v]`, `val[k][v]`: $v$ の $2^k$ 個上の祖先（根を越えるときは根）と、そこまでの辺の重みを `op` でまとめた値
- `depth[v]`: 根からの深さ（辺の本数）

`op` と `e` の例は、最大値なら `max` と十分小さい値、最小値なら `min` と十分大きい値、和なら `lambda a, b: a + b` と $0$、gcd なら `math.gcd` と $0$ です。

辺の重みが途中で変わるときは、[HL分解](hld.html) とセグメント木を組み合わせると、重みの更新とパス上の集約をどちらも $O(\log^2 N)$ で処理できます。

例（ABC 235 E。最小全域木に辺 $(u, v, w)$ を加えたとき、木の $u$ と $v$ を結ぶパス上の最大の重みが $w$ より大きければ、その辺を使う最小全域木がある。[最小全域木（Kruskal・Prim）](mst.html) の `kruskal` を使う）:

```python
cost, used = kruskal(n, edges)
td = TreeDoubling(n, [edges[i] for i in used], max, 0)  # 重みは正
for u, v, w in queries:
    print("Yes" if w < td.query(u, v) else "No")
```
