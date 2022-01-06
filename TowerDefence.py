import random

import pygame
import math
import time
import engine as e

countx = 34
county = 23
cellsize = 20
sclsz = 2
sclsz1 = 1.3
width1 = 1600
height1 = 900
width = width1 / sclsz
height = height1 / sclsz
fps = 60
inviztime = 0
bullets = []
towers = []
meat = []
drops = []
heals = []
walls = []
way = []
allmetal = []
tile_rects = []
tile_rects_coord = []
towernum = 0
uirect = [pygame.Rect(1361, 160, 240, 170), pygame.Rect(1361, 340, 240, 170),
          pygame.Rect(1361, 510, 240, 170), pygame.Rect(1361, 680, 240, 170)]
Map = [
        [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9],
        [9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9],
        [9, 0, 0, 0, 0, 0, 0, 0, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9],
        [9, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9],
        [9, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9],
        [9, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9],
        [9, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9],
        [9, 0, 0, 0, 0, 0, 0, 0, 4, 1, 1, 1, 1, 1, 5, 0, 0, 0, 0, 0, 0, 3, 1, 1, 1, 2, 0, 0, 0, 0, 0, 0, 0, 9],
        [9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 9],
        [9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 9],
        [9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 9],
        [3, 1, 1, 1, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 3, 1, 1, 1, 6],
        [9, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 9],
        [9, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 9],
        [9, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 9],
        [9, 0, 0, 0, 0, 1, 0, 0, 0, 3, 1, 1, 1, 1, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 9],
        [9, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 1, 1, 1, 4, 0, 0, 0, 9],
        [9, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9],
        [9, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9],
        [9, 0, 0, 0, 0, 3, 1, 1, 1, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9],
        [9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9],
        [9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9],
        [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9]
]
# down == 2
# right == 3
# up == 4
# left == 5
# end == 6
down = []
right = []
up = []
left = []
napr = ''
mousx = 0
mousy = 0
alive = True
pygame.init()
pygame.font.init()
myfont = pygame.font.Font('MaredivRegular.ttf', 30)
myfont1 = pygame.font.Font('MaredivRegular.ttf', 80)
window = pygame.Surface((width, height))
display = pygame.display.set_mode((width1, height1))
deadscreen = pygame.Surface((width, height), pygame.SRCALPHA)
crosshairsurf = pygame.Surface((width, height), pygame.SRCALPHA)
ss = pygame.image.load('data_img/spritesheet_3.png').convert()
sand = pygame.image.load('data_img/sand.png')
ssway = pygame.image.load('data_img/way.png')
ss.set_colorkey((0, 0, 0))
clock = pygame.time.Clock()
for y in range(len(Map)):
    if Map[y][0] == 3:
        meatstrt = cellsize / 2, y * cellsize + (cellsize / 2)
    for x in range(len(Map[y])):
        if Map[y][x] == 2:
            down.append([x * cellsize + cellsize / 2, y * cellsize + cellsize / 2])
        if Map[y][x] == 3:
            right.append([x * cellsize + cellsize / 2, y * cellsize + cellsize / 2])
        if Map[y][x] == 4:
            up.append([x * cellsize + cellsize / 2, y * cellsize + cellsize / 2])
        if Map[y][x] == 5:
            left.append([x * cellsize + cellsize / 2, y * cellsize + cellsize / 2])
        if Map[y][x] == 9:
            tile_rects.append(pygame.Rect(x * cellsize, y * cellsize, cellsize, cellsize))
            walls.append(pygame.Rect(x * cellsize, y * cellsize, cellsize, cellsize))
            tile_rects_coord.append([x, y])


class Player:
    def __init__(self, money):
        self.money = money

    def money(self):
        return self.money


class Healthpoints:
    def __init__(self, fullhp, nowhp):
        self.fullhp = fullhp
        self.nowhp = nowhp

    def draw(self, fullhp, nowhp):
        if nowhp < 1:
            nowhp = 0
        pygame.draw.rect(display, 'black', (0.03 * width, 0.05 * height, 250, 40))
        pygame.draw.rect(display, 'white', (0.03 * width, 0.05 * height, 250, 40), 8)
        pygame.draw.rect(display, 'red',
                         (0.03 * width + 1, 0.05 * height + 1, (nowhp / fullhp) * 250 - 1, 40 - 1))
        hp = myfont.render(str(f'{nowhp}/{fullhp}'), False, 'white')
        display.blit(hp, (0.01 * width + 250 / 3, 0.05 * height - 2))


