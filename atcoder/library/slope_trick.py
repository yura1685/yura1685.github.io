from heapq import heappush, heappop


class SlopeTrick:
    # 区分線形な凸関数 f(x) を持つ（最初は f(x) = 0）
    INF = 1 << 62

    def __init__(self):
        self.min_f = 0
        self.L = []  # 最小値をとる区間より左の、傾きが 1 変わる点（-x を入れた最小ヒープ）
        self.R = []  # 最小値をとる区間より右の、傾きが 1 変わる点
        self.add_l = 0  # L の全要素に足す値
        self.add_r = 0  # R の全要素に足す値

    def _push_l(self, a):
        heappush(self.L, -(a - self.add_l))

    def _push_r(self, a):
        heappush(self.R, a - self.add_r)

    def _pop_l(self):
        return -heappop(self.L) + self.add_l

    def _pop_r(self):
        return heappop(self.R) + self.add_r

    def top_l(self):
        # f が最小になる x の左端（なければ -INF）
        return -self.L[0] + self.add_l if self.L else -self.INF

    def top_r(self):
        # f が最小になる x の右端（なければ INF）
        return self.R[0] + self.add_r if self.R else self.INF

    def add_all(self, a):
        # f(x) += a
        self.min_f += a

    def add_x_minus_a(self, a):
        # f(x) += max(0, x - a)
        self.min_f += max(0, self.top_l() - a)
        self._push_l(a)
        self._push_r(self._pop_l())

    def add_a_minus_x(self, a):
        # f(x) += max(0, a - x)
        self.min_f += max(0, a - self.top_r())
        self._push_r(a)
        self._push_l(self._pop_r())

    def add_abs(self, a):
        # f(x) += |x - a|
        self.add_x_minus_a(a)
        self.add_a_minus_x(a)

    def clear_right(self):
        # f(x) を min_{y <= x} f(y) にする（右側を平らにする）
        self.R = []
        self.add_r = 0

    def clear_left(self):
        # f(x) を min_{y >= x} f(y) にする（左側を平らにする）
        self.L = []
        self.add_l = 0

    def shift(self, a, b=None):
        # f(x) を min_{x - b <= y <= x - a} f(y) にする（b を省略すると f(x - a) に平行移動）
        if b is None:
            b = a
        self.add_l += a
        self.add_r += b

    def get(self, x):
        # f(x)。O(ヒープの大きさ)
        res = self.min_f
        for l in self.L:
            res += max(0, -l + self.add_l - x)
        for r in self.R:
            res += max(0, x - r - self.add_r)
        return res
