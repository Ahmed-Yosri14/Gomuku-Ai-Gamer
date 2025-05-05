import random


class Player:
    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol
        self.score = 0  

    def getMove(self, board):
        raise NotImplementedError()

    def addWin(self):
        self.score += 1 

    def __str__(self):
        return f"{self.name} ({self.symbol}) - Score: {self.score}"


class HumanPlayer(Player):
    def getMove(self, board):
        while True:
            move = input("Enter move (row col): ").strip()
            try:
                x, y = map(int, move.split())
                if board.validMove(x, y):
                    return x, y
            except:
                pass
            print("Invalid input. Try again.")


class AIPlayer(Player):
    def __init__(self, name, symbol, algorithm, depth=3):
        super().__init__(name, symbol)
        self.algorithm = algorithm
        self.depth = depth

    def getMove(self, board):
        move = self.algorithm(board, self.symbol, self.depth)
        if not board.validMove(*move):  # Validate AI move
            move = self.get_fallback_move(board)
        return move

    def get_fallback_move(self, board):
        """Get center or random valid move if AI fails"""
        center = board.l // 2
        if board.validMove(center, center):
            return (center, center)
        return random.choice(board.possibleMoves()) if board.possibleMoves() else (0,0)

