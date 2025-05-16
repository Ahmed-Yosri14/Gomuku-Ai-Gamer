import tkinter as tk
from tkinter import messagebox
from Core.board import Board
from Core.player import HumanPlayer, AIPlayer
from Core.game_engine import GameEngine
from Ai.minimax import MiniMax
from Ai.alphabeta import AlphaBeta

STONE_RADIUS_RATIO = 0.40
SYMBOL_TO_COLOR    = {"X": "black", "O": "white"}
SYMBOL_TO_NAME     = {"X": "Black", "O": "White"}
DARK_BG    = "#1e1e1e"
BOARD_BG   = "#262626"
GRID_COLOR = "#555555"
LABEL_FG   = "#e0e0e0"
LABEL_BG   = DARK_BG
def center_window(win, w=None, h=None):
    win.update_idletasks()
    if w is None or h is None:
        w = win.winfo_width()
        h = win.winfo_height()
    x = (win.winfo_screenwidth()  - w) // 2
    y = (win.winfo_screenheight() - h) // 2
    win.geometry(f"{w}x{h}+{x}+{y}")


class GomokuGUI:
    def __init__(self, root: tk.Tk, size: int, mode: str, names):
        self.root, self.size, self.mode, self.names = root, size, mode, names
        self.cell_size = 40
        self.hover_cell = None

        root.configure(bg=DARK_BG)
        root.tk_setPalette(
            background=DARK_BG, foreground=LABEL_FG,
            activeBackground="#3a3a3a", activeForeground=LABEL_FG,
            highlightColor=LABEL_FG
        )

        board          = Board(size)
        self.minimax   = MiniMax(playerOne="X", playerTwo="O", maxDepth=2)
        self.alphabeta = AlphaBeta(playerOne="X", playerTwo="O", maxDepth=2)

        def minimax_move(b, symbol, depth):
            self.minimax.playerOne = symbol
            self.minimax.playerTwo = "O" if symbol == "X" else "X"
            return self.minimax.FindBestMove(b, symbol)

        def alphabeta_move(b, symbol, depth):
            self.alphabeta.playerOne = symbol
            self.alphabeta.playerTwo = "O" if symbol == "X" else "X"
            return self.alphabeta.FindBestMove(b, symbol)

        if mode == "1":
            p1 = HumanPlayer(names[0], "X")
            p2 = HumanPlayer(names[1], "O")
        elif mode == "2":
            p1 = HumanPlayer(names[0], "X")
            p2 = AIPlayer("AI Bot", "O", minimax_move)
        else:
            p1 = AIPlayer("AI X", "X", alphabeta_move)
            p2 = AIPlayer("AI O", "O", alphabeta_move)

        self.engine = GameEngine(board, p1, p2)
        self.awaiting_human_move = False

        self.canvas = tk.Canvas(
            root, width=size * self.cell_size, height=size * self.cell_size,
            bg=BOARD_BG, highlightthickness=0
        )
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<Motion>", self.on_motion)
        self.canvas.bind("<Leave>", self.on_leave)

        self.status_var = tk.StringVar()
        self.update_status_label()
        tk.Label(root, textvariable=self.status_var, font=("Arial", 14),
                 fg=LABEL_FG, bg=LABEL_BG).pack(pady=8)

        self.draw_board()
        self.root.after(100, self.next_turn)

    def draw_board(self):
        self.canvas.delete("all")
        sz = self.cell_size
        for i in range(self.size):
            y = sz * i + sz // 2
            self.canvas.create_line(sz // 2, y, sz*self.size - sz // 2, y,
                                    fill=GRID_COLOR, width=1)
        for j in range(self.size):
            x = sz * j + sz // 2
            self.canvas.create_line(x, sz // 2, x, sz*self.size - sz // 2,
                                    fill=GRID_COLOR, width=1)
        for i in range(self.size):
            for j in range(self.size):
                s = self.engine.board.grid[i][j]
                if s in SYMBOL_TO_COLOR:
                    self.draw_stone(i, j, SYMBOL_TO_COLOR[s])

    def draw_stone(self, r, c, color):
        x = c*self.cell_size + self.cell_size//2
        y = r*self.cell_size + self.cell_size//2
        rad = int(self.cell_size * STONE_RADIUS_RATIO)
        outline = "#aaaaaa" if color == "white" else "#404040"
        self.canvas.create_oval(x-rad, y-rad, x+rad, y+rad,
                                fill=color, outline=outline)

    def show_hover(self, r, c):
        self.canvas.delete("hover")
        self.hover_cell = (r, c)
        player = self.engine.players[self.engine.currIdx]
        outline = "#888888" if player.symbol == "X" else "#cccccc"
        x = c*self.cell_size + self.cell_size//2
        y = r*self.cell_size + self.cell_size//2
        rad = int(self.cell_size * STONE_RADIUS_RATIO)
        self.canvas.create_oval(x-rad, y-rad, x+rad, y+rad,
                                outline=outline, width=2, tags="hover")

    def clear_hover(self):
        self.canvas.delete("hover")
        self.hover_cell = None

    def on_click(self, event):
        if not self.awaiting_human_move: return
        c = event.x // self.cell_size
        r = event.y // self.cell_size
        self.clear_hover()
        res = self.engine.step(move=(r, c))
        self.awaiting_human_move = False
        self.draw_board()
        if res["status"] == "invalid":
            self.awaiting_human_move = True
            messagebox.showinfo("Invalid Move",
                                "That position is already taken!")
        elif res["status"] == "win":
            messagebox.showinfo("Game Over",
                                f"{self.engine.players[self.engine.currIdx].name} wins!")
            self.root.destroy()
        elif res["status"] == "draw":
            messagebox.showinfo("Game Over", "It's a draw!")
            self.root.destroy()
        else:
            self.update_status_label()

    def on_motion(self, event):
        if not self.awaiting_human_move: return
        c = event.x // self.cell_size
        r = event.y // self.cell_size
        if 0 <= r < self.size and 0 <= c < self.size \
           and self.engine.board.grid[r][c] == '.':
            if self.hover_cell != (r, c):
                self.show_hover(r, c)
        else:
            self.clear_hover()

    def on_leave(self, _): self.clear_hover()

    def update_status_label(self):
        p = self.engine.players[self.engine.currIdx]
        self.status_var.set(f"{p.name} ({SYMBOL_TO_NAME[p.symbol]}) to move")

    def next_turn(self):
        player = self.engine.players[self.engine.currIdx]
        if isinstance(player, HumanPlayer):
            self.awaiting_human_move = True
            self.update_status_label()
        else:
            self.awaiting_human_move = False
            res = self.engine.step()
            self.draw_board(); self.clear_hover()
            if res["status"] in ("win", "draw"):
                msg = (f"{self.engine.players[self.engine.currIdx].name} wins!"
                       if res["status"] == "win" else "It's a draw!")
                messagebox.showinfo("Game Over", msg)
                self.root.destroy()
                return
            else:
                self.update_status_label()
        self.root.after(100, self.next_turn)