class Tower:
    def __init__(self, x, y, size, color, damage, firespeed, price, bullspeed):
        self.x = x
        self.y = y
        self.size = size / sclsz1
        self.color = color
        self.damage = damage
        self.firespeed = firespeed
        self.firerate = 0
        self.price = price
        self.bullspeed = bullspeed

    # def draw(self):
    #     pygame.draw.circle(window, self.color, [self.x, self.y], self.size)

    def cost(self):
        return self.price


class CommonTower(Tower):
    def fire(self):
        if self.firerate <= 0:
            addbullet(self.x, self.y, 6, self.color, self.damage, self.bullspeed, 0)
            self.firerate = self.firespeed
        else:
            self.firerate -= 1 / fps

    def draw(self):
        outline_mask(greentow, (self.x - cellsize / 2, self.y - cellsize / 2))
        window.blit(pygame.transform.scale(greentow, (20, 20)), (self.x - cellsize / 2, self.y - cellsize / 2))
        # pygame.draw.circle(window, self.color, [self.x, self.y], self.size)


class QuadTower(Tower):
    def fire(self):
        if self.firerate <= 0:
            for direction in range(4):
                addbullet(self.x, self.y, 6, self.color, self.damage, self.bullspeed, direction)
            self.firerate = self.firespeed
        else:
            self.firerate -= 1 / fps

    def draw(self):
        outline_mask(yellowtow, (self.x - cellsize / 2, self.y - cellsize / 2))
        window.blit(pygame.transform.scale(yellowtow, (20, 20)), (self.x - cellsize / 2, self.y - cellsize / 2))


class TheEighthTower(Tower):
    def fire(self):
        if self.firerate <= 0:
            for direction in range(8):
                addbullet(self.x, self.y, 6, self.color, self.damage, self.bullspeed, direction)
            self.firerate = self.firespeed
        else:
            self.firerate -= 1 / fps

    def draw(self):
        outline_mask(redtow, (self.x - cellsize / 2, self.y - cellsize / 2))
        window.blit(pygame.transform.scale(redtow, (20, 20)), (self.x - cellsize / 2, self.y - cellsize / 2))


class HomingTower(Tower):
    def fire(self):
        if meat:
            if self.firerate <= 0:
                addbullet(self.x, self.y, 6, self.color, self.damage, self.bullspeed, 8)
                self.firerate = self.firespeed
            else:
                self.firerate -= 1 / fps

    def draw(self):
        outline_mask(bluetow, (self.x - cellsize / 2, self.y - cellsize / 2))
        window.blit(pygame.transform.scale(bluetow, (20, 20)), (self.x - cellsize / 2, self.y - cellsize / 2))


class Bullet:
    def __init__(self, x, y, size, color, damage, speed, direction):
        self.x = x
        self.y = y
        self.size = size / sclsz1
        self.color = color
        self.damage = damage
        self.speed = speed
        self.rect = pygame.Rect(x - size, y - size, size * 2, size * 2)
        self.direction = direction

    def move(self):
        if self.direction == 0:
            self.x += self.speed
        if self.direction == 1:
            self.x -= self.speed
        if self.direction == 2:
            self.y += self.speed
        if self.direction == 3:
            self.y -= self.speed
        if self.direction == 4:
            self.x += self.speed / math.sqrt(2)
            self.y += self.speed / math.sqrt(2)
        if self.direction == 5:
            self.x += self.speed / math.sqrt(2)
            self.y -= self.speed / math.sqrt(2)
        if self.direction == 6:
            self.x -= self.speed / math.sqrt(2)
            self.y += self.speed / math.sqrt(2)
        if self.direction == 7:
            self.x -= self.speed / math.sqrt(2)
            self.y -= self.speed / math.sqrt(2)
        if self.direction == 8:
            if meat:
                self.homingx = \
                    (meat[0].x - self.x) / math.sqrt((meat[0].x - self.x) ** 2 + (meat[0].y - self.y) ** 2) * self.speed
                self.homingxy = \
                    (meat[0].y - self.y) / math.sqrt((meat[0].x - self.x) ** 2 + (meat[0].y - self.y) ** 2) * self.speed
                self.x += self.homingx
                self.y += self.homingxy
            else:
                self.x += self.homingx
                self.y += self.homingxy
        self.rect = pygame.Rect(self.x - self.size, self.y - self.size, self.size * 2, self.size * 2)

    def draw(self):
        pygame.draw.circle(window, self.color, [self.x, self.y], self.size)
        # pygame.draw.rect(window, (255, 0, 0), self.rect, 1)

    def rng(self):
        return self.x

    def rect(self):
        return self.rect

    def damage(self):
        return self.damage


