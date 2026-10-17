class Doubling:
    def __init__(self, nxt, max_k, w=None):
        # nxt[v] は v の 1 回先（0 <= nxt[v] < N）。max_k 回先まで求められるようにする
        # w[v] は v から nxt[v] へ進むときの重み（使わなければ None）
        self.log = max(1, max_k.bit_length())
        self.up = [nxt[:]]
        self.ws = None if w is None else [w[:]]
        for _ in range(self.log - 1):
            p = self.up[-1]
            if self.ws is not None:
                s = self.ws[-1]
                self.ws.append([s[v] + s[p[v]] for v in range(len(p))])
            self.up.append([p[p[v]] for v in range(len(p))])

    def kth(self, v, k):
        # v の k 回先
        i = 0
        while k:
            if k & 1:
                v = self.up[i][v]
            k >>= 1
            i += 1
        return v

    def kth_sum(self, v, k):
        # (v の k 回先, その間に通った k 本の重みの和)
        res = 0
        i = 0
        while k:
            if k & 1:
                res += self.ws[i][v]
                v = self.up[i][v]
            k >>= 1
            i += 1
        return v, res

    def max_step(self, v, ok):
        # ok(v の k 回先) が True である最大の k と、そのときの頂点（ok(v) は True とする）
        k = 0
        for i in range(self.log - 1, -1, -1):
            u = self.up[i][v]
            if ok(u):
                v = u
                k += 1 << i
        return k, v


def kth_all(nxt, k):
    # すべての v について、v の k 回先を求める
    res = list(range(len(nxt)))
    p = nxt[:]
    while k:
        if k & 1:
            res = [p[v] for v in res]
        p = [p[v] for v in p]
        k >>= 1
    return res
