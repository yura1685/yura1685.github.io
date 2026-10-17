def mat_mul(A, B, mod=998244353):
    Bt = list(zip(*B))
    C = []
    for row in A:
        C.append([sum(a * b for a, b in zip(row, col)) % mod for col in Bt])
    return C


def mat_pow(A, k, mod=998244353):
    n = len(A)
    R = [[int(i == j) for j in range(n)] for i in range(n)]
    while k:
        if k & 1:
            R = mat_mul(R, A, mod)
        A = mat_mul(A, A, mod)
        k >>= 1
    return R
