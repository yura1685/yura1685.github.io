from collections import deque

DIR4 = [(1, 0), (-1, 0), (0, 1), (0, -1)]
DIR8 = DIR4 + [(1, 1), (1, -1), (-1, 1), (-1, -1)]
INF = 1 << 60

def grid_bfs(grid, sy, sx, wall="#", dirs=DIR4):
    # grid は文字列のリスト。到達できないマスは -1
    return grid_bfs_multi(grid, [(sy, sx)], wall, dirs)

def grid_bfs_multi(grid, starts, wall="#", dirs=DIR4):
    # starts = [(y, x), ...] のどれかから各マスへの最短手数。到達できないマスは -1
    h, w = len(grid), len(grid[0])
    dist = [[-1] * w for _ in range(h)]
    q = []
    for y, x in starts:
        if dist[y][x] == -1:
            dist[y][x] = 0
            q.append((y, x))
    for y, x in q:
        d = dist[y][x] + 1
        for dy, dx in dirs:
            ny, nx = y + dy, x + dx
            if 0 <= ny < h and 0 <= nx < w and grid[ny][nx] != wall and dist[ny][nx] == -1:
                dist[ny][nx] = d
                q.append((ny, nx))
    return dist

def bfs(g, s):
    # 重みなしグラフ g[v] = [to, ...] で、s からの最短距離と最短路木での親。到達できない頂点は距離 -1
    return bfs_multi(g, [s])

def bfs_multi(g, starts):
    # starts のどれかから各頂点への最短距離と、最短路木での親（始点と到達できない頂点は -1）
    n = len(g)
    dist = [-1] * n
    prev = [-1] * n
    q = []
    for s in starts:
        if dist[s] == -1:
            dist[s] = 0
            q.append(s)
    for v in q:
        d = dist[v] + 1
        for to in g[v]:
            if dist[to] == -1:
                dist[to] = d
                prev[to] = v
                q.append(to)
    return dist, prev

def restore_path(prev, t):
    # 始点から t までの最短路の頂点列（t に到達できるときだけ使う）
    path = []
    while t != -1:
        path.append(t)
        t = prev[t]
    return path[::-1]

def bfs01(g, s):
    # g[v] = [(to, cost), ...]、cost は 0 か 1
    n = len(g)
    dist = [INF] * n
    dist[s] = 0
    dq = deque([s])
    while dq:
        v = dq.popleft()
        d = dist[v]
        for to, c in g[v]:
            if d + c < dist[to]:
                dist[to] = d + c
                if c == 0:
                    dq.appendleft(to)
                else:
                    dq.append(to)
    return dist
