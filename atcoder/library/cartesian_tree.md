---
title: Cartesian Tree
category: 木
description: 列の Cartesian Tree をスタックで $O(N)$ で作る
order: 11
---

列 $a$ の最小値の位置を根とし、それより左の部分と右の部分から同じように作った木を、それぞれ左の部分木・右の部分木とする二分木です。どの頂点の部分木も元の列の連続する区間になり、その区間の最小値が部分木の根にあります。通りがけ順に並べると元の列の順番になります。

左から順に、根から右の子だけをたどった道をスタックに持っておき、 $a_i$ より大きい頂点を道から取り除いて $i$ の左の部分木にし、 $i$ を道の最後につなぎます。各頂点はスタックに 1 回入って 1 回出るだけなので $O(N)$ です。再帰は使いません。

同じ値があるときは、左にあるものが祖先になります（同じ値だけが並んでいると、右の子をたどる 1 本の道になります）。根は最小値のうち最も左にあるものです。

- `cartesian_tree(a)`: 列 $a$ の Cartesian Tree の親のリスト `par` を返す（根は `par[root] = -1`）。値は大小を比べられれば何でもよい。 $O(N)$

根でない頂点 $v$ は、`v < par[v]` なら `par[v]` の左の子、`v > par[v]` なら右の子です。最大値を根にするときは、値を $-1$ 倍して `cartesian_tree([-x for x in a])` とします（このときも、同じ値では左にあるものが祖先になります）。

$l \le r$ のとき、 $a_l, \ldots, a_r$ の最小値（のうち最も左のもの）の位置は、 $l$ と $r$ の [LCA](lca.html) です。

頂点 $v$ の部分木が受け持つ区間を $[L_v, R_v)$ とすると、 $L_v \le x \le v < y \le R_v$ となる区間 $[x, y)$ は、ちょうど $a_v$ を最小値（のうち最も左のもの）とする区間です。たとえば、すべての区間の最小値の和は $a_v (v - L_v + 1)(R_v - v)$ の和で、ヒストグラムの中の最大の長方形の面積は $a_v (R_v - L_v)$ の最大値です。これらは木を作らずに、 [スライド最小値・単調スタック](monotone_stack.html) の `prev_smaller` と `next_smaller` でも求められます。

例（ $L_v$ は左の子から、 $R_v$ は右の子から求まるので、 $L_v$ は左から、 $R_v$ は右から順に求める）:

```python
a = [2, 1, 5, 6, 2, 3]
n = len(a)
par = cartesian_tree(a)
print(par)  # [1, -1, 4, 2, 1, 4]
L = list(range(n))  # 頂点 v の部分木は区間 [L[v], R[v])
R = list(range(1, n + 1))
for v in range(n):
    if v < par[v]:  # v は par[v] の左の子
        L[par[v]] = L[v]
for v in range(n - 1, -1, -1):
    if 0 <= par[v] < v:  # v は par[v] の右の子
        R[par[v]] = R[v]
print(sum(a[v] * (v - L[v] + 1) * (R[v] - v) for v in range(n)))  # 43
print(max(a[v] * (R[v] - L[v]) for v in range(n)))  # 10
```
