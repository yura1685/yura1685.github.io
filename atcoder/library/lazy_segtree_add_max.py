from atcoder.lazysegtree import LazySegTree

# 区間加算・区間最大値
INF = 1 << 60
op = max
e = -INF
mapping = lambda f, x: f + x
composition = lambda f, g: f + g
id_ = 0
seg = LazySegTree(op, e, mapping, composition, id_, a)
# seg.apply(l, r, x): a[l:r] に x を足す / seg.prod(l, r): max(a[l:r])
