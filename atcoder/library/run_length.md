---
title: ランレングス圧縮
category: 基礎
description: 列を同じ値の連ごとに、値と個数や、値と区間の組にまとめる
order: 12
---

ランレングス圧縮は、列を同じ値が続く部分（連）に区切り、各連を値と長さの組で表すものです。例えば `"aaabbc"` は `[("a", 3), ("b", 2), ("c", 1)]` になります。左から添字 $i$ を進め、 $a_i$ と同じ値が続く間だけ $j$ を進めると、 $[i, j)$ が 1 つの連になり、次は $j$ から見ます。各位置は 1 回しか見ないので $O(N)$ です。

- `run_length(a)`: 連ごとの `(値, 長さ)` のリストを左から順に返す。 $O(N)$
- `run_length_ranges(a)`: 連ごとの `(値, l, r)` のリストを返す。連は区間 $[l, r)$ で、`a[l:r]` がすべて同じ値になる。 $O(N)$
- `run_length_decode(rle)`: `(値, 長さ)` のリストを元の列のリストに戻す。 $O(N)$

`a` はリストでも文字列でもよく、空の列には空のリストを返します。文字列に戻すときは `"".join(run_length_decode(rle))` とします。`itertools.groupby` を使って `[(x, len(list(g))) for x, g in groupby(a)]` と書いても同じ結果になります。

例（`"aaabbc"` を `"a3b2c1"` の形にする）:

```python
t = "".join(c + str(k) for c, k in run_length(s))
```

例（ABC 329 C、1 種類の文字だけからなる部分文字列の種類数）: 各文字について、最も長い連の長さを足します。

```python
best = {}
for c, k in run_length(s):
    best[c] = max(best.get(c, 0), k)
ans = sum(best.values())
```

例（各位置について、その位置を含む連の長さ）:

```python
length = [0] * n
for x, l, r in run_length_ranges(a):
    for i in range(l, r):
        length[i] = r - l
```
