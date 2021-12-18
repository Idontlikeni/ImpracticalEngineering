import pygame, math, os, random
from pygame.locals import *

global e_colorkey
e_colorkey = (255,255,255)

def set_global_colorkey(colorkey):
    global e_colorkey
    e_colorkey = colorkey

def collision_test(object_1,object_list):
    collision_list = []
    for obj in object_list:
        if obj.colliderect(object_1):
            collision_list.append(obj)
    return collision_list

TILE_SIZE = 20

class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.objects = []
        self.field = [['1'] * width for _ in range(height)]
        self.tile_rects = []

    def generate_map(self):
        for i in range(self.height):
            self.field[i][0] = 'x'
        for i in range(self.height):
            self.field[i][self.width - 1] = 'x'
        for i in range(self.width):
            self.field[0][i] = 'x'
        for i in range(self.width):
            self.field[self.height - 1][i] = 'x'
        
        numer_of_cells = random.randint(self.width * self.height, self.width * self.height * 2)

        x, y = random.randint(1, self.width - 2), random.randint(1, self.height - 2)
        self.field[y][x] = '0'
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)] 

        for i in range(numer_of_cells):
            vec = directions[random.randint(0, 3)]
            if self.field[y + vec[1]][x + vec[0]] == 'x':
                for v in directions:
                    if self.field[y + v[1]][x + v[0]] == '1' or self.field[y + v[1]][x + v[0]] == '2':
                        self.field[y + v[1]][x + v[0]] = '0'
                        y += v[1]
                        x += v[0]
            else:
                self.field[y + vec[1]][x + vec[0]] = '0'
                y += vec[1]
                x += vec[0]
            for v in directions:
                if self.field[y + v[1]][x + v[0]] == '1':
                    self.field[y + v[1]][x + v[0]] = '2'
        
        y = 0
        for row in self.field:
            x = 0
            for tile in row:
                if tile != '0' and tile != '1':
                    self.tile_rects.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                x += 1
            y += 1
        
    def add_game_object(self, Object):
        self.objects.append(Object)

    def update(self):
        for object in self.objects:
            object.update()
    
    def draw(self, display, scroll):
        y = 0
        for row in self.field:
            x = 0
            for tile in row:
                if tile == '1':
                    pygame.draw.rect(display, (255, 255, 255), pygame.Rect((x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]), (TILE_SIZE, TILE_SIZE)), 1)
                    #  display.blit(dirt_image, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                if tile == '2':
                    pygame.draw.rect(display, (0, 255, 0), pygame.Rect((x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]), (TILE_SIZE, TILE_SIZE)), 1)
                if tile == 'x':
                    pygame.draw.rect(display, (255, 0, 0), pygame.Rect((x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]), (TILE_SIZE, TILE_SIZE)), 1)
                x += 1
            y += 1

    def get_rects(self):
        return self.tile_rects

class GameObject:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
    
    def draw(self, display, scroll, is_debug=False):
        if is_debug:
            pygame.draw.rect(display, (255, 0, 0), self.rect, 1)
    
    def set_position(self, x, y):
        self.x, self.y = x, y

class PhysicalObject(GameObject):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)

    def move(self,movement,platforms):
        self.x += movement[0]
        self.rect.x = int(self.x)
        block_hit_list = collision_test(self.rect, platforms)
        collision_types = {'top':False,'bottom':False,'right':False,'left':False,'slant_bottom':False,'data':[]}
        # added collision data to "collision_types". ignore the poorly chosen variable name
        for block in block_hit_list:
            markers = [False,False,False,False]
            if movement[0] > 0:
                self.rect.right = block.left
                collision_types['right'] = True
                markers[0] = True
            elif movement[0] < 0:
                self.rect.left = block.right
                collision_types['left'] = True
                markers[1] = True
            collision_types['data'].append([block,markers])
            self.x = self.rect.x
        # Y-collisions -------------------------------------------------
        self.y += movement[1]
        self.rect.y = int(self.y)
        block_hit_list = collision_test(self.rect,platforms)
        for block in block_hit_list:
            markers = [False,False,False,False]
            if movement[1] > 0:
                self.rect.bottom = block.top
                collision_types['bottom'] = True
                markers[2] = True
            elif movement[1] < 0:
                self.rect.top = block.bottom
                collision_types['top'] = True
                markers[3] = True
            collision_types['data'].append([block,markers])
            self.change_y = 0
            self.y = self.rect.y
        return collision_types

class Entity(GameObject):
    def __init__(self, x, y, width, height, type):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.type = type
        self.physical_object = PhysicalObject(x, y, width, height)
        self.projectiles = []
        self.shootTimer = 50

    def draw(self, surface, scroll):
        pygame.draw.rect(surface, (255, 0, 0), pygame.Rect(self.physical_object.x-scroll[0], self.physical_object.y-scroll[1],
                                                           self.physical_object.width, self.physical_object.height), 1)
    
    def set_pos(self,x,y):
        self.x = x
        self.y = y
        self.physical_object.x = x
        self.physical_object.y = y
        self.physical_object.rect.x = x
        self.physical_object.rect.y = y

    def update(self):
        if self.shootTimer < 50:
            self.shootTimer += 1
    
    def move(self,movement,platforms):
        collisions = self.physical_object.move(movement,platforms)
        self.x = self.physical_object.x
        self.y = self.physical_object.y
        return collisions
 
    def rect(self):
        return pygame.Rect(self.x,self.y,self.width,self.height)

    def shoot(self, angle):
        if self.shootTimer >= 50:
            projectile = Projectile(self.x + self.width / 2 - 4, self.y + self.height / 2 - 4, 8, 8, angle, 5, "player_projectile")
            self.projectiles.append(projectile)
            self.shootTimer = 0
    
    def draw_projectiles(self, surface, scroll):
        for projectile in self.projectiles:
            projectile.draw(surface, scroll)

    def move_projectiles(self, platforms):
        for count, projectile in enumerate(self.projectiles):
            collisions = projectile.move(platforms)
            print(collisions)
            if len(collisions['data']) > 0:
                self.projectiles.remove(projectile)


class Player(Entity):
    def __init__(self, x, y, width, height, type):
        super().__init__(x, y, width, height, type)

class Cursor(GameObject):
    def __init__(self, x, y, path):
        self.x = x
        self.y = y
        self.img = pygame.image.load(path)
        self.width = self.img.get_width()
        self.height = self.img.get_height()

    def set_pos(self, x, y):
        self.x = x
        self.y = y

    def draw(self, display):
        display.blit(self.img, (self.x - self.width // 2, self.y - self.height // 2))

class Projectile(Entity):
    def __init__(self, x, y, width, height, angle, velocity, type):
        super().__init__(x, y, width, height, type)
        self.angle = angle
        self.velocity = velocity

    def move(self, platforms):
        movement = [math.cos(self.angle) * self.velocity, math.sin(self.angle) * self.velocity]
        collisions = self.physical_object.move(movement,platforms)
        self.x = self.physical_object.x
        self.y = self.physical_object.y
        if len(collisions) > 0:
            del self
        return collisions

    def set_move_angle(self, angle):
        self.angle = angle