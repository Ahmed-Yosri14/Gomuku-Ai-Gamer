import tkinter as tk
from tkinter import simpledialog, messagebox, Toplevel, Label, Entry, Button, Radiobutton, Frame, StringVar

try:
    from Core.board import Board
    from Core.player import HumanPlayer, AIPlayer
    from Core.game_engine import GameEngine
    from Ai.minimax import MiniMax
    from Ai.alphabeta import AlphaBeta
except ImportError:
    print("Warning: Core or Ai modules not found. Using placeholder classes.")
    class Board:
        def __init__(self, size):
            self.size = size
            self.grid = [['.' for _ in range(size)] for _ in range(size)]
        def is_valid_move(self, r, c):
            return 0 <= r < self.size and 0 <= c < self.size and self.grid[r][c] == '.'
        def place_stone(self, r, c, symbol):
            if self.is_valid_move(r,c):
                self.grid[r][c] = symbol
                return True
            return False
        def check_win(self, symbol): return False
        def is_full(self): return all(self.grid[r][c] != '.' for r in range(self.size) for c in range(self.size))
    class Player:
        def __init__(self, name, symbol): self.name, self.symbol = name, symbol
    class HumanPlayer(Player):
        def get_move(self, board): return None
    class AIPlayer(Player):
        def __init__(self, name, symbol, move_func): super().__init__(name, symbol); self.move_func = move_func
        def get_move(self, board): return self.move_func(board, self.symbol, 3)
    class GameEngine:
        def __init__(self, board, p1, p2): self.board, self.players, self.currIdx = board, [p1, p2], 0
        def step(self, move=None):
            player = self.players[self.currIdx]
            if isinstance(player, HumanPlayer):
                if move is None or not self.board.is_valid_move(move[0], move[1]): return {"status": "invalid"}
                r, c = move
            else:
                r, c = player.get_move(self.board)
                if not self.board.is_valid_move(r, c): return {"status": "error", "message": "AI generated invalid move"}
            self.board.place_stone(r, c, player.symbol)
            if self.board.check_win(player.symbol): return {"status": "win"}
            if self.board.is_full(): return {"status": "draw"}
            self.currIdx = 1 - self.currIdx
            return {"status": "continue"}
    class MiniMax:
        def __init__(self, playerOne, playerTwo, maxDepth): pass
        def FindBestMove(self, board, symbol): return (0,0)
    class AlphaBeta:
        def __init__(self, playerOne, playerTwo, maxDepth): pass
        def FindBestMove(self, board, symbol): return (0,1)

DARK_BG = "#2b2b2b"
DARK_BG_WIDGET = "#3d3d3d"
DARK_FG = "white"
DARK_ACCENT = "#555555"
DARK_LINE = "#888888"
DARK_INSERT = "white"

STONE_RADIUS_RATIO = 0.4
SYMBOL_TO_COLOR = {'X': 'black', 'O': 'white'}
SYMBOL_TO_NAME = {'X': 'Black', 'O': 'White'}

