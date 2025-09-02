import pygame, sys, math
import planetarybody

pygame.init()

screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
pygame.display.set_caption('Snake')
(width, height) = pygame.display.get_window_size()
print("Debug: ",width, height)
clock = pygame.time.Clock()
zoom = 1
Maximized = True

space = pygame.Surface((width, height))

bodies = set()
Sun = planetarybody.star(space, "yellow", 1000, 200, (width//2, height//2), (0, 0), (width, height))
Earth = planetarybody.planet(space, "blue", 300, 100, (width//2 - (300), height//2 - (300)), (-2, 1), (width, height))
Mercury = planetarybody.planet(space, "white", 50, 30, (width//2 + (300), height//2 + (300)), (-1.15, 1), (width, height))
bodies.update([Sun, Earth, Mercury])

Running = True
Camera_pos = (500, 500)
changing_cam = False
Paused = True

def world_to_screen(x, y, camera_pos, zoom, screen_w, screen_h):
    sx = (x - camera_pos[0]) * zoom + screen_w // 2
    sy = (y - camera_pos[1]) * zoom + screen_h // 2
    return int(sx), int(sy)

def safe_spawn(x, y, bodies, radius=40):
    for body in bodies:
        dx = body.x - x
        dy = body.y - y
        if math.sqrt(dx**2 + dy**2) <= body.radius + radius:
            return None
    return planetarybody.planet(screen, "green", 80, radius, (x, y), (0, 0), (width, height))


while Running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            world_x = (event.pos[0] - screen.get_width()//2) / zoom + Camera_pos[0]
            world_y = (event.pos[1] - screen.get_height()//2) / zoom + Camera_pos[1]
            new_planet = safe_spawn(world_x, world_y, bodies, radius=40)
            if new_planet:
                bodies.add(new_planet)        
        elif event.type == pygame.MOUSEBUTTONDOWN and (event.button == 2 or event.button == 3):
            changing_cam = True
            pygame.mouse.get_rel()
        elif event.type == pygame.MOUSEBUTTONUP and (event.button == 2 or event.button == 3):
            changing_cam = False
        elif event.type == pygame.MOUSEWHEEL:
            zoom = min(zoom * 1.2, 10) if event.y > 0 else max(zoom / 1.2, 0.1)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                Running = False
            elif event.key == pygame.K_SPACE:
                Paused = not Paused
            elif event.key == pygame.K_f:
                pygame.display.toggle_fullscreen()
                Maximized = not Maximized

    screen.fill((0, 0, 0))
    
    if not Paused:
        for body in bodies:
            others = [b for b in bodies if b is not body]
            body.move_real(*others)

    for body in bodies:
        body.draw(screen, Camera_pos, zoom, screen.get_width(), screen.get_height())
        body.draw_path(screen, Camera_pos, zoom, screen.get_width(), screen.get_height())

    to_remove_all = set()
    for body in list(bodies):
        if body in to_remove_all:
            continue
        others = [b for b in bodies if b is not body and b not in to_remove_all]
        losers = body.merge(*others)
        if losers:
            to_remove_all.update(losers)
    bodies.difference_update(to_remove_all)

    if changing_cam:
        dx, dy = pygame.mouse.get_rel()
        Camera_pos = (Camera_pos[0] - dx/zoom, Camera_pos[1] - dy/zoom)

    pygame.display.flip()

pygame.quit()
sys.exit()