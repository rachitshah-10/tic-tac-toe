# Tic-Tac-Toe Project Plan

## Goal
A CLI based tic-tac-toe game implemented in Python supporting two player mode and a single player mode against computer. The single player mode further has two levels of difficulty - easy and hard.

## Requirements

| ID | Requirement | Type | Priority | How verified |
| :--- | :--- | :--- | :--- | :--- |
| R1 | Players enter moves as row and column from 1 - 3 | Functional | Must | Tests for valid coordinate input parsing |
| R2 | Moves to occupied cells or out of bounds cells are rejected without losing the turn | Functional | Must | Tests for occupied cell, out-of-bounds and bad text |
| R3 | The game detects a win across any row, column, or diagonal for either player and announces the result | Functional | Must | Tests for all horizontal, vertical, and diagonal win conditions |
| R4 | The game detects a draw when the board is full and there is no winner | Functional | Must | Test with a full board and no winning condition meeting |
| R5 | The board is printed to the terminal after every valid move | Functional | Must | Manually playing in terminal |
| R6 | In single-player mode, the human plays X, computer plays O, and the player chooses Easy or Hard difficulty | Functional | Must | Tests checking player moves and setup for both levels |
| R7 | Easy AI picks a random available empty cell | Functional | Must | Tests with seeded RNG |
| R8 | Hard AI uses minimax algorithm and never loses when playing second | Functional | Must | AI unit tests for winning moves |

## Components

- **`board.py`**: Manages the 3x3 board grid, manages player moves, checks for available moves
- **`ai.py`**: Contains the base AI class and implementations for Easy (random) and Hard (minimax) opponents.
- **`game.py`**: Coordinates game flow, and win/draw checks without doing any terminal I/O.
- **`main.py`**: Handles user interactions, printing the board, reading input.
- **`tests/`**: Contains pytest test cases to verify board rules, game logic, and AI behavior.

## Decisions

### Decision 1: AI structure and difficulty handling
- **Options considered**:
  1. A single AI function or class with `if/else` statements checking the difficulty mode.
  2. An abstract base class `AI` with separate subclasses for `EasyAI` and `HardAI`.
- **Choice**: Option 2.
- **Why**: Keeps the easy and hard logic separate and easy to maintain. The game can call `choose_move` on any AI without needing to know which difficulty is active.

### Decision 2: Internal data structure for the board grid
- **Options considered**:
  1. A 1D list of 9 elements (indexed by `row * 3 + col`).
  2. A 2D list of lists (3x3 grid, indexed by `grid[row][col]`).
  3. A dictionary with `(row, col)` coordinate tuples as keys.
- **Choice**: Option 2 (2D list of lists).
- **Why**: The board methods receive row and column as separate arguments. A 2D list makes accessing rows, columns, and diagonals straightforward and readable without needing index arithmetic or dictionary overhead.
