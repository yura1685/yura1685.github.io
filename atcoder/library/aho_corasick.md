---
title: Aho–Corasick
category: 文字列
description: 複数のパターン文字列を Trie にまとめ、テキストの中に各パターンが何回現れるかを $O(\lvert T \rvert + \sum \lvert P \rvert)$ で数える
order: 5
---

パターンを Trie に入れ、各ノードに「そのノードの文字列の真の接尾辞のうち、Trie にある最長のもの」への失敗リンクを張ります。テキストを 1 文字ずつ読みながら Trie をたどり、進めないときは失敗リンクで戻ることで、すべてのパターンの出現をまとめて数えます。文字は辞書のキーにできれば何でもよいです（整数のリストも使えます）。

以下、 $\lvert T \rvert$ はテキストの長さ、 $\sum \lvert P \rvert$ はパターンの長さの合計です。

- `AhoCorasick(patterns)`: パターン（空でない文字列）のリストから構築。 $O(\sum \lvert P \rvert)$
- `count(text)`: 各パターンがテキストに現れる回数（重なりも数える）のリスト。 $O(\lvert T \rvert + \sum \lvert P \rvert)$
- `step(v, c)`: 状態 $v$ で文字 $c$ を読んだあとの状態。何も読んでいない状態は $0$。テキストを先頭から読むときはならし $O(1)$
- `out[v]`: 状態 $v$ までに読んだ文字列の接尾辞になっているパターンの個数
- `node[i]`: パターン $i$ を読み終えた状態

`step` で求めた遷移は覚えておくので、文字列についての DP で同じ遷移を何度も使っても速いです。

例（パターンを 1 つも含まない長さ $L$ の英小文字列の個数を $998244353$ で割った余り）:

```python
ac = AhoCorasick(patterns)
dp = {0: 1}
for _ in range(L):
    ndp = {}
    for v, x in dp.items():
        for c in "abcdefghijklmnopqrstuvwxyz":
            to = ac.step(v, c)
            if ac.out[to] == 0:
                ndp[to] = (ndp.get(to, 0) + x) % 998244353
    dp = ndp
ans = sum(dp.values()) % 998244353
```
