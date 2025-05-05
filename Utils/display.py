def printWelcome():
    print("=" * 30)
    print("      Welcome to Gomoku      ")
    print("=" * 30)

def printScores(players):
    print("\nScores:")
    if not players:
        print("No players yet!")
    else:
        for player in players:
            print(f"{player.name} ({player.symbol}) - {player.score}")

def printTurn(player):
    print(f"\n{player.name}'s turn ({player.symbol})")

def printWinner(player):
    print(f"\n{player.name} wins! 🎉")

def printDraw():
    print("\nIt's a draw! 🙁")

def printInvalid():
    print("\nInvalid move. Try again. 🔴")
