import pygame
import sys
import math
from pygame import mixer
from Board import Board


def draw_board(board):
    for c in range(boards.column):
        for r in range(boards.row):
            pygame.draw.rect(screen, Blue, (c * Square_Size, r * Square_Size + Square_Size, Square_Size, Square_Size))
            pygame.draw.circle(screen, Background_color, (
                int(c * Square_Size + Square_Size / 2), int(r * Square_Size + Square_Size + Square_Size / 2)), Radius)

    for c in range(boards.column):
        for r in range(boards.row):
            if board[r][c] == boards.Player_Piece:
                pygame.draw.circle(screen, Red, (
                    int(c * Square_Size + Square_Size / 2), height - int(r * Square_Size + Square_Size / 2)), Radius)
            elif board[r][c] == boards.AI_Piece:
                pygame.draw.circle(screen, Yellow, (
                    int(c * Square_Size + Square_Size / 2), height - int(r * Square_Size + Square_Size / 2)), Radius)
    pygame.display.update()


def buttons(buttonx, buttony, buttonw, buttonh, color, msg, size, level):
    global win, current_screen, ai_level

    pos = pygame.mouse.get_pos()
    fontb = pygame.font.SysFont("arial", size)
    text = fontb.render(msg, True, Black)

    # draw button outline and fill
    outline = pygame.Rect(buttonx - 2, buttony - 2, buttonw + 4, buttonh + 4)
    win.fill(Black, outline)
    button = pygame.Rect(buttonx, buttony, buttonw, buttonh)
    win.fill(color, button)

    # draw button text
    textplace = text.get_rect(
        center=(buttonx + buttonw / 2, buttony + buttonh / 2))
    win.blit(text, textplace)

    if button.collidepoint(pos):  # button mouse-hover
        win.fill(Green, button)
        win.blit(text, textplace)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:  # button pressed
                current_screen = "blank"
                if level == 1:
                    ai_level = 1
                elif level == 2:
                    ai_level = 2
                else:
                    ai_level = 3


def main_menu():
    # draw welcome message
    font1 = pygame.font.SysFont("arial", 45)
    welcoming = font1.render("Pick your level!", True, Black, Grey)
    wRect = welcoming.get_rect(center=(WIDTH / 2, 75))
    win.blit(welcoming, wRect)

    # draw buttons
    buttons(WIDTH / 3, 150, 175, 100, Red, "Level : Easy", 30, 1)
    buttons(WIDTH / 3, 300, 175, 100, Red, "Level : Normal", 30, 2)
    buttons(WIDTH / 3, 450, 175, 100, Red, "Level : Hard", 30, 3)
    # left, top, width, height, color, message


# Colors
Blue = (0, 0, 255)
Background_color = (37.5, 55, 25)
Red = (255, 0, 0)
Yellow = (255, 255, 0)
Black = (0, 0, 0)
Grey = (211, 211, 211)
Green = (0, 255, 0)

WIDTH = 600
HEIGHT = 700

# Initialize Pygame
pygame.init()

# Game Start
boards = Board(6, 7)

# Level status
game_status = True
player_status = False
level_check = True
game_over = False
current_screen = "main menu"

# Display Menu
win = pygame.display.set_mode((WIDTH, HEIGHT))
win.fill(Grey)

# Window Caption
pygame.display.set_caption("Connect Four")

# Logo
icon = pygame.image.load("logo.png")
pygame.display.set_icon(icon)

# Banner
banner = pygame.image.load("banner.png")
banner = pygame.transform.scale(banner, (450, 250))

# Player and AI
# turn = random.randint(PLAYER, AI)
turn = 0
ai_level = 0
winner = " "

# Text Font
myfont = pygame.font.SysFont("monospace", 75)

# Backgroung sound
mixer.music.load("PekoBMG.wav")
mixer.music.play(-1)
mixer.music.set_volume(0.15)

while level_check:
    if current_screen == "main menu":
        main_menu()
    elif current_screen == "blank":
        win.fill(Grey)
        win.blit(banner, (100, 150))
        font1 = pygame.font.SysFont("arial", 45)
        welcoming = font1.render("Press A to start!", True, Black, Grey)
        wRect = welcoming.get_rect(center=(WIDTH / 2, 75))
        win.blit(welcoming, wRect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            level_check = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                level_check = False
                game_status = False

    pygame.display.update()

if not game_status:
    # Screen
    Square_Size = 100

    width = boards.column * Square_Size
    height = (boards.row + 1) * Square_Size

    size = (width, height)

    Radius = int(Square_Size / 2 - 5)

    screen = pygame.display.set_mode(size)
    temp = boards.create_board()
    draw_board(temp)
    pygame.display.update()

    while not game_status:

        for event in pygame.event.get():
            # To exit the game
            if event.type == pygame.QUIT:
                sys.exit()

            # Draw the circle at the top
            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, Background_color, (0, 0, width, Square_Size))
                posx = event.pos[0]
                if turn == boards.Player:
                    pygame.draw.circle(screen, Red, (posx, int(Square_Size / 2)), Radius)

            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, Background_color, (0, 0, width, Square_Size))
                # print(event.pos)
                # Ask for Player 1 Input
                if turn == boards.Player:
                    posx = event.pos[0]
                    col = int(math.floor(posx / Square_Size))

                    if boards.check_valid_position(temp, col):
                        row = boards.get_free_row(temp, col)
                        boards.drop_piece(temp, row, col, boards.Player_Piece)
                        touch = mixer.Sound("touch.mp3")
                        touch.play()

                        if boards.win_condition(temp, boards.Player_Piece):
                            winner = "Player 1 wins!!"
                            player_status = True

                        boards.print_board(temp)
                        draw_board(temp)

                        turn += 1
                        turn = turn % 2

            if turn == boards.AI and not game_status and player_status is False:

                # col = random.randint(0, COLUMN_COUNT-1)
                # col = pick_best_move(board, AI_PIECE)
                if ai_level == 1:
                    col = boards.pick_best_move(temp, boards.AI_Piece)
                elif ai_level == 2:
                    col, minimax_score = boards.minimax(temp, 5, -math.inf, math.inf, False)
                else:
                    col, minimax_score = boards.minimax(temp, 5, -math.inf, math.inf, True)

                if boards.check_valid_position(temp, col):
                    # pygame.time.wait(500)
                    row = boards.get_free_row(temp, col)
                    boards.drop_piece(temp, row, col, boards.AI_Piece)
                    touch = mixer.Sound("touch.mp3")
                    touch.play()

                    if boards.win_condition(temp, boards.AI_Piece):
                        winner = "Player 2 wins!!"
                        player_status = True

                    boards.print_board(temp)
                    draw_board(temp)

                    turn += 1
                    turn = turn % 2

            if player_status:
                # screen.blit(Beta,(10,10))
                game_status = True
                game_over = True

if game_over:
    while game_over:
        win.fill(Grey)
        font1 = pygame.font.SysFont("arial", 30)
        welcoming = font1.render("Game Over! Please Press ESC to quit ", True, Black, Grey)
        wRect = welcoming.get_rect(center=(WIDTH / 2, 75))
        win.blit(welcoming, wRect)

        label = myfont.render(winner, True, Yellow)
        win.blit(label, (30, 150))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_over = False

        pygame.display.update()
