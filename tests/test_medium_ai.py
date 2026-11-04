import random

import pytest

from ai import AI, EasyAI, HardAI, MediumAI
from board import Board

SIMULATION_GAMES = 100
MIN_WIN_RATE_GAP = 0.10


def simulate_win_rate(ai, games, seed):
    """Return the fraction of games `ai` (playing O) wins against random X.

    X moves first and picks uniformly random cells. The opponent RNG uses a
    fixed seed so every difficulty faces the same sequence of random
    choices, which keeps the comparison fair and the test deterministic.
    """
    opponent = random.Random(seed)
    wins = 0
    for _ in range(games):
        board = Board()
        while True:
            row, col = opponent.choice(board.empty_cells())
            board.place_mark(row, col, "X")
            if board.has_won("X") or board.is_full():
                break
            row, col = ai.choose_move(board, "O")
            board.place_mark(row, col, "O")
            if board.has_won("O"):
                wins += 1
                break
            if board.is_full():
                break
    return wins / games


def winning_position_for_o():
    """Return a board where O to move has exactly one best move: (0, 2).

    O O .
    X X .
    . . .

    Minimax takes the win at (0, 2). Any of the other four empty cells
    ((1, 2), (2, 0), (2, 1), (2, 2)) is a worse move.
    """
    board = Board()
    board.place_mark(0, 0, "O")
    board.place_mark(0, 1, "O")
    board.place_mark(1, 0, "X")
    board.place_mark(1, 1, "X")
    return board


def winning_position_for_x():
    """Mirror of winning_position_for_o: X to move, best move is (0, 2)."""
    board = Board()
    board.place_mark(0, 0, "X")
    board.place_mark(0, 1, "X")
    board.place_mark(1, 0, "O")
    board.place_mark(1, 1, "O")
    return board


BEST_MOVE = (0, 2)


def test_medium_ai_is_an_ai():
    """Verify MediumAI follows the AI interface and can be instantiated."""
    assert isinstance(MediumAI(), AI)


def test_returns_a_valid_empty_cell():
    """Verify the chosen move is always an empty cell."""
    board = winning_position_for_o()
    ai = MediumAI(random.Random(1))
    for _ in range(50):
        assert ai.choose_move(board, "O") in board.empty_cells()


def test_always_minimax_when_chance_is_one():
    """Verify minimax_chance=1.0 always plays the minimax (winning) move."""
    board = winning_position_for_o()
    for seed in range(30):
        ai = MediumAI(random.Random(seed), minimax_chance=1.0)
        assert ai.choose_move(board, "O") == BEST_MOVE


def test_never_minimax_when_chance_is_zero():
    """Verify minimax_chance=0.0 behaves like random play."""
    board = winning_position_for_o()
    moves = [
        MediumAI(random.Random(seed), minimax_chance=0.0).choose_move(board, "O")
        for seed in range(200)
    ]
    # Random play over 5 empty cells hits every cell, not just the best one.
    assert set(moves) == set(board.empty_cells())


def test_default_mixes_random_and_minimax_across_turns():
    """Verify one AI instance sometimes plays minimax and sometimes random.

    With 5 empty cells, always-random finds the best move ~20% of the time
    and always-minimax 100%. A 50/50 mix should land around 60%.
    """
    board = winning_position_for_o()
    ai = MediumAI(random.Random(2024))
    turns = 400

    moves = [ai.choose_move(board, "O") for _ in range(turns)]
    best_rate = moves.count(BEST_MOVE) / turns

    assert any(move != BEST_MOVE for move in moves), "never played randomly"
    assert 0.4 < best_rate < 0.8


def test_chance_controls_how_often_minimax_is_used():
    """Verify a higher minimax_chance finds the best move more often."""
    board = winning_position_for_o()

    def best_rate(chance):
        ai = MediumAI(random.Random(7), minimax_chance=chance)
        moves = [ai.choose_move(board, "O") for _ in range(300)]
        return moves.count(BEST_MOVE) / 300

    assert best_rate(0.2) < best_rate(0.5) < best_rate(0.8)


def test_works_as_x_player():
    """Verify the AI handles the X mark (minimax needs the right opponent)."""
    board = winning_position_for_x()
    ai = MediumAI(random.Random(0), minimax_chance=1.0)
    assert ai.choose_move(board, "X") == BEST_MOVE


def test_deterministic_with_seed():
    """Verify two AIs with the same seed make the same sequence of moves."""
    board = winning_position_for_o()
    ai1 = MediumAI(random.Random(99))
    ai2 = MediumAI(random.Random(99))
    seq1 = [ai1.choose_move(board, "O") for _ in range(20)]
    seq2 = [ai2.choose_move(board, "O") for _ in range(20)]
    assert seq1 == seq2


def test_choose_move_leaves_board_unchanged():
    """Verify choosing a move (either strategy) does not alter the board."""
    board = winning_position_for_o()
    before = [board.get_cell(r, c) for r in range(3) for c in range(3)]
    ai = MediumAI(random.Random(5))
    for _ in range(20):
        ai.choose_move(board, "O")
    after = [board.get_cell(r, c) for r in range(3) for c in range(3)]
    assert before == after


def test_full_board_returns_none():
    """Verify there is no move to make on a full board."""
    board = Board()
    marks = ["X", "O", "X", "X", "O", "O", "O", "X", "X"]
    for index, mark in enumerate(marks):
        board.place_mark(index // 3, index % 3, mark)
    assert board.is_full()
    for chance in (0.0, 0.5, 1.0):
        assert MediumAI(random.Random(0), minimax_chance=chance).choose_move(
            board, "O"
        ) is None


@pytest.mark.parametrize("bad_chance", [-0.1, 1.1, 2, -1])
def test_invalid_minimax_chance_rejected(bad_chance):
    """Verify minimax_chance outside 0..1 raises ValueError."""
    with pytest.raises(ValueError):
        MediumAI(minimax_chance=bad_chance)


@pytest.mark.parametrize("chance", [0, 0.0, 0.5, 1, 1.0])
def test_boundary_minimax_chance_accepted(chance):
    """Verify 0 and 1 are valid boundary values."""
    MediumAI(minimax_chance=chance)


def test_win_rate_easy_below_medium_below_hard():
    """Verify difficulty ordering: Easy < Medium < Hard in win rate.

    Each AI plays 100 games as O against a random X player. Expected rates
    are roughly 30% (Easy), 55% (Medium) and 80% (Hard). Requiring a gap of
    at least 10 percentage points between levels is about 2 standard errors
    at this sample size, so ordering is not a fluke of a lucky seed.
    """
    easy = simulate_win_rate(EasyAI(random.Random(1)), SIMULATION_GAMES, seed=42)
    medium = simulate_win_rate(MediumAI(random.Random(1)), SIMULATION_GAMES, seed=42)
    hard = simulate_win_rate(HardAI(), SIMULATION_GAMES, seed=42)

    assert easy + MIN_WIN_RATE_GAP < medium, f"easy={easy}, medium={medium}"
    assert medium + MIN_WIN_RATE_GAP < hard, f"medium={medium}, hard={hard}"
