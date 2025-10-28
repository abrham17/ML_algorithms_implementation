# no huristics used
# uses priority queue to explore least cost node first
# 

"""Uniform Cost Search (UCS) implementation.

This module provides a small UCS class that finds a least-cost path
from a start node to a goal node in a weighted graph. The graph is
represented as an adjacency dict mapping node -> list of (neighbor, cost).

        maze={'E':1,'W':0,'N':1,'S':0, 'edge_weight': {'E':inf,'W':inf,'N':inf,'S':inf}}


The UCS.ucs(start, goal) method returns a tuple (path, cost) on success
or (None, inf) if the goal is unreachable.
"""

import heapq
from math import inf
from typing import Dict, List, Tuple, Any
from pyamaze import maze,agent,COLOR,textLabel
from itertools import count


class ASTAR:
    def __init__(self, maze):
        self.maze = maze
    def manhattan_distance(self, node1, node2):
        """Calculate the Manhattan distance between two nodes."""
        return abs(node1[0] - node2[0]) + abs(node1[1] - node2[1])

    def A_star(self, start, goal):
        """Run A* Search from start to goal.
        h(n) is the manhattan distance between n and goal
        """
        deltas = {'N': (-1, 0), 'E': (0, 1), 'S': (1, 0), 'W': (0, -1)}
        h0 = self.manhattan_distance(start, goal)
        # frontier is a min-heap of tuples (cost_so_far, node, path_so_far)
        open_heap = []
        g_score = {start: 0}
        counter = count()
        # push initial entry: (f_score, tie, g_score, node, path)
        heapq.heappush(open_heap, (h0, next(counter), 0.0, start, [start]))

        while open_heap:
            f, _, g, node, path = heapq.heappop(open_heap)

            if node == goal:
                return path, g
            else:
                for d, (dx, dy) in deltas.items():
                    if not self.maze.maze_map[node][d]:
                        continue
                    else:
                            nbr = (node[0]+dx,node[1]+dy)
                            w = self.maze.maze_map[node]['edge_weight'][d]
                            tentative_g = g + w
                            if tentative_g < g_score.get(nbr, inf):
                                g_score[nbr] = tentative_g
                                f_score = tentative_g + self.manhattan_distance(nbr, goal)
                            # when pushing neighbor:
                                heapq.heappush(open_heap, (f_score, next(counter), tentative_g, nbr, path + [nbr]))

                        


        return None, inf

"""
#agent_1 = agent(maze_1,footprints=True,filled=True,color='red')
path = UCS(maze_1)
maze_1.tracePath({agent_1:path})
maze_1.run()
"""
if __name__ == "__main__":
    # Demo graph and run
    maze_1 = maze(5,7)
    maze_1.CreateMaze()
    solver = ASTAR(maze_1)
    agent_1 = agent(maze_1,footprints=True,filled=True,color='red')
    path, cost = solver.A_star((maze_1.rows, maze_1.cols) ,(1 , 1))
    print("Path found:", path)
    maze_1.tracePath({agent_1:path})
    maze_1.run()