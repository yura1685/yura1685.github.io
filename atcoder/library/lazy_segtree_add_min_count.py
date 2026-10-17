from atcoder.lazysegtree import LazySegTree

# 区間加算・区間最小値とその個数。値は (最小値, 個数)
INF = 1 << 60


def op(x, y):
    if x[0] < y[0]:
        return x
    if x[0] > y[0]:
        return y
    return (x[0], x[1] + y[1])


e = (INF, 0)
mapping = lambda f, x: (x[0] + f, x[1])
composition = lambda f, g: f + g
id_ = 0
seg = LazySegTree(op, e, mapping, composition, id_, [(x, 1) for x in a])
# seg.apply(l, r, x): a[l:r] に x を足す / seg.prod(l, r): (min(a[l:r]), その値の個数)
