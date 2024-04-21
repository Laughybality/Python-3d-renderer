import pygame
from math import tan, pi, cos, sin

WIDTH, HEIGHT = 1200, 800
DEFAULT_FOV = pi / 0.314159
MIN_FOV = 30
MAX_FOV = 60
Z_NEAR = 0.1
Z_FAR = 1000.0

vertices = [
    (-1, -1, -1),
    (-1, -1, 1),
    (-1, 1, -1),
    (-1, 1, 1),
    (1, -1, -1),
    (1, -1, 1),
    (1, 1, -1),
    (1, 1, 1)
]

edges = [
    (0, 1), (1, 3), (3, 2), (2, 0),
    (4, 5), (5, 7), (7, 6), (6, 4),
    (0, 4), (1, 5), (2, 6), (3, 7)
]

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

def project(vertex, fov):
    x, y, z = vertex
    if z == 0:
        z = 0.1
    scale = (HEIGHT / 2) / tan(fov / 2)
    x_proj = int((x / z) * scale + WIDTH / 2)
    y_proj = int((y / z) * scale + HEIGHT / 2)
    return (x_proj, y_proj)

running = True
fov = DEFAULT_FOV
angle_x = pi / 4
angle_y = pi / 4
mouse_pressed = False
last_mouse_pos = None
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_RIGHT:
                mouse_pressed = True
                last_mouse_pos = pygame.mouse.get_pos()
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == pygame.BUTTON_RIGHT:
                mouse_pressed = False

    if mouse_pressed:
        current_mouse_pos = pygame.mouse.get_pos()
        if last_mouse_pos:
            dx = current_mouse_pos[0] - last_mouse_pos[0]
            dy = current_mouse_pos[1] - last_mouse_pos[1]
            angle_x -= dx * 0.01
            angle_y += dy * 0.01
        last_mouse_pos = current_mouse_pos

    if pygame.mouse.get_pressed()[0]:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if 100 <= mouse_x <= 300 and 10 <= mouse_y <= 30:
            fov = MIN_FOV + (MAX_FOV - MIN_FOV) * ((mouse_x - 100) / 200)

    screen.fill((0, 0, 0))

    pygame.draw.rect(screen, (255, 255, 255), (100, 10, 200, 20))
    pygame.draw.rect(screen, (0, 0, 255), (100, 10, int(((fov - MIN_FOV) / (MAX_FOV - MIN_FOV)) * 200), 20))

    rotated_vertices = [(x * cos(angle_x) + z * sin(angle_x),
                         y * cos(angle_y) - z * sin(angle_y),
                         z * cos(angle_x) - x * sin(angle_x))
                        for x, y, z in vertices]

    for edge in edges:
        start = rotated_vertices[edge[0]]
        end = rotated_vertices[edge[1]]
        start_proj = project(start, fov)
        end_proj = project(end, fov)
        pygame.draw.line(screen, (255, 255, 255), start_proj, end_proj, 2)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
