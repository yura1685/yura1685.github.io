from atcoder.lazysegtree import LazySegTree

# 区間更新・区間最大値（作用 None は「何もしない」）
INF = 1 << 60
op = max
e = -INF
mapping = lambda f, x: x if f is None else f
composition = lambda f, g: g if f is None else f
id_ = None
seg = LazySegTree(op, e, mapping, composition, id_, a)
# seg.apply(l, r, x): a[l:r] をすべて x にする / seg.prod(l, r): max(a[l:r])
