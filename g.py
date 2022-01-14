import pygame

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Движущийся круг 2')
    size = width, height = 300, 400
    screen = pygame.display.set_mode(size)
    usl = 0
    V = 0
    n = 0
    sveta1 = (0, 0, 0)
    running = True
    sveta = (255, 255, 255)
    x_pos = 0
    v = 20  # пикселей в секунду
    ghj = 0
    clock = pygame.time.Clock()
    flag = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEMOTION:
                pos = event.pos
                flag = True
            if flag == True:
                if int(event.pos[0]) >= 20 and int(event.pos[0]) <= 250 and int(event.pos[1]) >= 20 and int(event.pos[1]) <= 75:
                    V = 1
                if int(event.pos[0]) < 20 or int(event.pos[0]) > 250 or int(event.pos[1]) < 20 or int(event.pos[1]) > 75:
                    V = 0
                    print("1")
            if V == 1:
                sveta = (255, 255, 0)
                sveta1 = (200, 0, 0)
            if V == 0:
                sveta = (255, 255, 255)
                sveta1 = (0, 0, 0)
            pygame.draw.rect(screen, sveta, (25, 20, 250, 50))
            font = pygame.font.Font('MaredivRegular.ttf', 30)
            text = font.render("play", True, sveta1)
            screen.blit(text, (100, 20))
            pygame.display.flip()
