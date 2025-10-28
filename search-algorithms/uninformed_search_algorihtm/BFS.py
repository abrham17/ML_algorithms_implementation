"""
add a node to the frontier
remove a node from the frontier
check if the node contains the goal state
expand the node to generate its children
check if the child nodes have been explored or are already in the frontier
"""
from collections import deque
class Bfs:
    def __init__(self , graph):
        self.graph = graph
        self.parent = {}
    def bfs(self , start , goal):
        frontier = deque([start])
        explored = set()
        while frontier:
            current = frontier.popleft()
            if current == goal:
                return self.reconstruct_path(start , goal)
            explored.add(current)
            for child in self.graph[current]:
                if child not in explored and child not in frontier:
                    self.parent[current] = child
                    frontier.append(child)

        return "No Solution Found"
    def reconstruct_path(self , start , goal):
        path = []
        current = self.parent.get(start)
        while current is not None:
            path.append(current)
            current = self.parent.get(current)
        return path

    
graph = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': [],
    'E': ['F'],
    'F': []
}

bfs = Bfs(graph)
path = bfs.bfs("A" , "F")
print("Path found:", path)
