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
    # boardSize: int - The size of the board 
    #
    # Returns: None
    ############################################
    def __init__(self, players=DEFAULT_PLAYERS, boardSize=BOARD_SIZE):
        self._players = cycle(players)
        self.boardSize = boardSize
        self.currentPlayer = next(self._players)
        self._currentMoves = [
            [Move(row, col) for col in range(self.boardSize)]
            for row in range(self.boardSize)
        ]
        self._winningCombos = self._getWinningCombos()
        self._hasWinner = False
        self.winnerCombo = []

    ########## _getWinningCombos ##############
    # Defines all possible winning combinations.
    #
    # Parameters: None
    #
    # Returns: list - A list of winning combinations.
    ############################################
    def _getWinningCombos(self):
        rows = [
            [(move.row, move.col) for move in row]
            for row in self._currentMoves
        ]
        
        columns = [
            [(move.row, move.col) for move in col]
            for col in zip(*self._currentMoves)
        ]
        
        firstDiagonal = [(row, row) for row in range(self.boardSize)]
        
        secondDiagonal = [(row, self.boardSize - 1 - row) for row in range(self.boardSize)]
        
        twoByTwos = []
        for row in range(self.boardSize - 1):
            for col in range(self.boardSize - 1):
                twoByTwos.append([
                    (row, col), (row, col+1),
                    (row+1, col), (row+1, col+1)
                ])
        
        corners = [
            (0, 0), (0, self.boardSize - 1),
            (self.boardSize - 1, 0), (self.boardSize - 1, self.boardSize - 1)
        ]

        winningCombos = rows + columns + [firstDiagonal, secondDiagonal] + twoByTwos + [corners]
        
        return winningCombos

    ################ checkWinner #################
    # Checks if there's a winner.
    #
    # Parameters: None
    #
    # Returns: bool - True if there's a winner, False otherwise.
    #############################################
    def checkWinner(self):
        for combo in self._winningCombos:
            results = set(self._currentMoves[n][m].label for n, m in combo)
            if len(results) == 1 and "" not in results:
                self._hasWinner = True
                self.winnerCombo = combo
                return True
        return False

    ############### anyMovesLeft #################
    # Checks if there are any moves left.
    #
    # Parameters: None
    #
    # Returns: bool - True if there are moves left, False otherwise.
    ##############################################
    def anyMovesLeft(self):
        return any(move.label == "" for row in self._currentMoves for move in row)

    ################ isGameOver ##################
    # Checks if the game is over.
    #
    # Parameters: None
    #
    # Returns: bool - True if the game is over, False otherwise.
    ##############################################
    def isGameOver(self):
        return self._hasWinner or not self.anyMovesLeft()

############### printBoard ##################
# Prints the current state of the game board to the console.
#
# Parameters:
# game: TicTacToeGame - The game instance to print the board for.
#
# Returns: None
############################################
def printBoard(game):
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear console screen
    print("Press 'q' to quit at any time.")
    print("Welcome to 4x4 Tic-Tac-Toe!")
    print(f"Player {game.currentPlayer.label}'s turn")
    print("   " + "   ".join(str(i) for i in range(game.boardSize)))
    print("  " + "----" * game.boardSize + "-")
    for i, row in enumerate(game._currentMoves):
        rowStr = f"{i} | " + " | ".join(move.label if move.label else " " for move in row) + " |"
        print(rowStr)
        print("  " + "----" * game.boardSize + "-")
    print()

############### getUserInput #################
# Get the input from user and validates it
#
# Parameters: 
# prompt: str
# validValues: list
#
# Returns: 
# user_input: int if a valid input is provided otherwise it will quit
#############################################
def getUserInput(prompt, validValues):
    while True:
        userInput = input(prompt).strip()  # Strip whitespace from input
        if userInput.lower() == 'q':
            print("Quitting the game...")
            exit()
        elif userInput.isdigit() and int(userInput) in validValues:
            return int(userInput)
        else:
            print("Invalid input! Please enter a number from the valid range.")

################### main ###################
# Create the game and run it.
#
# Parameters : None
#
# Returns: None
############################################
def main():
    game = TicTacToeGame()
    printBoard(game)

    while not game.isGameOver():
        row = getUserInput(
            f"Player {game.currentPlayer.name} - {game.currentPlayer.label}, enter row (0-{game.boardSize-1}) or 'q' to quit: ",
            list(range(game.boardSize))
        )
        col = getUserInput(
            f"Player {game.currentPlayer.name} - {game.currentPlayer.label}, enter column (0-{game.boardSize-1}) or 'q' to quit: ",
            list(range(game.boardSize))
        )
        
        move = Move(row, col, game.currentPlayer.label)
        if game._currentMoves[row][col].label == "":
            game._currentMoves[row][col] = move
            printBoard(game)
            if game.checkWinner():
                print(f"Player {game.currentPlayer.name} - {game.currentPlayer.label} wins!")
                break
            elif not game.anyMovesLeft():
                print("It's a tie!")
                break
            game.currentPlayer = next(game._players)
        else:
            print("Invalid move! Try again.")

if __name__ == "__main__":
    main()
