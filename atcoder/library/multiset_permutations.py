def next_permutation(a):
    # a を辞書順で次の並びに書き換える（同じ値があっても、同じ並びは飛ばす）。最後の並びなら False
    i = len(a) - 2
    while i >= 0 and a[i] >= a[i + 1]:
        i -= 1
    if i < 0:
        return False
    j = len(a) - 1
    while a[j] <= a[i]:
        j -= 1
    a[i], a[j] = a[j], a[i]
    a[i + 1:] = a[i + 1:][::-1]
    return True


def multiset_permutations(a, r=None):
    # a から r 個（省略すると全部）選んで並べたものを、同じ並びは 1 回だけ、辞書順に列挙する
    a = sorted(a)
    n = len(a)
    if r is None:
        r = n
    if r > n:
        return
    while True:
        yield tuple(a[:r])
        a[r:] = a[r:][::-1]  # 残りを降順にして、先頭 r 個が次の並びに進むようにする
        if not next_permutation(a):
            return
