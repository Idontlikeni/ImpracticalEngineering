import pygame, math, os
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

class World:
    def __init__(self):
        self.objects = []
        self.field = [[0] * 15 for _ in range(15)]

    def generate_map(self):
        for i in range(15):
            self.field[i][0] = 1
        for i in range(15):
            self.field[i][14] = 1
        for i in range(15):
            self.field[0][i] = 1
        for i in range(15):
            self.field[14][i] = 1

    def add_gameobject(self, Object):
        self.objects.append(Object)

    def update(self):
        for object in self.objects:
            object.update()
    
    def draw(self):
        pass

class GameObject:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
    
    def draw(self, is_debug=False):
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

    def draw(self, surface, scroll):
        pygame.draw.rect(surface, (255, 0, 0), pygame.Rect(self.physical_object.x-scroll[0], self.physical_object.y-scroll[1],
                                                           self.physical_object.width, self.physical_object.height), 1)
