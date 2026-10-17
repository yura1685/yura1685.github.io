class WeightedUnionFind:
    def __init__(self, n):
        self.p = [-1] * n
        self.w = [0] * n  # w[a] = (a の値) - (p[a] の値)

    def leader(self, a):
        path = []
        while self.p[a] >= 0:
            path.append(a)
            a = self.p[a]
        for v in reversed(path):
            if self.p[v] != a:
                self.w[v] += self.w[self.p[v]]
            self.p[v] = a
        return a

    def weight(self, a):
        # (a の値) - (a の根の値)
        self.leader(a)
        return self.w[a]

    def merge(self, a, b, w):
        # (b の値) - (a の値) = w という条件を加える。今までの条件と矛盾するときだけ False
        wa, wb = self.weight(a), self.weight(b)
        a, b = self.leader(a), self.leader(b)
        if a == b:
            return wb - wa == w
        w += wa - wb
        if self.p[a] > self.p[b]:
            a, b = b, a
            w = -w
        self.p[a] += self.p[b]
        self.p[b] = a
        self.w[b] = w
        return True

    def diff(self, a, b):
        # (b の値) - (a の値)。a と b が同じ集合にあるときだけ使う
        return self.weight(b) - self.weight(a)

    def same(self, a, b):
        return self.leader(a) == self.leader(b)

    def size(self, a):
        return -self.p[self.leader(a)]
