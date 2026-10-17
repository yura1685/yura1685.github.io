---
title: Mo's algorithm
category: 基礎
description: 区間の端を 1 つ動かしたときの答えの変化がすぐに求まるとき、 $Q$ 個の区間クエリをまとめて $O(N \sqrt{Q})$ 回の移動で処理する
order: 6
---

クエリを左端のブロック（幅 $B = N / \sqrt{Q}$）ごとに分け、ブロックの中では右端の順に並べてから、今の区間の端を 1 つずつ動かして答えていきます。ブロックごとに右端の向きを交互に変えて、移動を減らしています。クエリを先にすべて読んでおく必要があります（オフライン）。

- `mo(N, queries, add, remove, get)`: 長さ $N$ の列に対する区間クエリ `queries = [(l, r), ...]`（半開区間 $[l, r)$）の答えを、クエリの順に並べたリストで返す
- `add(i)`, `remove(i)`: 位置 $i$ を今の区間に加える関数・今の区間から除く関数
- `get(k)`: 今の区間が $k$ 番目のクエリの区間になったときに呼ばれ、その答えを返す関数
- `add_left`, `remove_left`: 左端で出し入れするときの処理が右端と違うとき（区間の転倒数など）だけ渡す。省略すると `add`, `remove` を使う
- 計算量: `add` と `remove` を合わせて $O(N \sqrt{Q})$ 回、`get` を $Q$ 回呼ぶ

`add` と `remove` はとても多く呼ばれるので、中身はなるべく軽くします。

例（区間に含まれる値の種類数）:

```python
cnt = [0] * (max(a) + 1)
kinds = 0


def add(i):
    global kinds
    cnt[a[i]] += 1
    if cnt[a[i]] == 1:
        kinds += 1


def remove(i):
    global kinds
    cnt[a[i]] -= 1
    if cnt[a[i]] == 0:
        kinds -= 1


ans = mo(n, queries, add, remove, lambda k: kinds)
```
