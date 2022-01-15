import pygame, math, os, random, itertools
from pygame import display
from pygame.locals import *

global e_colorkey
e_colorkey = (255, 255, 255)

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

def blitRotate(surf, image, pos, originPos, angle):
    image_rect = image.get_rect(topleft = (pos[0] - originPos[0], pos[1]-originPos[1]))
    offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center
    rotated_offset = offset_center_to_pivot.rotate(-angle)
    rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)
    rotated_image = pygame.transform.rotate(image, angle)
    rotated_image_rect = rotated_image.get_rect(center = rotated_image_center)
    surf.blit(rotated_image, rotated_image_rect)

class spritesheet(object):
    def __init__(self, filename):
        self.sheet = pygame.image.load(filename).convert()
    
    # Load a specific image from a specific rectangle
    def image_at(self, rectangle, colorkey = None):
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
        self.usable_entities = []
        self.drops = []

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
        self.enemies_count = random.randint(10, 15)
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
                self.add_enemy(Enemy(*self.to_screen_coordinates(x, y), 16, 16, 5, 'enemy'))
        
        #  print(*self.enemies_positions)

        y = 0
        for row in self.field:
            x = 0
            for tile in row:
                if tile != '0' and tile != '1':
                    self.tile_rects.append(pygame.Rect(x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size))
                x += 1
            y += 1
    
    def check_use(self, player):
        for entity in self.usable_entities:
            entity.used()

    def to_screen_coordinates(self, x, y):
        return x * self.tile_size, y * self.tile_size

    def get_start_pos(self):
        return self.to_screen_coordinates(self.start_pos[0], self.start_pos[1])

    def add_game_object(self, Object):
        self.objects.append(Object)

    def add_enemy(self, enemy):
        self.enemies.append(enemy)

    def add_usable_entity(self, entity):
        self.usable_entities.append(entity)

    def add_drop(self, drop):
        self.drops.append(drop)

    def update(self, player, dt):
        for i, enemy in sorted(enumerate(self.enemies), reverse=True):
            if enemy.dead:
                enemy.die(self)
                self.effects.append(Explosion(enemy.x + enemy.width / 2, enemy.y + enemy.height / 2))
                del enemy
                self.enemies.pop(i)
            else:
                #  print(enemy.shootTimer)
                enemy.update()
                enemy.move(enemy.movement, self.get_rects(), [])
                enemy.check_player(self.field, player)
                enemy.move_projectiles(self.get_rects(), [player], dt)
        
        for i, drop in sorted(enumerate(self.drops), reverse=True):
            drop.update(player)
            if drop.dead:
                del drop
                self.drops.pop(i)

        for i, entity in sorted(enumerate(self.usable_entities), reverse=True):
            entity.update(player)

        for i, effect in sorted(enumerate(self.effects), reverse=True):
            effect.update()
            if len(effect.particles) == 0:
                del effect
                effect.pop(i)
                self.effects.pop(i)
    
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

        for i, drop in sorted(enumerate(self.drops), reverse=True):
            drop.draw(display, scroll)
            
        for i, entity in sorted(enumerate(self.usable_entities), reverse=True):
            entity.draw(display, scroll)

        for effect in self.effects:
            effect.draw(display, scroll)

    def get_rects(self):
        return self.tile_rects

    def get_enemies_rects(self):
        rects = []
        for enemy in self.enemies:
            rects.append(enemy.physical_object.rect)
        return rects

    def get_enemies(self):
        return self.enemies

