class GameEngine:
    def __init__(self, board, playerI, playerII):
        self.board = board
        self.players = [playerI, playerII]
        self.currIdx = 0

    def play(self):
        while True:
            player = self.players[self.currIdx]
            print(f"\n{player.name}'s turn ({player.symbol})")
            self.board.printBoard()

            x, y = player.getMove(self.board)

            if self.board.playMove(x, y, player.symbol):
                if self.board.winCheck(x, y, player.symbol):
                    self.board.printBoard()
                    print(f"\n{player.name} wins!")
                    player.addWin()
                    break
                elif self.board.isFull():
                    self.board.printBoard()
                    print("\nIt's a draw!")
                    break
                self.currIdx = 1 - self.currIdx
            else:
                print("Invalid move. Try again.")
