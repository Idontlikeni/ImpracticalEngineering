import pygame, math, os, random, itertools
from pygame.locals import *

global e_colorkey
e_colorkey = (255,255,255)

TILE_SIZE = 20

def set_global_colorkey(colorkey):
    global e_colorkey
    e_colorkey = colorkey

def collision_test(object_1,object_list):
    collision_list = []
    for obj in object_list:
        if obj.colliderect(object_1):
            collision_list.append(obj)
    return collision_list

def object_collision_test(object_1,object_list):
    collision_list = []
    for obj in object_list:
        if obj.physical_object.rect.colliderect(object_1):
            collision_list.append(obj)
    return collision_list

def circle_surf(radius, color):
    surf = pygame.Surface((radius * 2, radius * 2))
    pygame.draw.circle(surf, color, (radius, radius), radius)
    surf.set_colorkey((0, 0, 0))
    return surf

class spritesheet(object):
    def __init__(self, filename):
        self.sheet = pygame.image.load(filename).convert()
    
    # Load a specific image from a specific rectangle
    def image_at(self, rectangle, colorkey = None):
        "Loads image from x,y,x+offset,y+offset"
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image
    
    # Load a whole bunch of images and return them as a list
    def images_at(self, rects, colorkey = None):
        "Loads multiple images, supply a list of coordinates" 
        return [self.image_at(rect, colorkey) for rect in rects]
    
    # Load a whole strip of images
    def load_strip(self, rect, image_count, colorkey = None):
        "Loads a strip of images and returns them as a list"
        tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, colorkey)

