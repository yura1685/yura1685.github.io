import random

MOD = (1 << 61) - 1
BASE = random.randrange(1 << 20, MOD - 1)


class RollingHash:
    def __init__(self, s):
        if type(s) is str:
            s = list(map(ord, s))
        n = len(s)
        self.h = [0] * (n + 1)
        self.pw = [1] * (n + 1)
        for i, x in enumerate(s):
            self.h[i + 1] = (self.h[i] * BASE + x) % MOD
            self.pw[i + 1] = self.pw[i] * BASE % MOD

    def get(self, l, r):
        # s[l:r] のハッシュ
        return (self.h[r] - self.h[l] * self.pw[r - l]) % MOD

    def lcp(self, other, i, j):
        # self の i 文字目からと other の j 文字目からの最長共通接頭辞の長さ
        ok, ng = 0, min(len(self.h) - i, len(other.h) - j)
        while ng - ok > 1:
            m = (ok + ng) // 2
            if self.get(i, i + m) == other.get(j, j + m):
                ok = m
            else:
                ng = m
        return ok


def connect(h1, h2, len2):
    # 長さ len2 の文字列のハッシュ h2 を、ハッシュ h1 の文字列の後ろにつなげる
    return (h1 * pow(BASE, len2, MOD) + h2) % MOD