class GomokuGUI:
    def __init__(self, root, size, mode, names):
        self.root = root
        self.root.configure(bg=DARK_BG)
        self.size = size
        self.mode = mode
        self.names = names
        self.cell_size = 40
        board = Board(size)
        self.minimaxAlgo = MiniMax(playerOne='X', playerTwo='O', maxDepth=3)
        self.alphabetaAlgo = AlphaBeta(playerOne='X', playerTwo='O', maxDepth=2)

        if mode in ("1", "2"):
            self.switch_button = Button(root, text="Switch to AI vs AI", command=self.switch_to_ai_vs_ai,
                                        bg=DARK_BG_WIDGET, fg=DARK_FG, activebackground=DARK_ACCENT, activeforeground=DARK_FG)
            self.switch_button.pack(pady=6)

        def ai_move(b, symbol, depth):
            self.minimaxAlgo.playerOne = symbol
            self.minimaxAlgo.playerTwo = 'O' if symbol == 'X' else 'X'
            return self.minimaxAlgo.FindBestMove(b, symbol)

        def alpha_move(b, symbol, depth):
            self.alphabetaAlgo.playerOne = symbol
            self.alphabetaAlgo.playerTwo = 'O' if symbol == 'X' else 'X'
            return self.alphabetaAlgo.FindBestMove(b, symbol)

        if mode == "1":
            p1 = HumanPlayer(names[0], 'X')
            p2 = HumanPlayer(names[1], 'O')
        elif mode == "2":
            p1 = HumanPlayer(names[0], 'X')
            p2 = AIPlayer("AI Bot", 'O', alpha_move)
        else:
            p1 = AIPlayer("AI X", 'X', ai_move)
            p2 = AIPlayer("AI O", 'O', alpha_move)

        self.engine = GameEngine(board, p1, p2)
        self.awaiting_human_move = False

        self.canvas = tk.Canvas(root, bg=DARK_BG)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<Motion>", self.on_hover)
        self.hovered_cell = None

        self.status_var = StringVar()
        self.update_status_label()
        tk.Label(root, textvariable=self.status_var, font=("Arial", 14), fg=DARK_FG, bg=DARK_BG).pack(pady=8)

        self.root.geometry("1000x1000")
        self.center_window()
        self.root.minsize(600, 600)
        self.root.bind("<Configure>", self.on_resize)

        self.draw_board()
        self.root.after(100, self.next_turn)

    def center_window(self):
        self.root.update_idletasks()
        w = self.root.winfo_width()
        h = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (w // 2)
        y = (self.root.winfo_screenheight() // 2) - (h // 2)
        self.root.geometry(f'{w}x{h}+{x}+{y}')

    def play_ai_move(self):
        if not isinstance(self.engine.players[self.engine.currIdx], AIPlayer):
            return

        res = self.engine.step()
        self.draw_board()

        if res["status"] == "win":
            winner_name = self.engine.players[self.engine.currIdx].name
            messagebox.showinfo("Game Over", f"{winner_name} wins!")
            self.root.destroy()
        elif res["status"] == "draw":
            messagebox.showinfo("Game Over", "It's a draw!")
            self.root.destroy()
        else:
            self.update_status_label()
            self.root.after(100, self.next_turn)

    def switch_to_ai_vs_ai(self):
        def alpha_move(b, symbol, depth):
            self.alphabetaAlgo.playerOne = symbol
            self.alphabetaAlgo.playerTwo = 'O' if symbol == 'X' else 'X'
            return self.alphabetaAlgo.FindBestMove(b, symbol)

        self.engine.players[0] = AIPlayer("AI X", 'X', alpha_move)
        self.engine.players[1] = AIPlayer("AI O", 'O', alpha_move)
        self.awaiting_human_move = False
        self.status_var.set("Switched to AI vs AI mode")
        self.root.after(100, self.next_turn)

    def draw_board(self):
        self.canvas.delete("all")
        sz = self.cell_size
        for i in range(self.size):
            y = sz * i + sz // 2
            self.canvas.create_line(sz // 2, y, sz * self.size - sz // 2, y, fill=DARK_LINE)
        for j in range(self.size):
            x = sz * j + sz // 2
            self.canvas.create_line(x, sz // 2, x, sz * self.size - sz // 2, fill=DARK_LINE)

        for i in range(self.size):
            for j in range(self.size):
                symbol = self.engine.board.grid[i][j]
                if symbol in SYMBOL_TO_COLOR:
                    self.draw_stone(i, j, SYMBOL_TO_COLOR[symbol], filled=True)

        if self.hovered_cell and self.awaiting_human_move:
            row, col = self.hovered_cell
            color = SYMBOL_TO_COLOR[self.engine.players[self.engine.currIdx].symbol]
            self.draw_stone(row, col, color, filled=False)

    def draw_stone(self, row, col, color, filled=True):
        x = col * self.cell_size + self.cell_size // 2
        y = row * self.cell_size + self.cell_size // 2
        r = int(self.cell_size * STONE_RADIUS_RATIO)
        if filled:
            self.canvas.create_oval(x - r, y - r, x + r, y + r, fill=color, outline="gray20")
        else:
            self.canvas.create_oval(x - r, y - r, x + r, y + r, outline=color, width=2, stipple="gray50")

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
            self.root.after(100, self.next_turn)

    def on_hover(self, event):
        col = event.x // self.cell_size
        row = event.y // self.cell_size
        if 0 <= row < self.size and 0 <= col < self.size and self.engine.board.grid[row][col] == '.':
            self.hovered_cell = (row, col)
        else:
            self.hovered_cell = None
        self.draw_board()

    def on_resize(self, event):
        w, h = event.width, event.height
        size = min(w, h)
        self.cell_size = size // self.size
        self.canvas.config(width=self.cell_size * self.size, height=self.cell_size * self.size)
        self.draw_board()

    def update_status_label(self):
        player = self.engine.players[self.engine.currIdx]
        self.status_var.set(f"{player.name} ({SYMBOL_TO_NAME[player.symbol]}) to move")

    def next_turn(self):
        player = self.engine.players[self.engine.currIdx]
        if isinstance(player, HumanPlayer):
            self.awaiting_human_move = True
            self.update_status_label()
        else:
            self.awaiting_human_move = False
            self.update_status_label()
            self.root.after(100, self.play_ai_move)


def get_setup_gui():
    def center_window(win, width=400, height=300):
        screen_width = win.winfo_screenwidth()
        screen_height = win.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        win.geometry(f"{width}x{height}+{x}+{y}")

    def create_mode_selection():
        win = Toplevel()
        win.title("Gomoku Mode Selection")
        win.grab_set()
        center_window(win, 400, 200)
        win.configure(bg=DARK_BG)

        Label(win, text="Choose Game Mode:", font=("Arial", 14), fg=DARK_FG, bg=DARK_BG).pack(pady=10)

        mode_var = StringVar(value="1")

        radio_frame = Frame(win, bg=DARK_BG)
        radio_frame.pack(pady=10)

        modes = [
            ("Human vs Human", "1"),
            ("Human vs AI", "2"),
            ("AI vs AI", "3")
        ]

        for text, value in modes:
            rb = Radiobutton(
                radio_frame, text=text, variable=mode_var, value=value,
                font=("Arial", 12), fg=DARK_FG, bg=DARK_BG, selectcolor=DARK_BG_WIDGET,
                activebackground=DARK_BG, activeforeground=DARK_FG,
                highlightthickness=0,
                bd=0
            )
            rb.pack(anchor="w", padx=20, pady=5)

        def on_confirm(event=None):
            win.mode_result = mode_var.get()
            win.destroy()

        win.bind("<Return>", on_confirm)
        win.focus_set()

        win.wait_window()
        return getattr(win, 'mode_result', None)

    def create_entry_window(title, prompts):
        win = Toplevel()
        win.title(title)
        win.grab_set()
        center_window(win, 400, 100 + 60 * len(prompts))
        win.configure(bg=DARK_BG)

        entries = []
        result = []

        for prompt in prompts:
            label = Label(win, text=prompt, font=("Arial", 12), fg=DARK_FG, bg=DARK_BG)
            label.pack(pady=(10, 0))
            entry = Entry(win, font=("Arial", 12), bg=DARK_BG_WIDGET, fg=DARK_FG, insertbackground=DARK_INSERT)
            entry.pack(pady=5, ipadx=10)
            entries.append(entry)

        def submit(event=None):
            for e in entries:
                result.append(e.get().strip() or None)
            win.destroy()

        win.bind("<Return>", submit)
        win.focus_set()
        entries[0].focus_set()

        win.wait_window()
        return result

    root = tk.Tk()
    root.withdraw()

    mode = create_mode_selection()
    if mode is None:
        root.destroy()
        exit()

    size = None
    while size is None:
        [size_str] = create_entry_window("Board Size", ["Enter board size (5 to 30, default 15):"])
        if size_str is None:
            root.destroy()
            exit()
        try:
            size = int(size_str)
            if not (5 <= size <= 30):
                size = None
                messagebox.showerror("Invalid Size", "Please enter a number between 5 and 30")
        except:
            size = None
            messagebox.showerror("Invalid Size", "Please enter a valid number")

    if mode == "1":
        name1, name2 = create_entry_window("Player Names", ["Black stone name:", "White stone name:"])
        name1 = name1 or "Black"
        name2 = name2 or "White"
    elif mode == "2":
        [name1] = create_entry_window("Player Name", ["Your name (Black stones):"])
        name1 = name1 or "You"
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
    root.geometry("1000x1000")
    root.update_idletasks()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (1000 // 2)
    y = (screen_height // 2) - (1000 // 2)
    root.geometry(f"1000x1000+{x}+{y}")
    root.minsize(800, 800)
    GomokuGUI(root, size, mode, names)
    root.mainloop()

if __name__ == "__main__":
    main()