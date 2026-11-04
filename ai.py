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


class MediumAI(AI):
    """AI that randomly mixes minimax and random moves, turn by turn."""

    def __init__(self, rng=None, minimax_chance=0.5):
        """Set the per-turn probability (0 to 1) of playing minimax."""
        if not 0 <= minimax_chance <= 1:
            raise ValueError("minimax_chance must be between 0 and 1")
        super().__init__(rng)
        self.minimax_chance = minimax_chance
        self._easy = EasyAI(self.rng)
        self._hard = HardAI(self.rng)

    def choose_move(self, board, mark):
        """Pick minimax with probability minimax_chance, else a random cell."""
        if self.rng.random() < self.minimax_chance:
            return self._hard.choose_move(board, mark)
        return self._easy.choose_move(board, mark)


class HardAI(AI):
    def choose_move(self, board, mark):
        """Pick the best move using minimax."""
        opponent = "O" if mark == "X" else "X"
        best_score = float("-inf")
        best_move = None

        for row, col in board.empty_cells():
            board.place_mark(row, col, mark)
            score = self._minimax(board, 0, False, mark, opponent)
            board.remove_mark(row, col)

            if score > best_score:
                best_score = score
                best_move = (row, col)

        return best_move

    def _minimax(self, board, depth, is_maximizing, ai_mark, opponent):
        """Recursively score board states to find the best outcome."""
        if board.has_won(ai_mark):
            return 10 - depth
        if board.has_won(opponent):
            return depth - 10
        if board.is_full():
            return 0

        if is_maximizing:
            max_score = float("-inf")
            for row, col in board.empty_cells():
                board.place_mark(row, col, ai_mark)
                score = self._minimax(board, depth + 1, False, ai_mark, opponent)
                board.remove_mark(row, col)
                max_score = max(max_score, score)
            return max_score
        else:
            min_score = float("inf")
            for row, col in board.empty_cells():
                board.place_mark(row, col, opponent)
                score = self._minimax(board, depth + 1, True, ai_mark, opponent)
                board.remove_mark(row, col)
                min_score = min(min_score, score)
            return min_score

