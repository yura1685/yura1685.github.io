from atcoder.lazysegtree import LazySegTree

# 区間加算・区間和。値は (和, 区間の長さ)
op = lambda x, y: (x[0] + y[0], x[1] + y[1])
e = (0, 0)
mapping = lambda f, x: (x[0] + f * x[1], x[1])
composition = lambda f, g: f + g
id_ = 0
seg = LazySegTree(op, e, mapping, composition, id_, [(x, 1) for x in a])
# seg.apply(l, r, x): a[l:r] に x を足す / seg.prod(l, r)[0]: sum(a[l:r])