class World:  #  ZA WARUDOOOOOO
    def __init__(self, width, height, tile_size):
        self.width = width
        self.height = height
        self.objects = []
        self.field = [['1'] * width for _ in range(height)]
        self.tile_rects = []
        self.projectiles = []
        self.enemies = []
        self.start_pos = []
        self.enemies_positions = []
        self.chest_positions = []
        self.enemies_count = 0
        self.effects = []
        self.tile_size = tile_size

        ss1 = spritesheet('data_img/spritesheet_3.png')
        ss2 = spritesheet('data_img/spritesheet_4.png')
        self.img = pygame.image.load('data_img/wall_2.png')
        self.images1 = []
        self.images2 = []
        for i in range(3):
            for j in range(3):
                self.images1.append(ss1.image_at((j * 20, i * 20, 20, 20), (0, 0, 0)))
        for i in range(6):
            self.images2.append(ss2.image_at((i * 20, 40, 20, 20), (0, 0, 0)))
        for i in range(5):
            self.images2.append(ss2.image_at((40, i * 20, 20, 20), (0, 0, 0)))
        

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
        self.enemies_count = random.randint(10, 25)
        #  print(self.enemies_count, numer_of_cells)

        for i in range(self.enemies_count):
            self.enemies_positions.append(random.randint(0, numer_of_cells - 1))

        x, y = random.randint(1, self.width - 2), random.randint(1, self.height - 2)
        self.field[y][x] = '0'
        self.start_pos = [x, y]
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
            if i in self.enemies_positions:
                self.enemies_positions.append([x, y])
                self.add_enemy(Entity(*self.to_screen_coordinates(x, y), 16, 16, 'enemy'))
        
        #  print(*self.enemies_positions)

        y = 0
        for row in self.field:
            x = 0
            for tile in row:
                if tile != '0' and tile != '1':
                    self.tile_rects.append(pygame.Rect(x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size))
                x += 1
            y += 1
    
    def to_screen_coordinates(self, x, y):
        return x * self.tile_size, y * self.tile_size

    def get_start_pos(self):
        return self.to_screen_coordinates(self.start_pos[0], self.start_pos[1])

    def add_game_object(self, Object):
        self.objects.append(Object)

    def add_enemy(self, enemy):
        self.enemies.append(enemy)

    def update(self, player, dt):
        for i, enemy in sorted(enumerate(self.enemies), reverse=True):
            if enemy.hp <= 0:
                del enemy
                self.enemies.pop(i)
            else:
                #  print(enemy.shootTimer)
                enemy.update()
                enemy.shoot(0)
                enemy.move_projectiles(self.get_rects(), [player], dt)
        
        for i, effect in sorted(enumerate(self.effects), reverse=True):
            effect.update()
            if len(effect.particles) == 0:
                del effect
                effect.pop(i)
    
    def draw(self, display, scroll):
        for y in range(len(self.field)):
            for x in range(len(self.field[y])):
                if self.field[y][x] == '1':
                    pygame.draw.rect(display, (207, 117, 43), pygame.Rect((x * self.tile_size - scroll[0], y * self.tile_size - scroll[1]), (self.tile_size, self.tile_size)))
                    #  display.blit(dirt_image, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                if self.field[y][x] == '2':
                    # if self.field[y + 1][x] == '0':
                    #     pygame.draw.rect(display, (255, 255, 0), pygame.Rect((x * self.tile_size - scroll[0], y * self.tile_size - scroll[1]), (self.tile_size, self.tile_size)), 1)
                    if self.field[y + 1][x] == '0' and self.field[y - 1][x] != '0' and self.field[y][x + 1] != '0' and self.field[y][x - 1] != '0':
                        display.blit(self.images1[7], (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                    elif self.field[y + 1][x] == '0' and self.field[y - 1][x] != '0' and self.field[y][x + 1] == '0' and self.field[y][x - 1] != '0':
                        display.blit(self.images1[8], (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                    elif self.field[y + 1][x] == '0' and self.field[y - 1][x] != '0' and self.field[y][x + 1] != '0' and self.field[y][x - 1] == '0':
                        display.blit(self.images1[6], (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                    elif self.field[y + 1][x] != '0' and self.field[y - 1][x] != '0' and self.field[y][x + 1] == '0' and self.field[y][x - 1] != '0':
                        display.blit(self.images1[5], (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                    elif self.field[y + 1][x] != '0' and self.field[y - 1][x] != '0' and self.field[y][x + 1] != '0' and self.field[y][x - 1] == '0':
                        display.blit(self.images1[3], (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                    elif self.field[y + 1][x] != '0' and self.field[y - 1][x] == '0' and self.field[y][x + 1] == '0' and self.field[y][x - 1] != '0':
                        display.blit(self.images1[2], (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                    elif self.field[y + 1][x] != '0' and self.field[y - 1][x] == '0' and self.field[y][x + 1] != '0' and self.field[y][x - 1] != '0':
                        display.blit(self.images1[1], (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                    elif self.field[y + 1][x] != '0' and self.field[y - 1][x] == '0' and self.field[y][x + 1] != '0' and self.field[y][x - 1] == '0':
                        display.blit(self.images1[0], (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                    elif self.field[y + 1][x] == '0' and self.field[y - 1][x] == '0' and self.field[y][x + 1] != '0' and self.field[y][x - 1] == '0':
                        display.blit(self.images2[0], (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                    elif self.field[y + 1][x] == '0' and self.field[y - 1][x] == '0' and self.field[y][x + 1] != '0' and self.field[y][x - 1] != '0':
                        display.blit(self.images2[1], (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                    elif self.field[y + 1][x] == '0' and self.field[y - 1][x] == '0' and self.field[y][x + 1] == '0' and self.field[y][x - 1] != '0':
                        display.blit(self.images2[4], (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                    elif self.field[y + 1][x] == '0' and self.field[y - 1][x] == '0' and self.field[y][x + 1] == '0' and self.field[y][x - 1] == '0':
                        display.blit(self.images2[5], (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                    elif self.field[y + 1][x] != '0' and self.field[y - 1][x] == '0' and self.field[y][x + 1] == '0' and self.field[y][x - 1] == '0':
                        display.blit(self.images2[6], (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                    elif self.field[y + 1][x] != '0' and self.field[y - 1][x] != '0' and self.field[y][x + 1] == '0' and self.field[y][x - 1] == '0':
                        display.blit(self.images2[7], (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                    elif self.field[y + 1][x] == '0' and self.field[y - 1][x] != '0' and self.field[y][x + 1] == '0' and self.field[y][x - 1] == '0':
                        display.blit(self.images2[10], (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                    else:
                        pygame.draw.rect(display, (207, 117, 43), pygame.Rect((x * self.tile_size - scroll[0], y * self.tile_size - scroll[1]), (self.tile_size, self.tile_size)))
                if self.field[y][x] == 'x':
                    pygame.draw.rect(display, (255, 0, 0), pygame.Rect((x * self.tile_size - scroll[0], y * self.tile_size - scroll[1]), (self.tile_size, self.tile_size)), 1)
        # y = 0
        # for row in self.field:
        #     x = 0
        #     for tile in row:
        #         if tile == '1':
        #             pygame.draw.rect(display, (255, 255, 255), pygame.Rect((x * self.tile_size - scroll[0], y * self.tile_size - scroll[1]), (self.tile_size, self.tile_size)), 1)
        #             #  display.blit(dirt_image, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
        #         if tile == '2':
        #             pygame.draw.rect(display, (0, 255, 0), pygame.Rect((x * self.tile_size - scroll[0], y * self.tile_size - scroll[1]), (self.tile_size, self.tile_size)), 1)
        #             if(self.field[y + 1][x + 1] == '0'):
        #                 pygame.draw.rect(display, (255, 255, 0), pygame.Rect((x * self.tile_size - scroll[0], y * self.tile_size - scroll[1]), (self.tile_size, self.tile_size)), 1)
        #         if tile == 'x':
        #             pygame.draw.rect(display, (255, 0, 0), pygame.Rect((x * self.tile_size - scroll[0], y * self.tile_size - scroll[1]), (self.tile_size, self.tile_size)), 1)
        #         x += 1
        #     y += 1
        
        for enemy in self.enemies:
            enemy.draw(display, scroll)
            enemy.draw_projectiles(display, scroll)
        for effect in self.effects:
            effect.draw(display)

    def get_rects(self):
        return self.tile_rects

    def get_enemies_rects(self):
        rects = []
        for enemy in self.enemies:
            rects.append(enemy.physical_object.rect)
        return rects

    def get_enemies(self):
        return self.enemies


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

    def move(self,movement,platforms,enemies=[]):
        enemies_rects = []
        for enemy in enemies:
            enemies_rects.append(enemy.physical_object.rect)
        
        self.x += movement[0]
        self.rect.x = int(self.x)
        block_hit_list = collision_test(self.rect, platforms)
        enemies_hit_list = object_collision_test(self.rect, enemies) #  Сода надо добавить возможность управлять id
        collision_types = {'top':False,'bottom':False,'right':False,'left':False,'slant_bottom':False,'data':[],'enemies':[],'projectiles':[]}
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
        
        for enemy in enemies_hit_list:
            markers = [False,False,False,False]
            if movement[0] > 0:
                self.rect.right = enemy.physical_object.rect.left
                collision_types['right'] = True
                markers[0] = True
            elif movement[0] < 0:
                self.rect.left = enemy.physical_object.rect.right
                collision_types['left'] = True
                markers[1] = True
            collision_types['data'].append([enemy,markers])
            if enemy.type == 'projectile':
                collision_types['projectiles'].append(enemy)
            else:
                collision_types['enemies'].append(enemy)
            self.x = self.rect.x
        # Y-collisions -------------------------------------------------
        self.y += movement[1]
        self.rect.y = int(self.y)
        block_hit_list = collision_test(self.rect, platforms)
        enemies_hit_list = object_collision_test(self.rect, enemies)
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

        for enemy in enemies_hit_list:
            markers = [False,False,False,False]
            if movement[1] > 0:
                self.rect.bottom = enemy.physical_object.rect.top
                collision_types['bottom'] = True
                markers[2] = True
            elif movement[1] < 0:
                self.rect.top = enemy.physical_object.rect.bottom
                collision_types['top'] = True
                markers[3] = True
            collision_types['data'].append([enemy,markers])
            if enemy.type == 'projectile':
                collision_types['projectiles'].append(enemy)
            else:
                collision_types['enemies'].append(enemy)
            self.change_y = 0
            self.y = self.rect.y
        return collision_types

class Entity(GameObject):
    id_iter = itertools.count()
    def __init__(self, x, y, width, height, type):
        self.id = next(self.id_iter)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.type = type
        self.physical_object = PhysicalObject(x, y, width, height)
        self.projectiles = []
        self.shootTimer = 50
        self.id += 1
        self.hp = 10

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
    
    def move(self,movement,platforms, enemies):
        collisions = self.physical_object.move(movement,platforms, enemies)
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
            return projectile
        return None
    
    def draw_projectiles(self, surface, scroll):
        for projectile in self.projectiles:
            projectile.draw(surface, scroll)

    def move_projectiles(self, platforms, enemies, dt):
        for count, projectile in enumerate(self.projectiles):
            collisions = projectile.move(platforms, enemies, dt)
            #  print(collisions)
            
            if len(collisions['data']) > 0:
                #  print(self, collisions['data'][0])
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
        self.type = 'projectile'

    def move(self, platforms, enemies, dt):
        movement = [math.cos(self.angle) * self.velocity * dt, math.sin(self.angle) * self.velocity * dt]
        collisions = self.physical_object.move(movement,platforms,enemies)
        self.x = self.physical_object.x
        self.y = self.physical_object.y
        if len(collisions['enemies']) > 0:
            #  print(collisions)
            for enemy in collisions['enemies']:
                enemy.hp -= 1
        if len(collisions) > 0:
            del self
        return collisions

    def set_move_angle(self, angle):
        self.angle = angle


class Particle:
    def __init__(self, x, y, velocity, time, scroll):
        self.x = x
        self.y = y
        self.velocity = velocity
        self.time = time
        self.spent_time = 0
        self.scroll = scroll

    def __init__(self, x, y, scroll):
        self.x = x
        self.y = y
        self.scroll = scroll
        self.velocity = [random.randint(0, 20) / 10 - 1, random.randint(0, 20) / 10 - 1]
        self.time = random.randint(1, 3)
        self.spent_time = 0
        self.color = (random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))
        
    def update(self):
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        self.time -= 0.05
        self.spent_time += 0.1

    def draw(self, display, scroll):
        #  display.set_colorkey((0,0,0))
        #  pygame.draw.circle(display, (241, 100, 31, 255), [int(self.x), int(self.y)], int(self.time * 2))
        radius = self.time * 2
        display.blit(circle_surf(radius, (31, 100, 241)), 
        [int(self.x - radius - scroll[0] + self.scroll[0]), int(self.y - radius - scroll[1] + self.scroll[1])], special_flags=BLEND_RGB_ADD)
        
        pygame.draw.circle(display, (255, 255, 255), 
        [int(self.x - scroll[0] + self.scroll[0]), int(self.y - scroll[1] + self.scroll[1])], int(self.time))

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