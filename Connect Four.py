import pygame
import sys
import math
from pygame import mixer
from Board import Board


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


Blue = (0, 0, 255)
Black = (0, 0, 0)
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

#Game status
game_status = False

#Player Turn
# turn = random.randint(PLAYER, AI)
turn = 0
#Text Font
myfont = pygame.font.SysFont("monospace", 75)

# Backgroung sound
mixer.music.load("Driftveil City.wav")
mixer.music.play(-1)
mixer.music.set_volume(0.15)

temp = boards.create_board()
draw_board(temp)
pygame.display.update()

while not game_status:

    for event in pygame.event.get():
        #To exit the game
        if event.type == pygame.QUIT:
            sys.exit()

        #Draw the circle at the top
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
                        game_status = True

                    turn += 1
                    turn = turn % 2

                    boards.print_board(temp)
                    draw_board(temp)

        if turn == boards.AI and not game_status:

            # col = random.randint(0, COLUMN_COUNT-1)
            # col = pick_best_move(board, AI_PIECE)
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
                    game_status = True

                boards.print_board(temp)
                draw_board(temp)

                turn += 1
                turn = turn % 2

        if game_status:
            pygame.time.wait(3000)
