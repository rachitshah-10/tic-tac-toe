class Board:
    def __init__(self, size=3):
        if size < 3:
            raise ValueError("size must be at least 3")
        self._size = size
        self._board = [[''] * size for _ in range(size)]
    
    def _is_valid_coordinate(self, row, col):
        """Private method to check whether the coordinates are out of bounds"""
        if 0 <= row < self._size and 0 <= col < self._size:
            return True
        return False

    def place_mark(self, row, col, mark):
        """Place mark at row, col. Returns False if not allowed."""
        # Check for out of bounds
        if not self._is_valid_coordinate(row, col):
            return False
        # Check if it's already taken
        if self._board[row][col] != '':
            return False
        
        # Valid move
        self._board[row][col] = mark
        return True
    
    def remove_mark(self, row, col):
        """Remove mark at the given coordinate"""
        if not self._is_valid_coordinate(row, col):
            return None
        self._board[row][col] = ''
    
    def empty_cells(self):
        """Returns a list of empty celss"""
        result = []
        for i in range(self._size):
            for j in range(self._size):
                if self._board[i][j] == '':
                    result.append((i, j))
        return result
    
    def is_full(self):
        """Check if the board is full"""
        for i in range(self._size):
            for j in range(self._size):
                if self._board[i][j] == '':
                    return False
        return True
    
    def get_cell(self, row, col):
        """Get the mark at the given coordinate"""
        if not self._is_valid_coordinate(row, col):
            return None
        
        return self._board[row][col]
    
    def has_won(self, mark):
        """Return True if mark fills a whole row, column, or diagonal."""
        for row in self._board:
            if all(cell == mark for cell in row):
                return True
        for col in range(self._size):
            if all(self._board[row][col] == mark for row in range(self._size)):
                return True
        if all(self._board[i][i] == mark for i in range(self._size)):
            return True
        return all(self._board[i][self._size - 1 - i] == mark for i in range(self._size))
            

