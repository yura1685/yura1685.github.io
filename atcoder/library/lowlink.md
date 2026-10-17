---
title: lowlink（橋・関節点）
category: グラフ
description: 無向グラフの橋と関節点を DFS の lowlink で求める
order: 5
---

DFS での訪問順 `ord` と、DFS 木の辺を下りたあと後退辺を高々 1 本使って戻れる最小の訪問順 `low` を求め、橋と関節点を判定します。再帰は使いません。多重辺や自己ループ、非連結なグラフでも正しく動きます。

- `LowLink(n, edges)`: 頂点数 $n$ と無向辺のリスト `edges = [(u, v), ...]` から前計算。 $O(N + M)$
- `bridges`: 橋の辺番号（`edges` での添字）のリスト
- `articulation`: 関節点の頂点番号の昇順リスト
- `ord[v]`, `low[v]`: 上で説明した値
