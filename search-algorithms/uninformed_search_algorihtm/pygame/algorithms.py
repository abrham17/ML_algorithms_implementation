import heapq
from collections import deque


def get_neighbors(pos, maze):
    x, y = pos
    moves = [(0,1), (1,0), (0,-1), (-1,0)]
    neighbors = []
    for dx, dy in moves:
        nx, ny = x+dx, y+dy
        if 0 <= nx < len(maze) and 0 <= ny < len(maze[0]) and maze[nx][ny] == 0:
            neighbors.append((nx, ny))
    return neighbors

def bfs(start, goal, maze):
    queue = deque([(start, [start])])
    visited = set()
    while queue:
        (x, y), path = queue.popleft()
        if (x, y) == goal:
            return path
        for n in get_neighbors((x, y), maze):
            if n not in visited:
                visited.add(n)
                queue.append((n, path + [n]))
    return []

def dfs(start, goal, maze):
    stack = [(start, [start])]
    visited = set()
    while stack:
        (x, y), path = stack.pop()
        if (x, y) == goal:
            return path
        for n in get_neighbors((x, y), maze):
            if n not in visited:
                visited.add(n)
                stack.append((n, path + [n]))
    return []

def ucs(start, goal, maze):
    pq = [(0, start, [start])]
    visited = set()
    while pq:
        cost, node, path = heapq.heappop(pq)
        if node == goal:
            return path
        if node in visited:
            continue
        visited.add(node)
        for n in get_neighbors(node, maze):
            heapq.heappush(pq, (cost + 1, n, path + [n]))
    return []

def astar(start, goal, maze):
    def h(n):
        return abs(n[0]-goal[0]) + abs(n[1]-goal[1])  # Manhattan distance
    pq = [(0 + h(start), 0, start, [start])]
    visited = set()
    while pq:
        f, g, node, path = heapq.heappop(pq)
        if node == goal:
            return path
        if node in visited:
            continue
        visited.add(node)
        for n in get_neighbors(node, maze):
            heapq.heappush(pq, (g + 1 + h(n), g + 1, n, path + [n]))
    return []

