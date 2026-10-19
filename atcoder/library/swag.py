class SWAG:
    # 結合的な演算 op（可換でなくてよい）と単位元 e を持つキュー
    # fold() は先頭から末尾の順に op でまとめた値
    def __init__(self, op, e):
        self.op = op
        self.e = e
        self.fv = []  # 先頭側のスタック（末尾が先頭の値）
        self.fs = []  # fs[i] = op(fv[i], fv[i - 1], ..., fv[0])
        self.bv = []  # 末尾側のスタック（入れた順）
        self.bs = e  # op(bv[0], ..., bv[-1])

    def push(self, x):
        # 末尾に x を加える
        self.bv.append(x)
        self.bs = self.op(self.bs, x)

    def pop(self):
        # 先頭の値を取り除いて返す（空でないときだけ使う）
        if not self.fv:
            # 末尾側をすべて先頭側に移す
            op = self.op
            fv, fs = self.fv, self.fs
            s = self.e
            for x in reversed(self.bv):
                s = op(x, s)
                fv.append(x)
                fs.append(s)
            self.bv = []
            self.bs = self.e
        self.fs.pop()
        return self.fv.pop()

    def fold(self):
        # op(先頭, ..., 末尾)（空なら e）
        if self.fs:
            return self.op(self.fs[-1], self.bs)
        return self.bs

    def __len__(self):
        return len(self.fv) + len(self.bv)
