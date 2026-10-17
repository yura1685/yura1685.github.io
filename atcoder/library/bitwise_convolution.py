def xor_convolution(f, g, mod=0):
    # h[k] = (i xor j = k となるすべての組についての f[i] g[j] の和)。長さは同じ 2 べき
    n = len(f)
    f, g = list(f), list(g)
    for a in (f, g):
        b = 1
        while b < n:
            for i in range(0, n, 2 * b):
                for j in range(i, i + b):
                    a[j], a[j + b] = a[j] + a[j + b], a[j] - a[j + b]
            b *= 2
    h = [x * y % mod for x, y in zip(f, g)] if mod else [x * y for x, y in zip(f, g)]
    b = 1
    while b < n:
        for i in range(0, n, 2 * b):
            for j in range(i, i + b):
                h[j], h[j + b] = h[j] + h[j + b], h[j] - h[j + b]
        b *= 2
    if mod:
        inv = pow(n, -1, mod)
        return [x * inv % mod for x in h]
    return [x // n for x in h]


def and_convolution(f, g, mod=0):
    # h[k] = (i and j = k となるすべての組についての f[i] g[j] の和)。長さは同じ 2 べき
    n = len(f)
    f, g = list(f), list(g)
    for a in (f, g):
        b = 1
        while b < n:
            for i in range(0, n, 2 * b):
                for j in range(i, i + b):
                    a[j] += a[j + b]
            b *= 2
    h = [x * y % mod for x, y in zip(f, g)] if mod else [x * y for x, y in zip(f, g)]
    b = 1
    while b < n:
        for i in range(0, n, 2 * b):
            for j in range(i, i + b):
                h[j] -= h[j + b]
        b *= 2
    return [x % mod for x in h] if mod else h


def or_convolution(f, g, mod=0):
    # h[k] = (i or j = k となるすべての組についての f[i] g[j] の和)。長さは同じ 2 べき
    n = len(f)
    f, g = list(f), list(g)
    for a in (f, g):
        b = 1
        while b < n:
            for i in range(0, n, 2 * b):
                for j in range(i, i + b):
                    a[j + b] += a[j]
            b *= 2
    h = [x * y % mod for x, y in zip(f, g)] if mod else [x * y for x, y in zip(f, g)]
    b = 1
    while b < n:
        for i in range(0, n, 2 * b):
            for j in range(i, i + b):
                h[j + b] -= h[j]
        b *= 2
    return [x % mod for x in h] if mod else h
