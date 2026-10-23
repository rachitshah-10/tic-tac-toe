from abc import ABC, abstractmethod
import random


class AI(ABC):
    def __init__(self, rng=None):
        """Initialize AI with a random number generator."""
        self.rng = rng if rng is not None else random.Random()

    @abstractmethod
    def choose_move(self, board, mark):
        """Choose a move (row, col) for the given mark."""
        pass


class EasyAI(AI):
    def choose_move(self, board, mark):
        """Pick a random empty cell from the board."""
        empty = board.empty_cells()
        if not empty:
            return None
        return self.rng.choice(empty)