def get_setup_gui():
    root = tk.Tk()
    root.title("Gomoku Setup")
    root.configure(bg=DARK_BG)
    root.tk_setPalette(background=DARK_BG, foreground=LABEL_FG,
                       activeBackground="#3a3a3a",
                       activeForeground=LABEL_FG, highlightColor=LABEL_FG)

    mode_var = tk.StringVar(value="1")
    tk.Label(root, text="Choose Mode:", fg=LABEL_FG, bg=DARK_BG,
             font=("Arial", 12, "bold")).pack(anchor="w", padx=10, pady=(10, 2))

    for text, val in (("Human vs Human", "1"),
                      ("Human vs AI",    "2"),
                      ("AI vs AI",       "3")):
        tk.Radiobutton(root, text=text, variable=mode_var, value=val,
                       selectcolor=DARK_BG, fg=LABEL_FG, bg=DARK_BG,
                       activebackground=DARK_BG,
                       highlightthickness=0).pack(anchor="w", padx=20)

    tk.Label(root, text="Board size (5–20):", fg=LABEL_FG, bg=DARK_BG,
             font=("Arial", 12, "bold")).pack(anchor="w", padx=10, pady=(10, 2))

    size_entry = tk.Entry(root, width=5, fg=LABEL_FG, bg="#404040",
                          insertbackground=LABEL_FG, highlightthickness=1,
                          highlightbackground="#555555")
    size_entry.insert(0, "15")
    size_entry.pack(anchor="w", padx=20, pady=(0, 12))

    def on_ok():
        txt = size_entry.get().strip()
        if not txt.isdigit():
            messagebox.showerror("Error", "Size must be an integer 5–20.",
                                 parent=root); return
        size = int(txt)
        if not 5 <= size <= 20:
            messagebox.showerror("Error", "Size must be between 5 and 20.",
                                 parent=root); return

        mode = mode_var.get()
        names = (["Black", "White"] if mode == "1"
                 else ["You", "AI Bot"] if mode == "2"
                 else ["AI Black", "AI White"])
        root.result = (size, mode, names)
        root.destroy()

    tk.Button(root, text="Start", command=on_ok,
              fg=LABEL_FG, bg="#3a3a3a", activebackground="#505050",
              relief="flat").pack(pady=(0, 18))

    root.update_idletasks()
    w = root.winfo_reqwidth() + 20
    h = root.winfo_reqheight() + 10
    root.geometry(f"{w}x{h}")
    center_window(root, w, h)
    root.resizable(False, False)

    root.mainloop()
    if not hasattr(root, "result"):
        exit()
    return root.result
def main():
    size, mode, names = get_setup_gui()
    root = tk.Tk()
    root.title("Gomoku")
    GomokuGUI(root, size, mode, names)
    root.update_idletasks()
    center_window(root)
    root.mainloop()


if __name__ == "__main__":
    main()