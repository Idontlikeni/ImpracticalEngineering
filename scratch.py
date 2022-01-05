import pygame, sys, os, random, math, time

from pygame import mouse
from pygame.locals import *
from pygame.mixer import set_num_channels

pygame.init()
pygame.display.set_caption("Yandex game")
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.set_num_channels(64)
random.seed()
clock = pygame.time.Clock()

WINDOW_SIZE = (1600, 900)
TILE_SIZE = 16
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
n = 0
m = 0
pygame.mouse.set_visible(True)
SCALE_MULTIPLIER = 5
click = False
cveta = (200, 25, 23)
cveta1 = (200, 200, 200)
cveta2 = (255, 255, 255)
cveta3 = (0, 255, 0)
usl1 = 0
usl2 = 0
uslza = 0
font = pygame.font.Font('MaredivRegular.ttf', 15)
font1 = pygame.font.Font('MaredivRegular.ttf', 25)
display = pygame.Surface((WINDOW_SIZE[0] / SCALE_MULTIPLIER, WINDOW_SIZE[1] / SCALE_MULTIPLIER))

while True:
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


    print(usl1)
    screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
    pygame.display.update()
    clock.tick(60)
