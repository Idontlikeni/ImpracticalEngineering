from cmath import pi
from dis import dis
from platform import machine
import pygame, sys, os, random, math, time
from pygame import mouse
import engine as e
from pygame.locals import *
from pygame.mixer import set_num_channels
import os

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
towerrects = []
explosions = []
towernum = 0
spawntime = 0
playerv = 2
stats = open('stats\\stats.txt', 'r')
x = stats.readlines()
plrkills = int(str(x[0]))
plrdamage = int(str(x[1]))
plrtowers = int(str(x[2]))
plrmetal = int(str(x[3]))
stats.close()
volume = 50
curstype = 'data_img/curs1.png'
stats = open(f'{os.getcwd()}\\options\\audio.txt', 'r')
x = stats.readlines()
if x:
    volume = int(str(x[0]))
stats.close()
pygame.mixer.music.set_volume(volume / 100)
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
        if Map[y][x] == 6:
            portalcoord = x * cellsize + (cellsize / 2), y * cellsize + (cellsize / 2)
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

spaceship = e.SpaceShip(300, 140, 21, 20, 1, "spaceship")


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
        self.rect = pygame.Rect(self.x - cellsize / 2, self.y - cellsize / 2, cellsize, cellsize)

    # def draw1(self):
    #     pygame.draw.rect(window, 'green', self.rect)

    def cost(self):
        return self.price


class CommonTower(Tower):
    def fire(self, tow):
        if self.firerate <= 0:
            addbullet(self.x, self.y, 6, self.color, self.damage, self.bullspeed, 0, tow)
            self.firerate = self.firespeed
        else:
            self.firerate -= 1 / fps

    def draw(self):
        outline_mask(greentow, (self.x - cellsize / 2, self.y - cellsize / 2))
        window.blit(greentow, (self.x - cellsize / 2, self.y - cellsize / 2))
        # pygame.draw.circle(window, self.color, [self.x, self.y], self.size)


class QuadTower(Tower):
    def fire(self, tow):
        if self.firerate <= 0:
            for direction in range(4):
                addbullet(self.x, self.y, 6, self.color, self.damage, self.bullspeed, direction, tow)
            self.firerate = self.firespeed
        else:
            self.firerate -= 1 / fps

    def draw(self):
        outline_mask(yellowtow, (self.x - cellsize / 2, self.y - cellsize / 2))
        window.blit(yellowtow, (self.x - cellsize / 2, self.y - cellsize / 2))


class TheEighthTower(Tower):
    def fire(self, tow):
        if self.firerate <= 0:
            for direction in range(8):
                addbullet(self.x, self.y, 6, self.color, self.damage, self.bullspeed, direction, tow)
            self.firerate = self.firespeed
        else:
            self.firerate -= 1 / fps

    def draw(self):
        outline_mask(redtow, (self.x - cellsize / 2, self.y - cellsize / 2))
        window.blit(redtow, (self.x - cellsize / 2, self.y - cellsize / 2))


class HomingTower(Tower):
    def fire(self, tow):
        if meat:
            if math.sqrt((meat[0].x - self.x) ** 2 + (meat[0].y - self.y) ** 2) < cellsize * 8:
                if self.firerate <= 0:
                    addbullet(self.x, self.y, 6, self.color, self.damage, self.bullspeed, 8, tow)
                    self.firerate = self.firespeed
                else:
                    self.firerate -= 1 / fps

    def draw(self):
        outline_mask(bluetow, (self.x - cellsize / 2, self.y - cellsize / 2))
        window.blit(bluetow, (self.x - cellsize / 2, self.y - cellsize / 2))


class Bullet:
    def __init__(self, x, y, size, color, damage, speed, direction, tower):
        self.x = x
        self.y = y
        self.size = size / sclsz1 * cellsize / 20
        self.color = color
        self.damage = damage
        self.speed = speed * cellsize / 20 * 60 / clock.get_fps()
        self.rect = pygame.Rect(x - size, y - size, size * 2, size * 2)
        self.direction = direction
        self.tower = tower

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


class FreshMeat(e.Enemy):
    def __init__(self, x, y, hp, speed, size, color, slowed=False):
        super().__init__(x, y, 10, 16, 16, "meat")
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
        # self.animations_frames = {}
        # self.animation_database = {}
        # self.action = 'idle'
        # self.frame = 0
        # self.is_flipped = False
        # self.image = None
        # self.dead = False

    def update(self):
        super().update()

    def draw(self):

        #  pygame.draw.circle(window, self.color, [self.x, self.y], self.size)
        window.blit(pygame.transform.flip(self.image, self.is_flipped, False),
                    (self.x - self.size + 2, self.y - self.size + 2))
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


def addbullet(x, y, size, color, damage, speed, direction, tower):
    bullets.append(Bullet(x, y, size, color, damage, speed, direction, tower))


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
    rct = pygame.Surface((11 * cellsize, 2.2 * cellsize), pygame.SRCALPHA)
    rct.fill((0, 0, 0, 128))
    monitor.blit(rct, (0.5 * width - 5 * cellsize, 0.045 * height))
    pygame.draw.rect(monitor, 'white', [0.5 * width - 5 * cellsize, 0.045 * height, 11 * cellsize, 2.2 * cellsize], 4)
    if spawntime == 0:
        if wawe == 0:
            hp = myfont.render(str(f'Wave: 3/3'), False, 'white')
        else:
            hp = myfont.render(str(f'Wave: {wawe}/3'), False, 'white')
        monitor.blit(hp, (16.8 * cellsize, 0.9 * cellsize))
    else:
        hp = myfont.render(str(f'Next wave: {(300 - spawntime) // 50}'), False, 'white')
        monitor.blit(hp, (15.9 * cellsize, 0.9 * cellsize))


def showfps():
    if show:
        cost = myfont.render(f'{clock.get_fps()}', False, 'white')
        monitor.blit(cost, (0, 0))


def uiswtch():
    x, y = getmpos()
    for i in uirect:
        if i.collidepoint((x, y)):
            return uirect.index(i) + 1


def dieui():
    global running, alive, bullets, towers, meat, drops, heals, wawe, playerv, player_movement, tile_rects, tile_rects_coord, wawe1, meatend, moving_right, use, metalmoneypast
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
            alive = True
            bullets = []
            towers = []
            meat = []
            drops = []
            heals = []
            tile_rects = tile_rects[:lenwalls]
            tile_rects_coord = tile_rects_coord[:lenwalls]
            wawe = 0
            wawe1 = 1
            player.set_pos(cellsize * countx - player.width, cellsize * 11.1)
            player.hp = 10
            spaceship.metal = 0
            player.ammo = 128
            plr.money = 0
            playerv = 2
            t = 0
            meatend = False
            moving_right = False
            portal = e.Portal(*portalcoord, 10, 'portal')
            portal.is_active = False
            use = False
            player.show_weapon = False
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
            spaceship.metal = 0
            player.ammo = 128
            plr.money = 0
            playerv = 2
            player_movement = [0, 0]
            running = False
            return True
    f1 = myfont.render('Retry', False, 'white')
    monitor.blit(f1, (width - 15 * cellsize, height + 3 * cellsize))
    f2 = myfont.render('Exit', False, 'white')
    monitor.blit(f2, (width + 6 * cellsize, height + 3 * cellsize))


