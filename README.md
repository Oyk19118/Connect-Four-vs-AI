# Connect 4 Game Project

The Connect 4 Game is an interactive two-player strategy game implemented in Python using the pygame library. It enables a player to play against an AI opponent, which selects optimal moves using the Minimax algorithm with Alpha-Beta Pruning.

## Features

Interactive Game: The game is played interactively, where a player selects the column to place his move by clicking the mouse.
AI Opponent: The computer uses a decision-making algorithm in selecting its moves.

The conditions of winning are controlled by horizontal, vertical, and diagonal connections of four successive pieces. A "Restart" button allows the players to reset the board and start a new game after a game is over. All the visual elements, such as a grid and colored pieces, were drawn using pygame for smooth gameplay. Python: Core language for logic and implementation. NumPy: Grid-based data manipulation and calculations.

Pygame: To display the game grid, handle user input, and manage graphics.

## How It Works

The game starts with an empty grid.
Players take turns to drop pieces into the grid. The human player moves first by default.
The AI calculates the best possible move using the Minimax algorithm to play effectively.
The game is over when either player gets four in a row or the grid is full (draw).
