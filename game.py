from board import Board


class Game:
    def __init__(self):
        """Initialize game with a new board and set X to go first."""
        self.board = Board()
        self.current_player = "X"
        self.winner = None

    def play_turn(self, row, col):
        """Place mark for current player and switch turn if valid."""
        if not self.board.place_mark(row, col, self.current_player):
            return False

        if self.board.has_won(self.current_player):
            self.winner = self.current_player
        elif not self.is_draw():
            self._switch_player()

        return True

    def _switch_player(self):
        """Switch current player between X and O."""
        self.current_player = "O" if self.current_player == "X" else "X"

    def is_draw(self):
        """Return True if the board is full and no one won."""
        return self.board.is_full() and self.winner is None

    def is_over(self):
        """Return True if someone won or the game is a draw."""
        return self.winner is not None or self.is_draw()
