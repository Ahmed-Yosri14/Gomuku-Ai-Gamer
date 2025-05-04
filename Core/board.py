class Board:
    def __init__(self, l=15): # defult 15 but it can be square of any l
        self.l = l
        self.grid = [['.' for _ in range(l)] for _ in range(l)]

    def validMove(self, x, y):
        if 0 <= x < self.l and 0 <= y < self.l and self.grid[x][y] == '.':
            return True
        return False
    
    def playMove(self, x, y, X_O):
        if self.validMove(x, y):
            self.grid[x][y] = X_O
            return True
        return False

    def isFull(self):
        ok=True
        for row in self.grid :
            for cell in row:
                if cell == '.':
                    ok = False
                    break
        return ok
    

    def possibleMoves(self):
        all = []
        for i in self.l:
            for j in self.l:
                if self.grid[i][j] == '.':
                    all.append((i,j))
        return all

    def winCheck(self, x, y, X_O):
        def count(dx, dy):
            i = x + dx
            j = y + dy
            c = 0
            while 0 <= i < self.l and 0 <= j < self.l and self.grid[i][j] == X_O:
                count += 1
                i += dx
                j += dy
            return count

        dxdy= [(1,0), (0,1), (1,1), (1,-1)]
        for dx, dy in dxdy:
            if 1 + count(dx, dy) + count(-dx, -dy) >= 5: # counting upwand and downward( if it was two parts in the same directions starting from the current point)
                return True
        return False

    def makeBoard(self):
        nwBoard = Board(self.size)
        nwBoard.grid = [row[:] for row in self.grid]
        return nwBoard

    def printBoard(self):
        print("  ", end="")
        for i in range(self.size):
            print(f"{i:2}", end=" ")
        print()

        for idx in range(self.size):
            print(f"{idx:2} ", end="")
            for cell in self.grid[idx]:
                print(f"{cell}  ", end="")
            print() 