class FreshMeat:
    def __init__(self, x, y, hp, speed, size, color, reward):
        self.x = x
        self.y = y
        self.size = size / sclsz1
        self.color = color
        self.hp = hp
        self.speed = speed
        self.point = 0
        self.reward = reward
        self.napx = 1
        self.napy = 0
        self.rect = pygame.Rect(self.x - self.size, self.y - self.size, self.size * 2, self.size * 2)

    def draw(self):
        pygame.draw.circle(window, self.color, [self.x, self.y], self.size)
        # pygame.draw.rect(window, (255, 0, 0), self.rect, 1)

    def go(self):
        if [self.x, self.y] in right:
            self.napy = 0
            self.napx = 1
        if [self.x, self.y] in left:
            self.napy = 0
            self.napx = -1
        if [self.x, self.y] in up:
            self.napy = -1
            self.napx = 0
        if [self.x, self.y] in down:
            self.napy = 1
            self.napx = 0
        self.x += self.speed * self.napx
        self.y += self.speed * self.napy
        self.rect = pygame.Rect(self.x - self.size, self.y - self.size, self.size * 2, self.size * 2)

    def rng(self):
        return self.x

    def rect(self):
        return self.rect

    def damage(self, damage):
        self.hp -= damage

    def check(self):
        if self.hp <= 0:
            return False
        return True


class Drop:
    def __init__(self, x, y, speed, x0, y0, heal=False, met=False):
        self.x = x
        self.y = y
        self.speed = speed
        self.speedfly = speed
        self.t = False
        self.m = False
        self.x0 = x0
        self.y0 = y0
        self.a = 0
        self.heal = heal
        if met:
            self.met = met

    def fly(self):
        if round(self.x) != round(self.x0) and round(self.y0) != round(self.y) and not self.m and self.a < self.speed:
            self.x0 += (self.x - self.x0) / math.sqrt((self.x - self.x0) ** 2 +
                                                      (self.y - self.y0) ** 2) * self.speedfly - self.a
            self.y0 += (self.y - self.y0) / math.sqrt((self.x - self.x0) ** 2 +
                                                      (self.y - self.y0) ** 2) * self.speedfly - self.a
            self.a += 0.03
        else:
            self.m = True

    def draw(self):
        if self.heal:
            outline_mask(healim, (self.x0, self.y0))
            window.blit(pygame.transform.scale(healim, (5, 5)), (self.x0, self.y0))
            # pygame.draw.rect(window, 'red', (self.x0, self.y0, 5, 5))
        else:
            outline_mask(self.met, (self.x0, self.y0))
            window.blit(pygame.transform.scale(self.met, (5, 5)), (self.x0, self.y0))
            # pygame.draw.rect(window, 'gray', (self.x0, self.y0, 5, 5))

    def take(self):
        x = player.x + 8
        y = player.y + 8
        if math.sqrt((x - self.x0) ** 2 + (y - self.y0) ** 2) < 30:
            self.t = True
        if self.t:
            self.x0 += (x - self.x0) / math.sqrt((x - self.x0) ** 2 + (y - self.y0) ** 2) * self.speed
            self.y0 += (y - self.y0) / math.sqrt((x - self.x0) ** 2 + (y - self.y0) ** 2) * self.speed

    def taked(self):
        x = player.x
        y = player.y
        if x < self.x0 < (x + 16) and y < self.y0 < (y + 16):
            if self.heal:
                if player.hp + 2 > 10:
                    player.hp = 10
                else:
                    player.hp += 2
            return True
        return False


class Crosshair:
    def __init__(self):
        self.Cursor = pygame.image.load('data_img/curs_4x2.png')
        pygame.mouse.set_visible(False)

    def render(self):
        display.blit(self.Cursor, (pygame.mouse.get_pos()))


def createway():
    for y in range(len(Map)):
        for x in range(len(Map[0])):
            if Map[y][x] != 0 and Map[y][x] != 9:
                pygame.draw.rect(window, (186, 145, 65), [x * cellsize, y * cellsize,
                                                  cellsize, cellsize])
                way.append([x, y])


