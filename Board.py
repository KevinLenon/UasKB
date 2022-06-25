import numpy as np
import random
import pygame
import sys
import math


class Board:

    def __init__(self, row, column):
        self.row = row
        self.column = column
        self.Player = 0
        self.AI = 1
        self.Empty = 0
        self.Player_Piece = 1
        self.AI_Piece = 2
        self.Window_Length = 4
        self.stat = 1

    def create_board(self):
        # Membuat array kosong dengan panjanga row x column
        board = np.zeros((self.row, self.column))
        return board

    def drop_piece(self, board, row, col, piece):
        self.stat = 0
        board[row][col] = piece

    def check_valid_position(self, board, col):
        return board[self.row - 1][col] == 0

    def get_valid_locations(self, board):
        self.stat = 1
        valid_locations = []
        for col in range(self.column):
            if self.check_valid_position(board, col):
                valid_locations.append(col)
        return valid_locations

    def get_free_row(self, board, col):

        for i in range(self.row):
            if board[i][col] == 0:
                return i

    def print_board(self, board):
        self.stat = 1
        print(np.flip(board, 0))

    def win_condition(self, board, piece):
        for i in range(self.column - 3):
            for j in range(self.row):
                if board[j][i] == piece and board[j][i + 1] == piece and board[j][i + 2] == piece and board[j][
                    i + 3] == piece:
                    return True

        # Check vertical locations for win
        for i in range(self.column):
            for j in range(self.row - 3):
                if board[j][i] == piece and board[j + 1][i] == piece and board[j + 2][i] == piece and board[j + 3][
                    i] == piece:
                    return True

        # Check positively sloped diaganols
        for i in range(self.column - 3):
            for j in range(self.row - 3):
                if board[j][i] == piece and board[j + 1][i + 1] == piece and board[j + 2][i + 2] == piece and \
                        board[j + 3][i + 3] == piece:
                    return True

        # Check negatively sloped diaganols
        for i in range(self.column - 3):
            for j in range(3, self.row):
                if board[j][i] == piece and board[j - 1][i + 1] == piece and board[j - 2][i + 2] == piece and \
                        board[j - 3][i + 3] == piece:
                    return True

    def get_score(self, window, piece):
        score = 0
        opp_Piece = self.Player_Piece
        if piece == self.Player_Piece:
            opp_Piece = self.AI_Piece

        if window.count(piece) == 4:
            score += 100
        elif window.count(piece) == 3 and window.count(self.Empty) == 1:
            score += 5
        elif window.count(piece) == 2 and window.count(self.Empty) == 2:
            score += 2

        if window.count(opp_Piece) == 3 and window.count(self.Empty) == 1:
            score -= 4

        return score

    def score_position(self, board, piece):
        score = 0

        ## Score center column
        center_array = [int(i) for i in list(board[:, self.column // 2])]
        center_count = center_array.count(piece)
        score += center_count * 3

        ## Score Horizontal
        for r in range(self.row):
            row_array = [int(i) for i in list(board[r, :])]
            for c in range(self.column - 3):
                window = row_array[c:c + self.Window_Length]
                score += self.get_score(window, piece)

        ## Score Vertical
        for c in range(self.column):
            col_array = [int(i) for i in list(board[:, c])]
            for r in range(self.row - 3):
                window = col_array[r:r + self.Window_Length]
                score += self.get_score(window, piece)

        ## Score posiive sloped diagonal
        for r in range(self.row - 3):
            for c in range(self.column - 3):
                window = [board[r + i][c + i] for i in range(self.Window_Length)]
                score += self.get_score(window, piece)

        for r in range(self.row - 3):
            for c in range(self.column - 3):
                window = [board[r + 3 - i][c + i] for i in range(self.Window_Length)]
                score += self.get_score(window, piece)

        return score

    def is_terminal_node(self, board):
        return self.win_condition(board, self.Player_Piece) or self.win_condition(board, self.AI_Piece) or len(
            self.get_valid_locations(board)) == 0

    def minimax(self,board, depth, alpha, beta, maximizingPlayer):
        valid_locations = self.get_valid_locations(board)
        is_terminal = self.is_terminal_node(board)
        if depth == 0 or is_terminal:
            if is_terminal:
                if self.win_condition(board, self.AI_Piece):
                    return None, 100000000000000
                elif self.win_condition(board, self.Player_Piece):
                    return None, -10000000000000
                else:  # Game is over, no more valid moves
                    return None, 0
            else:  # Depth is zero
                return None, self.score_position(board, self.AI_Piece)
        if maximizingPlayer:
            value = -math.inf
            column = random.choice(valid_locations)
            for col in valid_locations:
                row = self.get_free_row(board, col)
                b_copy = board.copy()
                self.drop_piece(b_copy, row, col, self.AI_Piece)
                new_score = self.minimax(b_copy, depth - 1, alpha, beta, False)[1]
                if new_score > value:
                    value = new_score
                    column = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return column, value

        else:  # Minimizing player
            value = math.inf
            column = random.choice(valid_locations)
            for col in valid_locations:
                row = self.get_free_row(board, col)
                b_copy = board.copy()
                self.drop_piece(b_copy, row, col, self.Player_Piece)
                new_score = self.minimax(b_copy, depth - 1, alpha, beta, True)[1]
                if new_score < value:
                    value = new_score
                    column = col
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return column, value

    def pick_best_move(self,board, piece):
        valid_locations = self.get_valid_locations(board)
        best_score = -10000
        best_col = random.choice(valid_locations)
        for col in valid_locations:
            row = self.get_free_row(board, col)
            temp_board = board.copy()
            self.drop_piece(temp_board, row, col, piece)
            score = self.score_position(temp_board, piece)
            if score > best_score:
                best_score = score
                best_col = col

        return best_col
