import pygame
import math

class planet:
    def __init__(self, screen, color, mass, radius, position:tuple, velocity:tuple, screen_size) -> None:
        self.screen = screen
        self.name = "Planet"
        self.screen_size = screen_size
        self.mass = mass
        self.radius = radius
        self.density = (self.mass)/(math.pi * (self.radius)**2)
        self.color = color
        self.x = float(position[0])
        self.y = float(position[1])
        self.velx = float(velocity[0])
        self.vely = float(velocity[1])
        self.path = []
        self.age = 0

    def draw(self, screen, camera_pos, zoom, screen_w, screen_h):
        sx = (self.x - camera_pos[0]) * zoom + screen_w // 2
        sy = (self.y - camera_pos[1]) * zoom + screen_h // 2
        pygame.draw.circle(screen, self.color, (int(sx), int(sy)), max(1, int(self.radius * zoom)))

    def move_real(self, *bodies):
        G = 1  # scaled constant for fun
        self.age += 1
        ax_total, ay_total = 0, 0

        for body in bodies:
            dx = body.x - self.x
            dy = body.y - self.y
            r = math.sqrt(dx**2 + dy**2)
            if r == 0: 
                continue
            force = G * (self.mass * body.mass) / (r**2)
            ax_total += force * dx / (r * self.mass)
            ay_total += force * dy / (r * self.mass)

        dt = 0.1
        self.velx += ax_total * dt
        self.vely += ay_total * dt
        self.x += self.velx * dt
        self.y += self.vely * dt

        self.path.append((self.x, self.y))
        self.path = self.path[-200:]

    def detect_collision(self, *bodies):
        collided_objects = []
        for body in bodies:
            dx = body.x - self.x
            dy = body.y - self.y
            r = math.sqrt(dx**2 + dy**2)
            if math.sqrt((dx)**2+ (dy)**2) <= self.radius + body.radius:
                collided_objects.append(body)
        if collided_objects:
            return collided_objects
        return None

    def merge(self, *bodies):
        bodies_n = self.detect_collision(*bodies)
        to_remove = []

        if bodies_n:
            for body in bodies_n:
                if self.age < 30 or body.age < 30:
                    continue  
                if body.name == "star" and self.name != "star":
                    return [self]  # this planet removed
                elif self.name == "star" and body.name != "star":
                    to_remove.append(body)
                
                else:
                    total_mass = self.mass + body.mass
                    self.velx = (self.velx * self.mass + body.velx * body.mass) / total_mass
                    self.vely = (self.vely * self.mass + body.vely * body.mass) / total_mass
                    self.x = (self.x * self.mass + body.x * body.mass) / total_mass
                    self.y = (self.y * self.mass + body.y * body.mass) / total_mass
                    self.mass = total_mass
                    self.radius = math.sqrt(self.mass / (math.pi * self.density))
                    to_remove.append(body)

            return to_remove

        return []

    def draw_path(self, screen, camera_pos, zoom, screen_w, screen_h):
        if len(self.path) > 2:
            points = [((x - camera_pos[0]) * zoom + screen_w // 2,
                       (y - camera_pos[1]) * zoom + screen_h // 2)
                      for (x, y) in self.path]
            pygame.draw.lines(screen, "red", False, points, 2)

    
class star(planet):
    def __init__(self, screen, color, mass, radius, position: tuple, velocity: tuple, screen_size) -> None:
        super().__init__(screen, color, mass, radius, position, velocity, screen_size)
        self.name = "star"