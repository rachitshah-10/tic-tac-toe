from game import Game


def test_game_initial_state():
    """Verify that a new game starts with player X."""
    game = Game()
    assert game.current_player == "X"


def test_invalid_move_preserves_turn():
    """Verify that an invalid move returns False and does not advance the turn."""
    game = Game()
    assert game.play_turn(1, 1) is True
    assert game.current_player == "O"
    # Attempting to play on already occupied cell
    assert game.play_turn(1, 1) is False
    assert game.current_player == "O"
    # Attempting an out of bounds move
    assert game.play_turn(3, 3) is False
    assert game.current_player == "O"


def test_game_win_detection():
    """Verify that winning a game sets the winner and marks game as over."""
    game = Game()
    game.play_turn(0, 0)
    game.play_turn(1, 0)
    game.play_turn(0, 1)
    game.play_turn(1, 1)
    game.play_turn(0, 2)

    assert game.is_over() is True
    assert game.winner == "X"
    assert not game.is_draw()


def test_game_draw_detection():
    """Verify that filling the board with no winner ends in a draw."""
    game = Game()
    moves = [
        (0, 0),
        (0, 1),
        (0, 2),
        (1, 1),
        (1, 0),
        (1, 2),
        (2, 1),
        (2, 0),
        (2, 2),
    ]
    for r, c in moves:
        game.play_turn(r, c)

    assert game.is_over() is True
    assert game.is_draw() is True
    assert game.winner is None

