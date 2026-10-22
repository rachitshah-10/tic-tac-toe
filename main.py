from game import Game


def prompt_choice(prompt_text, options):
    """Show options and return user's choice."""
    print(prompt_text)
    for key, desc in options.items():
        print(f"{key} - {desc}")
    while True:
        choice = input().strip()
        if choice in options:
            return choice
        print("Please enter a valid input!")
        print("-------------------------------------------------------------------------")


def print_board(board):
    """Print the current board state."""
    for r in range(3):
        row_cells = [board.get_cell(r, c) or " " for c in range(3)]
        print(" " + " | ".join(row_cells))
        if r < 2:
            print("---+---+---")
    print()


def get_player_move(player):
    """Ask player for row and column, returning 0-indexed values."""
    while True:
        parts = input(f"Player {player}, enter row and column (e.g. 2 3): ").split()
        if len(parts) != 2:
            print("Please enter exactly two numbers separated by a space.")
            continue
        try:
            row = int(parts[0]) - 1
            col = int(parts[1]) - 1
            return row, col
        except ValueError:
            print("Coordinates must be numbers. Try again.")


def main():
    """Run the tic-tac-toe game."""
    print("-------------------------------------------------------------------------")
    print("WELCOME TO TIC-TAC-TOE. COMMAND LINE IS NEVER MORE FUN!")
    print("-------------------------------------------------------------------------\n")

    mode = prompt_choice(
        "Please select single player or two players",
        {"1": "Single Player", "2": "Two Players"},
    )
    num_players = int(mode)

    if num_players == 1:
        diff = prompt_choice(
            "Please select difficulty",
            {"1": "Easy", "2": "Hard"},
        )
        print("Single player mode will be available in the next branch!")
        return

    # Two player game
    game = Game()
    while not game.is_over():
        print_board(game.board)
        row, col = get_player_move(game.current_player)

        if not game.play_turn(row, col):
            print("Invalid move: that cell is taken or off the board. Try again!\n")

    print_board(game.board)
    if game.winner:
        print(f"Player {game.winner} wins!")
    else:
        print("It's a draw!")


if __name__ == "__main__":
    main()