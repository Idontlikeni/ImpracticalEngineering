from dis import dis
import pygame, sys, os, random, math, time

from pygame import mouse
import engine as e
from pygame.locals import *
from pygame.mixer import set_num_channels

pygame.init()
pygame.display.set_caption("Yandex game")
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.set_num_channels(64)
random.seed()
clock = pygame.time.Clock()

WINDOW_SIZE = (1920, 1080)
TILE_SIZE = 16
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
flscr = False
# Vladimir's code
import random
import os
import pygame
import math
import time
import engine as e

countx = 34
county = 23
sclsz = 2
sclsz1 = 1.3
width1 = WINDOW_SIZE[0]
height1 = WINDOW_SIZE[1]
width = width1 / sclsz
height = height1 / sclsz
cellsize = (width - 120) // countx
cellsize1 = (width / 2) // countx
countx1 = round(width / 2 / cellsize)
county1 = round(height / 2 / cellsize)
if county1 * cellsize < height / 2:
    county1 += 1
if countx1 * cellsize < width / 2:
    countx1 += 1
fps = 60
flscr = False
show = False
inviztime = 0
inhub = True
meatend = False
bullets = []
towers = []
meat = []
drops = []
heals = []
walls = []
way = []
allmetal = []
tile_rects = []
tile_rects1 = []
tile_rects_coord = []
explosions = []
towernum = 0
spawntime = 0
playerv = 2
speedcoef = cellsize / 20
uirect = [pygame.Rect(68.05 * cellsize, 8 * cellsize, 12 * cellsize, 8.5 * cellsize),
          pygame.Rect(68.05 * cellsize, 17 * cellsize, 12 * cellsize, 8.5 * cellsize),
          pygame.Rect(68.05 * cellsize, 25.5 * cellsize, 12 * cellsize, 8.5 * cellsize),
          pygame.Rect(68.05 * cellsize, 34 * cellsize, 12 * cellsize, 8.5 * cellsize)]
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
dieuiclicked = False
alive = True
if 'fullscreen.txt' in os.listdir(os.getcwd()):
    stats = open('fullscreen.txt', 'r')
    x = stats.readlines()
    if x:
        if x[0] == "1":
            flscr = True
        else:
            flscr = False
    else:
        flscr = False
    stats.close()
pygame.init()
pygame.font.init()
myfont = pygame.font.Font('MaredivRegular.ttf', round(1.5 * cellsize))
myfont1 = pygame.font.Font('MaredivRegular.ttf', round(4 * cellsize))
window = pygame.Surface((width, height))
hubscreen = pygame.Surface((width / 2, height / 2))
hubscreen.fill((50, 50, 50))
if flscr:
    monitor = pygame.display.set_mode((width1, height1), pygame.FULLSCREEN)
else:
    monitor = pygame.display.set_mode((width1, height1))
deadscreen = pygame.Surface((width, height), pygame.SRCALPHA)
crosshairsurf = pygame.Surface((width, height), pygame.SRCALPHA)
ss = pygame.image.load('data_img/spritesheet_3.png').convert_alpha()
ss = pygame.transform.scale(ss, (3 * cellsize, 3 * cellsize))
sand = pygame.image.load('data_img/sand.png').convert_alpha()
sand = pygame.transform.scale(sand, (cellsize, cellsize))
ssand = pygame.Surface((cellsize, cellsize), pygame.SRCALPHA)
ssand.blit(sand, (0, 0), (0, 0, cellsize, cellsize))
ssway = pygame.image.load('data_img/way.png').convert_alpha()
cross = pygame.image.load('data_img/curs_4x2.png').convert_alpha()
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
    for y in range(len(Map)):
        for x in range(len(Map[0])):
            if Map[y][x] != 0 and Map[y][x] != 9:
                way.append([x, y])
for x in range(countx1):
    for y in range(county1):
        if x == 0 or x == countx1 - 1 or y == 0 or y == county1 - 1:
            tile_rects1.append(pygame.Rect(x * cellsize, y * cellsize, cellsize, cellsize))
