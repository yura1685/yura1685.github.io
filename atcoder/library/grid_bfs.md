---
title: BFS・グリッド BFS・0-1 BFS
category: グラフ
description: BFS・グリッド BFS・0-1 BFS で最短距離を求める（経路復元付き）
order: 6
---

辺の重みがすべて $1$ のグラフでは、始点から近い順に頂点をキューから取り出す BFS で、最短距離を $O(N + M)$ で求めます。グリッドでは、隣のマスへの移動を長さ $1$ の辺とみなして BFS をします。辺の重みが $0$ か $1$ のグラフでは、重み $0$ の辺で進んだ頂点を deque の先頭に、重み $1$ の辺で進んだ頂点を末尾に入れる 0-1 BFS で、Dijkstra 法より速く最短距離を求めます。以下、グリッドの大きさを $H \times W$ とします。

- `bfs(g, s)`: 重みなしグラフの隣接リスト `g[v] = [to, ...]` で、 $s$ から各頂点への最短距離のリスト `dist` と、最短路木での親のリスト `prev` を返す。到達できない頂点の距離は $-1$、始点と到達できない頂点の親は $-1$。 $O(N + M)$
- `bfs_multi(g, starts)`: 始点のリスト `starts` のどれかから各頂点への最短距離（最も近い始点からの距離）と、最短路木での親を返す。 $O(N + M)$
- `restore_path(prev, t)`: 始点から $t$ までの最短路の頂点列を返す（ $t$ に到達できるときだけ使う）。 $O(N)$
- `grid_bfs(grid, sy, sx, wall, dirs)`: 文字列のリスト `grid` で、マス $(s_y, s_x)$ から各マスへの最短手数を 2 次元リストで返す。`wall`（既定は `"#"`）のマスには入れず、到達できないマスは $-1$。 $O(HW)$
- `grid_bfs_multi(grid, starts, wall, dirs)`: 始点のリスト `starts = [(y, x), ...]` のどれかから各マスへの最短手数（最も近い始点からの手数）を返す。 $O(HW)$
- `DIR4`, `DIR8`: 4 近傍・8 近傍の移動方向。`dirs` に渡す（既定は `DIR4`）
- `bfs01(g, s)`: 隣接リスト `g[v] = [(to, cost), ...]`（cost は $0$ か $1$）で、 $s$ から各頂点への最短距離を返す。到達できない頂点は `INF`（ $= 2^{60}$）。 $O(N + M)$

BFS で到達できない頂点の距離は、グリッド BFS と同じく $-1$ です（重みのある 0-1 BFS と [Dijkstra](dijkstra.html) は `INF`）。0-1 BFS をグリッドで使うときは、マス $(y, x)$ を頂点 $yW + x$ として辺を作ります。

例（ $s$ から $t$ への最短路の頂点列）:

```python
dist, prev = bfs(g, s)
path = restore_path(prev, t) if dist[t] != -1 else None
```

例（壁を壊すとコスト 1 で進めるときの最短コスト）:

```python
h, w = len(grid), len(grid[0])
g = [[] for _ in range(h * w)]
for y in range(h):
    for x in range(w):
        for dy, dx in DIR4:
            ny, nx = y + dy, x + dx
            if 0 <= ny < h and 0 <= nx < w:
                g[y * w + x].append((ny * w + nx, int(grid[ny][nx] == "#")))
dist = bfs01(g, sy * w + sx)
```
