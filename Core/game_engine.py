from Core.player import AIPlayer

class GameEngine:
    def __init__(self, board, playerI, playerII):
        self.board = board
        self.players = [playerI, playerII]
        self.currIdx = 0

    def play(self):
        self.board.printBoard()
        while not self.board.isFull():
            player = self.players[self.currIdx]
            print(f"\n{player.name}'s turn ({player.symbol})")

            try:
                x, y = player.getMove(self.board)
                if not self.board.validMove(x, y):
                    print("Invalid move. Try again.")
                    continue

                self.board.playMove(x, y, player.symbol)
                self.board.printBoard()

                if self.board.winCheck(x, y, player.symbol):
                    print(f"\n{player.name} ({player.symbol}) wins!")
                    player.addWin()
                    return

                self.currIdx = 1 - self.currIdx

            except (ValueError, TypeError):
                print("Invalid input format. Please enter two integers (row col).")
                continue
            except KeyboardInterrupt:
                print("\nGame interrupted.")
                return

        print("\nIt's a draw!")

    def step(self, move=None):
        player = self.players[self.currIdx]
        if isinstance(player, AIPlayer):
            x, y = player.getMove(self.board)
        else:
            if move is None:
                return {"status": "awaiting_input", "winner": None}
            x, y = move
        if not self.board.validMove(x, y):
            return {"status": "invalid", "winner": None}
        self.board.playMove(x, y, player.symbol)
        if self.board.winCheck(x, y, player.symbol):
            player.addWin()
            return {"status": "win", "winner": player.symbol, "winner_name": player.name}
        elif self.board.isFull():
            return {"status": "draw", "winner": None}
        else:
            self.currIdx = 1 - self.currIdx
            return {"status": "ongoing", "winner": None}