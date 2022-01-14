from time import time
import pygame, sys, random, math
from pygame.locals import *

pygame.init()
pygame.display.set_caption("Yandex game")
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.set_num_channels(64)
random.seed()
clock = pygame.time.Clock()

WINDOW_SIZE = (1600, 900)
TILE_SIZE = 16
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)

SCALE_MULTIPLIER = 3
display = pygame.Surface((WINDOW_SIZE[0] / SCALE_MULTIPLIER, WINDOW_SIZE[1] / SCALE_MULTIPLIER))

def circle_surf(radius, color):
    surf = pygame.Surface((radius * 2, radius * 2))
    pygame.draw.circle(surf, color, (radius, radius), radius)
    surf.set_colorkey((0, 0, 0))
    return surf

class Particle:
    def __init__(self, x, y, velocity, time):
        self.x = x
        self.y = y
        self.velocity = velocity
        self.time = time
        self.spent_time = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocity = [random.randint(0, 20) / 10 - 1, random.randint(0, 20) / 10 - 1]
        self.time = random.randint(2, 6)
        self.spent_time = 0
        self.color = (random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))

    def update(self):
        if(self.y < WINDOW_SIZE[1] // SCALE_MULTIPLIER):
            self.x += self.velocity[0]
            self.y += self.velocity[1]
        self.time = max(1, self.time - 0.05)
        self.spent_time += 0.1
        self.velocity[1] += 0.04

    def draw(self, display):
        #  display.set_colorkey((0,0,0))
        #  pygame.draw.circle(display, (241, 100, 31, 255), [int(self.x), int(self.y)], int(self.time * 2))
        radius = self.time * 2
        display.blit(circle_surf(radius, (31, 100, 241)), [int(self.x - radius), int(self.y - radius)], special_flags=BLEND_RGB_ADD)
        pygame.draw.circle(display, (255, 255, 255), [int(self.x), int(self.y)], int(self.time))

class ExplodeParticle(Particle):
    def __init__(self, x, y, velocity, time):
        self.x = x
        self.y = y
        self.velocity = velocity
        self.time = time
        self.spent_time = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocity = random.randint(25, 30) / 15
        self.time = random.randint(2, 6)
        self.length = random.randint(10, 15)
        self.spent_time = 0
        self.color = (random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))
        self.angle = math.radians(random.randint(0, 360))
        self.width = random.randint(1, 3)

    def update(self):
        self.time += 0.1
        self.x += self.velocity * math.cos(self.angle)
        self.y += self.velocity * math.sin(self.angle)
        self.length -= 0.9

    def draw(self, display):
        #  display.set_colorkey((0,0,0))
        #  pygame.draw.circle(display, (241, 100, 31, 255), [int(self.x), int(self.y)], int(self.time * 2))
        pygame.draw.line(display, (255, 255, 255), (self.x, self.y), 
        (self.length * math.cos(self.angle) + self.x, self.length * math.sin(self.angle) + self.y), self.width)

class Explosion:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.particles = []
        for i in range(random.randint(5, 8)):
            self.particles.append(ExplodeParticle(x, y))

    def update(self):
        #  print(self.particles)
        for i, particle in sorted(enumerate(self.particles), reverse=True):
            particle.update()
            if particle.length <= 0:
                del particle
                self.particles.pop(i)
            
    def draw(self, display):
        for particle in self.particles:
            particle.draw(display)

particles = []
x1, y1 = 0, 113

clicked = False
explosions = []
while True:
    #  display.fill((43, 78, 149))
    display.fill((0, 0, 0))
    x, y = pygame.mouse.get_pos()
    x //= SCALE_MULTIPLIER
    y //= SCALE_MULTIPLIER
    x1 += 1

    # particles.append(Particle(x, y))

    # for i, particle in sorted(enumerate(particles), reverse=True):
    #     particle.update()
    #     particle.draw(display)
    #     if particle.spent_time >= 15 + particle.time:
    #         del particle
    #         particles.pop(i)

    #  pygame.draw.line(display, (0, 255, 0), (x, y), (0, 0), 5)

    #  pygame.draw.line(display, (0, 255, 0), (x, y), ())
    if clicked:
        explosions.append(Explosion(x, y))
    for i, explosion in sorted(enumerate(explosions), reverse=True):
            explosion.update()
            explosion.draw(display)
            if len(explosion.particles) == 0:
                del explosion
                explosions.pop(i)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            clicked = True
        if event.type == MOUSEBUTTONUP:
            clicked = False
    screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
    pygame.display.update()
    clock.tick(60)