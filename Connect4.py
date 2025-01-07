from flask import Flask, render_template, request, jsonify
import numpy as np
import random

app = Flask(__name__)

# Game configurations
GRID_ROWS = 6
GRID_COLUMNS = 7
EMPTY_SLOT = 0
PLAYER1_PIECE = 1
PLAYER2_PIECE = 2
WIN_LENGTH = 4

# Initialize grid
grid = np.zeros((GRID_ROWS, GRID_COLUMNS))

def is_column_available(grid, col):
    return grid[GRID_ROWS - 1][col] == EMPTY_SLOT

def get_next_open_row(grid, col):
    for r in range(GRID_ROWS):
        if grid[r][col] == EMPTY_SLOT:
            return r

def place_piece(grid, row, col, piece):
    grid[row][col] = piece

def check_win(grid, piece):
    # Horizontal check
    for col in range(GRID_COLUMNS - 3):
        for row in range(GRID_ROWS):
            if all(grid[row][col + i] == piece for i in range(WIN_LENGTH)):
                return True

    # Vertical check
    for col in range(GRID_COLUMNS):
        for row in range(GRID_ROWS - 3):
            if all(grid[row + i][col] == piece for i in range(WIN_LENGTH)):
                return True

    # Positive diagonal check
    for col in range(GRID_COLUMNS - 3):
        for row in range(GRID_ROWS - 3):
            if all(grid[row + i][col + i] == piece for i in range(WIN_LENGTH)):
                return True

    # Negative diagonal check
    for col in range(GRID_COLUMNS - 3):
        for row in range(3, GRID_ROWS):
            if all(grid[row - i][col + i] == piece for i in range(WIN_LENGTH)):
                return True

    return False

def minimax(grid, depth, alpha, beta, maximizing):
    valid_columns = [col for col in range(GRID_COLUMNS) if is_column_available(grid, col)]
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

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/move", methods=["POST"])
def ai_move():
    global grid
    data = request.get_json()
    player_col = data["player_col"]

    # Player move
    if is_column_available(grid, player_col):
        row = get_next_open_row(grid, player_col)
        place_piece(grid, row, player_col, PLAYER1_PIECE)

        if check_win(grid, PLAYER1_PIECE):
            return jsonify({"winner": "Player", "ai_col": None})

    # AI move
    ai_col, _ = minimax(grid, 4, -float('inf'), float('inf'), True)
    if ai_col is not None and is_column_available(grid, ai_col):
        row = get_next_open_row(grid, ai_col)
        place_piece(grid, row, ai_col, PLAYER2_PIECE)

        if check_win(grid, PLAYER2_PIECE):
            return jsonify({"winner": "AI", "ai_col": ai_col})

    return jsonify({"winner": None, "ai_col": ai_col})

@app.route("/reset", methods=["POST"])
def reset_game():
    global grid
    grid = np.zeros((GRID_ROWS, GRID_COLUMNS))  # Reset the grid
    return "Game reset!", 200

if __name__ == "__main__":
    app.run(debug=True)