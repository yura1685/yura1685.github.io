from collections import deque


def sliding_window_min(a, k):
    # res[i] = min(a[i:i + k])（0 <= i <= len(a) - k）
    dq = deque()  # 値が昇順になるように添字を持つ
    res = []
    for i, x in enumerate(a):
        while dq and a[dq[-1]] >= x:
            dq.pop()
        dq.append(i)
        if dq[0] <= i - k:
            dq.popleft()
        if i >= k - 1:
            res.append(a[dq[0]])
    return res


def sliding_window_max(a, k):
    # res[i] = max(a[i:i + k])（0 <= i <= len(a) - k）
    dq = deque()  # 値が降順になるように添字を持つ
    res = []
    for i, x in enumerate(a):
        while dq and a[dq[-1]] <= x:
            dq.pop()
        dq.append(i)
        if dq[0] <= i - k:
            dq.popleft()
        if i >= k - 1:
            res.append(a[dq[0]])
    return res


def prev_smaller(a, strict=True):
    # res[i] = a[j] < a[i] となる最大の j < i（なければ -1）。strict=False なら a[j] <= a[i]
    res = [-1] * len(a)
    st = []  # 値が単調増加になるように添字を持つ
    for i, x in enumerate(a):
        if strict:
            while st and a[st[-1]] >= x:
                st.pop()
        else:
            while st and a[st[-1]] > x:
                st.pop()
        if st:
            res[i] = st[-1]
        st.append(i)
    return res


def next_smaller(a, strict=True):
    # res[i] = a[j] < a[i] となる最小の j > i（なければ len(a)）。strict=False なら a[j] <= a[i]
    n = len(a)
    res = [n] * n
    st = []
    for i in range(n - 1, -1, -1):
        x = a[i]
        if strict:
            while st and a[st[-1]] >= x:
                st.pop()
        else:
            while st and a[st[-1]] > x:
                st.pop()
        if st:
            res[i] = st[-1]
        st.append(i)
    return res
