import pygame
import sys
import math
from pygame import mixer
from Board import Board

WIDTH = 600
HEIGHT = 700

RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREY = (211, 211, 211)
GREEN = (0, 255, 0)


def draw_board(board):
    for c in range(boards.column):
        for r in range(boards.row):
            pygame.draw.rect(screen, Blue, (c * Square_Size, r * Square_Size + Square_Size, Square_Size, Square_Size))
            pygame.draw.circle(screen, Black, (
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

def buttons(buttonx, buttony, buttonw, buttonh, color, msg, size,level):
    global win, current_screen,ai_level

    pos = pygame.mouse.get_pos()
    fontb = pygame.font.SysFont("arial", size)
    text = fontb.render(msg, True, BLACK)

    # draw button outline and fill
    outline = pygame.Rect(buttonx - 2, buttony - 2, buttonw + 4, buttonh + 4)
    win.fill(BLACK, outline)
    button = pygame.Rect(buttonx, buttony, buttonw, buttonh)
    win.fill(color, button)

    # draw button text
    textplace = text.get_rect(
        center=(buttonx + buttonw/2, buttony + buttonh/2))
    win.blit(text, textplace)

    if button.collidepoint(pos):  # button mouse-hover
        win.fill(GREEN, button)
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
    welcoming = font1.render("Welcome!", True, BLACK, GREY)
    wRect = welcoming.get_rect(center=(WIDTH / 2, 75))
    win.blit(welcoming, wRect)

    # draw buttons
    buttons(100, 150, 400, 100, RED, "Level : Easy", 60,1)
    buttons(100, 300, 175, 100, RED, "Level : Normal", 30,2)
    buttons(325, 300, 175, 100, RED, "Level : Hard", 30,3)
    # left, top, width, height, color, message


Blue = (0, 0, 255)
Black = (63, 35, 47)
Red = (255, 0, 0)
Yellow = (255, 255, 0)

#Initialize Pygame
pygame.init()

#Game Start
boards = Board(6, 7)

#Screen
Square_Size = 100

width = boards.column * Square_Size
height = (boards.row + 1) * Square_Size

size = (width, height)

Radius = int(Square_Size / 2 - 5)
screen = pygame.display.set_mode(size)

#Level status
game_status = True
player_status = False
level_check = True
current_screen = "main menu"

#Game status
# game_status = False
win = pygame.display.set_mode((WIDTH, HEIGHT))
win.fill(GREY)

pygame.display.set_caption("Connect Four")
Beta = pygame.image.load("Kucing.png")

#Player and AI
# turn = random.randint(PLAYER, AI)
turn = 0
ai_level = 0

#Text Font
myfont = pygame.font.SysFont("monospace", 75)

# Backgroung sound
mixer.music.load("Driftveil City.wav")
mixer.music.play(-1)
mixer.music.set_volume(0.15)

while level_check:
    if current_screen == "main menu":
        main_menu()
    elif current_screen == "blank":
        win.fill(GREY)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            level_check = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                level_check = False
                game_status = False

    pygame.display.update()

if not game_status:
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
                pygame.draw.rect(screen, Black, (0, 0, width, Square_Size))
                posx = event.pos[0]
                if turn == boards.Player:
                    pygame.draw.circle(screen, Red, (posx, int(Square_Size / 2)), Radius)

            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, Black, (0, 0, width, Square_Size))
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
                            label = myfont.render("Player 1 wins!!", True, Red)
                            screen.blit(label, (40, 10))
                            player_status = True

                        turn += 1
                        turn = turn % 2

                        boards.print_board(temp)
                        draw_board(temp)

            if turn == boards.AI and not game_status:

                # col = random.randint(0, COLUMN_COUNT-1)
                # col = pick_best_move(board, AI_PIECE)
                print(ai_level)
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
                        label = myfont.render("Player 2 wins!!", True, Yellow)
                        screen.blit(label, (40, 10))
                        player_status = True

                    boards.print_board(temp)
                    draw_board(temp)

                    turn += 1
                    turn = turn % 2

            if player_status:
                # screen.blit(Beta,(10,10))
                screen.fill(Blue)
                pygame.display.flip()
                pygame.time.wait(3000)
                game_status = True



