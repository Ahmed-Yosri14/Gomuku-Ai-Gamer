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
                    return

                self.currIdx = 1 - self.currIdx

            except (ValueError, TypeError):
                print("Invalid input format. Please enter two integers (row col).")
                continue

            except KeyboardInterrupt:
                print("\nGame interrupted.")
                return

        print("\nIt's a draw!")
