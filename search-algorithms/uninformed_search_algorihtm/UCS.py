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


class UCS:
    def __init__(self, maze):
        self.maze = maze

    def ucs(self, start, goal):
        
        deltas = {'N': (-1, 0), 'E': (0, 1), 'S': (1, 0), 'W': (0, -1)}
        # frontier is a min-heap of tuples (cost_so_far, node, path_so_far)
        frontier = []
        best_score = {start: 0}
        # push initial entry: (f_score, tie, g_score, node, path)
        heapq.heappush(frontier, (0.0, start, [start]))

        while frontier:
            cost ,node, path = heapq.heappop(frontier)

            if node == goal:
                return path
            else:
                for d, (dx, dy) in deltas.items():
                    if not self.maze.maze_map[node][d]:
                        continue
                    else:
                            nbr = (node[0]+dx,node[1]+dy)
                            w = self.maze.maze_map[node]['edge_weight'][d]
                            tentative_score =  w
                            if tentative_score < best_score.get(nbr, inf):
                                best_score[nbr] = tentative_score
                            # when pushing neighbor:
                                heapq.heappush(frontier, (tentative_score, nbr, path + [nbr]))

                        


        return None

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
    solver = UCS(maze_1)
    agent_1 = agent(maze_1,footprints=True,filled=True,color='red')
    path = solver.ucs((maze_1.rows, maze_1.cols) ,(1 , 1))
    print("Path found:", path)
    maze_1.tracePath({agent_1:path})
    maze_1.run()