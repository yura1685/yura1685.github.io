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


def z_algorithm(s):
    # z[i] = s と s[i:] の最長共通接頭辞の長さ（z[0] = len(s)）
    n = len(s)
    z = [0] * n
    if n:
        z[0] = n
    l = r = 0  # s[l:r] = s[:r - l] である、r が最大の区間
    for i in range(1, n):
        k = min(r - i, z[i - l]) if i < r else 0
        while i + k < n and s[k] == s[i + k]:
            k += 1
        z[i] = k
        if i + k > r:
            l, r = i, i + k
    return z
