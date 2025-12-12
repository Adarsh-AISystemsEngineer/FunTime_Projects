import pygame

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

# Polygon defined in local coordinates
triangle_points = [(0,0), (100,0), (50,100)]
poly_pos = pygame.Vector2(200, 200)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("purple")

    # Move polygon
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        poly_pos.y -= 300 * dt
    if keys[pygame.K_s]:
        poly_pos.y += 300 * dt
    if keys[pygame.K_a]:
        poly_pos.x -= 300 * dt
    if keys[pygame.K_d]:
        poly_pos.x += 300 * dt

    # Shift local coords by the polygon's position
    shifted = [(poly_pos.x + x, poly_pos.y + y) for (x,y) in triangle_points]

    # Draw polygon
    pygame.draw.polygon(screen, 'red', shifted)

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()
  