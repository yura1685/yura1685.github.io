from collections import deque

DIR4 = [(1, 0), (-1, 0), (0, 1), (0, -1)]
DIR8 = DIR4 + [(1, 1), (1, -1), (-1, 1), (-1, -1)]


def grid_bfs(grid, sy, sx, wall="#", dirs=DIR4):
    # grid は文字列のリスト。到達できないマスは -1
    h, w = len(grid), len(grid[0])
    dist = [[-1] * w for _ in range(h)]
    dist[sy][sx] = 0
    q = [(sy, sx)]
    for y, x in q:
        d = dist[y][x] + 1
        for dy, dx in dirs:
            ny, nx = y + dy, x + dx
            if 0 <= ny < h and 0 <= nx < w and grid[ny][nx] != wall and dist[ny][nx] == -1:
                dist[ny][nx] = d
                q.append((ny, nx))
    return dist


def bfs01(g, s):
    # g[v] = [(to, cost), ...]、cost は 0 か 1
    n = len(g)
    INF = 1 << 62
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
