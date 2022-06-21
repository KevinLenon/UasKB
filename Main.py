import pygame

def player():
    screen.blit(playerImg,(playerX,playerY))

pygame.init()
mainClock = pygame.time.Clock()

#Window Maker
screen = pygame.display .set_mode((1000,800))

#Background
background = pygame.image.load("pk.png")

#Title and Icon
pygame.display.set_caption("TheLastWillLose")
icon = pygame.image.load("kucing.png")
pygame.display.set_icon(icon)

#Player
playerImg = pygame.image.load("gundam.png")
playerImg = pygame.transform.scale(playerImg,(50,50))
playerX = 750
playerY = 480

#Mouse
offset = [0, 0]

clicking = False
right_clicking = False
middle_click = False

#Game loop
running = True
while running:
    screen.fill((0,0,0))

    # Input move
    mx, my = pygame.mouse.get_pos()

    rot = 0
    loc = [mx, my]
    if clicking:
        rot -= 90
    if right_clicking:
        rot += 180
    if middle_click:
        rot += 90
    screen.blit(playerImg, (playerX, playerY))
    # screen.blit(pygame.transform.rotate(playerImg, rot), (loc[0] + offset[0], loc[1] + offset[1]))

    # Buttons ------------------------------------------------ #
    right_clicking = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                clicking = True
            if event.button == 3:
                right_clicking = True
            if event.button == 2:
                middle_click = not middle_click
            if event.button == 4:
                offset[1] -= 10
            if event.button == 5:
                offset[1] += 10
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                clicking = False


    # player()
    pygame.display.update()
    mainClock.tick(60)