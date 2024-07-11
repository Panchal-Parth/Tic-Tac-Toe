from itertools import cycle
from typing import NamedTuple
import os

################### Player ##################
# Represents a player in the game.
#
# Parameters:
# label: str - The label representing the player (e.g., "X" or "O").
# name: str - The name of the player.
#
# Returns: NamedTuple - A named tuple representing a player.
############################################
class Player(NamedTuple):
    label: str
    name: str

################### Move ###################
# Represents a move in the game.
#
# Parameters:
# row: int - The row index of the move.
# col: int - The column index of the move.
# label: str - The label representing the player (e.g., "X" or "O") making the move
#
# Returns: NamedTuple - A named tuple representing a move.
############################################
class Move(NamedTuple):
    row: int
    col: int
    label: str = ""

BOARD_SIZE = 4
DEFAULT_PLAYERS = (
    Player(label="X", name="SimpliSafe"),
    Player(label="O", name="Parth"),
)

############### TicTacToeGame ##############
# Manages the state of the Tic-Tac-Toe game.
############################################
class TicTacToeGame:
    ################### __init__ ###################
    # Initializes the game with players and board size.
    #
    # Parameters:
    # players: tuple - A tuple of Player 
    # board_size: int - The size of the board 
    #
    # Returns: None
    ############################################
    def __init__(self, players=DEFAULT_PLAYERS, board_size=BOARD_SIZE):
        self._players = cycle(players)
        self.board_size = board_size
        self.current_player = next(self._players)
        self.winner_combo = []
        self._current_moves = []
        self._has_winner = False
        self._winning_combos = []
        self._setup_board()

    ################ _setup_board ###############
    # Sets up the initial state of the game board.
    #
    # Parameters: None
    #
    # Returns: None
    ############################################
    def _setup_board(self):
        self._current_moves = [
            [Move(row, col) for col in range(self.board_size)]
            for row in range(self.board_size)
        ]
        self._winning_combos = self._get_winning_combos()

    ########## _get_winning_combos ##############
    # Defines all possible winning combinations.
    #
    # Parameters: None
    #
    # Returns: list - A list of winning combinations.
    ############################################
    def _get_winning_combos(self):
        rows = [
            [(move.row, move.col) for move in row]
            for row in self._current_moves
        ]
        
        columns = [
            [(move.row, move.col) for move in col]
            for col in zip(*self._current_moves)
        ]
        
        first_diagonal = [(row, row) for row in range(self.board_size)]
        
        second_diagonal = [(row, self.board_size - 1 - row) for row in range(self.board_size)]
        
        winning_combos = rows + columns + [first_diagonal, second_diagonal]
        
        two_by_twos = []
        for row in range(self.board_size - 1):
            for col in range(self.board_size - 1):
                two_by_twos.append([
                    (row, col), (row, col+1),
                    (row+1, col), (row+1, col+1)
                ])
        winning_combos.extend(two_by_twos)
        
        corners = [
            (0, 0), (0, self.board_size - 1),
            (self.board_size - 1, 0), (self.board_size - 1, self.board_size - 1)
        ]
        winning_combos.append(corners)
        
        return winning_combos

    ############# is_valid_move #################
    # Checks if a move is valid.
    #
    # Parameters:
    # move: Move - The move to check.
    #
    # Returns: bool - True if the move is valid, False otherwise.
    #############################################
    def is_valid_move(self, move):
        row, col = move.row, move.col
        move_was_not_played = self._current_moves[row][col].label == ""
        no_winner = not self._has_winner
        return no_winner and move_was_not_played

    ############### process_move ################
    # Processes a move and checks for a winner.
    #
    # Parameters:
    # move: Move - The move to process.
    #
    # Returns: None
    ############################################
    def process_move(self, move):
        row, col = move.row, move.col
        self._current_moves[row][col] = move
        for combo in self._winning_combos:
            results = set(self._current_moves[n][m].label for n, m in combo)
            is_win = (len(results) == 1) and ("" not in results)
            if is_win:
                self._has_winner = True
                self.winner_combo = combo
                break
    
    ################ has_winner ################
    # Returns whether the game has a winner.
    #
    # Parameters: None
    #
    # Returns: bool - True if the game has a winner, False otherwise.
    ############################################
    def has_winner(self):
        return self._has_winner

    ################### is_tied ################
    # Returns whether the game is tied.
    #
    # Parameters: None
    #
    # Returns: bool - True if the game is tied, False otherwise.
    ############################################
    def is_tied(self):
        no_winner = not self._has_winner
        played_moves = (
            move.label for row in self._current_moves for move in row
        )
        return no_winner and all(played_moves)

    ################ toggle_player #############
    # Switches to the next player.
    #
    # Parameters: None
    #
    # Returns: None
    ############################################
    def toggle_player(self):
        self.current_player = next(self._players)

    ################ reset_game ################
    # Resets the game state to play again.
    #
    # Parameters: None
    #
    # Returns: None
    ############################################
    def reset_game(self):
        for row, row_content in enumerate(self._current_moves):
            for col, _ in enumerate(row_content):
                row_content[col] = Move(row, col)
        self._has_winner = False
        self.winner_combo = []

############### print_board ################
# Prints the current state of the game board to the console.
#
# Parameters:
# game: TicTacToeGame - The game instance to print the board for.
#
# Returns: None
############################################
def print_board(game):
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear console screen
    print("Press 'q' to quit at any time.")
    print("Welcome to 4x4 Tic-Tac-Toe!")
    print(f"Player {game.current_player.label}'s last move")
    print("   " + "   ".join(str(i) for i in range(game.board_size)))
    print("  " + "----" * game.board_size + "-")
    for i, row in enumerate(game._current_moves):
        row_str = f"{i} | " + " | ".join(move.label if move.label else " " for move in row) + " |"
        print(row_str)
        print("  " + "----" * game.board_size + "-")
    print()

############### get_user_input ##############
# Get the input from user and validates it
#
# Parameters: 
# prompt: str
# valid_values: str
#
# Returns: 
# user_input: int
############################################
def get_user_input(prompt, valid_values):
    while True:
        user_input = input(prompt).strip()  # Strip whitespace from input
        if user_input.lower() == 'q':
            print("Quitting the game...")
            exit()
        elif user_input.isdigit() and int(user_input) in valid_values:
            return int(user_input)
        else:
            print("Invalid input! Please enter a number from the valid range.")

################### main ###################
# Create the game and run it in the console.
#
# Parameters : None
#
# Returns: None
############################################
def main():
    
    game = TicTacToeGame()
    print_board(game)

    while not game.has_winner() and not game.is_tied():
        row = get_user_input(f"Player {game.current_player.name} - {game.current_player.label}, enter row (0-{game.board_size-1}) or 'q' to quit: ", list(range(game.board_size)))
        if isinstance(row, str):
            print("Invalid move! Try again.")
            continue
        col = get_user_input(f"Player {game.current_player.name} - {game.current_player.label}, enter column (0-{game.board_size-1}) or 'q' to quit: ", list(range(game.board_size)))
        if isinstance(col, str):
            print("Invalid move! Try again.")
            continue
        
        move = Move(row, col, game.current_player.label)
        if game.is_valid_move(move):
            game.process_move(move)
            print_board(game)
            if game.has_winner():
                print(f"Player {game.current_player.name} - {game.current_player.label} wins!")
            elif game.is_tied():
                print("It's a tie!")
            else:
                game.toggle_player()
        else:
            print("Invalid move! Try again.")

if __name__ == "__main__":
    main()