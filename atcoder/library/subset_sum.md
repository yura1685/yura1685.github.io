---
title: 部分和（bitset）
category: DP
description: Python の整数をビット列として使い、いくつかを選んだ和として作れる値を高速に求める（復元付き）
order: 4
---

和 $x$ を作れるかを整数の $x$ ビット目で表し、要素 $a_i$ を加えるたびに `bits |= bits << a_i` とします。シフトと OR がまとめて行われるので、普通の DP よりかなり速くなります。

- `subset_sums(a, s)`: 非負整数の列 $a$ からいくつかを選んだ和として作れる $s$ 以下の値を、ビットの集合（整数）で返す。和 $x$ を作れるのは `(res >> x) & 1` が $1$ のとき。 $O(Ns / w)$
- `subset_sum_restore(a, s)`: 和がちょうど $s$ になる選び方を 1 つ、添字の昇順のリストで返す。作れなければ `None`。途中の結果をすべて持つので、メモリは $Ns$ ビットほど使う。 $O(Ns / w)$

ここで $w$ はワードの大きさ（ $64$）です。

例（ $a$ を 2 つに分けたときの、和の差の最小値）:

```python
total = sum(a)
bits = subset_sums(a, total // 2)
x = bits.bit_length() - 1  # total // 2 以下で作れる最大の和
ans = total - 2 * x
```
