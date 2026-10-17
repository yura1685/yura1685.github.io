---
title: 重心分解
category: 木
description: 木の重心を取り除いて分割することを繰り返し、深さ $O(\log N)$ の重心分解の木を作る
order: 6
---

木の重心（取り除くと、残りの各部分の頂点数が全体の半分以下になる頂点）を取り除き、残った各部分でも同じことを繰り返します。各頂点は $O(\log N)$ 個の部分にしか含まれないので、各部分で「重心を通るパス」を部分の大きさに比例する時間で数えれば、全体で $O(N \log N)$ になります。再帰は使いません。

- `centroid_decomposition(g)`: 木の隣接リスト `g[v] = [to, ...]` から `(cpar, level)` を返す。 $O(N \log N)$
- `cpar[v]`: 重心分解の木での $v$ の親（最初に取り除いた重心は $-1$）
- `level[v]`: 重心分解の木での $v$ の深さ（ $0$ 以上 $\log_2 N$ 以下）

重心 $c$ を取り除くときの部分は、 $c$ から `level` が `level[c]` より大きい頂点だけをたどって行ける頂点全体です。

例（長さがちょうど $K$ のパスの本数）:

```python
cpar, level = centroid_decomposition(g)
ans = 0
for c in range(n):
    cnt = [1]  # cnt[d] = これまでに見た頂点のうち、c からの距離が d のものの個数
    for s in g[c]:
        if level[s] < level[c]:
            continue
        ds = []
        q = [(s, c, 1)]
        for v, p, d in q:
            ds.append(d)
            for to in g[v]:
                if to != p and level[to] > level[c]:
                    q.append((to, v, d + 1))
        for d in ds:
            if d <= K and K - d < len(cnt):
                ans += cnt[K - d]
        for d in ds:
            if d == len(cnt):
                cnt.append(0)
            cnt[d] += 1
```
