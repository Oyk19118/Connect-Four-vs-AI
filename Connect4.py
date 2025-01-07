import numpy as np
import pygame
import sys
import math
import random

# Define new colors
GRID_COLOR = (50, 50, 150)
BACKGROUND_COLOR = (10, 10, 30)
PLAYER1_COLOR = (200, 0, 50)
PLAYER2_COLOR = (250, 200, 0)
EMPTY_COLOR = (30, 30, 30)

# Grid dimensions
GRID_ROWS = 6
GRID_COLUMNS = 7

# Piece definitions
PLAYER1 = 0
PLAYER2 = 1
EMPTY_SLOT = 0
PLAYER1_PIECE = 1
PLAYER2_PIECE = 2

# Winning length
WIN_LENGTH = 4

# Pygame settings
CELL_SIZE = 100
GRID_WIDTH = GRID_COLUMNS * CELL_SIZE
GRID_HEIGHT = GRID_ROWS * CELL_SIZE
SCREEN_HEIGHT = GRID_HEIGHT + CELL_SIZE
SCREEN_WIDTH = GRID_WIDTH
PIECE_RADIUS = CELL_SIZE // 2 - 10  # Slightly smaller than half the cell size


def initialize_grid():
    return np.zeros((GRID_ROWS, GRID_COLUMNS))


def place_piece(grid, row, col, piece):
    grid[row][col] = piece


def is_column_available(grid, col):
    return grid[GRID_ROWS - 1][col] == EMPTY_SLOT


def get_next_open_row(grid, col):
    for r in range(GRID_ROWS):
        if grid[r][col] == EMPTY_SLOT:
            return r


def check_win(grid, piece):
    # Horizontal
    for col in range(GRID_COLUMNS - 3):
        for row in range(GRID_ROWS):
            if all(grid[row][col + i] == piece for i in range(WIN_LENGTH)):
                return True

    # Vertical
    for col in range(GRID_COLUMNS):
        for row in range(GRID_ROWS - 3):
            if all(grid[row + i][col] == piece for i in range(WIN_LENGTH)):
                return True

    # Diagonals
    for col in range(GRID_COLUMNS - 3):
        for row in range(GRID_ROWS - 3):
            if all(grid[row + i][col + i] == piece for i in range(WIN_LENGTH)):
                return True

    for col in range(GRID_COLUMNS - 3):
        for row in range(3, GRID_ROWS):
            if all(grid[row - i][col + i] == piece for i in range(WIN_LENGTH)):
                return True

    return False


def get_valid_columns(grid):
    return [col for col in range(GRID_COLUMNS) if is_column_available(grid, col)]


def minimax(grid, depth, alpha, beta, maximizing):
    valid_columns = get_valid_columns(grid)
    is_terminal = check_win(grid, PLAYER1_PIECE) or check_win(grid, PLAYER2_PIECE) or len(valid_columns) == 0

    if depth == 0 or is_terminal:
        if is_terminal:
            if check_win(grid, PLAYER2_PIECE):
                return None, float('inf')
            elif check_win(grid, PLAYER1_PIECE):
                return None, float('-inf')
            else:
                return None, 0
        return None, calculate_score(grid, PLAYER2_PIECE)

    if maximizing:
        value = -float('inf')
        column = random.choice(valid_columns)
        for col in valid_columns:
            temp_grid = grid.copy()
            row = get_next_open_row(temp_grid, col)
            place_piece(temp_grid, row, col, PLAYER2_PIECE)
            _, new_score = minimax(temp_grid, depth - 1, alpha, beta, False)
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value
    else:
        value = float('inf')
        column = random.choice(valid_columns)
        for col in valid_columns:
            temp_grid = grid.copy()
            row = get_next_open_row(temp_grid, col)
            place_piece(temp_grid, row, col, PLAYER1_PIECE)
            _, new_score = minimax(temp_grid, depth - 1, alpha, beta, True)
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value


def calculate_score(grid, piece):
    center_col = [int(i) for i in list(grid[:, GRID_COLUMNS // 2])]
    return center_col.count(piece) * 3


def draw_grid(grid, screen):
    screen.fill(BACKGROUND_COLOR)
    for col in range(GRID_COLUMNS):
        for row in range(GRID_ROWS):
            pygame.draw.rect(screen, GRID_COLOR, (col * CELL_SIZE, row * CELL_SIZE + CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.circle(screen, EMPTY_COLOR, (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE + CELL_SIZE // 2), PIECE_RADIUS)
    for col in range(GRID_COLUMNS):
        for row in range(GRID_ROWS):
            if grid[row][col] == PLAYER1_PIECE:
                pygame.draw.circle(screen, PLAYER1_COLOR, (col * CELL_SIZE + CELL_SIZE // 2, SCREEN_HEIGHT - (row * CELL_SIZE + CELL_SIZE // 2)), PIECE_RADIUS)
            elif grid[row][col] == PLAYER2_PIECE:
                pygame.draw.circle(screen, PLAYER2_COLOR, (col * CELL_SIZE + CELL_SIZE // 2, SCREEN_HEIGHT - (row * CELL_SIZE + CELL_SIZE // 2)), PIECE_RADIUS)
    pygame.display.update()


# Initialize game
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Connect 4 (Aligned)")
grid = initialize_grid()
game_over = False
turn = random.randint(PLAYER1, PLAYER2)

draw_grid(grid, screen)

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if turn == PLAYER1 and not game_over:
            if event.type == pygame.MOUSEBUTTONDOWN:
                col = event.pos[0] // CELL_SIZE
                if is_column_available(grid, col):
                    row = get_next_open_row(grid, col)
                    place_piece(grid, row, col, PLAYER1_PIECE)
                    if check_win(grid, PLAYER1_PIECE):
                        print("Player 1 wins!")
                        game_over = True
                    turn = PLAYER2
                    draw_grid(grid, screen)

        elif turn == PLAYER2 and not game_over:
            col, _ = minimax(grid, 4, -float('inf'), float('inf'), True)
            if is_column_available(grid, col):
                row = get_next_open_row(grid, col)
                place_piece(grid, row, col, PLAYER2_PIECE)
                if check_win(grid, PLAYER2_PIECE):
                    print("Player 2 wins!")
                    game_over = True
                turn = PLAYER1
                draw_grid(grid, screen)
