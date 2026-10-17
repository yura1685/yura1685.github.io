from functools import cmp_to_key


def arg_cmp(p, q):
    # 偏角（x 軸の正の向きから反時計回り、0 以上 2π 未満）で p と q を比べる。原点は最小とする
    hp = -1 if p[0] == 0 and p[1] == 0 else (0 if p[1] > 0 or (p[1] == 0 and p[0] > 0) else 1)
    hq = -1 if q[0] == 0 and q[1] == 0 else (0 if q[1] > 0 or (q[1] == 0 and q[0] > 0) else 1)
    if hp != hq:
        return hp - hq
    c = p[0] * q[1] - p[1] * q[0]
    return -1 if c > 0 else (1 if c < 0 else 0)


def arg_sort(ps):
    # 点（タプル (x, y)）を偏角の順に並べたリストを返す。偏角が同じ点は元の順
    return sorted(ps, key=cmp_to_key(arg_cmp))
