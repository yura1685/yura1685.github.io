---
title: 部分永続 Union-Find
category: データ構造
description: 過去の時刻での連結性や集合の大きさを求められる Union-Find
order: 18
---

経路圧縮をせず union by size だけを行うと、根でなくなった頂点の親はその後ずっと変わりません。そこで、各頂点が根でなくなった時刻を覚えておくと、時刻 $t$ での根は、根でなくなった時刻が $t$ 以下である間だけ親をたどれば求まります。集合の大きさは、各根について、大きさが変わった時刻と変わった後の大きさの履歴を持っておき、二分探索で求めます。

`unite` を $t$ 回呼んだ直後を時刻 $t$ とします（初期状態が時刻 $0$）。すでに同じ集合にある 2 頂点を `unite` しても、時刻は 1 進みます。過去の状態は聞けるだけで、過去の状態から `unite` することはできません（それには [完全永続 Union-Find](persistent_union_find.html) を使います）。

- `PartiallyPersistentUnionFind(n)`: $n$ 頂点で初期化（時刻 $0$）
- `unite(a, b)`: 時刻を 1 進めて、 $a$ と $b$ をつなぐ。すでに同じ集合なら `False`（このときも時刻は進む）。 $O(\log N)$
- `now()`: 今の時刻（これまでに `unite` を呼んだ回数）。 $O(1)$
- `find(t, x)`: 時刻 $t$ での $x$ の根。 $O(\log N)$
- `same(t, a, b)`: 時刻 $t$ で $a$ と $b$ が同じ集合にあるか。 $O(\log N)$
- `size(t, x)`: 時刻 $t$ での $x$ を含む集合の大きさ。 $O(\log N)$

時刻 $t$ は $0$ 以上 `now()` 以下で指定します。

辺を 1 本ずつ加えていくとき、「 $a$ と $b$ が初めて連結になった時刻」は、`same(t, a, b)` が $t$ について単調（一度連結になればその後もずっと連結）なので、 $t$ についての二分探索で $O(\log Q \log N)$ で求められます（ $Q$ は `unite` の回数）。クエリを先読みしなくても、聞かれるたびに答えられます。「 $x$ を含む集合と $y$ を含む集合を合わせて $z$ 頂点以上になる最初の時刻」のように、`size` を使う条件でも同じです。

例（ $i$ 本目の辺を加えた直後が時刻 $i$）:

```python
uf = PartiallyPersistentUnionFind(n)
for u, v in edges:
    uf.unite(u, v)

def first_time(ok):
    # ok(t) が真になる最初の時刻（ok は t について単調。最後まで偽なら -1）
    if not ok(uf.now()):
        return -1
    lo, hi = -1, uf.now()
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if ok(mid):
            hi = mid
        else:
            lo = mid
    return hi

# a と b が初めて連結になった時刻
print(first_time(lambda t: uf.same(t, a, b)))

# x を含む集合と y を含む集合を合わせて z 頂点以上になる最初の時刻
def total(t):
    if uf.same(t, x, y):
        return uf.size(t, x)
    return uf.size(t, x) + uf.size(t, y)

print(first_time(lambda t: total(t) >= z))
```
