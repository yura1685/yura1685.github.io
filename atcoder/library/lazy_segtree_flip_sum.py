from atcoder.lazysegtree import LazySegTree

# 0/1 の列の区間反転・区間の 1 の個数。値は (1 の個数, 区間の長さ)、作用は反転するかどうか
op = lambda x, y: (x[0] + y[0], x[1] + y[1])
e = (0, 0)
mapping = lambda f, x: (x[1] - x[0], x[1]) if f else x
composition = lambda f, g: f ^ g
id_ = False
seg = LazySegTree(op, e, mapping, composition, id_, [(x, 1) for x in a])
# seg.apply(l, r, True): a[l:r] の 0 と 1 を入れ替える / seg.prod(l, r)[0]: a[l:r] の 1 の個数
