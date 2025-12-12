import pygame
import random
import time
import heapq

# -------------------------------
# 0. INITIALIZE PYGAME
# -------------------------------
pygame.init()
pygame.display.init()
pygame.font.init()

TILE = 20
COLS, ROWS = 41, 31  # odd dimensions
WIDTH, HEIGHT = COLS * TILE, ROWS * TILE + 40

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A* Maze")
clock = pygame.time.Clock()

# Colors
WALL  = (0, 0, 0)
MAZE  = (255, 0, 0)
AGENT = (255, 255, 255)
GOAL  = (255, 255, 0)
TEXT  = (200, 200, 200)

font = pygame.font.SysFont("consolas", 24)

# -------------------------------
# 1. MAZE GENERATION
# -------------------------------
maze = [[1] * COLS for _ in range(ROWS)]

def carve_maze():
    stack = []
    cx, cy = 1, 1
    maze[cy][cx] = 0
    stack.append((cx, cy))

    while stack:
        x, y = stack[-1]
        dirs = []
        if x > 2 and maze[y][x-2] == 1: dirs.append((-2, 0))
        if x < COLS - 3 and maze[y][x+2] == 1: dirs.append((2, 0))
        if y > 2 and maze[y-2][x] == 1: dirs.append((0, -2))
        if y < ROWS - 3 and maze[y+2][x] == 1: dirs.append((0, 2))

        if dirs:
            dx, dy = random.choice(dirs)
            maze[y + dy//2][x + dx//2] = 0
            maze[y + dy][x + dx] = 0
            stack.append((x + dx, y + dy))
        else:
            stack.pop()

carve_maze()

# Force the goal to be empty
maze[ROWS-2][COLS-2] = 0

# -------------------------------
# 2. AGENT SETTINGS
# -------------------------------
agent_x, agent_y = 1, 1
finish = (COLS - 2, ROWS - 2)
trail = []

start_time = time.time()
end_time = start_time

# -------------------------------
# 3. A* SEARCH
# -------------------------------
def heuristic(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def astar(start, goal):
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]

        x, y = current
        for dx, dy in [(0,-1),(0,1),(-1,0),(1,0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < COLS and 0 <= ny < ROWS and maze[ny][nx] == 0:
                neighbor = (nx, ny)
                tentative_g = g_score[current] + 1
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    g_score[neighbor] = tentative_g
                    f = tentative_g + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f, neighbor))
                    came_from[neighbor] = current
    return []

path = astar((agent_x, agent_y), finish)
if not path:
    print("No path found!")
    pygame.quit()
    exit()
path_index = 1  # start moving toward the first step

# -------------------------------
# 4. GAME LOOP
# -------------------------------
running = True
reached_goal = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(WALL)

    # ----- Heading -----
    heading = font.render("Algorithm: A* Search", True, TEXT)
    screen.blit(heading, (10, 5))

    # ----- Draw maze -----
    maze_offset = 40
    for y in range(ROWS):
        for x in range(COLS):
            if maze[y][x] == 0:
                pygame.draw.rect(screen, MAZE, (x*TILE+7, y*TILE+7+maze_offset, 6, 6))

    # Draw goal
    gx, gy = finish
    pygame.draw.rect(screen, GOAL, (gx*TILE+5, gy*TILE+5+maze_offset, 10, 10))

    # ----- Move agent -----
    if not reached_goal and path_index < len(path):
        agent_x, agent_y = path[path_index]
        trail.append((agent_x, agent_y))
        path_index += 1

        if (agent_x, agent_y) == finish:
            reached_goal = True
            end_time = time.time()

    # ----- Draw trail -----
    for tx, ty in trail:
        pygame.draw.rect(screen, AGENT, (tx*TILE+8, ty*TILE+8+maze_offset, 4, 4))

    # ----- Draw agent -----
    pygame.draw.rect(screen, AGENT, (agent_x*TILE+5, agent_y*TILE+5+maze_offset, 10, 10))

    # ----- Timer display -----
    elapsed = round(end_time - start_time, 2) if reached_goal else round(time.time() - start_time, 2)
    time_text = font.render(f"Time: {elapsed}s", True, TEXT)
    screen.blit(time_text, (300, 5))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