def deathui(surface, player):
    player.hp = 10
    player.metal = 0
    player.ammo = 128
    spaceship.metal = 0
    running = True
    pygame.mouse.set_visible(True)
    SCALE_MULTIPLIER = 5
    click = False
    font = pygame.font.Font('MaredivRegular.ttf', 20)
    display = pygame.Surface((WINDOW_SIZE[0] / SCALE_MULTIPLIER, WINDOW_SIZE[1] / SCALE_MULTIPLIER), pygame.SRCALPHA)
    background = pygame.Surface(WINDOW_SIZE, pygame.SRCALPHA)
    background.blit(pygame.transform.scale(surface, WINDOW_SIZE), (0, 0))
    while running:
        display.fill((0, 0, 0, 200))
        screen.blit(background, (0, 0))
        mx, my = pygame.mouse.get_pos()
        retry = pygame.Rect(WINDOW_SIZE[0] / SCALE_MULTIPLIER / 2 - 100, 106, 50, 23)
        exit = pygame.Rect(WINDOW_SIZE[0] / SCALE_MULTIPLIER / 2 + 50, 106, 38, 23)

        # retry = pygame.Rect(width - 20 * cellsize, height + 2.5 * cellsize, 15 * cellsize, 3.5 * cellsize)
        # exit = pygame.Rect(width, height + 2.5 * cellsize, 15 * cellsize, 3.5 * cellsize)

        # if exitnal:
        #     exitbtn = pygame.Rect(WINDOW_SIZE[0] / SCALE_MULTIPLIER / 2 - 20, 176, 36, 19)
        mx = mx / SCALE_MULTIPLIER
        my = my / SCALE_MULTIPLIER
        if retry.collidepoint((mx, my)):
            cveta1 = (214, 136, 17)
            if click:
                running = False
        else:
            cveta1 = (255, 235, 214)
        
        if exit.collidepoint((mx, my)):
            cveta3 = (214, 136, 17)
            if click:
                running = False
                return True
        else:
            cveta3 = (255, 235, 214)


        # if exitnal:
        #     if exitbtn.collidepoint((mx, my)):
        #         cveta5 = (214, 136, 17)
        #         if click:
        #             return True
        #     else:
        #         cveta5 = (255, 235, 214)

        # pygame.draw.rect(display, (255, 255, 255), retry, 1)
        # pygame.draw.rect(display, (255, 255, 255), exit, 1)

        text = font.render("retry", True, cveta1)
        display.blit(text, (WINDOW_SIZE[0] / SCALE_MULTIPLIER / 2 - 100, 100))

        text = font.render("exit", True, cveta3)
        display.blit(text, (WINDOW_SIZE[0] / SCALE_MULTIPLIER / 2 + 50, 100))

        # if exitnal:
        #     text = font.render("exit", True, cveta5)
        #     display.blit(text, (WINDOW_SIZE[0] / SCALE_MULTIPLIER / 2 - 20, 170))
        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

            if event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    click = False

            if event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    click = False
        screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
        pygame.display.update()
        clock.tick(60)
    pygame.mouse.set_visible(False)
    return False


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
                towerrects.append(pygame.Rect(x, y, cellsize, cellsize))
                tile_rects_coord.append([x // cellsize, y // cellsize])
            if n == 2 and plr.money >= 30:
                towers.append(QuadTower(x + cellsize / 2, y + cellsize / 2, 10, 'yellow', 30, 1.5, 40, 1.2))
                plr.money -= 30
                towerrects.append(pygame.Rect(x, y, cellsize, cellsize))
                tile_rects.append(pygame.Rect(x, y, cellsize, cellsize))
                tile_rects_coord.append([x // cellsize, y // cellsize])
            if n == 4 and plr.money >= 85:
                towers.append(HomingTower(x + cellsize / 2, y + cellsize / 2, 10, 'blue', 45, 1.3, 50, 1))
                plr.money -= 85
                towerrects.append(pygame.Rect(x, y, cellsize, cellsize))
                tile_rects.append(pygame.Rect(x, y, cellsize, cellsize))
                tile_rects_coord.append([x // cellsize, y // cellsize])
            if n == 3 and plr.money >= 55:
                towers.append(TheEighthTower(x + cellsize / 2, y + cellsize / 2, 10, 'red', 35, 1.7, 40, 1))
                plr.money -= 55
                towerrects.append(pygame.Rect(x, y, cellsize, cellsize))
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
    global spawntime, inviztime, wawe, playerv, meatend, wawe1, plrkills, plrdamage, plrtowers, plrmetal
    overwidth()
    if alive:
        if not meatend:
            for drop in drops:
                drop.fly()
                drop.take()
                drop.draw()
                if drop.taked():
                    drops.remove(drop)
                    plr.money += 1
                    plrmetal += 1
            for bullet in bullets:
                bullet.move()
                bullet.draw()
                # pygame.draw.rect(window, 'red', bullet.rect, 1)
                if player.rect().colliderect(bullet.rect):
                    player.hp -= 1
                    plrdamage += 1
                    bullets.remove(bullet)
                    break
                for wall in walls:
                    if wall.colliderect(bullet.rect):
                        bullets.remove(bullet)
                        break
                for tower in towers:
                    if tower.rect.colliderect(bullet.rect) and bullet.tower != tower:
                        tile_rects.remove(
                            pygame.Rect(tower.x - cellsize / 2, tower.y - cellsize / 2, cellsize, cellsize))
                        towerrects.remove(
                            pygame.Rect(tower.x - cellsize / 2, tower.y - cellsize / 2, cellsize, cellsize))
                        tile_rects_coord.remove(
                            [(tower.x - cellsize / 2) // cellsize, (tower.y - cellsize / 2) // cellsize])
                        towers.remove(tower)
                        bullets.remove(bullet)
                        plrtowers += 1
                        explosions.append(e.Explosion(tower.x, tower.y))
                        break
            for meats in meat:
                meats.update()
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
                        plrkills += 1
                if inviztime > 500 and player.rect().colliderect(meats.rect):
                    player.hp -= 1
                    plrdamage += 1
                    inviztime = 0
                else:
                    inviztime += 1
            if len(meat) == 0 and wawe < 3 and wawe1 == 1:
                if spawntime > 300:
                    for i in range(10 + wawe * 5):
                        if wawe == 0:
                            meatcreate(meatstrt[0] - 2 * i * cellsize, meatstrt[1], 50, 0.5, wawe + 10, 'red', False)
                        else:
                            meatcreate(meatstrt[0] - 2 * i * cellsize, meatstrt[1], wawe * 50 + wawe1 * 20,
                                       0.5 + wawe1 * 0.1, wawe + 10, 'red', False)
                    wawe += 1
                    if wawe == 3 and wawe1 != 3:
                        wawe1 += 1
                        wawe = 0
                    if wawe == 3 and wawe1 < 3:
                        wawe1 += 1
                    spawntime = 0
                else:
                    spawntime += 1
            if len(meat) == 0 and (wawe1 > 1):
                meatend = True
            else:
                meatend = False
            for tower in towers:
                tower.draw()
                tower.fire(tower)
        else:
            for drop in drops:
                drop.fly()
                drop.take()
                drop.draw()
                if drop.taked():
                    drops.remove(drop)
                    plr.money += 1
                    plrmetal += 1
            for bullet in bullets:
                bullet.move()
                bullet.draw()
                # pygame.draw.rect(window, 'red', bullet.rect, 1)
                if player.rect().colliderect(bullet.rect):
                    player.hp -= 1
                    plrdamage += 1
                    bullets.remove(bullet)
                    break
                for wall in walls:
                    if wall.colliderect(bullet.rect):
                        bullets.remove(bullet)
                        break
                for tower in towers:
                    if tower.rect.colliderect(bullet.rect) and bullet.tower != tower:
                        tile_rects.remove(
                            pygame.Rect(tower.x - cellsize / 2, tower.y - cellsize / 2, cellsize, cellsize))
                        towerrects.remove(
                            pygame.Rect(tower.x - cellsize / 2, tower.y - cellsize / 2, cellsize, cellsize))
                        tile_rects_coord.remove(
                            [(tower.x - cellsize / 2) // cellsize, (tower.y - cellsize / 2) // cellsize])
                        towers.remove(tower)
                        bullets.remove(bullet)
                        plrtowers += 1
                        explosions.append(e.Explosion(tower.x, tower.y))
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
            for tower in towers:
                tower.draw()
    else:
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
        for tower in towers:
            tower.draw()


plr = Player(35)
wawe = 0
wawe1 = 1
crosshair = Crosshair()
player = e.Player(*[cellsize * countx - 0.8 * cellsize, cellsize * 11], 0.8 * cellsize, 0.8 * cellsize, 10, 'player')
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


def towerdefence(metalmoney=0, ammo = 128, hpn=10):
    global countx, county, sclsz, sclsz1, width1, height1, width, height, cellsize, cellsize1, countx1, county1, fps
    global flscr, show, inviztime, inhub, meatend, bullets, towers, meat, drops, heals, walls, way, allmetal, tile_rects
    global tile_rects1, tile_rects_coord, explosions, towernum, spawntime, playerv, speedcoef, uirect, Map, down
    global right, up, left, napr, mousx, mousy, dieuiclicked, alive, myfont, myfont1, window, hubscreen, monitor
    global deadscreen, crosshairsurf, ss, sand, ssand, ssway, cross, clock, lenwalls, meatstrt, plr, wawe, crosshair
    global player, fullhp, playerhp, running, moving_right, moving_left, moving_up, moving_down, last_time, greentower
    global greentow, yellowtower, yellowtow, redtower, redtow, bluetower, bluetow, metim, metal, metim1, metal1, metim2
    global metal2, metim3, metal3, allmetal, helim, healim, greentow1, yellowtow1, redtow1, bluetow1, wawe1, portalcoord
    global metalmoneypast, plrkills, plrdamage, plrtowers, plrmetal

    running = True
    alive = True
    bullets = []
    towers = []
    meat = []
    drops = []
    heals = []
    tile_rects = tile_rects[:lenwalls]
    tile_rects_coord = tile_rects_coord[:lenwalls]
    wawe = 0
    wawe1 = 1
    player.set_pos(cellsize * countx - player.width, cellsize * 11.1)
    player.hp = 10
    player.ammo = ammo
    plr.money = metalmoney
    metalmoneypast = metalmoney
    playerv = 2
    t = 0
    meatend = False
    moving_right = False
    portal = e.Portal(*portalcoord, 10, 'portal')
    portal.is_active = False
    use = False
    player.show_weapon = False
    player.hp = hpn
    runningar = True
    mosang = 0
    while running:
        # print(f"{plrkills}\t{plrdamage}\t{plrtowers}\t{plrmetal}")
        pygame.mouse.set_visible(False)
        if alive:
            if meatend and t == 0:
                portal.is_active = True
                winwin(monitor)
                t = 1
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
            if player_movement[0] != 0 and player_movement[1] != 0:
                player_movement[0] *= math.sin(math.pi / 4)
                player_movement[1] *= math.sin(math.pi / 4)
            if use:
                use = False
                if portal.used(player):
                    running = False

            if player_movement[0] != 0 or player_movement[1] != 0:
                if player_movement[0] > 0:
                    mosang = 0
                if player_movement[0] < 0:
                    mosang = 3.2
                player.change_action('running')
            elif player_movement[0] == 0 and player_movement[1] == 0:
                player.change_action('idle')
            player.move(player_movement, tile_rects, [])
            player.update(mosang)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        maketower(towernum)
                        if getmpos()[0] >= 68 * cellsize:
                            towernum = uiswtch()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F5:
                        show = not show
                    if event.key == pygame.K_F9:
                        plr.money += 100
                    if event.key == pygame.K_F11:
                        fullscrn(screen)
                    if event.key == pygame.K_F1:
                        if fps == 120:
                            fps = 60
                        else:
                            fps = 120
                    if event.key == pygame.K_f:
                        use = True
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
                            if ingamemenu(monitor, False):
                                running = False
                                runningar = False
                                plr.money = 0
                                player.hp = 10
                                player.ammo = 128
                                spaceship.metal = 0
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_d:
                        moving_right = False
                    if event.key == pygame.K_a:
                        moving_left = False
                    if event.key == pygame.K_w:
                        moving_up = False
                    if event.key == pygame.K_s:
                        moving_down = False
            if player.x > cellsize * countx and meatend:
                break
            if pygame.Rect(cellsize * countx, 11 * cellsize, cellsize, cellsize) not in tile_rects:
                tile_rects.append(pygame.Rect(cellsize * countx, 11 * cellsize, cellsize, cellsize))
            if pygame.Rect(-cellsize, 11 * cellsize, cellsize, cellsize) not in tile_rects:
                tile_rects.append(pygame.Rect(-cellsize, 11 * cellsize, cellsize, cellsize))
            createfloor()
            createwall()
            createway()
            run()
            portal.update(player)
            portal.draw(window, [0, 0])
            player.draw(window, [0, 0])
            createrad()
            for i, explosion in sorted(enumerate(explosions), reverse=True):
                explosion.update()
                explosion.draw(window, [0, 0])
                if len(explosion.particles) == 0:
                    del explosion
                    explosions.pop(i)
            monitor.blit(pygame.transform.scale(window, (width1, height1)), (0, 0))
            playerhp.draw(fullhp, player.hp)
            ui()
            crosshair.render()
            checklife()
        else:
            plrtowers = 0
            plrdamage = 0
            plrmetal = 0
            plrkills = 0
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
            if dieui():
                runningar = False
            crosshair.render()
        showfps()
        pygame.display.update()
        clock.tick(fps)
    return plr.money, player.ammo, runningar, player.hp


def fullscrn(display):
    global flscr
    if flscr:
        display = pygame.display.set_mode(WINDOW_SIZE)
    else:
        display = pygame.display.set_mode(WINDOW_SIZE, pygame.FULLSCREEN)
    flscr = not flscr


def ingamemenu(surface, exitnal=True):
    running = True
    pygame.mouse.set_visible(True)
    SCALE_MULTIPLIER = 5
    click = False
    font = pygame.font.Font('MaredivRegular.ttf', 20)
    display = pygame.Surface((WINDOW_SIZE[0] / SCALE_MULTIPLIER, WINDOW_SIZE[1] / SCALE_MULTIPLIER), pygame.SRCALPHA)
    background = pygame.Surface(WINDOW_SIZE, pygame.SRCALPHA)
    background.blit(pygame.transform.scale(surface, WINDOW_SIZE), (0, 0))
    while running:
        display.fill((0, 0, 0, 200))
        screen.blit(background, (0, 0))
        mx, my = pygame.mouse.get_pos()
        playbtn = pygame.Rect(WINDOW_SIZE[0] / SCALE_MULTIPLIER / 2 - 20, 106, 36, 23)
        optionsbtn = pygame.Rect(WINDOW_SIZE[0] / SCALE_MULTIPLIER / 2 - 35, 141, 69, 23)
        if exitnal:
            exitbtn = pygame.Rect(WINDOW_SIZE[0] / SCALE_MULTIPLIER / 2 - 20, 176, 36, 19)
        mx = mx / SCALE_MULTIPLIER
        my = my / SCALE_MULTIPLIER
        if playbtn.collidepoint((mx, my)):
            cveta1 = (214, 136, 17)
            if click:
                break
        else:
            cveta1 = (255, 235, 214)
        if optionsbtn.collidepoint((mx, my)):
            cveta3 = (214, 136, 17)
            if click:
                options()
        else:
            cveta3 = (255, 235, 214)
        if exitnal:
            if exitbtn.collidepoint((mx, my)):
                cveta5 = (214, 136, 17)
                if click:
                    return True
            else:
                cveta5 = (255, 235, 214)
        text = font.render("play", True, cveta1)
        display.blit(text, (WINDOW_SIZE[0] / SCALE_MULTIPLIER / 2 - 20, 100))

        text = font.render("options", True, cveta3)
        display.blit(text, (WINDOW_SIZE[0] / SCALE_MULTIPLIER / 2 - 35, 135))

        if exitnal:
            text = font.render("exit", True, cveta5)
            display.blit(text, (WINDOW_SIZE[0] / SCALE_MULTIPLIER / 2 - 20, 170))
        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

            if event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    click = False

            if event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    click = False
        screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
        pygame.display.update()
        clock.tick(60)
    pygame.mouse.set_visible(False)


def winwin(surface):
    running = True
    pygame.mouse.set_visible(True)
    SCALE_MULTIPLIER = 5
    click = False
    font = pygame.font.Font('MaredivRegular.ttf', 20)
    display = pygame.Surface((WINDOW_SIZE[0] / SCALE_MULTIPLIER, WINDOW_SIZE[1] / SCALE_MULTIPLIER), pygame.SRCALPHA)
    background = pygame.Surface(WINDOW_SIZE, pygame.SRCALPHA)
    background.blit(pygame.transform.scale(surface, WINDOW_SIZE), (0, 0))
    while running:
        display.fill((0, 0, 0, 100))
        screen.blit(background, (0, 0))
        mx, my = pygame.mouse.get_pos()
        playbtn = pygame.Rect(WINDOW_SIZE[0] / SCALE_MULTIPLIER / 2 - 12, 187, 24, 17)
        mx = mx / SCALE_MULTIPLIER
        my = my / SCALE_MULTIPLIER
        if playbtn.collidepoint((mx, my)):
            cveta3 = (214, 136, 17)
            if click:
                running = False
        else:
            cveta3 = (255, 235, 214)
        text1 = font.render("The waves are over,", True, (255, 235, 214))
        display.blit(text1, (95, 50))
        text1 = font.render("you can go out!", True, (255, 235, 214))
        display.blit(text1, (115, 70))
        text = font.render("OK", True, cveta3)
        display.blit(text, (WINDOW_SIZE[0] / SCALE_MULTIPLIER / 2 - 12, 180))
        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

            if event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    click = False

            if event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    click = False
        screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
        pygame.display.update()
        clock.tick(60)


def main_menu():
    running = True
    pygame.mouse.set_visible(True)
    SCALE_MULTIPLIER = 5
    click = False
    font = pygame.font.Font('MaredivRegular.ttf', 15)
    display = pygame.Surface((WINDOW_SIZE[0] / SCALE_MULTIPLIER, WINDOW_SIZE[1] / SCALE_MULTIPLIER), pygame.SRCALPHA)
    stars = pygame.Surface((WINDOW_SIZE[0] / SCALE_MULTIPLIER, WINDOW_SIZE[1] / SCALE_MULTIPLIER), pygame.SRCALPHA)
    stars1 = pygame.Surface((WINDOW_SIZE[0] / SCALE_MULTIPLIER, WINDOW_SIZE[1] / SCALE_MULTIPLIER), pygame.SRCALPHA)
    stars2 = pygame.Surface((WINDOW_SIZE[0] / SCALE_MULTIPLIER, WINDOW_SIZE[1] / SCALE_MULTIPLIER), pygame.SRCALPHA)
    stars3 = pygame.Surface((WINDOW_SIZE[0] / SCALE_MULTIPLIER, WINDOW_SIZE[1] / SCALE_MULTIPLIER),
                            pygame.SRCALPHA)
    stars0 = pygame.Surface((WINDOW_SIZE[0], WINDOW_SIZE[1]))

    pygame.mixer.music.load("music/Space Lion.mp3")
    pygame.mixer.music.play(-1)

    for i in range(100):
        stars.fill(pygame.Color('white'),
                   (random.random() * WINDOW_SIZE[0] / SCALE_MULTIPLIER,
                    random.random() * WINDOW_SIZE[1] / SCALE_MULTIPLIER, 1, 1))
    for i in range(40):
        stars1.fill(pygame.Color('white'),
                    (random.random() * WINDOW_SIZE[0] / SCALE_MULTIPLIER,
                     random.random() * WINDOW_SIZE[1] / SCALE_MULTIPLIER, 1, 1))
    for i in range(20):
        stars2.fill(pygame.Color('white'),
                    (random.random() * WINDOW_SIZE[0] / SCALE_MULTIPLIER,
                     random.random() * WINDOW_SIZE[1] / SCALE_MULTIPLIER, 1, 1))
    for i in range(10):
        stars3.fill(pygame.Color('white'),
                    (random.random() * WINDOW_SIZE[0] / SCALE_MULTIPLIER,
                     random.random() * WINDOW_SIZE[1] / SCALE_MULTIPLIER, 1, 1))
    while running:
        mpx, mpy, = pygame.mouse.get_pos()
        stars0.fill((15, 11, 66))
        stars0.blit(stars, ((mpx - WINDOW_SIZE[0] / 2) / 280, (mpy - WINDOW_SIZE[1] / 2) / 280))
        stars0.blit(stars1, ((mpx - WINDOW_SIZE[0] / 2) / 200, (mpy - WINDOW_SIZE[1] / 2) / 200))
        stars0.blit(stars2, ((mpx - WINDOW_SIZE[0] / 2) / 140, (mpy - WINDOW_SIZE[1] / 2) / 140))
        stars0.blit(stars3, ((mpx - WINDOW_SIZE[0] / 2) / 80, (mpy - WINDOW_SIZE[1] / 2) / 80))
        display.blit(stars0, (0, 0))
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

        title_img = pygame.image.load('data_img/title2.png')
        display.blit(title_img, (121, 50))

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

            if event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    click = False
        screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
        pygame.display.update()
        clock.tick(60)
    pygame.mixer.music.fadeout(1000)


def trade_area(hpn=10):
    SCALE_MULTIPLIER = 4
    display = pygame.Surface((WINDOW_SIZE[0] / SCALE_MULTIPLIER, WINDOW_SIZE[1] / SCALE_MULTIPLIER))
    global spaceship #  comment if something goes wrong
    clicked = False
    running = True
    use = False
    swap_weapons = False
    moving_right = False
    moving_left = False
    moving_up = False
    moving_down = False
    one_click = False
    true_scroll = [0, 0]
    scroll = [0, 0]

    pygame.mixer.music.load("music/Don't Bother none.mp3")
    pygame.mixer.music.play(-1)
    last_time = time.time()

    pygame.mouse.set_visible(False)
    world = e.TradeWorld(24, 14, 20)
    world.field = [['0'] * world.width for _ in range(world.height)]
    world.generate_map()
    player = e.Player(200, 100, 16, 16, 10, 'player')
    cursor = e.Cursor(0, 0, curstype)
    portal1 = e.Portal(240, 30, 10, 'portal')
    portal2 = e.Portal(30, 140, 10, 'portal')
    metalcount = e.MetalCount(10, 25, 0)
    ammocount = e.AmmoCount(10, 35, 0)
    world.add_usable_entity(portal1)
    world.add_usable_entity(portal2)
    particles = []
    #  spaceship = e.SpaceShip(300, 140, 21, 20, 1, "spaceship")
    player.hp = hpn
    
    if 'autosave.txt' in os.listdir(f'{os.getcwd()}\\save'):
        stats = open(f'{os.getcwd()}\\save\\autosave.txt', 'r')
        x = stats.readlines()
        if x:
            player.hp = int(str(x[0]))
            player.metal = int(str(x[1]))
            player.ammo = int(str(x[2]))
            spaceship.metal = int(str(x[3]))
        stats.close()
    player.metal = 100
    pick = e.pickableWeapon(300, 100, e.AltMachineGun(300, 100, 0, player))
    world.add_usable_entity(pick)
    while running:
        # print(f"{plrkills}\t{plrdamage}\t{plrtowers}\t{plrmetal}")
        pygame.mouse.set_visible(False)
        dt = time.time() - last_time
        dt *= 60
        last_time = time.time()
        display.fill((207, 117, 43))
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
        if one_click:
            one_click = False
        if use:
            use = False
            world.check_use(player)
            spaceship.use(player)
            if spaceship.metal >= 60:
                winscreen(display, player.x - spaceship.x, player.y - spaceship.y)
                spaceship.metal = 0
                running = False
            if portal1.used(player):
                player.metal, player.ammo, player.hp, is_exit = game(player.metal, player.ammo, player.hp)
                if is_exit:
                    stats = open(f'{os.getcwd()}\\save\\autosave.txt', 'w')
                    stats.write(str(f"{10}\n{0}\n{128}\n{0}"))
                    stats.close()
                    running = False
            if portal2.used(player):
                player.metal, player.ammo, running, player.hp = towerdefence(player.metal, player.ammo, player.hp)
                if running == False:
                    stats = open(f'{os.getcwd()}\\save\\autosave.txt', 'w')
                    stats.write(str(f"{10}\n{0}\n{128}\n{0}"))
                    stats.close()

        if swap_weapons:
            player.swap_weapons()
            swap_weapons = False


        if player_movement[0] != 0 and player_movement[1] != 0:
            player_movement[0] *= math.sin(math.pi / 4)
            player_movement[1] *= math.sin(math.pi / 4)

        if player_movement[0] != 0 or player_movement[1] != 0:
            if player_movement[0] > 0:
                player.is_flipped = False
            if player_movement[0] < 0:
                player.is_flipped = True
            player.change_action('running')
        elif player_movement[0] == 0 and player_movement[1] == 0:
            player.change_action('idle')

        collision_types = player.move(player_movement, tile_rects, [spaceship])

        player.move_projectiles(world, world.get_enemies(), dt)
        player.update(mouse_angle)
        world.update(player, dt)
        #  pick.update(player)
        spaceship.update(player)
        world.draw(display, scroll)
        #  pick.draw(display, scroll)
        player.draw(display, scroll)
        player.draw_projectiles(display, scroll)
        spaceship.draw(display, scroll)
        metalcount.set_metal(player.metal)
        ammocount.set_ammo(player.ammo)
        print(player.hp, player.metal)
        #  player.move(player_movement)
        #  pygame.draw.line(display, (0, 255, 0), (player.x + player.width / 2 - scroll[0], player.y + player.height / 2 - scroll[1]), ((pygame.mouse.get_pos()[0] // SCALE_MULTIPLIER), (pygame.mouse.get_pos()[1] // SCALE_MULTIPLIER)))

        #  particles.append(e.Particle(player.x - scroll[0] + player.width // 2, player.y - scroll[1] + player.height // 2, scroll))

        for i, particle in sorted(enumerate(particles), reverse=True):
            particle.update()
            particle.draw(display, scroll)
            if particle.time < 0:
                del particle
                particles.pop(i)

        metalcount.draw(display)
        player.healthbar.draw(display)
        ammocount.draw(display)
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
                    if ingamemenu(screen):
                        running = False
                        stats = open(f'{os.getcwd()}\\save\\autosave.txt', 'w')
                        stats.write(str(f"{player.hp}\n{player.metal}\n{player.ammo}\n{spaceship.metal}"))
                        stats.close()
                    cursor = e.Cursor(0, 0, curstype)
                if event.key == pygame.K_F11:
                    fullscrn(display)
                if event.key == pygame.K_F10:
                    winscreen(display, player.x - spaceship.x, player.y - spaceship.y)
                if event.key == pygame.K_f:
                    use = True
                if event.key == pygame.K_q or event.key == pygame.K_SPACE:
                    swap_weapons = True
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
                if event.key == pygame.K_q or event.key == pygame.K_SPACE:
                    swap_weapons = False
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    clicked = True
                    one_click = True
            if event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    clicked = False
                    one_click = False

        screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
        pygame.display.update()
        clock.tick(60)
    pygame.mouse.set_visible(True)


def game(metal=0, ammo=128, hpn=10):
    SCALE_MULTIPLIER = 4
    display = pygame.Surface((WINDOW_SIZE[0] / SCALE_MULTIPLIER, WINDOW_SIZE[1] / SCALE_MULTIPLIER))
    global curstype, plrkills
    one_click = False
    clicked = False
    running = True
    use = False
    swap_weapons = False
    moving_right = False
    moving_left = False
    moving_up = False
    moving_down = False
    dead = False

    true_scroll = [0, 0]
    scroll = [0, 0]

    last_time = time.time()

    pygame.mouse.set_visible(False)
    world = e.World(48, 48, 20)
    world.generate_map()
    player = e.Player(*world.get_start_pos(), 16, 16, 10, 'player')
    cursor = e.Cursor(0, 0, curstype)
    portal = e.Portal(*world.get_start_pos(), 10, 'portal')
    metalcount = e.MetalCount(10, 25, 0)
    ammocount = e.AmmoCount(10, 35, 10)
    defense_timer = e.Timer(45, WINDOW_SIZE[0] / SCALE_MULTIPLIER / 2, 10)
    world.add_usable_entity(portal)
    particles = []
    player.metal = metal
    player.hp = hpn
    player.ammo = ammo
    enemy_count = 0
    enemy_num = len(world.get_enemies())
    while running:
        pygame.mouse.set_visible(False)
        dt = time.time() - last_time
        dt *= 60
        last_time = time.time()
        display.fill((207, 117, 43))
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
            if portal.used(player):
                running = False
        if swap_weapons:
            player.swap_weapons()
            swap_weapons = False


        if player_movement[0] != 0 and player_movement[1] != 0:
            player_movement[0] *= math.sin(math.pi / 4)
            player_movement[1] *= math.sin(math.pi / 4)

        if player_movement[0] != 0 or player_movement[1] != 0:
            # if player_movement[0] > 0:
            #     player.is_flipped = False
            # if player_movement[0] < 0:
            #     player.is_flipped = True
            player.change_action('running')
        elif player_movement[0] == 0 and player_movement[1] == 0:
            player.change_action('idle')

        collision_types = player.move(player_movement, tile_rects, [])



        player.move_projectiles(world, world.get_enemies(), dt)
        player.update(mouse_angle)
        world.update(player, dt)
        world.draw(display, scroll)
        player.draw(display, scroll)
        player.draw_projectiles(display, scroll)
        metalcount.set_metal(player.metal)
        ammocount.set_ammo(player.ammo)
        defense_timer.update()
        if defense_timer.get_time() <= 0 or player.hp <= 0:
            dead = True
        #  player.move(player_movement)
        #  pygame.draw.line(display, (0, 255, 0), (player.x + player.width / 2 - scroll[0], player.y + player.height / 2 - scroll[1]), ((pygame.mouse.get_pos()[0] // SCALE_MULTIPLIER), (pygame.mouse.get_pos()[1] // SCALE_MULTIPLIER)))

        #  particles.append(e.Particle(player.x - scroll[0] + player.width // 2, player.y - scroll[1] + player.height // 2, scroll))

        for i, particle in sorted(enumerate(particles), reverse=True):
            particle.update()
            particle.draw(display, scroll)
            if particle.time < 0:
                del particle
                particles.pop(i)

        defense_timer.draw(display)
        player.healthbar.draw(display)
        metalcount.draw(display)
        ammocount.draw(display)
        cursor.draw(display)

        if dead:
            if deathui(display, player):
                spaceship.metal = 0
                return player.metal, player.ammo, player.hp, True
            running = False

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
                    if ingamemenu(screen, False):
                        running = False
                    cursor = e.Cursor(0, 0, curstype)
                if event.key == pygame.K_F11:
                    fullscrn(display)
                if event.key == pygame.K_f:
                    use = True
                if event.key == pygame.K_q or event.key == pygame.K_SPACE:
                    swap_weapons = True
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
                if event.key == pygame.K_q or event.key == pygame.K_SPACE:
                    swap_weapons = False
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    clicked = True
                    one_click = True
            if event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    clicked = False
                    one_click = False

        screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
        
        pygame.display.update()
        clock.tick(60)
    pygame.mouse.set_visible(True)
    plrkills += enemy_num - len(world.get_enemies())
    return player.metal, player.ammo, player.hp, False



def options():
    pygame.mouse.set_visible(True)
    SCALE_MULTIPLIER = 5
    cveta1 = (200, 200, 200)
    font = pygame.font.Font('MaredivRegular.ttf', 15)
    display = pygame.Surface((WINDOW_SIZE[0] / SCALE_MULTIPLIER, WINDOW_SIZE[1] / SCALE_MULTIPLIER))
    n = 0
    running = True
    bomb_image = load_image("data_img/esc.png")
    while running:
        m = 0
        display.fill((0, 0, 0))
        mx, my = pygame.mouse.get_pos()
        all_sprites = pygame.sprite.Group()
        sprite = pygame.sprite.Sprite()
        bomb = pygame.sprite.Sprite(all_sprites)
        bomb.image = bomb_image
        bomb.rect = bomb.image.get_rect()
        bomb.rect.x = 0
        bomb.rect.y = 0
        button_4 = pygame.Rect(0, 0, 20, 20)
        mx = mx / SCALE_MULTIPLIER
        my = my / SCALE_MULTIPLIER
        all_sprites.draw(display)
        text1 = font.render("Audio", True, (cveta1))
        display.blit(text1, (WINDOW_SIZE[0] // 12, 0))
        text2 = font.render("Video", True, (cveta1))
        display.blit(text2, (WINDOW_SIZE[0] // 12, 20))
        text2 = font.render("Game", True, (cveta1))
        display.blit(text2, (WINDOW_SIZE[0] // 12, 40))
        text2 = font.render("Cotrols", True, (cveta1))
        display.blit(text2, (WINDOW_SIZE[0] // 12, 60))
        button_1 = pygame.Rect(WINDOW_SIZE[0] // 8 - 400 / SCALE_MULTIPLIER, 0, 250 / SCALE_MULTIPLIER,
                               100 / SCALE_MULTIPLIER)
        button_2 = pygame.Rect(WINDOW_SIZE[0] // 8 - 400 / SCALE_MULTIPLIER, 100 / SCALE_MULTIPLIER,
                               250 / SCALE_MULTIPLIER, 100 / SCALE_MULTIPLIER)
        # pygame.draw.circle(display, (0, 255, 0), (mx, my), 2)
        # pygame.draw.rect(display, (0, 255, 0), button_1, 1)
        # pygame.draw.rect(display, (0, 255, 0), button_2, 1)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_1.collidepoint((mx, my)):
                    n = 1
                if button_4.collidepoint((mx, my)):
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_2.collidepoint((mx, my)):
                    m = 1
        if n == 1:
            Audio()
            n = 0
        if m == 1:
            Video()
            m = 0
        screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
        pygame.display.update()
        clock.tick(60)


def Audio():
    global volume
    TILE_SIZE = 16
    #  screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
    n = 0
    pygame.mouse.set_visible(True)
    SCALE_MULTIPLIER = 5
    cveta1 = (200, 200, 200)
    usl1 = 0
    usl2 = 0
    uslza = 0
    font = pygame.font.Font('MaredivRegular.ttf', 15)
    font1 = pygame.font.Font('MaredivRegular.ttf', 18)
    bomb_image = load_image("data_img/esc.png")
    display = pygame.Surface((WINDOW_SIZE[0] / SCALE_MULTIPLIER, WINDOW_SIZE[1] / SCALE_MULTIPLIER))
    running = True
    stats = open(f'{os.getcwd()}\\options\\audio.txt', 'r')
    x = stats.readlines()
    if x:
        volume = int(str(x[0]))
    stats.close()
    while running:
        display.fill((0, 0, 0))
        mx, my = pygame.mouse.get_pos()
        all_sprites = pygame.sprite.Group()
        sprite = pygame.sprite.Sprite()
        bomb = pygame.sprite.Sprite(all_sprites)
        bomb.image = bomb_image
        bomb.rect = bomb.image.get_rect()
        bomb.rect.x = 0
        bomb.rect.y = 0
        all_sprites.draw(display)
        pygame.draw.rect(display, (255, 255, 255), (240, 2, 20, 20))
        pygame.draw.rect(display, (255, 255, 255), (210, 2, 20, 20))
        text3 = font1.render('+', True, (0, 0, 0))
        display.blit(text3, (244, -2))
        text3 = font1.render('-', True, (0, 0, 0))
        display.blit(text3, (214, -2))

        text2 = font.render(f"sound-{volume}/100", True, (cveta1))
        display.blit(text2, (100, 2))
        mx = mx / SCALE_MULTIPLIER
        my = my / SCALE_MULTIPLIER
        button_1 = pygame.Rect(100, 2, 100, 20)
        button_2 = pygame.Rect(240, 2, 20, 20)
        button_3 = pygame.Rect(210, 2, 20, 20)
        button_4 = pygame.Rect(0, 0, 20, 20)
        for event in pygame.event.get():

            if event.type == QUIT:
                pygame.quit()
                sys.exit()
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
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_4.collidepoint((mx, my)):
                    running = False
        uslza += 0.5
        if usl2 == 1 and uslza % 3 == 0:
            if volume - 1 >= 0:
                volume -= 1
        if usl1 == 1 and uslza % 3 == 0:
            if volume + 1 <= 100:
                volume += 1
        pygame.mixer.music.set_volume(volume / 100)
        screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
        pygame.display.update()
        clock.tick(60)
    stats = open('options\\audio.txt', 'w')
    stats.write(str(volume))
    stats.close()


def winscreen(surface, x, y):
    running = True
    pygame.mouse.set_visible(True)
    SCALE_MULTIPLIER = 4
    click = False
    font = pygame.font.Font('MaredivRegular.ttf', 20)
    display = pygame.Surface((WINDOW_SIZE[0] / SCALE_MULTIPLIER, WINDOW_SIZE[1] / SCALE_MULTIPLIER), pygame.SRCALPHA)
    background = pygame.Surface(WINDOW_SIZE, pygame.SRCALPHA)
    background.blit(pygame.transform.scale(surface, WINDOW_SIZE), (0, 0))
    center = [(WINDOW_SIZE[0] / SCALE_MULTIPLIER / 2 - player.width / 2) - x + 10, (WINDOW_SIZE[1] / SCALE_MULTIPLIER / 2 - player.width / 2) - y + 10]
    layer = pygame.Surface((WINDOW_SIZE[0] / SCALE_MULTIPLIER, WINDOW_SIZE[1] / SCALE_MULTIPLIER), pygame.SRCALPHA)
    stars = pygame.Surface((WINDOW_SIZE[0] / SCALE_MULTIPLIER, WINDOW_SIZE[1] / SCALE_MULTIPLIER),
                           pygame.SRCALPHA)
    stars.fill((15, 11, 66))
    for i in range(200):
        stars.fill(pygame.Color('white'),
                   (random.random() * WINDOW_SIZE[0] / SCALE_MULTIPLIER,
                    random.random() * WINDOW_SIZE[1] / SCALE_MULTIPLIER, 1, 1))
    stars = pygame.transform.scale(stars, (WINDOW_SIZE[0] + 10, WINDOW_SIZE[1] + 10))
    v = 250
    r = 0
    r1 = 0
    t = 0
    prz = 0
    prz1 = 0
    timer = 0
    explosion = True
    flying = True
    up = False
    click = False
    x1 = 0
    y1 = 0
    x2 = 0
    y2 = 0
    myfont2 = pygame.font.Font('MaredivRegular.ttf', round(cellsize))
    font3 = pygame.font.Font('MaredivRegular.ttf', 15)
    font4 = pygame.font.Font('MaredivRegular.ttf', 18)
    # explosion = False
    # timer = 700
    rocket = pygame.image.load('data_img/rocket7.png').convert_alpha()
    while running:
        while explosion:
            display.fill((0, 0, 0, 150))
            screen.blit(background, (0, 0))
            mx, my = pygame.mouse.get_pos()
            pygame.draw.circle(display, 'white', center, r)
            r += v / 60
            while timer < 90 and r > 25:
                if t == 0:
                    r1 = r
                    t = 1
                display.fill((0, 0, 0, 150))
                screen.blit(background, (0, 0))
                pygame.draw.circle(display, 'white', center, r1)
                if timer % 10 == 0:
                    if up:
                        r1 += 1
                    else:
                        r1 -= 1
                    up = not up
                timer += 1
                if timer == 90:
                    v = 700
                    r = r1
                screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
                pygame.display.update()
                clock.tick(60)
            if WINDOW_SIZE[0] / SCALE_MULTIPLIER < r:
                explosion = False
                timer = 0
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
            screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
            pygame.display.update()
            clock.tick(60)
        while flying:
            if timer % 2 == 0:
                x1 = random.randint(-10, 0)
                y1 -= random.randint(-10, 0)
                x2 = random.randint(-2, 2)
                y2 = random.randint(-2, 2)
                if y1 >= WINDOW_SIZE[1]:
                    y1 = 0
            screen.blit(stars, (x1, y1))
            screen.blit(stars, (x1, y1 - WINDOW_SIZE[1]))
            screen.blit(rocket, (WINDOW_SIZE[0] / 2 - 112 + x2, WINDOW_SIZE[1] / 2 - 250 + y2))
            display.fill((255, 255, 255, 255 - prz))
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        flying = False
                        running = False
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True

                if event.type == MOUSEBUTTONUP:
                    if event.button == 1:
                        click = False

            if timer > 700:
                mx, my = pygame.mouse.get_pos()
                layer.fill((0, 0, 0, prz1))
                hp = myfont2.render(str('You have left the planet!'), False, (255, 235, 214))
                layer.blit(hp, (4 * cellsize, 1.5 * cellsize))
                hp = font4.render(str(f'Mobs killed: {plrkills}'), False, (255, 235, 214))
                layer.blit(hp, (5 * cellsize, 3.5 * cellsize))
                hp = font4.render(str(f'Metal received: {plrmetal}'), False, (255, 235, 214))
                layer.blit(hp, (5 * cellsize, 4.5 * cellsize))
                hp = font4.render(str(f'Damage received: {plrdamage}'), False, (255, 235, 214))
                layer.blit(hp, (5 * cellsize, 5.5 * cellsize))
                hp = font4.render(str(f'Towers destroyed: {plrtowers}'), False, (255, 235, 214))
                layer.blit(hp, (5 * cellsize, 6.5 * cellsize))
                if prz1 < 180:
                    prz1 += 1
                playbtn = pygame.Rect(WINDOW_SIZE[0] / SCALE_MULTIPLIER / 2 - 45, 223, 95, 29)
                mx = mx / SCALE_MULTIPLIER
                my = my / SCALE_MULTIPLIER
                if playbtn.collidepoint((mx, my)):
                    cveta = (78, 29, 92)
                    cveta1 = (214, 136, 17)
                    if click:
                        running = False
                        flying = False
                else:
                    cveta = (109, 29, 112)
                    cveta1 = (255, 235, 214)
                pygame.draw.rect(layer, cveta, playbtn)
                text = font3.render("Main menu", True, cveta1)
                layer.blit(text, (WINDOW_SIZE[0] / SCALE_MULTIPLIER / 2 - 32, 225))
                click = False
            screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
            screen.blit(pygame.transform.scale(layer, WINDOW_SIZE), (0, 0))
            pygame.display.update()
            clock.tick(60)
            timer += 1
            if prz != 255:
                prz += 1
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
        screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
        pygame.display.update()
        clock.tick(60)
    pygame.mouse.set_visible(False)


def load_image(name, colorkey=None):
    fullname = os.path.join(name)
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def Video():
    global curstype, flscr
    #  screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
    n = 0
    m = 0
    pygame.mouse.set_visible(True)
    SCALE_MULTIPLIER = 5
    cveta1 = (200, 200, 200)
    cveta2 = (200, 200, 200)
    cveta3 = (200, 0, 0)
    uslza = 0
    font = pygame.font.Font('MaredivRegular.ttf', 15)
    font1 = pygame.font.Font('MaredivRegular.ttf', 25)
    display = pygame.Surface((WINDOW_SIZE[0] / SCALE_MULTIPLIER, WINDOW_SIZE[1] / SCALE_MULTIPLIER))
    bomb_image = load_image("data_img/esc.png")
    running = True
    stats = open(f'{os.getcwd()}\\options\\video.txt', 'r')
    x = stats.readlines()
    if x:
        m = int(str(x[0]))
        n = int(str(x[1]))
    stats.close()
    while running:
        display.fill((0, 0, 0))
        mx, my = pygame.mouse.get_pos()
        all_sprites = pygame.sprite.Group()
        sprite = pygame.sprite.Sprite()
        bomb = pygame.sprite.Sprite(all_sprites)
        bomb.image = bomb_image
        bomb.rect = bomb.image.get_rect()
        bomb.rect.x = 0
        bomb.rect.y = 0
        all_sprites.draw(display)
        text1 = font.render(f"Crosshair-{n + 1}/3", True, (cveta1))
        display.blit(text1, (100, 0))
        text1 = font.render("Fullscreen      /", True, (cveta1))
        display.blit(text1, (100, 20))
        text1 = font.render("                on", True, (cveta2))
        display.blit(text1, (100, 20))
        text1 = font.render("                       off", True, (cveta3))
        display.blit(text1, (100, 20))
        mx = mx / SCALE_MULTIPLIER
        my = my / SCALE_MULTIPLIER
        button_1 = pygame.Rect(100, 0, 100, 20)
        button_2 = pygame.Rect(180, 20, 15, 20)
        button_3 = pygame.Rect(215, 20, 25, 20)
        button_4 = pygame.Rect(0, 0, 20, 20)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                if button_1.collidepoint((mx, my)):
                    if n + 2 > 3:
                        n = 0
                    else:
                        n += 1
            if event.type == pygame.MOUSEBUTTONUP:
                if button_2.collidepoint((mx, my)):
                    m = 1
                    pygame.display.set_mode(WINDOW_SIZE, pygame.FULLSCREEN)

            if event.type == pygame.MOUSEBUTTONUP:
                if button_3.collidepoint((mx, my)):
                    m = 0
                    pygame.display.set_mode(WINDOW_SIZE)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_4.collidepoint((mx, my)):
                    running = False
        if m == 1:
            cveta2 = (200, 0, 0)
            cveta3 = (200, 200, 200)

        if m == 0:
            cveta2 = (200, 200, 200)
            cveta3 = (200, 0, 0)
        curstype = f'data_img/curs{n + 1}.png'
        stats = open('options\\video.txt', 'w')
        stats.write(str(f'{m}\n{n}'))
        stats.close()
        screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
        pygame.display.update()
        clock.tick(60)


stats = open(f'{os.getcwd()}\\options\\video.txt', 'r')
x = stats.readlines()
if x:
    m = int(str(x[0]))
    n = int(str(x[1]))
    curstype = f'data_img/curs{n + 1}.png'
    if m == 1:
        pygame.display.set_mode(WINDOW_SIZE, pygame.FULLSCREEN)

    if m == 0:
        pygame.display.set_mode(WINDOW_SIZE)
stats.close()


main_menu()

stats = open(f'{os.getcwd()}\\stats\\stats.txt', 'w')
stats.write(str(f"{plrkills}\n{plrdamage}\n{plrtowers}\n{plrmetal}"))
stats.close()
