import pygame
from pygame.math import Vector2
HEIGHT = 500
WIDTH = 800
g = 9.81
m = 2
clock = pygame.time.Clock()
dt = 0
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.init()
pygame.display.set_caption("Ball Simulation")
font = pygame.font.SysFont("bold", 36)


import pygame

class Polygon:
    def __init__(self, points, color):

        if len(points) != 4:
            raise ValueError("Il faut exactement 4 sommets pour un quadrilatère")
        self.vertices = points
        self.color = color

    def draw(self, screen):

        pygame.draw.polygon(screen, self.color, self.vertices, width=1)

    def getVertices(self):
        return self.vertices

    def getColor(self):
        return self.color
    def getX(self):
        return self.vertices[0][0]
    def getY(self):
        return self.vertices[0][1]
    def getWidth(self):
        return self.vertices[1][0] - self.vertices[0][0]
    def getHeight(self):
        return self.vertices[2][1] - self.vertices[0][1]


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
        self.x = x; self.y = y
        self.radius = radius
        self.color = color
        self.container = None
        self.velocity = Vector2(100, 0)

    def setContainer(self, container):
        self.container = container

    def draw(self, screen):
        pygame.draw.circle(screen, self.color,
                           (int(self.x), int(self.y)), self.radius)

    def freeFall(self, dt):
        self.velocity.y += g * dt
        self.y += self.velocity.y * dt
        self.x += self.velocity.x * dt
    def isInsideCircle(self):
        cr = self.container.getradius()
        cx = self.container.getx()
        cy = self.container.gety()
        dist = Vector2(self.x - cx, self.y - cy).length()
        return dist <= (cr - self.radius)

    def isInsidePolygon(self):
        verts = self.container.getVertices()
        P = Vector2(self.x, self.y)
        cx = sum(v[0] for v in verts) / len(verts)
        cy = sum(v[1] for v in verts) / len(verts)
        centroid = Vector2(cx, cy)

        for i in range(len(verts)):
            v1 = Vector2(verts[i])
            v2 = Vector2(verts[(i+1) % len(verts)])
            edge = v2 - v1
            normal = Vector2(-edge.y, edge.x)
            normal.normalize_ip()
            if (centroid - v1).dot(normal) > 0:
                normal = -normal
            if (P - v1).dot(normal) > 0:
                return False
        return True

    def update(self, dt):
        if self.container is None:
            return self.freeFall(dt)

        if isinstance(self.container, circle):
            inside = self.isInsideCircle()
        else:
            inside = self.isInsidePolygon()

        if not inside:
            return self.freeFall(dt)

        if isinstance(self.container, circle):

            self.velocity.y += g * dt
            self.x += self.velocity.x * dt
            self.y += self.velocity.y * dt

            cr = self.container.getradius()
            cx = self.container.getx()
            cy = self.container.gety()
            hit = Vector2(self.x - cx, self.y - cy)
            if hit.length() + self.radius >= cr:
                hit.normalize_ip()
                self.x = cx + (cr - self.radius) * hit.x
                self.y = cy + (cr - self.radius) * hit.y
                self.velocity -= 2 * (self.velocity.dot(hit)) * hit

        else:
            self.velocity.y += g * dt
            self.x += self.velocity.x * dt
            self.y += self.velocity.y * dt

            verts = self.container.getVertices()
            cx = sum(v[0] for v in verts) / len(verts)
            cy = sum(v[1] for v in verts) / len(verts)
            centroid = Vector2(cx, cy)
            P = Vector2(self.x, self.y)

            for i in range(len(verts)):
                v1 = Vector2(verts[i])
                v2 = Vector2(verts[(i+1) % len(verts)])
                edge = v2 - v1
                normal = Vector2(-edge.y, edge.x)
                normal.normalize_ip()
                if (centroid - v1).dot(normal) > 0:
                    normal = -normal
                dist = (P - v1).dot(normal)
                if dist + self.radius > 0:
                    corr = dist + self.radius
                    self.x -= corr * normal.x
                    self.y -= corr * normal.y
                    P = Vector2(self.x, self.y)
                    self.velocity -= 2 * self.velocity.dot(normal) * normal




circle_container  = circle(260, 250, 200, (0, 255, 0))
polygon_container = Polygon([(100,100),(400,100),(450,300),(80,350)], (255,255,255))
ball_obj = ball(0, 20, 9, (255, 0, 0))

choice = None
while choice is None:
    screen.fill((30, 30, 30))
    titre = font.render("Choisissez un conteneur via le clavier:", True, (200, 200, 200))
    opt1  = font.render("1 - Cercle", True, (200, 200, 200))
    opt2  = font.render("2 - Polygone", True, (200, 200, 200))
    screen.blit(titre, (80, 150))
    screen.blit(opt1,  (200, 230))
    screen.blit(opt2,  (200, 280))
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                ball_obj.setContainer(circle_container)
                choice = 'circle'
            elif event.key == pygame.K_2:
                ball_obj.setContainer(polygon_container)
                choice = 'polygon'
            elif event.key == pygame.K_n:
                pygame.quit()
                exit()

running = True
while running:
    dt = clock.tick(60) / 1000
    screen.fill((0, 0, 0))
    rules = font.render("Appuyez sur 'N' pour quitter", True, (200, 200, 200))
    screen.blit(rules, (20, 20))
    speed = font.render("Appuyez sur 'P' pour accelerer Vitesse: " + str(int(ball_obj.velocity.length())), True, (200, 200, 200))
    screen.blit(speed, (20, 60))

    ball_obj.update(dt)

    if choice == 'circle':
        circle_container.draw(screen)
    else:
        polygon_container.draw(screen)

    ball_obj.draw(screen)
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_n:
                running = False

            elif event.key == pygame.K_p:
                new_vel = ball_obj.velocity * 2
                if new_vel.length() > 1000:
                    new_vel.scale_to_length(1000)
                ball_obj.velocity = new_vel
pygame.quit()