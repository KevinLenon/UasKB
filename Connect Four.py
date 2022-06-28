import pygame
import sys
import math
import random
from pygame import mixer
from Board import Board


def play_BGM(choice):
    touch = mixer.Sound("touch.mp3")
    if choice == 1:
        touch = mixer.Sound("touch.mp3")
    elif choice == 2:
        touch = mixer.Sound("drop.wav")
    elif choice == 3:
        touch = mixer.Sound("win.wav")

    touch.play()


def draw_board(board):
    for i in range(boards.column):
        for j in range(boards.row):
            screen.blit(beta, (i * Board_Size, j * Board_Size + Board_Size, Board_Size, Board_Size))
            # pygame.draw.rect(screen, Blue, (i * Board_Size, j * Board_Size + Board_Size, Board_Size, Board_Size))
            pygame.draw.circle(screen, Background_color, (
                int(i * Board_Size + Board_Size / 2), int(j * Board_Size + Board_Size + Board_Size / 2)), Radius)

    for i in range(boards.column):
        for j in range(boards.row):
            if board[j][i] == boards.Player_Piece:
                pygame.draw.circle(screen, Red, (
                    int(i * Board_Size + Board_Size / 2), height - int(j * Board_Size + Board_Size / 2)), Radius)
            elif board[j][i] == boards.AI_Piece:
                pygame.draw.circle(screen, Yellow, (
                    int(i * Board_Size + Board_Size / 2), height - int(j * Board_Size + Board_Size / 2)), Radius)
    pygame.display.update()


def buttons(xpos, ypos, width, hight, color, msg, size, level):
    global win, current_screen, ai_level, game_over, game_start_again

    pos = pygame.mouse.get_pos()
    fontb = pygame.font.SysFont("javanesetext", size)
    text = fontb.render(msg, True, Black)

    # draw button outline and fill
    outline = pygame.Rect(xpos - 2, ypos - 2, width + 4, hight + 4)
    win.fill(Black, outline)
    button = pygame.Rect(xpos, ypos, width, hight)
    win.fill(color, button)

    # draw button text
    textplace = text.get_rect(center=(xpos + width / 2, ypos + hight / 2))
    win.blit(text, textplace)

    if button.collidepoint(pos):  # button mouse-hover
        win.fill(Green, button)
        win.blit(text, textplace)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:  # button pressed
                play_BGM(1)
                current_screen = "loading"
                if level == 1:
                    ai_level = 1
                if level == 2:
                    ai_level = 2
                if level == 3:
                    ai_level = 3
                if level == 4:
                    game_over = False
                    game_start_again = True
                if level == 5:
                    game_over = False


def main_menu():
    # draw welcome message
    font = pygame.font.SysFont("javanesetext", 38)
    header2 = font.render("Pick your level!", True, Black)
    header = font.render("Welcome To Connect Four", True, Black)
    window_rect = header.get_rect(center=(WIDTH / 2, 75))
    win.blit(background_menu, (0, 0))
    win.blit(header, window_rect)
    win.blit(header2, (200, 90))

    # draw buttons
    buttons(WIDTH / 3, 200, 200, 100, Red, "Level : Easy", 30, 1)
    buttons(WIDTH / 3, 350, 200, 100, Red, "Level : Normal", 30, 2)
    buttons(WIDTH / 3, 500, 200, 100, Red, "Level : Hard", 30, 3)
    pygame.display.update()
    # left, top, width, height, color, message


# Colors
Blue = (0, 0, 255)
Background_color = (255, 178, 102)
Red = (255, 0, 0)
Yellow = (255, 255, 0)
Black = (0, 0, 0)
Grey = (211, 211, 211)
Green = (0, 255, 0)

# Menu Screen
WIDTH = 700
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
game_start_again = False
current_screen = "main menu"

# Player and AI
turn = random.randint(boards.Player, boards.AI)
# turn = 0
count = 0
ai_level = 0
winner = " "

# Display Menu
win = pygame.display.set_mode((WIDTH, HEIGHT))
win.fill(Grey)

# Mainmenu texture
background_menu = pygame.image.load("menu.png")

# Board texture
beta = pygame.image.load("kucing.png")

# Game Over texture
background_game_over = pygame.image.load("Game_Over.png")

# Window Caption
pygame.display.set_caption("Connect Four")

# Logo
icon = pygame.image.load("logo.png")
pygame.display.set_icon(icon)

# Banner
banner = pygame.image.load("banner.png")
banner = pygame.transform.scale(banner, (450, 250))

# Background sound
mixer.music.load("PekoBMG.wav")
mixer.music.play(-1)
mixer.music.set_volume(0.25)

