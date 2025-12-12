import pygame
import random
import time

pygame.init()

TILE = 20
COLS, ROWS = 40, 30
WIDTH, HEIGHT = COLS * TILE, ROWS * TILE + 40   # extra for heading

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Colors
WALL  = (0, 0, 0)       # Background / walls
MAZE  = (255, 0, 0)     # Red maze path (now thinner)
AGENT = (255, 255, 255) # White agent
GOAL  = (255, 255, 0)   # Yellow goal point
TEXT  = (200, 200, 200)

font = pygame.font.SysFont("consolas", 24)

# ---------------------------------------------------
# 1. MAZE GENERATION (Depth-first carve)
# ---------------------------------------------------

maze = [[1] * COLS for _ in range(ROWS)]  # 1 = wall, 0 = path

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

# ---------------------------------------------------
# 2. AGENT SETTINGS
# ---------------------------------------------------

agent_x, agent_y = 1, 1
finish = (COLS - 2, ROWS - 2)

directions = [(0,-1),(0,1),(-1,0),(1,0)]
random.shuffle(directions)
dir_x, dir_y = directions[0]

trail = []

# Timer
start_time = time.time()
end_time = start_time

# ---------------------------------------------------
# 3. GAME LOOP
# ---------------------------------------------------

running = True
reached_goal = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(WALL)

    # ----- Heading -----
    heading = font.render("Algorithm: Random Walk", True, TEXT)
    screen.blit(heading, (10, 5))

    # ----- Draw maze (thin lines) -----
    maze_offset = 40
    for y in range(ROWS):
        for x in range(COLS):
            if maze[y][x] == 0:
                pygame.draw.rect(screen, MAZE, (x*TILE+7, y*TILE+7+maze_offset, 6, 6))

    # Draw goal
    gx, gy = finish
    pygame.draw.rect(screen, GOAL, (gx*TILE+5, gy*TILE+5+maze_offset, 10, 10))

    # ----- Move agent -----
    if not reached_goal:
        nx = agent_x + dir_x
        ny = agent_y + dir_y

        if 0 <= nx < COLS and 0 <= ny < ROWS and maze[ny][nx] == 0:
            agent_x, agent_y = nx, ny
        else:
            dir_x, dir_y = random.choice(directions)

        # Mark trail
        trail.append((agent_x, agent_y))

        # Check if reached goal
        if (agent_x, agent_y) == finish:
            reached_goal = True
            end_time = time.time()

    # ----- Draw trail -----
    for tx, ty in trail:
        pygame.draw.rect(screen, AGENT, (tx*TILE+8, ty*TILE+8+maze_offset, 4, 4))

    # ----- Agent -----
    pygame.draw.rect(screen, AGENT, (agent_x*TILE+5, agent_y*TILE+5+maze_offset, 10, 10))

    # ----- Timer display -----
    if reached_goal:
        elapsed = round(end_time - start_time, 2)
        time_text = font.render(f"Time to Goal: {elapsed}s", True, TEXT)
    else:
        elapsed = round(time.time() - start_time, 2)
        time_text = font.render(f"Time: {elapsed}s", True, TEXT)

    screen.blit(time_text, (300, 5))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
