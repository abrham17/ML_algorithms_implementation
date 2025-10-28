class DFS:
    def __init__(self , graph):
        self.graph = graph
        self.parent = {}
    def dfs(self ,start , goal):
        frontier = [start]
        explored = set()
        while frontier:
            current = frontier.pop()
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
    'C' : ['D'],
    'D': [],   
    'E': ['F'],         
}
dfs = DFS(graph)
path = dfs.dfs("A" , "F")
print("Path found:", path)

