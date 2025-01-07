import numpy as np
import pygame
import sys
import math
import random

# Define colors
COLOR_BLUE = (0, 0, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_RED = (255, 0, 0)
COLOR_YELLOW = (255, 255, 0)

# Define grid dimensions
GRID_ROWS = 6
GRID_COLUMNS = 7

# Piece definitions
HUMAN = 0
COMPUTER = 1
NO_PIECE = 0
HUMAN_PIECE = 1
COMPUTER_PIECE = 2

# Connection length for winning
CONNECTION = 4

# Pygame settings
SQUARE_SIZE = 100
RADIUS = int(SQUARE_SIZE / 2 - 5)
WIDTH = GRID_COLUMNS * SQUARE_SIZE
HEIGHT = (GRID_ROWS + 1) * SQUARE_SIZE
SCREEN_SIZE = (WIDTH, HEIGHT)


def initialize_grid():
    return np.zeros((GRID_ROWS, GRID_COLUMNS))


def place_piece(grid, row, col, piece_type):
    grid[row][col] = piece_type


def is_column_available(grid, col):
    return grid[GRID_ROWS - 1][col] == NO_PIECE


def get_row_for_piece(grid, col):
    for r in range(GRID_ROWS):
        if grid[r][col] == NO_PIECE:
            return r


def has_winning_combination(grid, piece):
    # Horizontal
    for col in range(GRID_COLUMNS - 3):
        for row in range(GRID_ROWS):
            if all(grid[row][col + i] == piece for i in range(CONNECTION)):
                return True
    # Vertical
    for col in range(GRID_COLUMNS):
        for row in range(GRID_ROWS - 3):
            if all(grid[row + i][col] == piece for i in range(CONNECTION)):
                return True
    # Positive diagonal
    for col in range(GRID_COLUMNS - 3):
        for row in range(GRID_ROWS - 3):
            if all(grid[row + i][col + i] == piece for i in range(CONNECTION)):
                return True
    # Negative diagonal
    for col in range(GRID_COLUMNS - 3):
        for row in range(3, GRID_ROWS):
            if all(grid[row - i][col + i] == piece for i in range(CONNECTION)):
                return True
    return False


def calculate_score(grid, piece):
    score = 0
    center_column = [int(i) for i in list(grid[:, GRID_COLUMNS // 2])]
    center_count = center_column.count(piece)
    score += center_count * 3
    return score


def get_valid_columns(grid):
    return [col for col in range(GRID_COLUMNS) if is_column_available(grid, col)]


def minimax(grid, depth, alpha, beta, maximizing):
    valid_columns = get_valid_columns(grid)
    is_terminal = has_winning_combination(grid, HUMAN_PIECE) or has_winning_combination(grid, COMPUTER_PIECE) or len(valid_columns) == 0
    if depth == 0 or is_terminal:
        if is_terminal:
            if has_winning_combination(grid, COMPUTER_PIECE):
                return None, float('inf')
            elif has_winning_combination(grid, HUMAN_PIECE):
                return None, float('-inf')
            else:
                return None, 0
        return None, calculate_score(grid, COMPUTER_PIECE)

    if maximizing:
        value = -float('inf')
        best_column = random.choice(valid_columns)
        for col in valid_columns:
            temp_grid = grid.copy()
            row = get_row_for_piece(temp_grid, col)
            place_piece(temp_grid, row, col, COMPUTER_PIECE)
            _, new_score = minimax(temp_grid, depth - 1, alpha, beta, False)
            if new_score > value:
                value = new_score
                best_column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return best_column, value
    else:
        value = float('inf')
        best_column = random.choice(valid_columns)
        for col in valid_columns:
            temp_grid = grid.copy()
            row = get_row_for_piece(temp_grid, col)
            place_piece(temp_grid, row, col, HUMAN_PIECE)
            _, new_score = minimax(temp_grid, depth - 1, alpha, beta, True)
            if new_score < value:
                value = new_score
                best_column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return best_column, value


def draw_grid(grid, screen):
    for col in range(GRID_COLUMNS):
        for row in range(GRID_ROWS):
            pygame.draw.rect(screen, COLOR_BLUE, (col * SQUARE_SIZE, row * SQUARE_SIZE + SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.circle(screen, COLOR_BLACK, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE // 2), RADIUS)
    for col in range(GRID_COLUMNS):
        for row in range(GRID_ROWS):
            if grid[row][col] == HUMAN_PIECE:
                pygame.draw.circle(screen, COLOR_RED, (col * SQUARE_SIZE + SQUARE_SIZE // 2, HEIGHT - (row * SQUARE_SIZE + SQUARE_SIZE // 2)), RADIUS)
            elif grid[row][col] == COMPUTER_PIECE:
                pygame.draw.circle(screen, COLOR_YELLOW, (col * SQUARE_SIZE + SQUARE_SIZE // 2, HEIGHT - (row * SQUARE_SIZE + SQUARE_SIZE // 2)), RADIUS)
    pygame.display.update()


# Initialize game
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Connect 4")
font = pygame.font.SysFont("monospace", 75)

grid = initialize_grid()
draw_grid(grid, screen)
game_over = False
turn = random.randint(HUMAN, COMPUTER)

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, COLOR_BLACK, (0, 0, WIDTH, SQUARE_SIZE))
            posx = event.pos[0]
            if turn == HUMAN:
                pygame.draw.circle(screen, COLOR_RED, (posx, SQUARE_SIZE // 2), RADIUS)
            pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, COLOR_BLACK, (0, 0, WIDTH, SQUARE_SIZE))
            if turn == HUMAN:
                posx = event.pos[0]
                col = int(math.floor(posx / SQUARE_SIZE))
                if is_column_available(grid, col):
                    row = get_row_for_piece(grid, col)
                    place_piece(grid, row, col, HUMAN_PIECE)

                    if has_winning_combination(grid, HUMAN_PIECE):
                        label = font.render("Player 1 wins!", True, COLOR_RED)
                        screen.blit(label, (40, 10))
                        game_over = True

                    turn = (turn + 1) % 2
                    draw_grid(grid, screen)

    if turn == COMPUTER and not game_over:
        col, _ = minimax(grid, 5, -float('inf'), float('inf'), True)
        if is_column_available(grid, col):
            pygame.time.wait(500)
            row = get_row_for_piece(grid, col)
            place_piece(grid, row, col, COMPUTER_PIECE)

            if has_winning_combination(grid, COMPUTER_PIECE):
                label = font.render("Player 2 wins!", True, COLOR_YELLOW)
                screen.blit(label, (40, 10))
                game_over = True

            turn = (turn + 1) % 2
            draw_grid(grid, screen)

    if game_over:
        pygame.time.wait(3000)