# Connect 4 Game Project

The Connect 4 Game is a two-player strategy game implemented in Python, using the pygame library to offer interaction. This allows a player to play against the AI opponent, whose move is decided with the help of the Minimax algorithm with Alpha-Beta Pruning.

## Features

Interactive Game: The game is interactive. A player selects the column to insert his move by clicking the mouse.
AI Opponent: The computer uses a decision-making algorithm to choose moves.

The winning conditions are made available by horizontal, vertical, and diagonal connection of four successive pieces. All the visual things, which include a grid and colored pieces, were drawn through pygame for smooth gameplay. 

Python: Core language for logic and implementation.
NumPy: Grid-based data manipulation and calculations.
Pygame: For displaying game grid, handling user input, and managing graphics.

## How It Works
The game starts with an empty grid.
Players take turns dropping pieces into the grid. Human players go first by default.
AI performs computation for the best possible move using the Minimax algorithm in order to play effectively.
The game is won when one of the players wins or the grid gets completely filled, hence it's a draw.
