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
countx = 34

def fullscrn(display):
    global flscr
    if flscr:
        display = pygame.display.set_mode(WINDOW_SIZE)
    else:
        display = pygame.display.set_mode(WINDOW_SIZE, pygame.FULLSCREEN)
    flscr = not flscr

def main_menu():
    pygame.mouse.set_visible(True)
    SCALE_MULTIPLIER = 5
    click = False
    cveta1 = (0, 255, 0)
    cveta2 = (255, 255, 255)
    cveta3 = (0, 255, 0)
    font = pygame.font.Font('MaredivRegular.ttf', 15)
    display = pygame.Surface((WINDOW_SIZE[0] / SCALE_MULTIPLIER, WINDOW_SIZE[1] / SCALE_MULTIPLIER))
    while True:
        display.fill((0, 0, 0))
        mx, my = pygame.mouse.get_pos()
        button_1 = pygame.Rect(WINDOW_SIZE[0] / SCALE_MULTIPLIER / 2 - 50, 50, 100, 25)
        button_2 = pygame.Rect(WINDOW_SIZE[0] / SCALE_MULTIPLIER / 2 - 50, 100, 100, 25)
        mx = mx / SCALE_MULTIPLIER
        my = my / SCALE_MULTIPLIER
        if button_1.collidepoint((mx, my)):
            cveta = (200, 25, 23)
            cveta1 = (255, 128, 0)
            if click:
                trade_area()
        else:
            cveta = (255, 255, 255)
            cveta1 = (0, 255, 0)
        if button_2.collidepoint((mx, my)):
            cveta2 = (200, 25, 23)
            cveta3 = (255, 128, 0)
            if click:
                options()
        else:
            cveta2 = (255, 255, 255)
            cveta3 = (0, 255, 0)
        pygame.draw.rect(display, cveta, button_1)
        pygame.draw.rect(display, (cveta2), button_2)
        text = font.render("play", True, (cveta1))
        display.blit(text, (WINDOW_SIZE[0] / SCALE_MULTIPLIER / 2 - 15, 50))

        text = font.render("options", True, (cveta3))
        display.blit(text, (WINDOW_SIZE[0] / SCALE_MULTIPLIER / 2 - 25, 100))
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

        screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
        pygame.display.update()
        clock.tick(60)

def towerDefense():
    pass


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
                towerDefense()

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

        collision_types = player.move(player_movement, tile_rects, [])

        player.move_projectiles(world, world.get_enemies(), dt)
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
        
        if player_movement[0] != 0 or player_movement[1] != 0:
            if player_movement[0] > 0:
                player.is_flipped = False
            if player_movement[0] < 0:
                player.is_flipped = True
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
