# Tic-Tac-Toe

A terminal-based 3x3 Tic-Tac-Toe game written in Python. It supports two players taking turns locally or a single player competing against an Easy (random) or Hard (minimax) computer opponent.

## Requirements

- Python 3.10 or later
-  modules listed in `requirements.txt`

## Setup

1. Create and activate a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## How to Run the Game

Start the game by running:

```bash
python main.py
```

### How to Play

1. Choose your game mode:
   - `1` for Single Player (then choose `1` for Easy or `2` for Hard)
   - `2` for Two Players
2. On your turn, enter your move as row and column numbers from 1 to 3, separated by a space (e.g. `2 3` for row 2, column 3).
3. The board is updated and displayed after every valid move.
4. Player X always makes the first move. In single-player mode, the human plays as X and the computer plays as O.

## How to Run the Tests

Run the full automated test suite using `pytest`:

```bash
pytest
```
