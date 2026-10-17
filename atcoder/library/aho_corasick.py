class AhoCorasick:
    def __init__(self, patterns):
        self.go = [{}]   # go[v][c] = 状態 v で文字 c を読んだあとの状態（Trie の辺と、step で求めたもの）
        self.node = []   # node[i] = パターン i を読み終えた状態
        for s in patterns:
            v = 0
            for c in s:
                to = self.go[v].get(c)
                if to is None:
                    to = len(self.go)
                    self.go[v][c] = to
                    self.go.append({})
                v = to
            self.node.append(v)
        n = len(self.go)
        self.fail = [0] * n  # fail[v] = v の文字列の真の接尾辞で、Trie にある最長のもの
        self.out = [0] * n   # out[v] = v の文字列の接尾辞になっているパターンの個数
        for v in self.node:
            self.out[v] += 1
        self.order = [0]     # BFS 順
        for v in self.order:
            for c, to in self.go[v].items():
                f = self.fail[v]
                while f and c not in self.go[f]:
                    f = self.fail[f]
                if v and c in self.go[f]:
                    self.fail[to] = self.go[f][c]
                self.out[to] += self.out[self.fail[to]]
                self.order.append(to)

    def step(self, v, c):
        # 状態 v で文字 c を読んだあとの状態
        go = self.go
        path = []
        while c not in go[v]:
            path.append(v)
            if v == 0:
                go[0][c] = 0
                break
            v = self.fail[v]
        res = go[v][c]
        for u in path:
            go[u][c] = res
        return res

    def count(self, text):
        # 各パターンが text に現れる回数のリスト
        cnt = [0] * len(self.go)
        v = 0
        for c in text:
            v = self.step(v, c)
            cnt[v] += 1
        for v in reversed(self.order[1:]):
            cnt[self.fail[v]] += cnt[v]
        return [cnt[v] for v in self.node]
