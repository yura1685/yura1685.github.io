---
title: 同じものを含む順列の列挙
category: 基礎
description: 同じ値を含む列の並べ替えを、同じ並びを出さずに辞書順に列挙する（itertools.permutations の重複なし版）
order: 8
---

`itertools.permutations` は同じ値も区別して並べるので、たとえば $0, 0, 1$ からは同じ並びが 2 回ずつ出てきます。ここでは C++ の `next_permutation` と同じ方法で、辞書順で次の並びに直接進むことで、同じ並びは 1 回だけ出します。全部作ってから `set` に入れるのと違い、出てくる並びの個数に比例する時間で済みます。並びの個数は [二項係数](combination.html) の `multinomial` で数えられます。

要素は大小を比べられるもの（数や文字列など）とします。

- `multiset_permutations(a, r)`: `a` から $r$ 個（省略すると全部）選んで並べたタプルを、同じものは 1 回だけ、辞書順に返すジェネレータ。`sorted(set(permutations(a, r)))` と同じものが順に出てくる。1 個あたり $O(N)$
- `next_permutation(a)`: リスト `a` をその場で辞書順の次の並びに書き換えて `True` を返す。最後の並びだったときは書き換えずに `False` を返す。 $O(N)$

例:

```python
for p in multiset_permutations([0, 0, 1, 2]):
    print(*p)
# 0 0 1 2
# 0 0 2 1
# 0 1 0 2
# ...（全部で 4! / 2! = 12 通り）
```
