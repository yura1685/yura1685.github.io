def _eliminate(M, m, p):
    # M の左から m 列を行基本変形で簡約化し、ピボットのある列のリストを返す（M を書き換える）
    n = len(M)
    cols = []
    r = 0
    for c in range(m):
        piv = -1
        for i in range(r, n):
            if M[i][c]:
                piv = i
                break
        if piv == -1:
            continue
        M[r], M[piv] = M[piv], M[r]
        row = M[r]
        inv = pow(row[c], p - 2, p)
        for k in range(c, len(row)):
            row[k] = row[k] * inv % p
        for i in range(n):
            if i != r and M[i][c]:
                f = M[i][c]
                Mi = M[i]
                for k in range(c, len(row)):
                    Mi[k] = (Mi[k] - f * row[k]) % p
        cols.append(c)
        r += 1
        if r == n:
            break
    return cols


def rank_mod(A, p):
    # 行列 A の mod p でのランク
    M = [[x % p for x in row] for row in A]
    return len(_eliminate(M, len(A[0]), p))


def det_mod(A, p):
    # 正方行列 A の行列式 mod p
    n = len(A)
    M = [[x % p for x in row] for row in A]
    det = 1
    for c in range(n):
        piv = -1
        for i in range(c, n):
            if M[i][c]:
                piv = i
                break
        if piv == -1:
            return 0
        if piv != c:
            M[c], M[piv] = M[piv], M[c]
            det = -det
        row = M[c]
        det = det * row[c] % p
        inv = pow(row[c], p - 2, p)
        for i in range(c + 1, n):
            if M[i][c]:
                f = M[i][c] * inv % p
                Mi = M[i]
                for k in range(c, n):
                    Mi[k] = (Mi[k] - f * row[k]) % p
    return det % p


def solve_mod(A, b, p):
    # A x ≡ b (mod p) の解を 1 つと、A x ≡ 0 の解全体の基底を (x, basis) で返す。解がなければ None
    n, m = len(A), len(A[0])
    M = [[x % p for x in A[i]] + [b[i] % p] for i in range(n)]
    cols = _eliminate(M, m, p)
    for i in range(len(cols), n):
        if M[i][m]:
            return None
    x = [0] * m
    for i, c in enumerate(cols):
        x[c] = M[i][m]
    is_piv = [False] * m
    for c in cols:
        is_piv[c] = True
    basis = []
    for f in range(m):
        if is_piv[f]:
            continue
        v = [0] * m
        v[f] = 1
        for i, c in enumerate(cols):
            v[c] = -M[i][f] % p
        basis.append(v)
    return x, basis
