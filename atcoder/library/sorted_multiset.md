---
title: SortedMultiset
category: データ構造
description: 平方分割で順序付き多重集合を管理する（tatyam 氏方式）
order: 2
---

要素をソート済みの複数のバケットに分けて持つことで、C++ の `std::multiset` に近い操作を行います。要素は互いに比較できれば何でもよいです。

- `SortedMultiset(a)`: 列 $a$ で初期化。 $O(N \log N)$
- `add(x)`: $x$ を 1 つ追加
- `discard(x)`: $x$ を 1 つ削除。削除できたら `True`
- `x in s`, `count(x)`: 存在判定・個数
- `lt(x)`, `le(x)`, `gt(x)`, `ge(x)`: $x$ 未満の最大値・ $x$ 以下の最大値・ $x$ より大きい最小値・ $x$ 以上の最小値。存在しなければ `None`
- `s[i]`: 小さい方から $i$ 番目（0-indexed、負の添字も可）
- `pop(i)`: $i$ 番目を削除して返す（既定は最大値）
- `index(x)`, `index_right(x)`: $x$ 未満・ $x$ 以下の要素の個数
- `len(s)`, `for x in s`: 要素数・昇順の走査
- 計算量: 各操作 $O(\sqrt{N})$（初期化以外）

入っていない値を `discard` してもエラーにはならず、`False` が返ります。重複を許さない集合として使いたい場合は、`add` の前に `x in s` を確認します。
