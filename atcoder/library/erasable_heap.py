from heapq import heapify, heappush, heappop


class ErasableHeap:
    def __init__(self, a=()):
        self.hq = list(a)
        heapify(self.hq)
        self.dq = []  # 削除を待っている値
        self.size = len(self.hq)

    def push(self, x):
        heappush(self.hq, x)
        self.size += 1

    def erase(self, x):
        # x が入っているときだけ使う
        heappush(self.dq, x)
        self.size -= 1

    def _clean(self):
        while self.dq and self.hq[0] == self.dq[0]:
            heappop(self.hq)
            heappop(self.dq)

    def top(self):
        self._clean()
        return self.hq[0]

    def pop(self):
        self._clean()
        self.size -= 1
        return heappop(self.hq)

    def __len__(self):
        return self.size
