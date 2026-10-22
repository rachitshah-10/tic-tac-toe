def prompt_choice(prompt_text, options):
    """Displays a menu prompt and returns a validated choice from the options dict."""
    print(prompt_text)
    for key, desc in options.items():
        print(f"{key} - {desc}")
    while True:
        choice = input().strip()
        if choice in options:
            return choice
        print("Please enter a valid input!")
        print("-------------------------------------------------------------------------")


def main():
    """Main execution function coordinating the application workflow."""

    # Welcome message
    print("-------------------------------------------------------------------------")
    print("WELCOME TO TIC-TAC-TOE. COMMAND LINE IS NEVER MORE FUN!")
    print("-------------------------------------------------------------------------\n")

    # Choose single player or two player
    mode = prompt_choice(
        "Please select single player or two players",
        {"1": "Single Player", "2": "Two Players"}
    )
    num_players = int(mode)
    print(f"You selected {num_players}!")

    # Select difficulty level if single player is selected
    difficulty_level = 0
    if num_players == 1:
        diff = prompt_choice(
            "Please select difficulty",
            {"1": "Easy", "2": "Hard"}
        )
        difficulty_level = int(diff)
        print(f"You selected {difficulty_level}")

    

if __name__ == "__main__":
    main()