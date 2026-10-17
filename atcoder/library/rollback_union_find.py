class RollbackUnionFind:
    def __init__(self, n):
        self.p = [-1] * n
        self.history = []  # merge のたびに (つないだ側の根, その元の p) を積む

    def leader(self, a):
        while self.p[a] >= 0:
            a = self.p[a]
        return a

    def merge(self, a, b):
        a, b = self.leader(a), self.leader(b)
        if a == b:
            self.history.append((-1, 0))
            return False
        if self.p[a] > self.p[b]:
            a, b = b, a
        self.history.append((b, self.p[b]))
        self.p[a] += self.p[b]
        self.p[b] = a
        return True

    def undo(self):
        # 最後の merge を取り消す
        b, pb = self.history.pop()
        if b == -1:
            return
        a = self.p[b]
        self.p[b] = pb
        self.p[a] -= pb

    def snapshot(self):
        # 今の状態を表す値（rollback に渡す）
        return len(self.history)

    def rollback(self, t=0):
        # snapshot() が t を返したときの状態に戻す
        while len(self.history) > t:
            self.undo()

    def same(self, a, b):
        return self.leader(a) == self.leader(b)

    def size(self, a):
        return -self.p[self.leader(a)]
