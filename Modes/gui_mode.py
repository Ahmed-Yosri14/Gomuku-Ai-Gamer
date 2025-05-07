import tkinter as tk
from tkinter import simpledialog, messagebox
from Core.board import Board
from Core.player import HumanPlayer, AIPlayer
from Core.game_engine import GameEngine
from Ai.minimax import MiniMax
from Ai.alphabeta import AlphaBeta

STONE_RADIUS_RATIO = 0.4
SYMBOL_TO_COLOR = {'X': 'black', 'O': 'white'}
SYMBOL_TO_NAME = {'X': 'Black', 'O': 'White'}

class GomokuGUI:
    def __init__(self, root, size, mode, names):
        self.root = root
        self.size = size
        self.mode = mode
        self.names = names
        self.cell_size = 40
        board = Board(size)
        minimaxAlgo = MiniMax(playerOne='X', playerTwo='O', maxDepth=3)
        alphabetaAlgo = AlphaBeta(playerOne='X', playerTwo='O', maxDepth=3)

        def ai_move(b, symbol, depth):
            # Configure minimax with the correct player symbols
            minimaxAlgo.playerOne = symbol
            minimaxAlgo.playerTwo = 'O' if symbol == 'X' else 'X'
            return minimaxAlgo.FindBestMove(b, symbol)

        def alpha_move(b, symbol, depth):
            alphabetaAlgo.playerOne = symbol
            alphabetaAlgo.playerTwo = 'O' if symbol == 'X' else 'X'
            return alphabetaAlgo.FindBestMove(b, symbol)
        if mode == "1":  # H vs H
            p1 = HumanPlayer(names[0], 'X')
            p2 = HumanPlayer(names[1], 'O')
        elif mode == "2":  # H vs AI
            p1 = HumanPlayer(names[0], 'X')
            p2 = AIPlayer("AI Bot", 'O', ai_move)
        else:  # AI vs AI
            p1 = AIPlayer("AI X", 'X', lambda b, s, d: ai_move(b, s, d))
            p2 = AIPlayer("AI O", 'O', lambda b, s, d: alpha_move(b, s, d))
        self.engine = GameEngine(board, p1, p2)
        self.awaiting_human_move = False

        self.canvas = tk.Canvas(root, width=size * self.cell_size, height=size * self.cell_size, bg="burlywood")
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_click)
        self.status_var = tk.StringVar()
        self.update_status_label()
        tk.Label(root, textvariable=self.status_var, font=("Arial", 14)).pack(pady=8)

        self.draw_board()
        self.root.after(100, self.next_turn)

    def draw_board(self):
        self.canvas.delete("all")
        sz = self.cell_size
        for i in range(self.size):
            y = sz * i + sz // 2
            self.canvas.create_line(sz // 2, y, sz * self.size - sz // 2, y)
        for j in range(self.size):
            x = sz * j + sz // 2
            self.canvas.create_line(x, sz // 2, x, sz * self.size - sz // 2)
        for i in range(self.size):
            for j in range(self.size):
                symbol = self.engine.board.grid[i][j]
                if symbol in SYMBOL_TO_COLOR:
                    self.draw_stone(i, j, SYMBOL_TO_COLOR[symbol])

    def draw_stone(self, row, col, color):
        x = col * self.cell_size + self.cell_size // 2
        y = row * self.cell_size + self.cell_size // 2
        r = int(self.cell_size * STONE_RADIUS_RATIO)
        self.canvas.create_oval(x - r, y - r, x + r, y + r, fill=color, outline="gray20")

    def on_click(self, event):
        if not self.awaiting_human_move:
            return
        col = event.x // self.cell_size
        row = event.y // self.cell_size
        res = self.engine.step(move=(row, col))
        self.awaiting_human_move = False
        self.draw_board()
        if res["status"] == "invalid":
            self.awaiting_human_move = True
            messagebox.showinfo("Invalid Move", "That position is already taken!")
        elif res["status"] == "win":
            winner_name = self.engine.players[self.engine.currIdx].name
            messagebox.showinfo("Game Over", f"{winner_name} wins!")
            self.root.destroy()
        elif res["status"] == "draw":
            messagebox.showinfo("Game Over", "It's a draw!")
            self.root.destroy()
        else:
            self.update_status_label()

    def update_status_label(self):
        player = self.engine.players[self.engine.currIdx]
        self.status_var.set(f"{player.name} ({SYMBOL_TO_NAME[player.symbol]}) to move")

    def next_turn(self):
        player = self.engine.players[self.engine.currIdx]
        if isinstance(player, HumanPlayer):
            self.awaiting_human_move = True
            self.update_status_label()
        else:  # AI's turn
            self.awaiting_human_move = False
            res = self.engine.step()
            self.draw_board()
            if res["status"] == "win":
                winner_name = self.engine.players[self.engine.currIdx].name
                messagebox.showinfo("Game Over", f"{winner_name} wins!")
                self.root.destroy()
                return
            elif res["status"] == "draw":
                messagebox.showinfo("Game Over", "It's a draw!")
                self.root.destroy()
                return
            else:
                self.update_status_label()
        self.root.after(100, self.next_turn)

def get_setup_gui():
    root = tk.Tk()
    root.withdraw()

    # Mode
    while True:
        mode = simpledialog.askstring(
            "Gomoku Mode",
            "Choose mode:\n1: Human vs Human\n2: Human vs AI\n3: AI vs AI",
            parent=root)
        if mode in ("1", "2", "3"):
            break
        if mode is None:
            root.destroy()
            exit()

    # Size
    while True:
        size = simpledialog.askinteger("Board Size", "Enter board size (default 15):",
                                       minvalue=5, maxvalue=30, parent=root)
        if size:
            break
        if size is None:
            root.destroy()
            exit()

    # Names
    if mode == "1":
        name1 = simpledialog.askstring("Player 1", "Black stone name:", parent=root) or "Black"
        name2 = simpledialog.askstring("Player 2", "White stone name:", parent=root) or "White"
    elif mode == "2":
        name1 = simpledialog.askstring("Player", "Your name (Black stones):", parent=root) or "You"
        name2 = "AI Bot"
    else:
        name1 = "AI Black"
        name2 = "AI White"
    root.destroy()
    return int(size), mode, [name1, name2]

def main():
    size, mode, names = get_setup_gui()
    root = tk.Tk()
    root.title("Gomoku")
    GomokuGUI(root, size, mode, names)
    root.mainloop()

if __name__ == "__main__":
    main()