class TradeWorld(World):
    def __init__(self, width, height, tile_size):
        super().__init__(width, height, tile_size)

    def generate_map(self):
        for i in range(self.height):
            self.field[i][0] = 'x'
        for i in range(self.height):
            self.field[i][self.width - 1] = 'x'
        for i in range(self.width):
            self.field[0][i] = 'x'
        for i in range(self.width):
            self.field[self.height - 1][i] = 'x'
    
        y = 0
        for row in self.field:
            x = 0
            for tile in row:
                if tile != '0' and tile != '1':
                    self.tile_rects.append(pygame.Rect(x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size))
                x += 1
            y += 1

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
    def __init__(self, x, y, width, height, hp, type):
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
        self.hp = hp
        self.movement = [0, 0]
        self.animations_frames = {}
        self.animation_database = {}
        self.animation_database['idle'] = self.load_animations('data_img/animations/idle', [6, 6, 6, 6, 6,])
        self.action = 'idle'
        self.frame = 0
        self.is_flipped = False
        self.image = None
        self.dead = False


    def load_animations(self, path, frame_durations):
        ss = spritesheet(path + '.png')
        animation_name = path.split('/')[-1]
        animation_frame_data = []
        n = 0
        for frame in frame_durations:
            animation_frame_id = animation_name + '_' + str(n)
            animation_image = ss.image_at((n * 16, 0, 16, 16), (0, 0, 0))
            self.animations_frames[animation_frame_id] = animation_image.copy()
            for i in range(frame):
                animation_frame_data.append(animation_frame_id)
            n += 1
        return animation_frame_data

    def change_action(action_var, frame_var, new_value):
        if action_var != new_value:
            action_var = new_value
            frame = 0
        return action_var, frame


    def draw(self, surface, scroll):
        pygame.draw.rect(surface, (255, 0, 0), pygame.Rect(self.physical_object.x-scroll[0], self.physical_object.y-scroll[1],
                                                           self.physical_object.width, self.physical_object.height), 1)
        if self.image != None:
            surface.blit(self.image, (self.physical_object.x-scroll[0], self.physical_object.y-scroll[1]))
    
    def set_pos(self,x,y):
        self.x = x
        self.y = y
        self.physical_object.x = x
        self.physical_object.y = y
        self.physical_object.rect.x = x
        self.physical_object.rect.y = y

    def update(self):
        if self.hp <= 0:
            self.dead = True
        else:
            self.frame += 1
            if self.frame >= len(self.animation_database[self.action]):
                self.frame = 0
            image_id = self.animation_database[self.action][self.frame]
            self.image = self.animations_frames[image_id]
            if self.shootTimer < 50:
                self.shootTimer += 1
    
    def move(self, movement, platforms, enemies):
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
    
    def die(self, world):
        num = random.randint(0, 100)
        if num <= 40:
            world.drops.append(AmmoDrop(self.x, self.y, 7, 7))
        else:
            num = random.randint(0, 100)
            if num <= 20:
                world.drops.append(HealthDrop(self.x, self.y, 7, 7))
        

class Drop(GameObject):
    def __init__(self, x, y, width, height, path):
        super().__init__(x, y, width, height)
        self.img = pygame.image.load(path)
        self.following = False
        self.velocity = 2.5
        self.dead = False
        
    
    def update(self, player):
        x1 = player.x + player.width / 2
        y1 = player.y + player.height / 2
        x2 = self.x + self.width / 2
        y2 = self.y + self.height / 2
        dist = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

        if dist <= 5:
            self.picked_action(player)
            self.dead = True

        if dist <= 20:
            self.following = True
        
        if self.following:
            self.x += (x1 - self.x) / math.sqrt((x1 - self.x) ** 2 + (y1 - self.y) ** 2) * self.velocity
            self.y += (y1 - self.y) / math.sqrt((x1 - self.x) ** 2 + (y1 - self.y) ** 2) * self.velocity
        

    def picked_action(self, player):
        pass


    def draw(self, surface, scroll):
        pygame.draw.rect(surface, (255, 0, 0), pygame.Rect(self.x-scroll[0], self.y-scroll[1],
                                                           self.width, self.height), 1)
        if self.img != None:
            surface.blit(self.img, (self.x-scroll[0], self.y-scroll[1]))


class AmmoDrop(Drop):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, 'data_img/ammo1.png')
    

    def picked_action(self, player):
        player.ammo += 32


class HealthDrop(Drop):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, 'data_img/healt.png')\


    def picked_action(self, player):
        player.hp += 2


class UsableEntity(Entity):
    def __init__(self, x, y, width, height, hp, type):
        super().__init__(x, y, width, height, hp, type)


class Portal(Entity):
    def __init__(self, x, y, radius, type):
        super().__init__(x, y, radius * 2, radius * 2, 1, type)
        self.radius = radius
        self.can_be_used = False
        self.use_img = pygame.image.load("data_img/use_item_pic.png")
        self.angle2 = random.uniform(0, math.pi * 2)
        self.angle3 = random.uniform(0, math.pi * 2)
        self.pos2 = [math.cos(self.angle2) * 2.5, math.sin(self.angle2) * 2.5]
        self.pos3 = [math.cos(self.angle3), math.sin(self.angle3)]
        
    def update(self, player):
        self.angle2 += 0.2
        self.angle3 += 0.2
        self.pos2 = [math.cos(self.angle2) * 2.5, math.sin(self.angle2) * 2.5]
        self.pos3 = [math.cos(self.angle3), math.sin(self.angle3)]
        x1 = player.x + player.width / 2
        y1 = player.y + player.height / 2
        x2 = self.x
        y2 = self.y
        dist = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
        if dist <= player.width / 2 + self.radius:
            self.can_be_used = True
            return True
        self.can_be_used = False
        return False
        

    def draw(self, surface, scroll):
        pygame.draw.circle(surface, (128, 0, 200), (self.x - scroll[0], self.y - scroll[1]), self.radius)
        pygame.draw.circle(surface, (100, 0, 175), (self.x - scroll[0] + self.pos2[0], self.y - scroll[1] + self.pos2[1]), self.radius / 1.3)
        pygame.draw.circle(surface, (100, 0, 175), (self.x - scroll[0], self.y - scroll[1]), self.radius * 0.8, 1)
        pygame.draw.circle(surface, (100, 0, 175), (self.x - scroll[0], self.y - scroll[1]), self.radius * 0.7, 1)
        pygame.draw.circle(surface, (80, 0, 150), (self.x - scroll[0] + self.pos3[0], self.y - scroll[1] + self.pos3[1]), self.radius / 2)
        pygame.draw.circle(surface, (100, 0, 175), (self.x - scroll[0], self.y - scroll[1]), self.radius * 1, 1)
        if self.can_be_used:
            surface.blit(self.use_img, (self.x - scroll[0] - self.use_img.get_width() / 2, self.y - scroll[1] - self.radius - self.use_img.get_height()))

    def used(self):
        if self.can_be_used:
            return True
        return False
    

