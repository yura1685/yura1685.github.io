from atcoder.lazysegtree import LazySegTree

# 区間アフィン変換・区間和（mod）。値は (和, 区間の長さ)、作用 (b, c) は x を b x + c にする
mod = 998244353
op = lambda x, y: ((x[0] + y[0]) % mod, x[1] + y[1])
e = (0, 0)
mapping = lambda f, x: ((f[0] * x[0] + f[1] * x[1]) % mod, x[1])
composition = lambda f, g: (f[0] * g[0] % mod, (f[0] * g[1] + f[1]) % mod)
id_ = (1, 0)
seg = LazySegTree(op, e, mapping, composition, id_, [(x, 1) for x in a])
# seg.apply(l, r, (b, c)): a[l:r] の各 x を b x + c にする / seg.prod(l, r)[0]: sum(a[l:r]) % mod
# 区間加算は (1, c)、区間更新は (0, c)
