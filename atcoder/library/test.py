class UnionFind:
    def __init__(self, n):
        self.p = [-1] * n

    def leader(self, a):
        while self.p[a] >= 0:
            if self.p[self.p[a]] >= 0:
                self.p[a] = self.p[self.p[a]]
            a = self.p[a]
        return a

    def merge(self, a, b):
        a, b = self.leader(a), self.leader(b)
        if a == b:
            return False
        if self.p[a] > self.p[b]:
            a, b = b, a
        self.p[a] += self.p[b]
        self.p[b] = a
        return True

    def same(self, a, b):
        return self.leader(a) == self.leader(b)

    def size(self, a):
        return -self.p[self.leader(a)]
