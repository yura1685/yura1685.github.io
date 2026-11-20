---
title: スライド最小値・単調スタック
category: 基礎
description: 長さ $k$ のすべての区間の最小値と、各要素の左右で最も近い、より小さい要素の位置を、値が単調に並ぶ deque やスタックで $O(N)$ で求める
order: 11
---

スライド最小値は、区間を右に 1 つずつずらしながら、長さ $k$ の区間 `a[i:i + k]` の最小値をすべて求めるものです。区間に入っている位置のうち、「それより右に、それ以下の値がない」ものだけを deque に左から順に持つと、値は昇順に並び、先頭が区間の最小値になります。新しい値を入れるときは、それ以上の値を末尾から捨て、区間から外れた位置を先頭から捨てます。

単調スタックは、各位置 $i$ について、左（右）で最も近い、 $a_i$ より小さい値の位置を求めるものです。左から順に見ながら、値が単調増加になるように位置をスタックに持ち、 $a_i$ 以上の値を上から捨てると、残ったスタックの一番上が答えになります。

どちらも、各位置は 1 回入って高々 1 回出るだけなので、全体で $O(N)$ です。

- `sliding_window_min(a, k)`, `sliding_window_max(a, k)`: `res[i]` が `a[i:i + k]` の最小値・最大値（ $0 \le i \le N - k$）であるリストを返す。 $O(N)$
- `prev_smaller(a, strict=True)`: `res[i]` が「 $a_j < a_i$ となる最大の $j < i$」（なければ $-1$）であるリストを返す。`strict=False` にすると $a_j \le a_i$ で探す。 $O(N)$
- `next_smaller(a, strict=True)`: `res[i]` が「 $a_j < a_i$ となる最小の $j > i$」（なければ $N$）であるリストを返す。`strict=False` にすると $a_j \le a_i$ で探す。 $O(N)$

より大きい値の位置を探すときは、符号を反転した列 `[-x for x in a]` を渡します。最小値の代わりに gcd などで区間をまとめたいときは [SWAG](swag.html) を、すべての区間について最小値の位置を木の形で持ちたいときは [Cartesian Tree](cartesian_tree.html) を使います。

例（ヒストグラムの中の最大の長方形の面積）: 高さ $h_i$ の棒を含み、高さが $h_i$ の長方形は、左右に $h_i$ 以上の棒が続くところまで伸ばせます。

```python
L = prev_smaller(h)
R = next_smaller(h)
ans = max(h[i] * (R[i] - L[i] - 1) for i in range(n))
```

例（すべての区間の最小値の和）: 最小値が複数ある区間は、最も右の最小値の位置で数えるように、左は $a_j < a_i$、右は $a_j \le a_i$ で探します。

```python
L = prev_smaller(a)
R = next_smaller(a, strict=False)
ans = sum(a[i] * (i - L[i]) * (R[i] - i) for i in range(n))
```
