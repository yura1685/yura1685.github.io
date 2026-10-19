from sortedcontainers import SortedList


class RangeSet:
    # 整数の集合を、互いに重ならず隣り合わない半開区間 [l, r) の集まりとして持つ
    def __init__(self):
        self.ls = SortedList()  # 区間の左端
        self.r = {}             # r[l] = 左端が l の区間の右端
        self.total = 0          # 入っている整数の個数

    def __iter__(self):
        for l in self.ls:
            yield l, self.r[l]

    def __len__(self):
        return len(self.ls)

    def get(self, x):
        # x を含む区間 (l, r)。なければ None
        i = self.ls.bisect_right(x)
        if i:
            l = self.ls[i - 1]
            if x < self.r[l]:
                return l, self.r[l]
        return None

    def __contains__(self, x):
        return self.get(x) is not None

    def mex(self, x=0):
        # x 以上で、入っていない最小の整数
        iv = self.get(x)
        return x if iv is None else iv[1]

    def add(self, l, r):
        # [l, r) を加え、新しく加わった整数の個数を返す
        if l >= r:
            return 0
        ls = self.ls
        i = ls.bisect_right(l)
        if i and self.r[ls[i - 1]] >= l:  # 左隣の区間と重なるか隣り合うなら、そこから始める
            i -= 1
            l = ls[i]
        removed = 0
        while i < len(ls) and ls[i] <= r:  # [l, r] と重なるか隣り合う区間をまとめる
            q = ls.pop(i)
            rq = self.r.pop(q)
            removed += rq - q
            r = max(r, rq)
        ls.add(l)
        self.r[l] = r
        res = r - l - removed
        self.total += res
        return res

    def remove(self, l, r):
        # [l, r) を取り除き、取り除いた整数の個数を返す
        if l >= r:
            return 0
        ls = self.ls
        res = 0
        i = ls.bisect_left(l)
        if i:
            p = ls[i - 1]
            rp = self.r[p]
            if rp > l:  # 左端が l より前の区間を l で切る
                self.r[p] = l
                if rp > r:
                    ls.add(r)
                    self.r[r] = rp
                    self.total -= r - l
                    return r - l
                res += rp - l
        while i < len(ls) and ls[i] < r:
            q = ls.pop(i)
            rq = self.r.pop(q)
            if rq > r:
                ls.add(r)
                self.r[r] = rq
                res += r - q
                break
            res += rq - q
        self.total -= res
        return res
