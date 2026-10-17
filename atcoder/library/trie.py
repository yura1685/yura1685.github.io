class Trie:
    def __init__(self):
        self.nxt = [{}]  # nxt[node][c] = 子ノード（根は 0）
        self.cnt = [0]   # そのノードが表す文字列を接頭辞に持つ、入っている文字列の個数
        self.end = [0]   # そのノードが表す文字列と等しい、入っている文字列の個数

    def insert(self, s):
        v = 0
        self.cnt[0] += 1
        for c in s:
            to = self.nxt[v].get(c)
            if to is None:
                to = len(self.cnt)
                self.nxt[v][c] = to
                self.nxt.append({})
                self.cnt.append(0)
                self.end.append(0)
            v = to
            self.cnt[v] += 1
        self.end[v] += 1

    def find(self, s):
        # s を表すノード（なければ -1）
        v = 0
        for c in s:
            v = self.nxt[v].get(c, -1)
            if v == -1:
                break
        return v

    def count(self, s):
        v = self.find(s)
        return 0 if v == -1 else self.end[v]

    def count_prefix(self, s):
        v = self.find(s)
        return 0 if v == -1 else self.cnt[v]

    def erase(self, s):
        # s を 1 つ削除する。s が入っていなければ False
        if self.count(s) == 0:
            return False
        v = 0
        self.cnt[0] -= 1
        for c in s:
            v = self.nxt[v][c]
            self.cnt[v] -= 1
        self.end[v] -= 1
        return True

    def lcp(self, s):
        # 入っている文字列との最長共通接頭辞の長さ
        v = 0
        res = 0
        for c in s:
            v = self.nxt[v].get(c, -1)
            if v == -1 or self.cnt[v] == 0:
                break
            res += 1
        return res
