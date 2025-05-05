from Ai.minimax import MiniMax
from Core.board import Board
from Core.player import HumanPlayer, AIPlayer
from Core.game_engine import GameEngine
from Utils.display import *

def run_console():
    printWelcome()
    mode = input("Choose mode (1=HvH, 2=HvAI, 3=AIvAI): ").strip()

    size = input("Enter board size (default 15): ").strip()
    size = int(size) if size.isdigit() else 15
    board = Board(size)
    minimaxAlgo = MiniMax(playerOne='X', playerTwo='O', maxDepth=3)

    def ai_move(b, symbol, depth):
        # Configure minimax with the correct player symbols
        minimaxAlgo.playerOne = symbol
        minimaxAlgo.playerTwo = 'O' if symbol == 'X' else 'X'
        return minimaxAlgo.FindBestMove(b, symbol)

    if mode == "1":
        name1 = input("Player 1 name: ")
        name2 = input("Player 2 name: ")
        p1 = HumanPlayer(name1, 'X')
        p2 = HumanPlayer(name2, 'O')
    elif mode == "2":
        name = input("Your name: ")
        p1 = HumanPlayer(name, 'X')
         # TODO: Replace (0, 0) with real AI move using minimax/alpha-beta later

        p2 = AIPlayer("AI Bot", 'O', ai_move)
    else:
         # TODO: Replace (0, 0) with real AI move using minimax/alpha-beta later
        p1 = AIPlayer("AI X", 'X', lambda b, s, d: (0, 0))
        p2 = AIPlayer("AI O", 'O', lambda b, s, d: (0, 0))

    game = GameEngine(board, p1, p2)
    game.play()
    printScores([p1, p2])
