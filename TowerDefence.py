import pygame
import math

countx = 20
county = 20
cellsize = 40
width = countx * cellsize + 1
height = county * cellsize + 1
fps = 60
bullets = []
towers = []

pygame.init()
window = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()


class Tower:
    def __init__(self, x, y, size, color, damage, firespeed, price, attackrad):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.damage = damage
        self.firespeed = firespeed
        self.fire_rate_tick = 0
        self.price = price
        self.attackrad = attackrad

    def draw(self):
        pygame.draw.circle(window, self.color, [self.x, self.y], self.size)


class CommonTower(Tower):
    def fire(self):
        if self.fire_rate_tick <= 0:
            addbullet(self.x, self.y, 3, 'green', 5, 20)
            self.fire_rate_tick = self.firespeed
        else:
            self.fire_rate_tick -= 1 / fps


class Bullet:
    def __init__(self, x, y, size, color, damage, speed):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.damage = damage
        self.speed = speed

    def move(self):
        self.x += 10

    def draw(self):
        pygame.draw.circle(window, self.color, [self.x, self.y], self.size)


def addbullet(x, y, size, color, damage, speed):
    bullets.append(Bullet(x, y, size, color, damage, speed))


def maycreatetower(x, y):
    x += cellsize / 2
    y += cellsize / 2
    if len(towers) > 0:
        for tower in towers:
            if tower.x == x and tower.y == y:
                return False
    return True


def windowrender():
    x, y = getmpos()
    pygame.draw.rect(window, 'blue', [x, y, cellsize, cellsize])
    for i in range(countx + 1):
        pygame.draw.line(window, 'white', [i * cellsize, 0], [i * cellsize, height * cellsize])
    for i in range(county + 1):
        pygame.draw.line(window, 'white', [0, i * cellsize], [width * cellsize, i * cellsize])


def maketower():
    x, y = getmpos()
    if maycreatetower(x, y):
        towers.append(CommonTower(x + cellsize / 2, y + cellsize / 2, 10, 'green', 5, 0.5, 10, 150))
        print(towers)


def getmpos():
    mpos = pygame.mouse.get_pos()
    x = math.floor(mpos[0] / cellsize) * cellsize
    y = math.floor(mpos[1] / cellsize) * cellsize
    return x, y


def run():
    windowrender()
    for tower in towers:
        tower.draw()
        tower.fire()
    for bullet in bullets:
        bullet.move()
        bullet.draw()


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                maketower()
    window.fill('black')
    run()
    pygame.display.update()
    clock.tick(fps)
pygame.quit()
