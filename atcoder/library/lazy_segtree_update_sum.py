from atcoder.lazysegtree import LazySegTree

# 区間更新・区間和。値は (和, 区間の長さ)、作用 None は「何もしない」
op = lambda x, y: (x[0] + y[0], x[1] + y[1])
e = (0, 0)
mapping = lambda f, x: x if f is None else (f * x[1], x[1])
composition = lambda f, g: g if f is None else f
id_ = None
seg = LazySegTree(op, e, mapping, composition, id_, [(x, 1) for x in a])
# seg.apply(l, r, x): a[l:r] をすべて x にする / seg.prod(l, r)[0]: sum(a[l:r])
