def compress(a):
    # 値の小さい順に 0, 1, 2, ... を振り直す
    vals = sorted(set(a))
    idx = {v: i for i, v in enumerate(vals)}
    return [idx[x] for x in a], vals
