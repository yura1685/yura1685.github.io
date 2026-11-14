class PersistentUnionFind:
    # 初期状態が版 0。unite は元の版を残したまま、新しい版の番号を返す
    # 各頂点の親（根なら -大きさ）を永続配列で持つ（union by size で経路圧縮はしない）
    def __init__(self, n):
        # 永続配列: 長さ 2^h の完全二分木。ノード o の子は C[o], C[o + 1]（最下段では値）
        h = 1
        while (1 << h) < n:
            h += 1
        self.h = h
        C = [-1, -1]
        for _ in range(h - 1):
            C += [len(C) - 2] * 2  # 初めはすべて -1 なので、各段のノードは 1 つを共有する
        self.C = C
        self.roots = [len(C) - 2]  # roots[ver] = 版 ver の配列の根

    def _get(self, o, i):
        # 根が o の配列の i 番目
        C = self.C
        s = self.h - 1
        while s:
            o = C[o + (i >> s & 1)]
            s -= 1
        return C[o + (i & 1)]

    def _set(self, o, i, x):
        # 根が o の配列の i 番目を x にした配列の根を返す（i までの道のノードだけ複製する）
        C = self.C
        root = len(C)
        C.append(C[o])
        C.append(C[o + 1])
        o = root
        s = self.h - 1
        while s:
            k = o + (i >> s & 1)
            c = C[k]
            o = len(C)
            C[k] = o
            C.append(C[c])
            C.append(C[c + 1])
            s -= 1
        C[o + (i & 1)] = x
        return root

    def find(self, ver, x):
        # 版 ver での x の根
        o = self.roots[ver]
        p = self._get(o, x)
        while p >= 0:
            x = p
            p = self._get(o, x)
        return x

    def unite(self, ver, a, b):
        # 版 ver で a と b をつないだ新しい版の番号を返す（すでに同じ集合なら ver をそのまま返す）
        a = self.find(ver, a)
        b = self.find(ver, b)
        if a == b:
            return ver
        o = self.roots[ver]
        sa = self._get(o, a)
        sb = self._get(o, b)
        if sa > sb:
            a, b = b, a
        o = self._set(o, a, sa + sb)
        o = self._set(o, b, a)
        self.roots.append(o)
        return len(self.roots) - 1

    def same(self, ver, a, b):
        # 版 ver で a と b が同じ集合にあるか
        return self.find(ver, a) == self.find(ver, b)

    def size(self, ver, x):
        # 版 ver での x を含む集合の大きさ
        return -self._get(self.roots[ver], self.find(ver, x))
