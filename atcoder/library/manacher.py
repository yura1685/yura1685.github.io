def manacher(s):
    # r[i] = s[i] を中心とする奇数長の最長回文の半径（s[i - r[i] + 1:i + r[i]] が回文）
    n = len(s)
    r = [0] * n
    i = j = 0
    while i < n:
        while i - j >= 0 and i + j < n and s[i - j] == s[i + j]:
            j += 1
        r[i] = j
        k = 1
        while i - k >= 0 and k + r[i - k] < j:
            r[i + k] = r[i - k]
            k += 1
        i += k
        j -= k
    return r


def palindromes(s):
    # res[c] = 中心が c / 2 の最長回文の長さ（長さ 2N - 1）
    n = len(s)
    t = [None] * (2 * n + 1)
    t[1::2] = s
    r = manacher(t)
    return [r[c + 1] - 1 for c in range(2 * n - 1)]
