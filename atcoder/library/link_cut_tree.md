---
title: Link-Cut Tree
category: データ構造
description: 森の辺の追加・削除と、パス上の値の集約をならし $O(\log N)$ で行う
order: 22
---

木を根から下るパスに分け、それぞれのパスを、根に近い頂点ほど左に来る splay 木で持ちます。根から $v$ までのパスを 1 つの splay 木につなぎ直すと（expose）、そのパス上の頂点の値をまとめたものが splay 木の根に集まります。根を $v$ に変えることは、根から $v$ までのパスを反転することなので、反転は遅延評価で行います。演算 `op` は結合的であればよく、可換でなくても、反転したときのために右からまとめた値も持っているので、パスの向きどおりにまとめます。`e` はその単位元です。再帰は使いません。

- `LinkCutTree(n, op, e, a)`: 頂点数 $n$、演算 `op` と単位元 `e`、頂点の値の初期値のリスト `a`（省略するとすべて `e`）で、辺のない森を作る。 $O(N)$
- `link(u, v)`: 辺 $(u, v)$ を加える。 $u$ と $v$ は別の木にあること。ならし $O(\log N)$
- `cut(u, v)`: 辺 $(u, v)$ を取り除く。辺 $(u, v)$ があること。ならし $O(\log N)$
- `evert(v)`: $v$ をその木の根にする。ならし $O(\log N)$
- `connected(u, v)`: $u$ と $v$ が同じ木にあるか。ならし $O(\log N)$
- `get(v)`: 頂点 $v$ の値。 $O(1)$
- `set(v, x)`: 頂点 $v$ の値を $x$ にする。ならし $O(\log N)$
- `prod(u, v)`: $u$ から $v$ へのパス上の頂点の値を、 $u$ の側から順に `op` でまとめたもの（ $u = v$ なら $v$ の値）。 $u$ と $v$ は同じ木にあること。ならし $O(\log N)$
- `lca(root, u, v)`: $\mathrm{root}$ を根としたときの $u$ と $v$ の最小共通祖先。 $\mathrm{root}$ と $u$ と $v$ は同じ木にあること。ならし $O(\log N)$
- `parent(root, v)`: $\mathrm{root}$ を根としたときの $v$ の親（ $v = \mathrm{root}$ なら $-1$）。ならし $O(\log N)$

`link`・`cut`・`prod`・`lca`・`parent` は中で `evert` を呼ぶので、そのあとどの頂点が根になっているかは決まっていません。根付き木として使うときは、`lca` と `parent` のように毎回根を渡します。

辺に値があるときは、辺 $(u, v)$ ごとに新しい頂点 $w$ を作って辺 $(u, w)$ と $(w, v)$ に分け、 $w$ に辺の値を、元の頂点には `e` を持たせます。

例（文字列をつなげる演算で、パスの向きどおりにまとまることを確かめる）:

```python
lct = LinkCutTree(5, lambda x, y: x + y, "", ["a", "b", "c", "d", "e"])
lct.link(0, 1)
lct.link(1, 2)
lct.link(1, 3)
print(lct.prod(2, 3), lct.prod(3, 0))  # cbd dba
print(lct.connected(0, 4))  # False
lct.cut(1, 3)
lct.link(3, 4)
lct.link(4, 0)
print(lct.prod(2, 3))  # cbaed
print(lct.lca(0, 2, 3), lct.parent(0, 3))  # 0 4
```

例（Library Checker の Dynamic Tree Vertex Set Path Composite。各頂点に 1 次関数があり、パス上の関数を順に通した値を求める）:

```python
MOD = 998244353

# 値 (b, c) は x を b x + c にする関数。op(f, g) は f のあとに g をする関数
def op(f, g):
    return (f[0] * g[0] % MOD, (f[1] * g[0] + g[1]) % MOD)

lct = LinkCutTree(n, op, (1, 0), fs)
for u, v in edges:
    lct.link(u, v)
for q in queries:
    if q[0] == 0:  # 辺 (u, v) を取り除き、辺 (w, x) を加える
        _, u, v, w, x = q
        lct.cut(u, v)
        lct.link(w, x)
    elif q[0] == 1:  # 頂点 p の関数を (c, d) にする
        _, p, c, d = q
        lct.set(p, (c, d))
    else:  # u から v へのパス上の関数を、u の側から順に x に通した値
        _, u, v, x = q
        b, c = lct.prod(u, v)
        print((b * x + c) % MOD)
```
