from atcoder.lazysegtree import LazySegTree

# 区間加算・区間最小値
INF = 1 << 60
op = min
e = INF
mapping = lambda f, x: f + x
composition = lambda f, g: f + g
id_ = 0
seg = LazySegTree(op, e, mapping, composition, id_, a)
# seg.apply(l, r, x): a[l:r] に x を足す / seg.prod(l, r): min(a[l:r])
