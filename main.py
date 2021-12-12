import pygame, sys, os, random
import engine as e
from pygame.locals import *
from pygame.mixer import set_num_channels

pygame.init()
pygame.display.set_caption("Yandex game")
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer,set_num_channels(64)
clock = pygame.time.Clock()

WINDOW_SIZE = (1920, 1080)
TILE_SIZE = 16
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)

moving_right = False
moving_left = False
moving_up = False
moving_down = False


true_scroll = [0,0]
scroll = [0, 0]
display = pygame.Surface((480, 270))
world = e.World()

player = e.Entity(0,0,16,16,'player')


while True:
    display.fill((0, 0, 0))

    true_scroll[0] += (player.x - true_scroll[0] - 480 / 2 + 8) / 20
    true_scroll[1] += (player.y -true_scroll[1] - 270 / 2 + 8) / 20
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    #  scroll = [0, 0]

    world.draw()

    player.draw(display,scroll)

    #  player.move(player_movement)
    pygame.draw.line(display, (0, 255, 0), (player.x + 8 - scroll[0], player.y + 8 - scroll[1]), ((pygame.mouse.get_pos()[0] // 4), (pygame.mouse.get_pos()[1] // 4)))
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
        
    
    world.update()
    screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
    pygame.display.update()
    clock.tick(60)