---
title: Static Top Tree
category: 木
description: 根付き木を heavy path と light な子に分けて深さ $O(\log N)$ の二分木にまとめ、頂点のデータを 1 つ変えるたびに木 DP を $O(\log N)$ で求め直す
order: 10
---

[HL 分解](hld.html) と同じく、各頂点から部分木が最も大きい子（heavy child）への辺で、木を heavy path に分けます。heavy path 上の頂点は上から順に compress でつなぎ、各頂点の light な子の部分木は rake でまとめます。どちらも部分木の大きさで釣り合うように二分木にするので、全体の深さが $O(\log N)$ になります。頂点 $v$ のデータを変えたら、 $v$ から根までの $O(\log N)$ 個のノードだけを計算し直します。前計算も更新も再帰は使いません。

まとめる値（クラスタ）は 2 種類です。パスクラスタは、heavy path の一続きの部分と、その頂点たちから下がる light な子の部分木をまとめたもので、下の端の頂点の heavy child から下は含みません（穴として残します）。点クラスタは、1 つの頂点の light な子いくつかの部分木を、その頂点への辺ごとまとめたものです。問題ごとに次の 5 つの関数を決めて渡します。値にはタプルのような、書き換えないものを使います。

- `vertex(v)`: light な子がない頂点 $v$ だけのパスクラスタ
- `compress(p, c)`: 上のパスクラスタ $p$ の穴に、下のパスクラスタ $c$ をつないだパスクラスタ（結合的であること）
- `rake(x, y)`: 同じ頂点の下にある 2 つの点クラスタをまとめた点クラスタ（結合的かつ可換であること）
- `add_edge(p)`: heavy path 全体のパスクラスタ $p$ に、一番上の頂点から親への辺を加えた点クラスタ
- `add_vertex(x, v)`: 頂点 $v$ の light な子の部分木をすべてまとめた点クラスタ $x$ に、 $v$ を加えたパスクラスタ

heavy path の一番下はいつも葉なので、`add_edge` と `get` で使うパスクラスタの穴は空です。

- `StaticTopTree(n, edges, root, vertex, compress, rake, add_edge, add_vertex)`: 頂点数 $n$、木の辺のリスト `edges = [(u, v), ...]`、根 `root` と上の 5 つの関数から作り、すべてのクラスタを計算する。 $O(N \log N)$
- `update(v)`: 頂点 $v$ のデータ（`vertex(v)` や `add_vertex(x, v)` が読む値）を変えたあとに呼び、 $v$ から根までのクラスタを計算し直す。 $O(\log N)$（5 つの関数が $O(1)$ のとき）
- `get()`: 木全体のパスクラスタ（根を含む heavy path 全体）。 $O(1)$

辺に値があるときは、辺 $(\mathrm{par}(v), v)$ の値を子の側の頂点 $v$ のデータとして、`vertex(v)` と `add_vertex(x, v)` で $v$ と一緒に加えます（値を変えたら `update(v)` を呼ぶ）。

例（ABC 351 G。頂点 $v$ の値 $f(v)$ を、 $v$ が葉なら $a_v$、葉でなければ $a_v$ に子 $c$ の $f(c)$ の積を足したものとする。 $a_v$ を変えるたびに $f(\mathrm{root}) \bmod 998244353$ を求める）:

パスクラスタを、穴の値（下の端の頂点の heavy child $h$ の $f(h)$）を $x$ として、上の端の頂点の $f$ の値を返す 1 次関数 $x \mapsto s x + t$ で表し、タプル `(s, t)` で持ちます。頂点 $v$ の light な子の $f$ の積を $m$ （light な子がなければ $m = 1$）とすると $f(v) = m x + a_v$ なので、 $v$ だけのパスクラスタは `(m, a[v])` です。`compress` は 1 次関数の合成、点クラスタは light な子の $f$ の積で、`rake` は掛け算です。葉には heavy child がありませんが、 $x = 0$ とすると $f(v) = a_v$ となって葉の式と一致します。なので `add_edge(p)` と答えは $x = 0$ のときの値 $t$ です。

```python
MOD = 998244353


# パスクラスタ (s, t): 穴の値 x から、上の端の頂点の値 s x + t を返す 1 次関数
def vertex(v):
    return (1, a[v])


def compress(p, c):
    # x を c に通してから p に通す
    return (p[0] * c[0] % MOD, (p[0] * c[1] + p[1]) % MOD)


def rake(x, y):
    return x * y % MOD


def add_edge(p):
    return p[1]  # 穴が空（x = 0）のときの値


def add_vertex(m, v):
    return (m, a[v])  # m は light な子の f の積


edges = [(p[i], i) for i in range(1, n)]  # p[i] は頂点 i の親（根は 0）
stt = StaticTopTree(n, edges, 0, vertex, compress, rake, add_edge, add_vertex)
for v, x in queries:
    a[v] = x
    stt.update(v)
    print(stt.get()[1])
```
