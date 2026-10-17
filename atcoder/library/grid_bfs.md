---
title: グリッドBFS・0-1 BFS
category: グラフ
description: グリッド上の最短距離を BFS で、辺の重みが $0$ か $1$ のグラフの最短距離を 0-1 BFS で求める
order: 6
---

- `grid_bfs(grid, sy, sx, wall, dirs)`: 文字列のリスト `grid` で、マス $(s_y, s_x)$ から各マスへの最短手数を 2 次元リストで返す。`wall`（既定は `"#"`）のマスには入れず、到達できないマスは $-1$。 $O(HW)$
- `DIR4`, `DIR8`: 4 近傍・8 近傍の移動方向。`dirs` に渡す（既定は `DIR4`）
- `bfs01(g, s)`: 隣接リスト `g[v] = [(to, cost), ...]`（cost は $0$ か $1$）で、 $s$ から各頂点への最短距離を返す。到達できない頂点は `1 << 62`。 $O(N + M)$

0-1 BFS をグリッドで使うときは、マス $(y, x)$ を頂点 $yW + x$ として辺を作ります。

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
