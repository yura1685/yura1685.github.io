def prefix_function(s):
    # pi[i] = s[:i + 1] の接頭辞と接尾辞が一致する最大の長さ（s[:i + 1] 自身は除く）
    n = len(s)
    pi = [0] * n
    k = 0
    for i in range(1, n):
        while k and s[i] != s[k]:
            k = pi[k - 1]
        if s[i] == s[k]:
            k += 1
        pi[i] = k
    return pi


def find_all(t, p):
    # t の中で p が現れる位置（先頭の添字）のリスト。p は空でないこと
    pi = prefix_function(p)
    res = []
    k = 0
    for i, c in enumerate(t):
        while k and c != p[k]:
            k = pi[k - 1]
        if c == p[k]:
            k += 1
        if k == len(p):
            res.append(i - k + 1)
            k = pi[k - 1]
    return res


def min_period(s):
    # すべての i で s[i] == s[i + p] となる最小の p
    return len(s) - prefix_function(s)[-1] if s else 0
