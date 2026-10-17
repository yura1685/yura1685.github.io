---
title: Warshall–Floyd
category: グラフ
description: 全点対間の最短距離を O(N^3) で求める（負の辺・負閉路の検出に対応）
order: 4
---

- `warshall_floyd(n, edges)`: 頂点数 $n$ と有向辺のリスト `edges = [(u, v, w), ...]` から、 $u$ から $v$ への最短距離を `d[u][v]` とする表を返す。到達できないときは `INF`（ $= 2^{60}$）。無向グラフなら両向きの辺を入れる
- 負の辺があっても使える。ある $i$ で `d[i][i] < 0` なら負閉路がある
- 計算量: $O(N^3)$
