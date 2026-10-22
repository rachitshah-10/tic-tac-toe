import pytest
from board import Board


def test_new_board_is_empty():
    """Verify that a newly instantiated board has 9 empty cells."""
    board = Board()
    assert len(board.empty_cells()) == 9
    for row in range(3):
        for col in range(3):
            assert board.get_cell(row, col) == ""


def test_place_mark_valid():
    """Verify placing a mark on an empty cell succeeds."""
    board = Board()
    assert board.place_mark(1, 1, "X") is True
    assert board.get_cell(1, 1) == "X"
    assert (1, 1) not in board.empty_cells()


def test_taken_cell_rejected():
    """Verify placing on an already occupied cell returns False."""
    board = Board()
    assert board.place_mark(0, 0, "X") is True
    assert board.place_mark(0, 0, "O") is False
    assert board.get_cell(0, 0) == "X"


def test_off_board_positions_rejected():
    """Verify off-board coordinates are rejected."""
    board = Board()
    invalid_coordinates = [
        (-1, 0),
        (0, -1),
        (-1, -1),
        (3, 0),
        (0, 3),
        (3, 3),
        (5, 2),
        (-5, -5),
    ]
    for row, col in invalid_coordinates:
        assert board.place_mark(row, col, "X") is False
        assert board.get_cell(row, col) is None


def test_remove_mark():
    """Verify removing a mark resets the cell."""
    board = Board()
    board.place_mark(0, 1, "X")
    board.remove_mark(0, 1)
    assert board.get_cell(0, 1) == ""


def test_win_rows():
    """Verify horizontal wins across all three rows."""
    for row in range(3):
        board = Board()
        assert not board.has_won("X")
        board.place_mark(row, 0, "X")
        board.place_mark(row, 1, "X")
        board.place_mark(row, 2, "X")
        assert board.has_won("X") is True
        assert board.has_won("O") is False


def test_win_columns():
    """Verify vertical wins down all three columns."""
    for col in range(3):
        board = Board()
        assert not board.has_won("O")
        board.place_mark(0, col, "O")
        board.place_mark(1, col, "O")
        board.place_mark(2, col, "O")
        assert board.has_won("O") is True
        assert board.has_won("X") is False


def test_win_main_diagonal():
    """Verify diagonal win from top-left to bottom-right."""
    board = Board()
    board.place_mark(0, 0, "X")
    board.place_mark(1, 1, "X")
    board.place_mark(2, 2, "X")
    assert board.has_won("X") is True
    assert board.has_won("O") is False


def test_win_anti_diagonal():
    """Verify diagonal win from top-right to bottom-left."""
    board = Board()
    board.place_mark(0, 2, "O")
    board.place_mark(1, 1, "O")
    board.place_mark(2, 0, "O")
    assert board.has_won("O") is True
    assert board.has_won("X") is False


def test_full_board_no_winner_is_draw():
    """Verify the case of a draw."""
    board = Board()
    moves = [
        (0, 0, "X"), (0, 1, "O"), (0, 2, "X"),
        (1, 0, "X"), (1, 1, "O"), (1, 2, "O"),
        (2, 0, "O"), (2, 1, "X"), (2, 2, "X"),
    ]
    for row, col, mark in moves:
        board.place_mark(row, col, mark)

    assert board.has_won("X") is False
    assert board.has_won("O") is False