tile_rects1.remove(pygame.Rect(0, county1 // 2 * cellsize, cellsize, cellsize))
tile_rects1.remove(pygame.Rect(countx1 // 2 * cellsize, 0, cellsize, cellsize))
lenwalls = len(tile_rects)


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
        pygame.draw.rect(monitor, 'black', (0.03 * width, 0.05 * height, 12.5 * cellsize, 2 * cellsize))
        pygame.draw.rect(monitor, 'white', (0.03 * width - 0.2 * cellsize, 0.05 * height - 0.2 * cellsize,
                                            12.5 * cellsize + 0.4 * cellsize, 2 * cellsize + 0.4 * cellsize))
        pygame.draw.rect(monitor, 'black', (0.03 * width, 0.05 * height, 12.5 * cellsize, 2 * cellsize))
        pygame.draw.rect(monitor, 'red',
                         (0.03 * width, 0.05 * height, (nowhp / fullhp) * 12.5 * cellsize, 2 * cellsize))
        hp = myfont.render(str(f'{nowhp}/{fullhp}'), False, 'white')
        monitor.blit(hp, (5.1 * cellsize, 0.9 * cellsize))


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
        window.blit(greentow, (self.x - cellsize / 2, self.y - cellsize / 2))
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
        window.blit(yellowtow, (self.x - cellsize / 2, self.y - cellsize / 2))


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
        window.blit(redtow, (self.x - cellsize / 2, self.y - cellsize / 2))


class HomingTower(Tower):
    def fire(self):
        if meat:
            if math.sqrt((meat[0].x - self.x) ** 2 + (meat[0].y - self.y) ** 2) < cellsize * 8:
                if self.firerate <= 0:
                    addbullet(self.x, self.y, 6, self.color, self.damage, self.bullspeed, 8)
                    self.firerate = self.firespeed
                else:
                    self.firerate -= 1 / fps

    def draw(self):
        outline_mask(bluetow, (self.x - cellsize / 2, self.y - cellsize / 2))
        window.blit(bluetow, (self.x - cellsize / 2, self.y - cellsize / 2))


class Bullet:
    def __init__(self, x, y, size, color, damage, speed, direction):
        self.x = x
        self.y = y
        self.size = size / sclsz1 * cellsize / 20
        self.color = color
        self.damage = damage
        self.speed = speed * cellsize / 20 * 60 / clock.get_fps()
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
    def __init__(self, x, y, hp, speed, size, color, slowed=False):
        self.x = x
        self.y = y
        self.size = size / sclsz1 * cellsize / 20
        self.color = color
        self.hp = hp
        self.speed = speed * cellsize / 20 * 60 / clock.get_fps()
        self.point = 0
        self.slowed = slowed
        self.napx = 1
        self.napy = 0
        self.rect = pygame.Rect(self.x - self.size, self.y - self.size, self.size * 2, self.size * 2)

    def draw(self):
        pygame.draw.circle(window, self.color, [self.x, self.y], self.size)
        # pygame.draw.rect(window, (255, 0, 0), self.rect, 1)

    def go(self):
        if [round(self.x), round(self.y)] in right:
            self.napy = 0
            self.napx = 1
        if [round(self.x), round(self.y)] in left:
            self.napy = 0
            self.napx = -1
        if [round(self.x), round(self.y)] in up:
            self.napy = -1
            self.napx = 0
        if [round(self.x), round(self.y)] in down:
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
        self.speed = speed * cellsize / 20 * 60 / clock.get_fps()
        self.speedfly = speed * cellsize / 20
        self.t = False
        self.m = False
        self.x0 = x0
        self.y0 = y0
        self.a = 0
        self.heal = heal
        if met:
            self.met = met

    def fly(self):
        if round(self.x) != round(self.x0) and round(self.y0) != round(self.y) and \
                not self.m and self.a < self.speed and self.speed > 0.03:
            self.x0 += (self.x - self.x0) / math.sqrt((self.x - self.x0) ** 2 +
                                                      (self.y - self.y0) ** 2) * self.speedfly - self.a
            self.y0 += (self.y - self.y0) / math.sqrt((self.x - self.x0) ** 2 +
                                                      (self.y - self.y0) ** 2) * self.speedfly - self.a
            self.a += 0.03
        else:
            self.m = True

    def draw(self):
        if self.heal:
            outline_mask2(healim, (self.x0, self.y0))
            window.blit(pygame.transform.scale(healim, (5 * cellsize / 20, 5 * cellsize / 20)), (self.x0, self.y0))
            # pygame.draw.rect(window, 'red', (self.x0, self.y0, 5, 5))
        else:
            outline_mask2(self.met, (self.x0, self.y0))
            window.blit(pygame.transform.scale(self.met, (5 * cellsize / 20, 5 * cellsize / 20)), (self.x0, self.y0))
            # pygame.draw.rect(window, 'gray', (self.x0, self.y0, 5, 5))

    def take(self):
        x = player.x + 8
        y = player.y + 8
        if math.sqrt((x - self.x0) ** 2 + (y - self.y0) ** 2) < cellsize * 3:
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
        self.Cursor = cross
        pygame.mouse.set_visible(False)

    def render(self):
        monitor.blit(self.Cursor, (pygame.mouse.get_pos()))


def createway():
    for y in range(len(Map)):
        for x in range(len(Map[0])):
            if Map[y][x] != 0 and Map[y][x] != 9:
                pygame.draw.rect(window, (186, 145, 65), [x * cellsize, y * cellsize,
                                                          cellsize, cellsize])


def createfloor():
    for y in range(len(Map)):
        for x in range(len(Map[0])):
            if Map[y][x] == 0:
                window.blit(ssand, (x * cellsize, y * cellsize))


def createwall():
    cropped = pygame.Surface((cellsize, cellsize), pygame.SRCALPHA)
    for y in range(len(Map)):
        for x in range(len(Map[0])):
            if (y == 0 and x == 0) or (y == 0 and x == 33) or (y == 22 and x == 0) or (y == 22 and x == 33):
                cropped.blit(ss, (0, 0), (cellsize, cellsize, cellsize, cellsize))
                window.blit(cropped, (x * cellsize, y * cellsize))
            elif y == 0:
                cropped.blit(ss, (0, 0), (cellsize, 2 * cellsize, cellsize, cellsize))
                window.blit(cropped, (x * cellsize, y * cellsize))
            elif y == 22:
                cropped.blit(ss, (0, 0), (cellsize, 0, cellsize, cellsize))
                window.blit(cropped, (x * cellsize, y * cellsize))
            elif x == 33:
                cropped.blit(ss, (0, 0), (0, cellsize, cellsize, cellsize))
                window.blit(cropped, (x * cellsize, y * cellsize))
            elif x == 0:
                cropped.blit(ss, (0, 0), (2 * cellsize, cellsize, cellsize, cellsize))
                window.blit(cropped, (x * cellsize, y * cellsize))
            if x == 0 and y == 10:
                cropped.blit(ss, (0, 0), (2 * cellsize, 2 * cellsize, cellsize, cellsize))
                window.blit(cropped, (x * cellsize, y * cellsize))
            if x == 0 and y == 12:
                cropped.blit(ss, (0, 0), (2 * cellsize, 0, cellsize, cellsize))
                window.blit(cropped, (x * cellsize, y * cellsize))
            if x == 33 and y == 10:
                cropped.blit(ss, (0, 0), (0, 2 * cellsize, cellsize, cellsize))
                window.blit(cropped, (x * cellsize, y * cellsize))
            if x == 33 and y == 12:
                cropped.blit(ss, (0, 0), (0, 0, cellsize, cellsize))
                window.blit(cropped, (x * cellsize, y * cellsize))


def hubwall():
    for i in tile_rects1:
        pygame.draw.rect(hubscreen, 'red', i, 1)


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
    pygame.draw.rect(monitor, (48, 48, 48), [68 * cellsize, 0, 12.05 * cellsize, height1])
    pygame.draw.rect(monitor, 'white', [70.1 * cellsize, 4.5 * cellsize, 8 * cellsize, 3 * cellsize], 4)
    can = myfont.render('Cancel', False, 'white')
    monitor.blit(can, (cellsize * 72, 4.9 * cellsize))
    outline_mask1(greentow1, (71 * cellsize, 8.5 * cellsize))
    monitor.blit(greentow1, (71 * cellsize, 8.5 * cellsize))
    cost = myfont.render('10', False, 'white')
    monitor.blit(cost, (cellsize * 73.35, cellsize * 14.25))
    outline_mask1(yellowtow1, (cellsize * 71, 17.5 * cellsize))
    monitor.blit(yellowtow1, (71 * cellsize, 17.5 * cellsize))
    cost = myfont.render('30', False, 'white')
    monitor.blit(cost, (73.35 * cellsize, 23.25 * cellsize))
    outline_mask1(redtow1, (71 * cellsize, 26 * cellsize))
    monitor.blit(redtow1, (71 * cellsize, 26 * cellsize))
    cost = myfont.render('55', False, 'white')
    monitor.blit(cost, (73.35 * cellsize, 31.75 * cellsize))
    outline_mask1(bluetow1, (71 * cellsize, 34.5 * cellsize))
    monitor.blit(bluetow1, (71 * cellsize, 34.5 * cellsize))
    money = myfont.render(str(plr.money), False, 'white')
    cost = myfont.render('85', False, 'white')
    monitor.blit(cost, (73.35 * cellsize, 40.25 * cellsize))
    monitor.blit(money, (cellsize * countx * sclsz + cellsize * 5, 30))
    if towernum == 0:
        pass
    if towernum == 1:
        pygame.draw.rect(monitor, 'white', [70.1 * cellsize, 8 * cellsize, 8 * cellsize, 8.5 * cellsize], 4)
    if towernum == 2:
        pygame.draw.rect(monitor, 'white', [70.1 * cellsize, 17 * cellsize, 8 * cellsize, 8.5 * cellsize], 4)
    if towernum == 3:
        pygame.draw.rect(monitor, 'white', [70.1 * cellsize, 25.5 * cellsize, 8 * cellsize, 8.5 * cellsize], 4)
    if towernum == 4:
        pygame.draw.rect(monitor, 'white', [70.1 * cellsize, 34 * cellsize, 8 * cellsize, 8.5 * cellsize], 4)


def showfps():
    if show:
        cost = myfont.render(f'{clock.get_fps()}', False, 'white')
        monitor.blit(cost, (0, 0))


# def fullscrn():
#     global flscr, monitor
#     if flscr:
#         monitor = pygame.display.set_mode((width1, height1))
#     else:
#         monitor = pygame.display.set_mode((width1, height1), pygame.FULLSCREEN)
#     flscr = not flscr
#     stats = open('fullscreen.txt', 'w')
#     stats.write(str(int(flscr)))
#     stats.close()


def uiswtch():
    x, y = getmpos()
    for i in uirect:
        if i.collidepoint((x, y)):
            return uirect.index(i) + 1


def dieui():
    global running, alive, bullets, towers, meat, drops, heals, wawe, playerv, player_movement, tile_rects
    mx, my = pygame.mouse.get_pos()
    retry = pygame.Rect(width - 20 * cellsize, height + 2.5 * cellsize, 15 * cellsize, 3.5 * cellsize)
    exit = pygame.Rect(width, height + 2.5 * cellsize, 15 * cellsize, 3.5 * cellsize)
    pygame.draw.rect(monitor, 'gray', retry)
    pygame.draw.rect(monitor, 'gray', exit)
    if retry.collidepoint(mx, my):
        pygame.draw.rect(monitor, (112, 112, 112), retry)
        if dieuiclicked:
            bullets = []
            towers = []
            meat = []
            drops = []
            heals = []
            tile_rects = tile_rects[:lenwalls]
            wawe = 0
            alive = True
            player.set_pos(cellsize * countx - player.width, cellsize * 11.1)
            player.hp = 10
            plr.money = 35
            playerv = 2
            player_movement = [0, 0]
            running = False
    if exit.collidepoint(mx, my):
        pygame.draw.rect(monitor, (112, 112, 112), exit)
        if dieuiclicked:
            bullets = []
            towers = []
            meat = []
            drops = []
            heals = []
            tile_rects = tile_rects[:lenwalls]
            wawe = 0
            alive = True
            player.set_pos(cellsize * countx - player.width, cellsize * 11.1)
            player.hp = 10
            plr.money = 35
            playerv = 2
            player_movement = [0, 0]
            running = False
    f1 = myfont.render('Retry', False, 'white')
    monitor.blit(f1, (width - 15 * cellsize, height + 3 * cellsize))
    f2 = myfont.render('Exit', False, 'white')
    monitor.blit(f2, (width + 6 * cellsize, height + 3 * cellsize))


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
    pygame.draw.polygon(monitor, (255, 255, 255), mask_outline, 7)


def outline_mask2(img, loc):
    img = pygame.transform.scale(img, (5 * cellsize / 20, 5 * cellsize / 20))
    mask = pygame.mask.from_surface(img)
    mask_outline = mask.outline()
    n = 0
    for point in mask_outline:
        mask_outline[n] = (point[0] + loc[0], point[1] + loc[1])
        n += 1
    pygame.draw.polygon(window, (255, 255, 255), mask_outline, 3)


def maketower(n):
    global towernum
    x, y = getmpos()
    if maycreatetower(x, y) and x <= width:
        if n:
            if n == 1 and plr.money >= 10:
                towers.append(CommonTower(x + cellsize / 2, y + cellsize / 2, 10, 'green', 20, 1.3, 30, 1.4))
                plr.money -= 10
                tile_rects.append(pygame.Rect(x, y, cellsize, cellsize))
                tile_rects_coord.append([x // cellsize, y // cellsize])
            if n == 2 and plr.money >= 30:
                towers.append(QuadTower(x + cellsize / 2, y + cellsize / 2, 10, 'yellow', 30, 1.5, 40, 1.2))
                plr.money -= 30
                tile_rects.append(pygame.Rect(x, y, cellsize, cellsize))
                tile_rects_coord.append([x // cellsize, y // cellsize])
            if n == 4 and plr.money >= 85:
                towers.append(HomingTower(x + cellsize / 2, y + cellsize / 2, 10, 'blue', 45, 1.3, 50, 1))
                plr.money -= 85
                tile_rects.append(pygame.Rect(x, y, cellsize, cellsize))
                tile_rects_coord.append([x // cellsize, y // cellsize])
            if n == 3 and plr.money >= 55:
                towers.append(TheEighthTower(x + cellsize / 2, y + cellsize / 2, 10, 'red', 35, 1.7, 40, 1))
                plr.money -= 55
                tile_rects.append(pygame.Rect(x, y, cellsize, cellsize))
                tile_rects_coord.append([x // cellsize, y // cellsize])


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


def overwidth():
    global alive
    if meat:
        if meat[0].x > cellsize * countx:
            alive = False


def outrng():
    global inhub, running, alive, bullets, towers, meat, drops, heals, wawe, playerv, player_movement
    if player.x > cellsize * countx and meatend:
        player.set_pos(0, 6.1 * cellsize)
        inhub = True
    elif player.x + player.width < 0 and inhub:
        bullets = []
        towers = []
        meat = []
        drops = []
        heals = []
        wawe = 0
        alive = True
        player.set_pos(cellsize * countx - player.width, cellsize * 11.1)
        inhub = False
    elif player.y < 0 and inhub:
        inhub = False


def createrad():
    if towernum:
        radius = cellsize * 3
        circle = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(circle, (0, 200, 0, 128), (radius, radius), radius, 1)
        window.blit(circle, (player.x + 8 - radius, player.y + 8 - radius))
        mx, my = getmpos()
        alphatower = pygame.Surface((cellsize, cellsize), pygame.SRCALPHA)
        if towernum == 1:
            tow = greentow
        if towernum == 2:
            tow = yellowtow
        if towernum == 3:
            tow = redtow
        if towernum == 4:
            tow = bluetow
        window.blit(tow, (mx // cellsize * cellsize, my // cellsize * cellsize))
        mask = pygame.mask.from_surface(tow)
        mask_outline = mask.to_surface().convert_alpha()
        if maycreatetower(mx, my):
            alphatower.fill((0, 255, 0, 128))
            mask_outline.set_colorkey('white')
            alphatower.blit(mask_outline, (0, 0), (0, 0, cellsize, cellsize))
            alphatower.set_colorkey('black')
        else:
            alphatower.fill((255, 0, 0, 128))
            mask_outline.set_colorkey('white')
            alphatower.blit(mask_outline, (0, 0), (0, 0, cellsize, cellsize))
            alphatower.set_colorkey('black')
        window.blit(alphatower, (mx // cellsize * cellsize, my // cellsize * cellsize))


def run():
    overwidth()
    if alive:
        global spawntime, inviztime, wawe, playerv, meatend
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
                    explosions.append(e.Explosion(meats.x, meats.y))
                    meat.remove(meats)
            if inviztime > 500 and player.rect().colliderect(meats.rect):
                player.hp -= 1
                inviztime = 0
            else:
                inviztime += 1
        if len(meat) == 0 and wawe < 3:
            if spawntime > 300:
                for i in range(10 + wawe * 2):
                    if wawe == 0:
                        meatcreate(meatstrt[0] - 2 * i * cellsize, meatstrt[1], 50, 0.5, wawe + 10, 'red', False)
                    else:
                        meatcreate(meatstrt[0] - 2 * i * cellsize, meatstrt[1], wawe * 50, 0.6, wawe + 10, 'red', False)
                wawe += 1
                spawntime = 0
            else:
                spawntime += 1
        if len(meat) == 0 and (wawe >= 3 or wawe == 0):
            meatend = True
        else:
            meatend = False
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


plr = Player(35)
wawe = 0
crosshair = Crosshair()
player = e.Entity(*[cellsize * 1.5, cellsize * 1.5], 0.8 * cellsize, 0.8 * cellsize, 10, 'player')
fullhp = player.hp
playerhp = Healthpoints(fullhp, player.hp)
running = True
moving_right = False
moving_left = False
moving_up = False
moving_down = False
last_time = time.time()
greentower = pygame.image.load('data_img/greentower.png').convert_alpha()
greentower = pygame.transform.scale(greentower, (cellsize, cellsize))
greentow = pygame.Surface((cellsize, cellsize), pygame.SRCALPHA)
greentow.blit(greentower, (0, 0), (0, 0, cellsize, cellsize))
yellowtower = pygame.image.load('data_img/yellowtower.png').convert_alpha()
yellowtower = pygame.transform.scale(yellowtower, (cellsize, cellsize))
yellowtow = pygame.Surface((cellsize, cellsize), pygame.SRCALPHA)
yellowtow.blit(yellowtower, (0, 0), (0, 0, cellsize, cellsize))
redtower = pygame.image.load('data_img/redtower.png').convert_alpha()
redtower = pygame.transform.scale(redtower, (cellsize, cellsize))
redtow = pygame.Surface((cellsize, cellsize), pygame.SRCALPHA)
redtow.blit(redtower, (0, 0), (0, 0, cellsize, cellsize))
bluetower = pygame.image.load('data_img/bluetower.png').convert_alpha()
bluetower = pygame.transform.scale(bluetower, (cellsize, cellsize))
bluetow = pygame.Surface((cellsize, cellsize), pygame.SRCALPHA)
bluetow.blit(bluetower, (0, 0), (0, 0, cellsize, cellsize))
metim = pygame.image.load('data_img/metal.png').convert_alpha()
metim = pygame.transform.scale(metim, (cellsize / 4, cellsize / 4))
metal = pygame.Surface((cellsize / 4, cellsize / 4), pygame.SRCALPHA)
metal.blit(metim, (0, 0), (0, 0, cellsize / 4, cellsize / 4))
metim1 = pygame.image.load('data_img/metal1.png').convert_alpha()
metim1 = pygame.transform.scale(metim1, (cellsize / 4, cellsize / 4))
metal1 = pygame.Surface((cellsize / 4, cellsize / 4), pygame.SRCALPHA)
metal1.blit(metim1, (0, 0), (0, 0, cellsize / 4, cellsize / 4))
metim2 = pygame.image.load('data_img/metal2.png').convert_alpha()
metim2 = pygame.transform.scale(metim2, (cellsize / 4, cellsize / 4))
metal2 = pygame.Surface((cellsize / 4, cellsize / 4), pygame.SRCALPHA)
metal2.blit(metim2, (0, 0), (0, 0, cellsize / 4, cellsize / 4))
metim3 = pygame.image.load('data_img/metal3.png').convert_alpha()
metim3 = pygame.transform.scale(metim3, (cellsize / 4, cellsize / 4))
metal3 = pygame.Surface((cellsize / 4, cellsize / 4), pygame.SRCALPHA)
metal3.blit(metim3, (0, 0), (0, 0, cellsize / 4, cellsize / 4))
allmetal.append(metal)
allmetal.append(metal1)
allmetal.append(metal2)
allmetal.append(metal3)
helim = pygame.image.load('data_img/heal.png').convert_alpha()
helim = pygame.transform.scale(helim, (cellsize / 4, cellsize / 4))
healim = pygame.Surface((cellsize / 4, cellsize / 4), pygame.SRCALPHA)
healim.blit(helim, (0, 0), (0, 0, cellsize / 4, cellsize / 4))
greentow1 = pygame.transform.scale(greentow, (6 * cellsize, 6 * cellsize))
yellowtow1 = pygame.transform.scale(yellowtow, (cellsize * 6, cellsize * 6))
redtow1 = pygame.transform.scale(redtow, (cellsize * 6, cellsize * 6))
bluetow1 = pygame.transform.scale(bluetow, (cellsize * 6, cellsize * 6))


# player.hp = 0


def towerdefence():
    # global last_time
    # global moving_up
    # global moving_down
    # global moving_right
    # global moving_left
    # global running
    # global playerhp
    # global fullhp
    # global player
    # global  crosshair
    # global wawe
    # global plr
    # global greentower
    # global greentow
    # global yellowtower
    # global yellowtow
    # global greentower
    # global greentow
    # global bluetower
    # global bluetow
    # global metal
    # global metim
    # global metim1
    # global metal1
    # global metim2
    # global metal2
    # global metim3
    # global metal3
    # global allmetal
    # global helim
    # global greentower1
    # global redtower1
    # global bluetower1
    # global yellowtower1
    global countx, county, sclsz, sclsz1, width1, height1, width, height, cellsize, cellsize1, countx1, county1, fps
    global flscr, show, inviztime, inhub, meatend, bullets, towers, meat, drops, heals, walls, way, allmetal, tile_rects
    global tile_rects1, tile_rects_coord, explosions, towernum, spawntime, playerv, speedcoef, uirect, Map, down
    global right, up, left, napr, mousx, mousy, dieuiclicked, alive, myfont, myfont1, window, hubscreen, monitor
    global deadscreen, crosshairsurf, ss, sand, ssand, ssway, cross, clock, lenwalls, meatstrt, plr, wawe, crosshair
    global player, fullhp, playerhp, running, moving_right, moving_left, moving_up, moving_down, last_time, greentower
    global greentow, yellowtower, yellowtow, redtower, redtow, bluetower, bluetow, metim, metal, metim1, metal1, metim2
    global metal2, metim3, metal3, allmetal, helim, healim, greentow1, yellowtow1, redtow1, bluetow1
    running = True
    alive = True
    while running:
        pygame.mouse.set_visible(False)
        # if inhub:
        #     hubscreen.fill((50, 50, 50))
        #     player_movement = [0, 0]
        #     dt = time.time() - last_time
        #     dt *= 60
        #     last_time = time.time()
        #     if moving_right:
        #         player_movement[0] += playerv * dt * speedcoef * 60 / clock.get_fps()
        #     if moving_left:
        #         player_movement[0] -= playerv * dt * speedcoef * 60 / clock.get_fps()
        #     if moving_up:
        #         player_movement[1] -= playerv * dt * speedcoef * 60 / clock.get_fps()
        #     if moving_down:
        #         player_movement[1] += playerv * dt * speedcoef * 60 / clock.get_fps()
        #     player.move(player_movement, tile_rects1, [])
        #     player.update()
        #     for event in pygame.event.get():
        #         if event.type == pygame.QUIT:
        #             running = False
        #         if event.type == pygame.KEYDOWN:
        #             if event.key == pygame.K_d:
        #                 moving_right = True
        #             if event.key == pygame.K_a:
        #                 moving_left = True
        #             if event.key == pygame.K_w:
        #                 moving_up = True
        #             if event.key == pygame.K_s:
        #                 moving_down = True
        #             if event.key == pygame.K_1:
        #                 towernum = 1
        #             if event.key == pygame.K_2:
        #                 towernum = 2
        #             if event.key == pygame.K_3:
        #                 towernum = 3
        #             if event.key == pygame.K_4:
        #                 towernum = 4
        #             if event.key == pygame.K_F5:
        #                 show = not show
        #             if event.key == pygame.K_F11:
        #                 fullscrn()
        #             if event.key == pygame.K_ESCAPE:
        #                 if towernum != 0:
        #                     towernum = 0
        #                 else:
        #                     running = False
        #         if event.type == pygame.KEYUP:
        #             if event.key == pygame.K_d:
        #                 moving_right = False
        #             if event.key == pygame.K_a:
        #                 moving_left = False
        #             if event.key == pygame.K_w:
        #                 moving_up = False
        #             if event.key == pygame.K_s:
        #                 moving_down = False
        #     outrng()
        #     player.draw(hubscreen, [0, 0])
        #     hubwall()
        #     monitor.blit(pygame.transform.scale(hubscreen, (width1, height1)), (0, 0))
        #     playerhp.draw(fullhp, player.hp)
        #     crosshair.render()
        if alive:
            for meats in meat:
                if math.sqrt((meats.x - (player.x + 8)) ** 2 + (meats.y - (player.y + 8)) ** 2) < cellsize * 2 and \
                        meats.slowed:
                    playerv = 1
                    break
                else:
                    playerv = 2
            player_movement = [0, 0]
            dt = time.time() - last_time
            dt *= 60
            last_time = time.time()
            if moving_right:
                player_movement[0] += playerv * dt * speedcoef
            if moving_left:
                player_movement[0] -= playerv * dt * speedcoef
            if moving_up:
                player_movement[1] -= playerv * dt * speedcoef
            if moving_down:
                player_movement[1] += playerv * dt * speedcoef
            player.move(player_movement, tile_rects, [])
            player.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        maketower(towernum)
                        if getmpos()[0] >= 68 * cellsize:
                            towernum = uiswtch()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F5:
                        show = not show
                    if event.key == pygame.K_F11:
                        fullscrn(screen)
                    if event.key == pygame.K_F1:
                        if fps == 120:
                            fps = 60
                        else:
                            fps = 120
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
            createfloor()
            createwall()
            createway()
            run()
            outrng()
            player.draw(window, [0, 0])
            createrad()
            for i, explosion in sorted(enumerate(explosions), reverse=True):
                explosion.update()
                explosion.draw(window)
                if len(explosion.particles) == 0:
                    del explosion
                    explosions.pop(i)
            monitor.blit(pygame.transform.scale(window, (width1, height1)), (0, 0))
            playerhp.draw(fullhp, player.hp)
            ui()
            crosshair.render()
            checklife()
        else:
            dieuiclicked = False
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F5:
                        show = not show
                    if event.key == pygame.K_F11:
                        fullscrn(screen)
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        dieuiclicked = True
            createfloor()
            createwall()
            createway()
            run()
            player.draw(window, [0, 0])
            monitor.blit(pygame.transform.scale(window, (width1, height1)), (0, 0))
            playerhp.draw(fullhp, player.hp)
            ui()
            deadscreen.fill((0, 0, 0, 128))
            monitor.blit(pygame.transform.scale(deadscreen, (width1, height1)), (0, 0))
            hp = myfont1.render('Game over!', False, 'white')
            monitor.blit(hp, (width - 13.4 * cellsize, height - 10 * cellsize))
            dieui()
            crosshair.render()
        showfps()
        pygame.display.update()
        clock.tick(fps)


def fullscrn(display):
    global flscr
    if flscr:
        display = pygame.display.set_mode(WINDOW_SIZE)
    else:
        display = pygame.display.set_mode(WINDOW_SIZE, pygame.FULLSCREEN)
    flscr = not flscr


def main_menu():
    running = True
    pygame.mouse.set_visible(True)
    SCALE_MULTIPLIER = 5
    click = False
    font = pygame.font.Font('MaredivRegular.ttf', 15)
    display = pygame.Surface((WINDOW_SIZE[0] / SCALE_MULTIPLIER, WINDOW_SIZE[1] / SCALE_MULTIPLIER), pygame.SRCALPHA)
    stars = pygame.Surface((WINDOW_SIZE[0] / SCALE_MULTIPLIER + 400, WINDOW_SIZE[1] / SCALE_MULTIPLIER + 400))
    stars.fill((15, 11, 66))
    for i in range(500):
        stars.fill(pygame.Color('white'),
                    (random.random() * width,
                     random.random() * height, 1, 1))
    while running:
        mx, my = pygame.mouse.get_pos()
        playbtn = pygame.Rect(132, 110, 120, 25)
        optionsbtn = pygame.Rect(132, 145, 120, 25)
        exitbtn = pygame.Rect(132, 180, 120, 25)
        mx = mx / SCALE_MULTIPLIER
        my = my / SCALE_MULTIPLIER
        if playbtn.collidepoint((mx, my)):
            cveta = (78, 29, 92)
            cveta1 = (214, 136, 17)
            if click:
                trade_area()
        else:
            cveta = (109, 29, 112)
            cveta1 = (255, 235, 214)
        if optionsbtn.collidepoint((mx, my)):
            cveta2 = (78, 29, 92)
            cveta3 = (214, 136, 17)
            if click:
                options()
        else:
            cveta2 = (109, 29, 112)
            cveta3 = (255, 235, 214)
        if exitbtn.collidepoint((mx, my)):
            cveta4 = (78, 29, 92)
            cveta5 = (214, 136, 17)
            if click:
                running = False
        else:
            cveta4 = (109, 29, 112)
            cveta5 = (255, 235, 214)
        pygame.draw.rect(display, cveta, playbtn)
        pygame.draw.rect(display, cveta2, optionsbtn)
        pygame.draw.rect(display, cveta4, exitbtn)
        text = font.render("play", True, cveta1)
        display.blit(text, (WINDOW_SIZE[0] / SCALE_MULTIPLIER / 2 - 15, 110))

        text = font.render("options", True, cveta3)
        display.blit(text, (WINDOW_SIZE[0] / SCALE_MULTIPLIER / 2 - 25, 145))

        text = font.render("exit", True, cveta5)
        display.blit(text, (WINDOW_SIZE[0] / SCALE_MULTIPLIER / 2 - 15, 180))
        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

            if event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    click = False
        mpx, mpy, = pygame.mouse.get_pos()
        screen.blit(pygame.transform.scale(stars, (WINDOW_SIZE[0] + 400, WINDOW_SIZE[1] + 400)), ((mpx - WINDOW_SIZE[0] / 2) / 30, (mpy - WINDOW_SIZE[1] / 2) / 30))
        screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
        pygame.display.update()
        clock.tick(60)


def trade_area():
    SCALE_MULTIPLIER = 4
    display = pygame.Surface((WINDOW_SIZE[0] / SCALE_MULTIPLIER, WINDOW_SIZE[1] / SCALE_MULTIPLIER))

    clicked = False
    running = True
    use = False

    moving_right = False
    moving_left = False
    moving_up = False
    moving_down = False

    true_scroll = [0, 0]
    scroll = [0, 0]

    last_time = time.time()

    pygame.mouse.set_visible(False)
    world = e.TradeWorld(24, 14, 20)
    world.generate_map()
    player = e.Player(200, 100, 16, 16, 10, 'player')
    cursor = e.Cursor(0, 0, 'data_img/curs3.png')
    portal1 = e.Portal(240, 30, 10, 'portal')
    portal2 = e.Portal(30, 140, 10, 'portal')
    world.add_usable_entity(portal1)
    world.add_usable_entity(portal2)
    particles = []

    while running:
        dt = time.time() - last_time
        dt *= 60
        last_time = time.time()
        display.fill((240, 181, 65))
        mouse_pos = pygame.mouse.get_pos()

        cursor.set_pos(mouse_pos[0] / SCALE_MULTIPLIER, mouse_pos[1] / SCALE_MULTIPLIER)

        true_scroll[0] += (player.x - true_scroll[0] - display.get_width() / 2 + 8) / 10
        true_scroll[1] += (player.y - true_scroll[1] - display.get_height() / 2 + 8) / 10
        scroll = true_scroll.copy()
        scroll[0] = int(scroll[0])
        scroll[1] = int(scroll[1])

        mouse_angle = math.atan2(
            mouse_pos[1] / SCALE_MULTIPLIER - player.y - player.height / 2 + scroll[1],
            mouse_pos[0] / SCALE_MULTIPLIER - player.x - player.width / 2 + scroll[0])

        #  scroll = [0, 0]

        tile_rects = world.get_rects()
        player_movement = [0, 0]

        if moving_right:
            player_movement[0] += 2 * dt
        if moving_left:
            player_movement[0] -= 2 * dt
        if moving_up:
            player_movement[1] -= 2 * dt
        if moving_down:
            player_movement[1] += 2 * dt
        if clicked == True:
            player.shoot(mouse_angle)
        if use:
            use = False
            if portal1.used():
                game()
            if portal2.used():
                towerdefence()

        if player_movement[0] != 0 and player_movement[1] != 0:
            player_movement[0] *= math.sin(math.pi / 4)
            player_movement[1] *= math.sin(math.pi / 4)

        collision_types = player.move(player_movement, tile_rects, [])

        player.move_projectiles(tile_rects, world.get_enemies(), dt)
        player.update(mouse_angle)
        print(portal1.update(player))
        print(portal2.update(player))
        world.update(player, dt)
        world.draw(display, scroll)
        player.draw(display, scroll)
        player.draw_projectiles(display, scroll)
        #  print(player.hp)
        #  player.move(player_movement)
        #  pygame.draw.line(display, (0, 255, 0), (player.x + player.width / 2 - scroll[0], player.y + player.height / 2 - scroll[1]), ((pygame.mouse.get_pos()[0] // SCALE_MULTIPLIER), (pygame.mouse.get_pos()[1] // SCALE_MULTIPLIER)))

        #  particles.append(e.Particle(player.x - scroll[0] + player.width // 2, player.y - scroll[1] + player.height // 2, scroll))

        for i, particle in sorted(enumerate(particles), reverse=True):
            particle.update()
            particle.draw(display, scroll)
            if particle.time < 0:
                del particle
                particles.pop(i)

        cursor.draw(display)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_d:
                    moving_right = True
                if event.key == K_a:
                    moving_left = True
                if event.key == K_w:
                    moving_up = True
                if event.key == K_s:
                    moving_down = True
                if event.key == K_ESCAPE:
                    running = False
                if event.key == pygame.K_F11:
                    fullscrn(display)
                if event.key == pygame.K_f:
                    use = True
            if event.type == KEYUP:
                if event.key == K_d:
                    moving_right = False
                if event.key == K_a:
                    moving_left = False
                if event.key == K_w:
                    moving_up = False
                if event.key == K_s:
                    moving_down = False
                if event.key == pygame.K_f:
                    use = False
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    #  print(math.atan2(mouse_pos[1] / SCALE_MULTIPLIER - player.y, mouse_pos[0] / SCALE_MULTIPLIER - player.x))
                    clicked = True
            if event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    clicked = False

        screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
        pygame.display.update()
        clock.tick(60)
    pygame.mouse.set_visible(True)


def game():
    SCALE_MULTIPLIER = 4
    display = pygame.Surface((WINDOW_SIZE[0] / SCALE_MULTIPLIER, WINDOW_SIZE[1] / SCALE_MULTIPLIER))

    clicked = False
    running = True
    use = False

    moving_right = False
    moving_left = False
    moving_up = False
    moving_down = False

    true_scroll = [0, 0]
    scroll = [0, 0]

    last_time = time.time()

    pygame.mouse.set_visible(False)
    world = e.World(48, 48, 20)
    world.generate_map()
    player = e.Player(*world.get_start_pos(), 16, 16, 10, 'player')
    cursor = e.Cursor(0, 0, 'data_img/curs3.png')
    portal = e.Portal(*world.get_start_pos(), 10, 'portal')
    world.add_usable_entity(portal)
    particles = []

    while running:
        dt = time.time() - last_time
        dt *= 60
        last_time = time.time()
        display.fill((240, 181, 65))
        mouse_pos = pygame.mouse.get_pos()

        cursor.set_pos(mouse_pos[0] / SCALE_MULTIPLIER, mouse_pos[1] / SCALE_MULTIPLIER)

        true_scroll[0] += (player.x - true_scroll[0] - display.get_width() / 2 + 8) / 10
        true_scroll[1] += (player.y - true_scroll[1] - display.get_height() / 2 + 8) / 10
        scroll = true_scroll.copy()
        scroll[0] = int(scroll[0])
        scroll[1] = int(scroll[1])

        mouse_angle = math.atan2(
            mouse_pos[1] / SCALE_MULTIPLIER - player.y - player.height / 2 + scroll[1],
            mouse_pos[0] / SCALE_MULTIPLIER - player.x - player.width / 2 + scroll[0])

        #  scroll = [0, 0]

        tile_rects = world.get_rects()
        player_movement = [0, 0]

        if moving_right:
            player_movement[0] += 2 * dt
        if moving_left:
            player_movement[0] -= 2 * dt
        if moving_up:
            player_movement[1] -= 2 * dt
        if moving_down:
            player_movement[1] += 2 * dt
        if clicked == True:
            player.shoot(mouse_angle)
        if use:
            use = False
            if portal.used():
                running = False

        if player_movement[0] != 0 and player_movement[1] != 0:
            player_movement[0] *= math.sin(math.pi / 4)
            player_movement[1] *= math.sin(math.pi / 4)

        collision_types = player.move(player_movement, tile_rects, [])

        player.move_projectiles(tile_rects, world.get_enemies(), dt)
        player.update(mouse_angle)
        world.update(player, dt)
        world.draw(display, scroll)
        player.draw(display, scroll)
        player.draw_projectiles(display, scroll)
        #  print(player.hp)
        #  player.move(player_movement)
        #  pygame.draw.line(display, (0, 255, 0), (player.x + player.width / 2 - scroll[0], player.y + player.height / 2 - scroll[1]), ((pygame.mouse.get_pos()[0] // SCALE_MULTIPLIER), (pygame.mouse.get_pos()[1] // SCALE_MULTIPLIER)))

        #  particles.append(e.Particle(player.x - scroll[0] + player.width // 2, player.y - scroll[1] + player.height // 2, scroll))

        for i, particle in sorted(enumerate(particles), reverse=True):
            particle.update()
            particle.draw(display, scroll)
            if particle.time < 0:
                del particle
                particles.pop(i)

        cursor.draw(display)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_d:
                    moving_right = True
                if event.key == K_a:
                    moving_left = True
                if event.key == K_w:
                    moving_up = True
                if event.key == K_s:
                    moving_down = True
                if event.key == K_ESCAPE:
                    running = False
                if event.key == pygame.K_F11:
                    fullscrn(display)
                if event.key == pygame.K_f:
                    use = True
            if event.type == KEYUP:
                if event.key == K_d:
                    moving_right = False
                if event.key == K_a:
                    moving_left = False
                if event.key == K_w:
                    moving_up = False
                if event.key == K_s:
                    moving_down = False
                if event.key == pygame.K_f:
                    use = False
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    #  print(math.atan2(mouse_pos[1] / SCALE_MULTIPLIER - player.y, mouse_pos[0] / SCALE_MULTIPLIER - player.x))
                    clicked = True
            if event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    clicked = False

        screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
        pygame.display.update()
        clock.tick(60)
    pygame.mouse.set_visible(True)


def options():
    running = True
    n = 0
    m = 0
    font = pygame.font.Font('MaredivRegular.ttf', 15)
    font1 = pygame.font.Font('MaredivRegular.ttf', 25)
    usl1 = 0
    usl2 = 0
    uslza = 0
    SCALE_MULTIPLIER = 5
    cveta1 = (200, 200, 200)
    display = pygame.Surface((WINDOW_SIZE[0] / SCALE_MULTIPLIER, WINDOW_SIZE[1] / SCALE_MULTIPLIER))
    while running:
        display.fill((0, 0, 0))
        mx, my = pygame.mouse.get_pos()
        pygame.draw.rect(display, (255, 255, 255), (240, 20, 20, 20))
        pygame.draw.rect(display, (255, 255, 255), (210, 20, 20, 20))
        text3 = font1.render('+', True, (0, 0, 0))
        display.blit(text3, (243, 11))
        text3 = font1.render('-', True, (0, 0, 0))
        display.blit(text3, (213, 11))
        text1 = font.render(f"Crosshair-{n + 1}/3", True, (cveta1))
        display.blit(text1, (100, 0))
        text2 = font.render(f"sound-{m}/100", True, (cveta1))
        display.blit(text2, (100, 20))
        mx = mx / SCALE_MULTIPLIER
        my = my / SCALE_MULTIPLIER
        button_1 = pygame.Rect(100, 0, 100, 20)
        button_2 = pygame.Rect(240, 20, 20, 20)
        button_3 = pygame.Rect(210, 20, 20, 20)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            if event.type == pygame.MOUSEBUTTONUP:
                if button_1.collidepoint((mx, my)):
                    if n + 2 > 3:
                        n = 0
                    else:
                        n += 1
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_2.collidepoint((mx, my)):
                    usl1 = 1
            if event.type == pygame.MOUSEBUTTONUP:
                usl1 = 0
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_3.collidepoint((mx, my)):
                    usl2 = 1
            if event.type == pygame.MOUSEBUTTONUP:
                usl2 = 0
        uslza += 0.5
        if usl2 == 1 and uslza % 3 == 0:
            if m - 1 >= 0:
                m -= 1
        if usl1 == 1 and uslza % 3 == 0:
            if m + 1 <= 100:
                m += 1

        screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
        pygame.display.update()
        clock.tick(60)


main_menu()
