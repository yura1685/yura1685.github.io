---
title: オフライン動的連結性
category: グラフ
description: 辺の追加・削除が混ざるグラフで、各時点の 2 頂点の連結性や連結成分の個数を、クエリを先読みして $O(Q \log Q \log N)$ で求める
order: 14
---

それぞれの辺が存在する時間の区間を求め、時間についてのセグ木の $O(\log Q)$ 個のノードに辺を載せます。セグ木を根から DFS し、ノードに入るときにその辺を [ロールバック付き Union-Find](rollback_union_find.html) でつなぎ、出るときに取り消すと、葉に着いたときにちょうどその時刻にある辺がつながっています。再帰は使いません。

操作を順に呼んで記録し、最後に `run()` でまとめて答えます。

- `OfflineDynamicConnectivity(n)`: $n$ 頂点の辺のないグラフで初期化
- `add_edge(u, v)`: 辺 $(u, v)$ を追加する（同じ辺を何本追加してもよい）
- `remove_edge(u, v)`: 今ある辺 $(u, v)$ を 1 本取り除く
- `same(u, v)`: この時点で $u$ と $v$ が連結かを質問する
- `count()`: この時点の連結成分の個数を質問する
- `run()`: 質問の答えを、質問した順に並べたリストを返す。操作の回数を $Q$ として $O(Q \log Q \log N)$

例:

```python
D = OfflineDynamicConnectivity(n)
for t, u, v in queries:
    if t == 0:
        D.add_edge(u, v)
    elif t == 1:
        D.remove_edge(u, v)
    else:
        D.same(u, v)
print(*D.run(), sep="\n")
```
