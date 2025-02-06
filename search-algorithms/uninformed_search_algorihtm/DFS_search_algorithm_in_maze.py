from pyamaze import maze,agent,COLOR,textLabel


def DFS(maze):
    start = (maze.rows , maze.cols)
    end = (1,1)
    frontier = [start]
    explored = [start]
    dfs_path = {}

    while frontier:
        current = frontier.pop()
        if current == end:
            break
        else:
            for d in "NESW":
                if maze.maze_map[current][d]:
                    if d == "N":
                        new = (current[0]-1,current[1])
                    elif d == "E":
                        new = (current[0],current[1]+1)
                    elif d == "S":
                        new = (current[0]+1,current[1])
                    elif d == "W":
                        new = (current[0],current[1]-1)
                if new and new not in explored:
                    dfs_path[new] = current
                    frontier.append(new)
                    explored.append(new)
    print(dfs_path)
    cell = end
    path = []
    while cell != start:
        path.append(cell)
        cell = dfs_path[cell]
    path.reverse()
    return path
maze_1 = maze(5,7)
maze_1.CreateMaze()
agent_1 = agent(maze_1,footprints=True,filled=True,color='red')
path = DFS(maze_1)
maze_1.tracePath({agent_1:path})
maze_1.run()