while True:
    while level_check:
        if current_screen == "main menu":
            main_menu()
        elif current_screen == "loading":
            font1 = pygame.font.SysFont("javanesetext", 45)
            header1 = font1.render("Press A to start!", True, Black)
            window_rect1 = header1.get_rect(center=(WIDTH / 2, 75))
            win.blit(background_menu, (0, 0))
            win.blit(banner, (125, 150))
            win.blit(header1, window_rect1)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                level_check = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    play_BGM(1)
                    level_check = False
                    game_status = False

        pygame.display.update()

    # Game screen
    if not game_status:
        # Screen
        Board_Size = 100

        width = boards.column * Board_Size
        height = (boards.row + 1) * Board_Size

        size = (width, height)

        Radius = int(Board_Size / 2 - 10)

        screen = pygame.display.set_mode(size)
        temp = boards.create_board()
        draw_board(temp)
        pygame.display.update()

        while not game_status:

            for event in pygame.event.get():
                # Exit the game
                if event.type == pygame.QUIT:
                    sys.exit()
                pygame.draw.rect(screen, Background_color, (0, 0, width, Board_Size))

                # Draw circle at the top and move it with mouse
                if event.type == pygame.MOUSEMOTION:
                    pygame.draw.rect(screen, Background_color, (0, 0, width, Board_Size))
                    posx = event.pos[0]
                    if turn == boards.Player:
                        pygame.draw.circle(screen, Red, (posx, int(Board_Size / 2)), Radius)

                pygame.display.update()

                # Checking event condition
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.draw.rect(screen, Background_color, (0, 0, width, Board_Size))
                    # Player turn to drop the pieces

                    if turn == boards.Player:
                        posx = event.pos[0]
                        col = int(math.floor(posx / Board_Size))

                        # Checking player position is valid or no
                        if boards.check_valid_position(temp, col):
                            row = boards.get_free_row(temp, col)
                            boards.drop_piece(temp, row, col, boards.Player_Piece)
                            play_BGM(2)

                            # Checking player is win or not
                            if boards.win_condition(temp, boards.Player_Piece):
                                play_BGM(3)
                                winner = "Player is the winner!"
                                player_status = True

                            # boards.print_board(temp)
                            draw_board(temp)

                            turn += 1
                            count += 1
                            turn = turn % 2

                            # Draw situation
                            if count == 42:
                                winner = "Draw"
                                player_status = True

                # AI turn to drop pieces
                if turn == boards.AI and not game_status and player_status is False:
                    # level 1 = easy, 2 = normal, 3 = hard
                    if ai_level == 1:
                        col = boards.easy_ai(temp, boards.AI_Piece)
                    elif ai_level == 2:
                        col, minimax_score = boards.ai_minimax(temp, 5, -math.inf, math.inf, False)
                    else:
                        col, minimax_score = boards.ai_minimax(temp, 5, -math.inf, math.inf, True)

                    if boards.check_valid_position(temp, col):
                        row = boards.get_free_row(temp, col)
                        boards.drop_piece(temp, row, col, boards.AI_Piece)
                        play_BGM(2)

                        if boards.win_condition(temp, boards.AI_Piece):
                            play_BGM(3)
                            winner = "AI is the winner!"
                            player_status = True

                        # boards.print_board(temp)
                        draw_board(temp)

                        turn += 1
                        count += 1
                        turn = turn % 2

                        if count == 42:
                            winner = "Draw!"
                            player_status = True

                # Game end Status
                if player_status:
                    # screen.blit(Beta,(10,10))
                    # Waiting time
                    pygame.time.wait(1250)
                    game_status = True
                    game_over = True

    # Game over screen
    if game_over:
        while game_over:
            font1 = pygame.font.SysFont("javanesetext", 25)
            end_Header = font1.render("Game Over! Please Press Quit button to end the game", True, Black)
            window_end_rect = end_Header.get_rect(center=(350, 150))
            win.blit(background_game_over, (0, 0))
            win.blit(end_Header, window_end_rect)

            label = font1.render(winner, True, Black)
            if winner == "AI is the winner!":
                win.blit(label, (250, 200))
            elif winner == "Player is the winner!":
                win.blit(label, (220, 200))



            # Play again button
            buttons(WIDTH / 3 + 35, 300, 150, 80, Red, "Play Again", 20, 4)
            buttons(WIDTH / 3 + 35, 400, 150, 80, Red, "Quit", 20, 5)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_over = False

            pygame.display.update()

    if not game_over and game_start_again:
        # ReDeclare

        # Level status
        game_status = True
        player_status = False
        level_check = True
        game_over = False
        game_start_again = False
        current_screen = "main menu"

        # Player and AI
        turn = random.randint(boards.Player, boards.AI)
        # turn = 0
        count = 0
        ai_level = 0
        winner = " "
    else:
        break
