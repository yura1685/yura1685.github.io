---
title: 尺取り法
category: 基礎
description: 区間 $[l, r)$ が条件を満たすなら、その中の区間もすべて満たすとき、各 $l$ について条件を満たす最大の $r$ を全体で $O(N)$ 回の出し入れで求める
order: 10
---

区間の左端 $l$ と右端 $r$ の 2 つの添字で、今の区間 $[l, r)$ を持ちます。各 $l$ について、位置 $r$ を加えても条件を満たす間だけ $r$ を進め、 $l$ を 1 つ進めるときに位置 $l$ を区間から除きます。条件を満たす区間の中の区間も条件を満たすとき、 $l$ を進めても条件を満たす最大の $r$ は小さくならないので、 $r$ は戻らず、加える回数も除く回数も全体で $N$ 回以下です。deque は使わず、区間の中身は `add` と `remove` で自分で管理します。

- `two_pointers(n, can_add, add, remove)`: 長さ $n$ の列について、`res[l]` が「区間 $[l, r)$ が条件を満たす最大の $r$」（ $l \le r \le n$）であるリスト `res` を返す。`can_add` を $O(N)$ 回、`add` と `remove` をそれぞれ $N$ 回以下呼ぶ
- `can_add(r)`: 今の区間に位置 $r$ を加えても条件を満たすかを返す関数
- `add(r)`, `remove(l)`: 位置を今の区間に加える関数・今の区間から除く関数

空の区間は条件を満たすものとします。 $1$ 要素だけでも条件を満たさない位置 $l$ では `res[l] = l` になり、そのときは `remove(l)` を呼びません。条件を満たす区間の個数は $\sum_l (\mathrm{res}[l] - l)$、最も長い区間の長さは $\max_l (\mathrm{res}[l] - l)$ です。

例（正の整数の列で、和が $K$ 以下の区間の個数）:

```python
s = 0

def can_add(r):
    return s + a[r] <= k

def add(r):
    global s
    s += a[r]

def remove(l):
    global s
    s -= a[l]

res = two_pointers(n, can_add, add, remove)
ans = sum(res[l] - l for l in range(n))
```

例（値の種類数が $K$ 以下の区間のうち、最も長いものの長さ）:

```python
cnt = {}

def can_add(r):
    return a[r] in cnt or len(cnt) < k

def add(r):
    cnt[a[r]] = cnt.get(a[r], 0) + 1

def remove(l):
    cnt[a[l]] -= 1
    if cnt[a[l]] == 0:
        del cnt[a[l]]

res = two_pointers(n, can_add, add, remove)
ans = max(res[l] - l for l in range(n))
```

関数を呼ぶ分だけ遅くなるので、PyPy でも時間が厳しいときは、同じ形のループを問題に合わせて直接書きます。
