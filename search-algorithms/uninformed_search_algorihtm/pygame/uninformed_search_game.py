# main.py
import pygame
from algorithms import bfs, dfs, ucs, astar

MAZE = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,1,0,0,0,0,0,0,0,0,1],
    [1,0,1,0,1,0,1,1,1,1,1,0,0,1],
    [1,0,1,0,0,0,0,0,0,1,0,0,0,1],
    [1,0,1,1,1,1,1,0,0,1,1,1,0,1],
    [1,0,0,0,0,0,1,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]

pygame.init()

WIDTH, HEIGHT = 700, 350
ROWS, COLS = len(MAZE), len(MAZE[0])
CELL_SIZE = WIDTH // COLS

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pacman Pathfinding Visualization")

WHITE = (255,255,255)
BLACK = (0,0,0)
BLUE = (0,0,255)
RED = (255,0,0)
GREEN = (0,255,0)
YELLOW = (255,255,0)

start = (1,1)
goal = (5,12)
algorithm = "UCS"  # Change to BFS, DFS, UCS, or A*

if algorithm == "BFS":
    path = bfs(start, goal, MAZE)
elif algorithm == "DFS":
    path = dfs(start, goal, MAZE)
elif algorithm == "UCS":
    path = ucs(start, goal, MAZE)
else:
    path = astar(start, goal, MAZE)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLACK)

    for i in range(ROWS):
        for j in range(COLS):
            rect = pygame.Rect(j*CELL_SIZE, i*CELL_SIZE, CELL_SIZE-1, CELL_SIZE-1)
            color = BLUE if MAZE[i][j] == 1 else WHITE
            pygame.draw.rect(screen, color, rect)

    for (x, y) in path:
        pygame.draw.rect(screen, YELLOW, (y*CELL_SIZE, x*CELL_SIZE, CELL_SIZE-1, CELL_SIZE-1))

    pygame.draw.rect(screen, GREEN, (start[1]*CELL_SIZE, start[0]*CELL_SIZE, CELL_SIZE-1, CELL_SIZE-1))
    pygame.draw.rect(screen, RED, (goal[1]*CELL_SIZE, goal[0]*CELL_SIZE, CELL_SIZE-1, CELL_SIZE-1))

    pygame.display.flip()

pygame.quit()
