class PrefixSum:
    def __init__(self, a):
        self.s = [0] * (len(a) + 1)
        for i, x in enumerate(a):
            self.s[i + 1] = self.s[i] + x

    def sum(self, l, r):
        # l <= i < r の a[i] の和
        return self.s[r] - self.s[l]


class PrefixSum2D:
    def __init__(self, a):
        h = len(a)
        w = len(a[0]) if h else 0
        s = [[0] * (w + 1) for _ in range(h + 1)]
        for i in range(h):
            for j in range(w):
                s[i + 1][j + 1] = s[i][j + 1] + s[i + 1][j] - s[i][j] + a[i][j]
        self.s = s

    def sum(self, x1, y1, x2, y2):
        # x1 <= i < x2, y1 <= j < y2 の a[i][j] の和
        s = self.s
        return s[x2][y2] - s[x1][y2] - s[x2][y1] + s[x1][y1]


class PrefixSum3D:
    def __init__(self, a):
        nx = len(a)
        ny = len(a[0]) if nx else 0
        nz = len(a[0][0]) if ny else 0
        s = [[[0] * (nz + 1) for _ in range(ny + 1)] for _ in range(nx + 1)]
        for i in range(nx):
            for j in range(ny):
                for k in range(nz):
                    s[i + 1][j + 1][k + 1] = (
                        a[i][j][k]
                        + s[i][j + 1][k + 1] + s[i + 1][j][k + 1] + s[i + 1][j + 1][k]
                        - s[i][j][k + 1] - s[i][j + 1][k] - s[i + 1][j][k]
                        + s[i][j][k]
                    )
        self.s = s

    def sum(self, x1, y1, z1, x2, y2, z2):
        # x1 <= i < x2, y1 <= j < y2, z1 <= k < z2 の a[i][j][k] の和
        s = self.s
        return (
            s[x2][y2][z2]
            - s[x1][y2][z2] - s[x2][y1][z2] - s[x2][y2][z1]
            + s[x1][y1][z2] + s[x1][y2][z1] + s[x2][y1][z1]
            - s[x1][y1][z1]
        )
