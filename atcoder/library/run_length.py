def run_length(a):
    res = []
    n = len(a)
    i = 0
    while i < n:
        j = i + 1
        while j < n and a[j] == a[i]:
            j += 1
        res.append((a[i], j - i))
        i = j
    return res

def run_length_ranges(a):
    res = []
    n = len(a)
    i = 0
    while i < n:
        j = i + 1
        while j < n and a[j] == a[i]:
            j += 1
        res.append((a[i], i, j))
        i = j
    return res

def run_length_decode(rle):
    res = []
    for x, k in rle:
        res.extend([x] * k)
    return res