class Enemy(Entity):
    def __init__(self, x, y, width, height, hp, type):
        super().__init__(x, y, width, height, hp, type)
        self.can_see_player = False
        self.is_wondering = False
        self.destination_pos = [x, y]
        self.angle = 0
        self.movement = [0, 0]
        self.wonder_timer = 0
        self.velocity = 0.8
        self.wait_timer = 0
        self.is_waiting = False
        self.sees_enemy = False
        self.color = [255, 0, 0]
        self.draw_pixels = []
        self.debug = [[0, 0], [0, 0]]
        self.player_angle = 0
        self.player_dist = 0
        self.primary_weapon = RustyRifle(self.x, self.y, 0, "data_img/weapon_2.png", self)


    def wonder(self):
        pass
    
    def shoot(self, angle):
        return self.primary_weapon.shoot(angle)


    def check_player(self, map, player):
        self.draw_pixels = []
        x1 = player.x + player.width / 2
        y1 = player.y + player.height / 2
        x2 = self.x + self.width / 2
        y2 = self.y + self.height / 2
        dist = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
        if dist <= 150: # can see player
            self.player_dist = dist
            angle = math.atan2(y1 - y2, x1 - x2)
            sin_a = math.sin(angle)
            cos_a = math.cos(angle)
            self.debug = [[x2, y2], [x1, y1]]
            for depth in range(int(dist)):
                x = x2 + depth * cos_a
                y = y2 + depth * sin_a
                if map[int(y) // TILE_SIZE][int(x) // TILE_SIZE] != '0':
                    self.can_see_player = False
                    self.color = [255, 0, 0]
                    break
                self.draw_pixels.append([x, y])
            else:
                self.can_see_player = True
                self.player_angle = angle
                self.player_dist = dist
                self.color = [0, 255, 0]
        else: 
            self.color = [255, 0, 0]
            return False

                
    def update(self):
        super().update()
        self.primary_weapon.update()
        self.primary_weapon.set_pos(self.x, self.y)
        #  print(self.wait_timer)
        if self.can_see_player:
            self.shoot(random.uniform(self.player_angle - 0.7, self.player_angle + 0.7))
        if self.is_waiting:
            self.wait_timer -= 1
            self.is_waiting = self.wait_timer > 0
            self.movement = [0, 0]
        else:
            if not self.is_wondering:
                angle = 0
                dist = 0
                if self.can_see_player:
                    angle = random.uniform(self.player_angle - 0.7, self.player_angle + 0.7)
                    dist = random.randint(30, max(51, int(self.player_dist)))
                else:    
                    angle = random.uniform(0, math.pi * 2)
                    dist = random.randint(50, 170)
                self.angle = angle
                self.destination_pos = [self.x + math.cos(self.angle) * dist, self.y + math.sin(self.angle) * dist]
                #  print("new: ", math.cos(angle) * 100)
                self.is_wondering = True
                self.movement = [math.cos(self.angle) * self.velocity, math.sin(self.angle) * self.velocity]
                self.wonder_timer = int(dist * 2)
                self.wait_timer -= 1
            self.wonder_timer -= 1
            #  print("update: ", math.cos(self.angle) * 100)
            if (abs(self.x - self.destination_pos[0]) < self.width and abs(self.y - self.destination_pos[1]) < self.height) or self.wonder_timer <= 0:
                self.is_waiting = True
                self.wait_timer = random.randint(30, 160)
                self.is_wondering = False
            self.primary_weapon.set_angle(self.angle)

        
    
    def draw(self, surface, scroll):
        self.primary_weapon.draw(surface, scroll)
        pygame.draw.rect(surface, self.color, pygame.Rect(self.physical_object.x-scroll[0], self.physical_object.y-scroll[1],
                                                           self.physical_object.width, self.physical_object.height), 1)
        # pygame.draw.line(surface, self.color, (self.x - scroll[0], self.y - scroll[1]), 
        # (self.destination_pos[0] - scroll[0], self.destination_pos[1] - scroll[1]))
        # for pixel in self.draw_pixels:
        #     pygame.draw.rect(surface, (0, 255, 255), pygame.Rect(pixel[0] - scroll[0], pixel[1] - scroll[1], 1, 1))
        # pygame.draw.line(surface, (0, 0, 255), (self.debug[0][0] - scroll[0], self.debug[0][1] - scroll[1]),
        # (self.debug[1][0] - scroll[0], self.debug[1][1] - scroll[1]))

    

class Player(Entity):
    def __init__(self, x, y, width, height, hp, type):
        super().__init__(x, y, width, height, hp, type)
        self.primary_weapon = Weapon(self.x, self.y, 0, "data_img/weapon_1.png", self)
        self.ammo = 128

    
    def shoot(self, angle):
        return self.primary_weapon.shoot(angle)
        #  return super().shoot(angle)
    
    def update(self, mouse_angle):
        self.primary_weapon.update()
        self.primary_weapon.set_pos(self.x, self.y)
        self.primary_weapon.set_angle(mouse_angle)
        return super().update()

    def draw(self, surface, scroll):
        self.primary_weapon.draw(surface, scroll)
        super().draw(surface, scroll)
        
    
    def use(self):
        pass

class Weapon:
    def __init__(self, x, y, angle, path, entity):
        self.x = x
        self.y = y
        self.angle = angle
        self.img = pygame.image.load(path).convert()
        self.img.set_colorkey((0, 0, 0))
        self.entity = entity
        self.shootTimer = 10
        self.cooldown = 10
        self.img_width = self.img.get_width()

    def set_pos(self, x, y):
        self.x = x
        self.y = y
    
    def set_angle(self, angle):
        self.angle = angle

    def shoot(self, angle=None):
        if angle is None:
            angle = self.angle
        if self.shootTimer >= self.cooldown:
            projectile = Projectile(self.entity.x + self.entity.width / 2 + math.cos(angle) * self.img_width, self.entity.y + self.entity.height / 2 + math.sin(angle) * self.img_width, 8, 8, angle, 8, self.entity.type + "_projectile")
            self.entity.projectiles.append(projectile)
            self.shootTimer = 0
            return projectile
        return None
    
    def draw(self, surface, scroll):

        blitRotate(surface, self.img, (self.x - scroll[0] + self.entity.width / 2, self.y - scroll[1] + self.entity.height / 2), (0, 0), -math.degrees(self.angle))

        # copy_img = pygame.transform.rotate(self.img, -math.degrees(self.angle))
        # print(math.degrees(self.angle))
        # surface.blit(copy_img, (self.x - scroll[0], self.y - scroll[1]))

    def update(self):
        self.shootTimer += 1

class RustyRifle(Weapon):
    def __init__(self, x, y, angle, path, entity):
        super().__init__(x, y, angle, path, entity)
        self.shootTimer = 0
        self.cooldown = 60
    
    def shoot(self, angle=None):
        
        if self.shootTimer >= self.cooldown:
            if angle is None:
                angle = self.angle
            else:
                self.angle = angle
            projectile = Projectile(self.entity.x + self.entity.width / 2 + math.cos(angle) * self.img_width, self.entity.y + self.entity.height / 2 + math.sin(angle) * self.img_width, 8, 8, angle, 2, self.entity.type + "_projectile")
            self.entity.projectiles.append(projectile)
            self.shootTimer = 0
            self.cooldown = random.randint(60, 180)
            return projectile
        return None

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
        super().__init__(x, y, width, height, 1, type)
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

class EnemyProjectiles(Projectile):
    def __init__(self):
        pass

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


    def draw(self, display, scroll):
        #  display.set_colorkey((0,0,0))
        #  pygame.draw.circle(display, (241, 100, 31, 255), [int(self.x), int(self.y)], int(self.time * 2))
        pygame.draw.line(display, (255, 255, 255), (self.x - scroll[0], self.y - scroll[1]), 
        (self.length * math.cos(self.angle) + self.x - scroll[0], self.length * math.sin(self.angle) + self.y - scroll[1]) , self.width)

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
            

    def draw(self, display, scroll):
        for particle in self.particles:
            particle.draw(display, scroll)