def createfloor():
    for y in range(len(Map)):
        for x in range(len(Map[0])):
            if Map[y][x] == 0:
                window.blit(sand, (x * cellsize, y * cellsize))


def createwall():
    cropped = pygame.Surface((20, 20))
    # cropped.fill((240, 181, 65))
    for y in range(len(Map)):
        for x in range(len(Map[0])):
            if (y == 0 and x == 0) or (y == 0 and x == 33) or (y == 22 and x == 0) or (y == 22 and x == 33):
                cropped.blit(ss, (0, 0), (20, 20, 20, 20))
                window.blit(pygame.transform.scale(cropped, (20, 20)), (x * cellsize, y * cellsize))
            elif y == 0:
                cropped.blit(ss, (0, 0), (20, 40, 20, 20))
                window.blit(pygame.transform.scale(cropped, (20, 20)), (x * cellsize, y * cellsize))
            elif y == 22:
                cropped.blit(ss, (0, 0), (20, 0, 20, 20))
                window.blit(pygame.transform.scale(cropped, (20, 20)), (x * cellsize, y * cellsize))
            elif x == 33:
                cropped.blit(ss, (0, 0), (0, 20, 20, 20))
                window.blit(pygame.transform.scale(cropped, (20, 20)), (x * cellsize, y * cellsize))
            elif x == 0:
                cropped.blit(ss, (0, 0), (40, 20, 20, 20))
                window.blit(pygame.transform.scale(cropped, (20, 20)), (x * cellsize, y * cellsize))
            if x == 0 and y == 10:
                cropped.blit(ss, (0, 0), (40, 40, 20, 20))
                window.blit(pygame.transform.scale(cropped, (20, 20)), (x * cellsize, y * cellsize))
            if x == 0 and y == 12:
                cropped.blit(ss, (0, 0), (40, 0, 20, 20))
                window.blit(pygame.transform.scale(cropped, (20, 20)), (x * cellsize, y * cellsize))
            if x == 33 and y == 10:
                cropped.blit(ss, (0, 0), (0, 40, 20, 20))
                window.blit(pygame.transform.scale(cropped, (20, 20)), (x * cellsize, y * cellsize))
            if x == 33 and y == 12:
                cropped.blit(ss, (0, 0), (0, 0, 20, 20))
                window.blit(pygame.transform.scale(cropped, (20, 20)), (x * cellsize, y * cellsize))


def meatcreate(x, y, hp, speed, size, color, reward):
    meat.append(FreshMeat(x, y, hp, speed, size, color, reward))


def addbullet(x, y, size, color, damage, speed, direction):
    bullets.append(Bullet(x, y, size, color, damage, speed, direction))


def adddrop(dx, dy, mx, my, heal=False):
    x = random.randint(-30, 30) + dx
    y = random.randint(-30, 30) + dy
    tex = random.choice(allmetal)
    drops.append(Drop(x, y, 1.3, mx, my, heal, tex))


