import pygame
from pygame.math import Vector2
HEIGHT = 500
WIDTH = 520
g = 9.81
m = 2
clock = pygame.time.Clock()
dt = 0
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.init()
pygame.display.set_caption("Ball Simulation")

class circle:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius, width=1)

    def getx(self):
        return self.x
    def gety(self):
        return self.y
    def getradius(self):
        return self.radius

class ball:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.container = None
        self.velocity = Vector2(100,0)

    def setContainer(self, container):
        self.container = container
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

    def move(self, dx, dy):
        self.x += dx
        self.y += dy


    def update(self, dt):
        self.velocity.y += g * dt
        self.x += self.velocity.x * dt
        self.y += self.velocity.y * dt
        cr = self.container.getradius()
        cx = self.container.getx()
        cy = self.container.gety()
        hitbox_Ball = Vector2(self.x - cx, self.y - cy)
        hitbox_Ball_length = hitbox_Ball.length()
        if hitbox_Ball_length + self.radius >= cr:
            hitbox_Ball.normalize_ip()
            self.x = cx + (cr - self.radius) * hitbox_Ball.x
            self.y = cy + (cr - self.radius) * hitbox_Ball.y

            self.velocity = self.velocity - 2 * (self.velocity.dot(hitbox_Ball)) * hitbox_Ball

ball = ball(250, 250, 20, (255, 0, 0))
circle = circle(250, 250, 200, (0, 255, 0))
ball.setContainer(circle)
running = True
while running:
    dt = clock.tick(60) / 1000
    screen.fill((0, 0, 0))

    ball.update(dt)

    ball.draw(screen)
    circle.draw(screen)
    pygame.display.flip()


    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_n:
                print("Yfdjnfdnjf")
                running = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_p:
                print("p")
                ball.velocity = Vector2(1000, 1000)
        elif event.type == pygame.QUIT:
            running = False



pygame.quit()