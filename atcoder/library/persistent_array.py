class PersistentArray:
    # 経路コピーで永続化した配列。版の番号は 0, 1, 2, ...（どの版からでも新しい版を作れる）
    # ノード 1 つが要素 1 つを持つ二分木。版 0 ではノード k が a[k] を持ち、子は 2k + 1 と 2k + 2
    def __init__(self, a):
        n = len(a)
        self.lch = list(range(1, 2 * n, 2))  # lch[t] = ノード t の左の子
        self.rch = list(range(2, 2 * n + 1, 2))  # rch[t] = ノード t の右の子
        self.val = list(a)  # val[t] = ノード t が持つ要素
        self.root = [0]  # root[v] = 版 v の根

    def get(self, ver, i):
        # 版 ver の a[i]
        # i + 1 の 2 進表記を、先頭の 1 の次の桁から見ていき、0 なら左、1 なら右の子に進む
        lch, rch = self.lch, self.rch
        t = self.root[ver]
        k = i + 1
        for j in range(k.bit_length() - 2, -1, -1):
            t = rch[t] if k >> j & 1 else lch[t]
        return self.val[t]

    def set(self, ver, i, x):
        # 版 ver の a[i] を x にした新しい版を作り、その番号を返す（版 ver は変わらない）
        lch, rch, val = self.lch, self.rch, self.val
        t = self.root[ver]
        k = i + 1
        c = len(val)  # 根から順に、通るノードをコピーしたノード c, c + 1, ... を作る
        self.root.append(c)
        for j in range(k.bit_length() - 2, -1, -1):
            c += 1
            val.append(val[t])
            if k >> j & 1:
                lch.append(lch[t])
                rch.append(c)
                t = rch[t]
            else:
                lch.append(c)
                rch.append(rch[t])
                t = lch[t]
        lch.append(lch[t])
        rch.append(rch[t])
        val.append(x)
        return len(self.root) - 1
