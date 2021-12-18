import pygame
import math

countx = 34
county = 23
cellsize = 40
width = countx * cellsize
height = county * cellsize + 1
fps = 60
bullets = []
towers = []
meat = []
way = []
towernum = 0
uirect = [pygame.Rect(1361, 160, 240, 170), pygame.Rect(1361, 340, 240, 170),
          pygame.Rect(1361, 510, 240, 170), pygame.Rect(1361, 680, 240, 170)]
Map = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 4, 1, 1, 1, 1, 1, 5, 0, 0, 0, 0, 0, 0, 3, 1, 1, 1, 5, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 3, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 0, 0, 3, 1, 1, 1, 1, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 1, 1, 1, 4, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 3, 1, 1, 1, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]
# down == 2
# right == 3
# up == 4
# left == 5
pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 30)
window = pygame.display.set_mode((width + 240, height))
clock = pygame.time.Clock()


class Player:
    def __init__(self, money):
        self.money = money

    def money(self):
        return self.money


class Tower:
    def __init__(self, x, y, size, color, damage, firespeed, price, attackrad):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.damage = damage
        self.firespeed = firespeed
        self.firerate = 0
        self.price = price
        self.attackrad = attackrad

    def draw(self):
        pygame.draw.circle(window, self.color, [self.x, self.y], self.size)

    def cost(self):
        return self.price


class CommonTower(Tower):
    def fire(self):
        if self.firerate <= 0:
            addbullet(self.x, self.y, 3, 'green', 5, 20)
            self.firerate = self.firespeed
        else:
            self.firerate -= 1 / fps


class CommonTower1(Tower):
    def fire(self):
        if self.firerate <= 0:
            addbullet(self.x, self.y, 3, 'yellow', 5, 20)
            self.firerate = self.firespeed
        else:
            self.firerate -= 1 / fps


class CommonTower2(Tower):
    def fire(self):
        if self.firerate <= 0:
            addbullet(self.x, self.y, 3, 'blue', 5, 20)
            self.firerate = self.firespeed
        else:
            self.firerate -= 1 / fps


class CommonTower3(Tower):
    def fire(self):
        if self.firerate <= 0:
            addbullet(self.x, self.y, 3, 'red', 5, 20)
            self.firerate = self.firespeed
        else:
            self.firerate -= 1 / fps


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


class FreshMeat:
    def __init__(self, x, y, hp, speed, size, color, reward):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.hp = hp
        self.speed = speed
        self.point = 0
        self.reward = reward

    def draw(self):
        pygame.draw.circle(window, self.color, [self.x, self.y], self.size)

    def go(self):
        pass


def createway():
    for j in range(len(Map)):
        for i in range(len(Map[0])):
            if Map[j][i] != 0:
                pygame.draw.rect(window, 'blue', [i * cellsize + 1, j * cellsize + 1,
                                                  cellsize - 1, cellsize - 1])
                way.append([i, j])


def meatcreate(hp, speed, size, color, reward):
    x = cellsize / 2
    for i in range(10):
        x += cellsize
        y = cellsize + cellsize / 2
        meat.append(FreshMeat(x, y, hp, speed, size, color, reward))


def addbullet(x, y, size, color, damage, speed):
    bullets.append(Bullet(x, y, size, color, damage, speed))


def maycreatetower(x, y):
    x += cellsize / 2
    y += cellsize / 2
    if len(towers) > 0:
        for tower in towers:
            if tower.x == x and tower.y == y:
                return False
    for i in way:
        if i[0] + cellsize / 2 == x and i[1] + cellsize / 2 == y:
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
    pygame.draw.rect(window, 'black', [1361, 0, 240, 921])
    pygame.draw.circle(window, 'green', [1482, 230], 60)
    cost = myfont.render('10', False, 'white')
    window.blit(cost, (1467, 285))
    pygame.draw.circle(window, 'yellow', [1482, 410], 60)
    cost = myfont.render('15', False, 'white')
    window.blit(cost, (1467, 465))
    pygame.draw.circle(window, 'red', [1482, 580], 60)
    cost = myfont.render('30', False, 'white')
    window.blit(cost, (1467, 635))
    pygame.draw.circle(window, 'blue', [1482, 750], 60)
    money = myfont.render(str(plr.money), False, 'white')
    cost = myfont.render('50', False, 'white')
    window.blit(cost, (1467, 805))
    window.blit(money, (1461, 30))
    if towernum == 0:
        pygame.draw.rect(window, 'white', [1402, 160, 160, 170], 4)
    if towernum == 1:
        pygame.draw.rect(window, 'white', [1402, 340, 160, 170], 4)
    if towernum == 2:
        pygame.draw.rect(window, 'white', [1402, 510, 160, 170], 4)
    if towernum == 3:
        pygame.draw.rect(window, 'white', [1402, 680, 160, 170], 4)


def uiswtch():
    x, y = getmpos()
    for i in uirect:
        if i.collidepoint((x, y)):
            return uirect.index(i)


def maketower(n):
    x, y = getmpos()
    if maycreatetower(x, y) and x <= width:
        if n == 0 and plr.money >= 10:
            towers.append(CommonTower(x + cellsize / 2, y + cellsize / 2, 10, 'green', 5, 0.5, 10, 150))
            plr.money -= 10
        if n == 1 and plr.money >= 15:
            towers.append(CommonTower1(x + cellsize / 2, y + cellsize / 2, 10, 'yellow', 5, 0.5, 15, 150))
            plr.money -= 15
        if n == 3 and plr.money >= 50:
            towers.append(CommonTower2(x + cellsize / 2, y + cellsize / 2, 10, 'blue', 5, 0.5, 30, 150))
            plr.money -= 50
        if n == 2 and plr.money >= 30:
            towers.append(CommonTower3(x + cellsize / 2, y + cellsize / 2, 10, 'red', 5, 0.5, 50, 150))
            plr.money -= 30


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
    for meats in meat:
        meats.draw()


plr = Player(100)
meatcreate(100, 3, 10, 'red', 10)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                maketower(towernum)
                if getmpos()[0] >= 1361:
                    towernum = uiswtch()
    window.fill('black')
    createway()
    run()
    ui()
    pygame.display.update()
    clock.tick(fps)
pygame.quit()
