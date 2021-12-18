import pygame, sys, os, random, math

from pygame import mouse
import engine as e
from pygame.locals import *
from pygame.mixer import set_num_channels

pygame.init()
pygame.display.set_caption("Yandex game")
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer,set_num_channels(64)
random.seed()
clock = pygame.time.Clock()

WINDOW_SIZE = (1600, 900)
TILE_SIZE = 16
SCALE_MULTIPLIER = 5

screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
clicked = False

pygame.mouse.set_visible(False)

moving_right = False
moving_left = False
moving_up = False
moving_down = False

true_scroll = [0,0]
scroll = [0, 0]

display = pygame.Surface((WINDOW_SIZE[0] / SCALE_MULTIPLIER, WINDOW_SIZE[1] / SCALE_MULTIPLIER))
world = e.World(48, 48)
player = e.Entity(0,0,16,16,'player')
cursor = e.Cursor(0, 0, 'data_img/curs3.png')
world.generate_map()

while True:
    display.fill((0, 0, 0))
    mouse_pos = pygame.mouse.get_pos()
    cursor.set_pos(mouse_pos[0] / SCALE_MULTIPLIER, mouse_pos[1] / SCALE_MULTIPLIER)
    true_scroll[0] += (player.x - true_scroll[0] - display.get_width() / 2 + 8) / 10
    true_scroll[1] += (player.y - true_scroll[1] - display.get_height() / 2 + 8) / 10
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])
    mouse_angle = math.atan2(mouse_pos[1] / SCALE_MULTIPLIER - player.y - player.height / 2 + scroll[1], mouse_pos[0] / SCALE_MULTIPLIER - player.x - player.width / 2 + scroll[0])

    #  scroll = [0, 0]

    tile_rects = world.get_rects()

    world.draw(display, scroll)

    player_movement = [0, 0]

    if moving_right:
        player_movement[0] += 2
    if moving_left:
        player_movement[0] -= 2
    if moving_up:
        player_movement[1] -= 2
    if moving_down:
        player_movement[1] += 2
    if clicked == True:
        player.shoot(mouse_angle)
    
    collision_types = player.move(player_movement,tile_rects)

    player.move_projectiles(tile_rects)
    player.update()
    player.draw(display,scroll)

    player.draw_projectiles(display, scroll)

    #  player.move(player_movement)
    pygame.draw.line(display, (0, 255, 0), (player.x + player.width / 2 - scroll[0], player.y + player.height / 2 - scroll[1]), ((pygame.mouse.get_pos()[0] // SCALE_MULTIPLIER), (pygame.mouse.get_pos()[1] // SCALE_MULTIPLIER)))
    
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
        if event.type == KEYUP:
            if event.key == K_d:
                moving_right = False
            if event.key == K_a:
                moving_left = False
            if event.key == K_w:
                moving_up = False
            if event.key == K_s:
                moving_down = False
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                #  print(math.atan2(mouse_pos[1] / SCALE_MULTIPLIER - player.y, mouse_pos[0] / SCALE_MULTIPLIER - player.x))
                clicked = True
        if event.type == MOUSEBUTTONUP:
            if event.button == 1:
                clicked = False

                
    world.update()
    screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
    pygame.display.update()
    clock.tick(60)