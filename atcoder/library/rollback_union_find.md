---
title: ロールバック付きUnion-Find
category: データ構造
description: 最後に行った merge を取り消せる Union-Find。経路圧縮をしないので、各操作 $O(\log N)$
order: 7
---

union by size だけを行い経路圧縮をしないことで、merge で書き換えた値を履歴に積んでおき、あとから取り消せるようにしたものです。

- `RollbackUnionFind(N)`: $N$ 頂点で初期化
- `merge(a, b)`: $a$ と $b$ をつなぐ。すでに同じ集合なら `False`（このときも履歴には積むので、`undo` 1 回で取り消せる）
- `undo()`: 最後の `merge` を取り消す。 $O(1)$
- `snapshot()`: 今の状態を表す値を返す。 $O(1)$
- `rollback(t)`: `snapshot()` が $t$ を返したときの状態に戻す（既定は $t = 0$ で、何もつないでいない状態）。取り消す `merge` 1 回につき $O(1)$
- `leader(a)`, `same(a, b)`, `size(a)`: 普通の Union-Find と同じ。 $O(\log N)$

辺の追加と削除が混ざるクエリを、時間を区間に分けたセグ木の上で DFS して処理する（ [オフライン動的連結性](offline_dynamic_connectivity.html)）ときなどに使います。

例:

```python
uf = RollbackUnionFind(n)
t = uf.snapshot()
for a, b in edges:
    uf.merge(a, b)
# ここで edges を加えたときの連結性を調べる
uf.rollback(t)  # edges を加える前に戻る
```
