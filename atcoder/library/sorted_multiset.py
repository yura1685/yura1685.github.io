import math
from bisect import bisect_left, bisect_right


class SortedMultiset:
    BUCKET_RATIO = 16
    SPLIT_RATIO = 24

    def __init__(self, a=[]):
        a = sorted(a)
        self.size = len(a)
        n = math.ceil(math.sqrt(self.size / self.BUCKET_RATIO))
        self.a = [a[self.size * i // n: self.size * (i + 1) // n] for i in range(n)]

    def __iter__(self):
        for b in self.a:
            yield from b

    def __reversed__(self):
        for b in reversed(self.a):
            yield from reversed(b)

    def __len__(self):
        return self.size

    def __repr__(self):
        return "SortedMultiset" + str(list(self))

    def _position(self, x):
        for i, b in enumerate(self.a):
            if x <= b[-1]:
                return b, i, bisect_left(b, x)
        return b, i, bisect_left(b, x)

    def __contains__(self, x):
        if self.size == 0:
            return False
        b, _, i = self._position(x)
        return i != len(b) and b[i] == x

    def count(self, x):
        return self.index_right(x) - self.index(x)

    def add(self, x):
        if self.size == 0:
            self.a = [[x]]
            self.size = 1
            return
        b, bi, i = self._position(x)
        b.insert(i, x)
        self.size += 1
        if len(b) > len(self.a) * self.SPLIT_RATIO:
            mid = len(b) >> 1
            self.a[bi:bi + 1] = [b[:mid], b[mid:]]

    def _pop(self, b, bi, i):
        x = b.pop(i)
        self.size -= 1
        if not b:
            del self.a[bi]
        return x

    def discard(self, x):
        if self.size == 0:
            return False
        b, bi, i = self._position(x)
        if i == len(b) or b[i] != x:
            return False
        self._pop(b, bi, i)
        return True

    def lt(self, x):
        for b in reversed(self.a):
            if b[0] < x:
                return b[bisect_left(b, x) - 1]

    def le(self, x):
        for b in reversed(self.a):
            if b[0] <= x:
                return b[bisect_right(b, x) - 1]

    def gt(self, x):
        for b in self.a:
            if b[-1] > x:
                return b[bisect_right(b, x)]

    def ge(self, x):
        for b in self.a:
            if b[-1] >= x:
                return b[bisect_left(b, x)]

    def __getitem__(self, i):
        if i < 0:
            for b in reversed(self.a):
                i += len(b)
                if i >= 0:
                    return b[i]
        else:
            for b in self.a:
                if i < len(b):
                    return b[i]
                i -= len(b)
        raise IndexError

    def pop(self, i=-1):
        if i < 0:
            for bi in range(len(self.a) - 1, -1, -1):
                b = self.a[bi]
                i += len(b)
                if i >= 0:
                    return self._pop(b, bi, i)
        else:
            for bi, b in enumerate(self.a):
                if i < len(b):
                    return self._pop(b, bi, i)
                i -= len(b)
        raise IndexError

    def index(self, x):
        res = 0
        for b in self.a:
            if b[-1] >= x:
                return res + bisect_left(b, x)
            res += len(b)
        return res

    def index_right(self, x):
        res = 0
        for b in self.a:
            if b[-1] > x:
                return res + bisect_right(b, x)
            res += len(b)
        return res
