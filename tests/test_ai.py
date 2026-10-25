import random
import pytest
from board import Board
from ai import AI, EasyAI, HardAI


def test_ai_base_class_cannot_be_instantiated():
    """Verify that the abstract AI class cannot be created directly."""
    with pytest.raises(TypeError):
        AI()


def test_easy_ai_returns_empty_cell():
    """Verify that EasyAI always picks a valid available cell."""
    board = Board()
    board.place_mark(0, 0, "X")
    rng = random.Random(42)
    ai = EasyAI(rng)

    move = ai.choose_move(board, "O")
    assert move in board.empty_cells()
    assert move != (0, 0)


def test_easy_ai_deterministic_with_seed():
    """Verify that EasyAI choices are predictable with a seeded RNG."""
    board = Board()
    ai1 = EasyAI(random.Random(100))
    ai2 = EasyAI(random.Random(100))
    assert ai1.choose_move(board, "O") == ai2.choose_move(board, "O")


def test_hard_ai_takes_winning_move():
    """Verify that HardAI takes an immediate win when available"""
    board = Board()
    board.place_mark(0, 0, "O")
    board.place_mark(0, 1, "O")
    ai = HardAI()

    move = ai.choose_move(board, "O")
    assert move == (0, 2)


def test_hard_ai_blocks_opponent_winning_move():
    """Verify that HardAI blocks the opponent from winning."""
    board = Board()
    board.place_mark(1, 0, "X")
    board.place_mark(1, 1, "X")
    ai = HardAI()

    move = ai.choose_move(board, "O")
    assert move == (1, 2)


def test_choose_move_leaves_board_unchanged():
    """Verify that calculating a move does not alter the board state."""
    board = Board()
    board.place_mark(0, 0, "X")
    before_cells = board.empty_cells()

    ai = HardAI()
    ai.choose_move(board, "O")

    assert board.empty_cells() == before_cells
    assert board.get_cell(0, 0) == "X"


def test_hard_ai_never_loses():
    """Verify that HardAI never loses when playing second."""
    ai = HardAI()
    # Test across 25 different seeded game sequences
    for seed in range(25):
        rng = random.Random(seed)
        board = Board()

        while not board.is_full() and not board.has_won("X") and not board.has_won("O"):
            # Human (X) makes a random move
            x_move = rng.choice(board.empty_cells())
            board.place_mark(x_move[0], x_move[1], "X")

            if board.has_won("X") or board.is_full():
                break

            # Computer (O) makes a move
            o_move = ai.choose_move(board, "O")
            board.place_mark(o_move[0], o_move[1], "O")

        # Hard AI playing O must never lose
        assert not board.has_won("X"), f"HardAI lost to random player on seed {seed}"