def maycreatetower(x, y):
    future = pygame.Rect(x, y, cellsize, cellsize)
    x += cellsize / 2
    y += cellsize / 2
    if player.rect().colliderect(future):
        return False
    if math.sqrt((player.x + 8 - x) ** 2 + (player.y + 8 - y) ** 2) > cellsize * 3:
        return False
    if [x // cellsize, y // cellsize] in tile_rects_coord:
        return False
    if [x // cellsize, y // cellsize] in way:
        return False
    return True


def windowrender():
    x, y = getmpos()
    pygame.draw.rect(window, 'blue', [x, y, cellsize, cellsize])
    pygame.draw.rect(window, 'black', [x + 6, y + 6, cellsize - 12, cellsize - 12])
    for i in range(countx + 1):
        pygame.draw.line(window, 'white', [i * cellsize, 0], [i * cellsize, height * cellsize])
    for i in range(county + 1):
        pygame.draw.line(window, 'white', [0, i * cellsize], [width, i * cellsize])


def ui():
    pygame.draw.rect(display, (58, 63, 94), [1360, 0, 241, 921])
    greentow1 = pygame.transform.scale(greentow, (120, 120))
    outline_mask1(greentow1, (1420, 170))
    display.blit(pygame.transform.scale(greentow, (120, 120)), (1420, 170))
    cost = myfont.render('10', False, 'white')
    display.blit(cost, (1467, 285))
    yellowtow1 = pygame.transform.scale(yellowtow, (120, 120))
    outline_mask1(yellowtow1, (1420, 350))
    display.blit(pygame.transform.scale(yellowtow, (120, 120)), (1420, 350))
    cost = myfont.render('15', False, 'white')
    display.blit(cost, (1467, 465))
    redtow1 = pygame.transform.scale(redtow, (120, 120))
    outline_mask1(redtow1, (1420, 520))
    display.blit(pygame.transform.scale(redtow, (120, 120)), (1420, 520))
    cost = myfont.render('30', False, 'white')
    display.blit(cost, (1467, 635))
    bluetow1 = pygame.transform.scale(bluetow, (120, 120))
    outline_mask1(bluetow1, (1420, 690))
    display.blit(pygame.transform.scale(bluetow, (120, 120)), (1420, 690))
    money = myfont.render(str(plr.money), False, 'white')
    cost = myfont.render('50', False, 'white')
    display.blit(cost, (1467, 805))
    display.blit(money, (1461, 30))
    if towernum == 0:
        pass
    if towernum == 1:
        pygame.draw.rect(display, 'white', [1402, 160, 160, 170], 4)
    if towernum == 2:
        pygame.draw.rect(display, 'white', [1402, 340, 160, 170], 4)
    if towernum == 3:
        pygame.draw.rect(display, 'white', [1402, 510, 160, 170], 4)
    if towernum == 4:
        pygame.draw.rect(display, 'white', [1402, 680, 160, 170], 4)


def uiswtch():
    x, y = getmpos()
    for i in uirect:
        if i.collidepoint((x, y)):
            return uirect.index(i) + 1


def dieui():
    mx, my = pygame.mouse.get_pos()
    menu = pygame.Rect(width - 400, height + 50, 300, 70)
    exit = pygame.Rect(width, height + 50, 300, 70)
    pygame.draw.rect(display, 'gray', menu)
    pygame.draw.rect(display, 'gray', exit)
    if menu.collidepoint(mx, my):
        pygame.draw.rect(display, (112, 112, 112), menu)
    if exit.collidepoint(mx, my):
        pygame.draw.rect(display, (112, 112, 112), exit)
    f1 = myfont.render('Back to menu', False, 'white')
    display.blit(f1, (width - 350, height + 60))
    f2 = myfont.render('Exit', False, 'white')
    display.blit(f2, (width + 120, height + 60))


def outline_mask(img, loc):
    mask = pygame.mask.from_surface(img)
    mask_outline = mask.outline()
    n = 0
    for point in mask_outline:
        mask_outline[n] = (point[0] + loc[0], point[1] + loc[1])
        n += 1
    pygame.draw.polygon(window, (255, 255, 255), mask_outline, 3)


def outline_mask1(img, loc):
    mask = pygame.mask.from_surface(img)
    mask_outline = mask.outline()
    n = 0
    for point in mask_outline:
        mask_outline[n] = (point[0] + loc[0], point[1] + loc[1])
        n += 1
    pygame.draw.polygon(display, (255, 255, 255), mask_outline, 7)


def maketower(n):
    global towernum
    x, y = getmpos()
    if maycreatetower(x, y) and x <= width:
        if n:
            if n == 1 and plr.money >= 10:
                towers.append(CommonTower(x + cellsize / 2, y + cellsize / 2, 10, 'green', 40, 1, 10, 3.5))
                plr.money -= 10
                tile_rects.append(pygame.Rect(x, y, cellsize, cellsize))
                tile_rects_coord.append([x // cellsize, y // cellsize])
            if n == 2 and plr.money >= 15:
                towers.append(QuadTower(x + cellsize / 2, y + cellsize / 2, 10, 'yellow', 30, 1, 15, 2))
                plr.money -= 15
                tile_rects.append(pygame.Rect(x, y, cellsize, cellsize))
                tile_rects_coord.append([x // cellsize, y // cellsize])
            if n == 4 and plr.money >= 50:
                towers.append(HomingTower(x + cellsize / 2, y + cellsize / 2, 10, 'blue', 50, 1, 50, 2))
                plr.money -= 50
                tile_rects.append(pygame.Rect(x, y, cellsize, cellsize))
                tile_rects_coord.append([x // cellsize, y // cellsize])
            if n == 3 and plr.money >= 30:
                towers.append(TheEighthTower(x + cellsize / 2, y + cellsize / 2, 10, 'red', 20, 1, 30, 2))
                plr.money -= 30
                tile_rects.append(pygame.Rect(x, y, cellsize, cellsize))
                tile_rects_coord.append([x // cellsize, y // cellsize])
            towernum = 0


def getmpos():
    mpos = pygame.mouse.get_pos()
    if mpos[0] > width1 - 240:
        x = math.floor(mpos[0] / cellsize) * cellsize
        y = math.floor(mpos[1] / cellsize) * cellsize
    else:
        x = math.floor(mpos[0] / cellsize / sclsz) * cellsize
        y = math.floor(mpos[1] / cellsize / sclsz) * cellsize
    return x, y


def checklife():
    global alive
    if player.hp < 1:
        alive = False


def createrad():
    if towernum:
        radius = cellsize * 3
        circle = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(circle, (0, 200, 0, 128), (radius, radius), radius)
        window.blit(circle, (player.x + 8 - radius, player.y + 8 - radius))
        mx, my = getmpos()
        if maycreatetower(mx, my):
            pygame.draw.circle(window, 'green',
                               (mx // cellsize * cellsize + cellsize / 2, my // cellsize * cellsize + cellsize / 2),
                               10 / sclsz1)
        else:
            pygame.draw.circle(window, 'red',
                               (mx // cellsize * cellsize + cellsize / 2, my // cellsize * cellsize + cellsize / 2),
                               10 / sclsz1)


def run():
    if alive:
        global inviztime
        for tower in towers:
            tower.draw()
            tower.fire()
        for drop in drops:
            drop.fly()
            drop.take()
            drop.draw()
            if drop.taked():
                drops.remove(drop)
                plr.money += 1
        for bullet in bullets:
            bullet.move()
            bullet.draw()
            if player.rect().colliderect(bullet.rect):
                player.hp -= 1
                bullets.remove(bullet)
                break
            for wall in walls:
                if wall.colliderect(bullet.rect):
                    bullets.remove(bullet)
                    break
        for meats in meat:
            meats.draw()
            meats.go()
            for bullet in bullets:
                if Bullet.rng(bullet) > width or bullet.x < 0:
                    bullets.remove(bullet)
                elif meats.rect.colliderect(bullet.rect):
                    meats.damage(bullet.damage)
                    bullets.remove(bullet)
                if not meats.check():
                    if meats in meat:
                        for i in range(random.randint(3, 5)):
                            adddrop(meats.x, meats.y, meats.x, meats.y)
                        ch = random.randint(1, 10)
                        if ch == 5 or ch == 2:
                            adddrop(meats.x, meats.y, meats.x, meats.y, True)
                        meat.remove(meats)
            if FreshMeat.rng(meats) > width:
                meat.remove(meats)
            if inviztime > 500 and player.rect().colliderect(meats.rect):
                player.hp -= 1
                inviztime = 0
            else:
                inviztime += 1
    else:
        for tower in towers:
            tower.draw()
        for drop in drops:
            drop.fly()
            drop.draw()
        for bullet in bullets:
            bullet.move()
            bullet.draw()
            if player.rect().colliderect(bullet.rect):
                player.hp -= 1
                bullets.remove(bullet)
                break
            for wall in walls:
                if wall.colliderect(bullet.rect):
                    bullets.remove(bullet)
                    break
        for meats in meat:
            meats.draw()
            for bullet in bullets:
                if Bullet.rng(bullet) > width or bullet.x < 0:
                    bullets.remove(bullet)
                elif meats.rect.colliderect(bullet.rect):
                    meats.damage(bullet.damage)
                    bullets.remove(bullet)


plr = Player(100)
for i in range(10):
    meatcreate(meatstrt[0] - i * 20, meatstrt[1], 100, 0.5, 10, 'red', 10)
crosshair = Crosshair()
player = e.Entity(*[21, 21], 16, 16, 10, 'player')
fullhp = player.hp
playerhp = Healthpoints(fullhp, player.hp)
running = True
moving_right = False
moving_left = False
moving_up = False
moving_down = False
last_time = time.time()
greentower = pygame.image.load('data_img/greentower.png').convert_alpha()
greentow = pygame.Surface((20, 20), pygame.SRCALPHA)
greentow.blit(greentower, (0, 0), (0, 0, 20, 20))
yellowtower = pygame.image.load('data_img/yellowtower.png').convert_alpha()
yellowtow = pygame.Surface((20, 20), pygame.SRCALPHA)
yellowtow.blit(yellowtower, (0, 0), (0, 0, 20, 20))
redtower = pygame.image.load('data_img/redtower.png').convert_alpha()
redtow = pygame.Surface((20, 20), pygame.SRCALPHA)
redtow.blit(redtower, (0, 0), (0, 0, 20, 20))
bluetower = pygame.image.load('data_img/bluetower.png').convert_alpha()
bluetow = pygame.Surface((20, 20), pygame.SRCALPHA)
bluetow.blit(bluetower, (0, 0), (0, 0, 20, 20))
metim = pygame.image.load('data_img/metal.png').convert_alpha()
metal = pygame.Surface((5, 5), pygame.SRCALPHA)
metal.blit(metim, (0, 0), (0, 0, 5, 5))
metim1 = pygame.image.load('data_img/metal1.png').convert_alpha()
metal1 = pygame.Surface((5, 5), pygame.SRCALPHA)
metal1.blit(metim1, (0, 0), (0, 0, 5, 5))
metim2 = pygame.image.load('data_img/metal2.png').convert_alpha()
metal2 = pygame.Surface((5, 5), pygame.SRCALPHA)
metal2.blit(metim2, (0, 0), (0, 0, 5, 5))
metim3 = pygame.image.load('data_img/metal3.png').convert_alpha()
metal3 = pygame.Surface((5, 5), pygame.SRCALPHA)
metal3.blit(metim3, (0, 0), (0, 0, 5, 5))
allmetal.append(metal)
allmetal.append(metal1)
allmetal.append(metal2)
allmetal.append(metal3)
helim = pygame.image.load('data_img/heal.png').convert_alpha()
healim = pygame.Surface((5, 5), pygame.SRCALPHA)
healim.blit(helim, (0, 0), (0, 0, 5, 5))
while running:
    if alive:
        player_movement = [0, 0]
        dt = time.time() - last_time
        dt *= 60
        last_time = time.time()
        display.fill((0, 0, 0))
        if moving_right:
            player_movement[0] += 2 * dt
        if moving_left:
            player_movement[0] -= 2 * dt
        if moving_up:
            player_movement[1] -= 2 * dt
        if moving_down:
            player_movement[1] += 2 * dt
        player.move(player_movement, tile_rects, [])
        player.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    maketower(towernum)
                    if getmpos()[0] >= 1361:
                        towernum = uiswtch()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    moving_right = True
                if event.key == pygame.K_a:
                    moving_left = True
                if event.key == pygame.K_w:
                    moving_up = True
                if event.key == pygame.K_s:
                    moving_down = True
                if event.key == pygame.K_1:
                    towernum = 1
                if event.key == pygame.K_2:
                    towernum = 2
                if event.key == pygame.K_3:
                    towernum = 3
                if event.key == pygame.K_4:
                    towernum = 4
                if event.key == pygame.K_ESCAPE:
                    if towernum != 0:
                        towernum = 0
                    else:
                        running = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    moving_right = False
                if event.key == pygame.K_a:
                    moving_left = False
                if event.key == pygame.K_w:
                    moving_up = False
                if event.key == pygame.K_s:
                    moving_down = False
        window.fill('black')
        createfloor()
        createwall()
        createway()
        run()
        player.draw(window, [0, 0])
        createrad()
        display.blit(pygame.transform.scale(window, (width1, height1)), (0, 0))
        playerhp.draw(fullhp, player.hp)
        ui()
        crosshair.render()
        pygame.display.update()
        checklife()
        clock.tick(fps)
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        createfloor()
        createwall()
        createway()
        run()
        player.draw(window, [0, 0])
        createrad()
        display.blit(pygame.transform.scale(window, (width1, height1)), (0, 0))
        playerhp.draw(fullhp, player.hp)
        ui()
        deadscreen.fill((0, 0, 0, 128))
        display.blit(pygame.transform.scale(deadscreen, (width1, height1)), (0, 0))
        hp = myfont1.render('You died', False, 'white')
        display.blit(hp, (width - 200, height - 200))
        dieui()
        crosshair.render()
        pygame.display.update()
        pygame.display.update()
        clock.tick(fps)
pygame.quit()
