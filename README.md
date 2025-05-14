# Gomoku AI Game

A Python-based AI engine to play **Gomoku (Five in a Row)**. Includes:
- **Human vs AI** mode using the Minimax algorithm
- **AI vs AI** mode using Minimax vs Alpha-Beta Pruning
- **GUI mode** for more user-friendly interaction

---

##  Game Overview

Gomoku is a strategy board game played on a grid. Players alternate turns to place marks on the board. The first player to align **five marks** in a row—**horizontally**, **vertically**, or **diagonally**—wins.

---

##  Project Features

- Board Size: Default **15x15**, but you can chose what you want ;)
- Three Game Modes:
  - Human vs Human
  - Human vs AI (Minimax)
  - AI vs AI (Minimax vs Alpha-Beta)
- AI algorithms:
  - Minimax (with depth limit)
  - Alpha-Beta Pruning
- Console and GUI versions available ;>

---

## Project Structure
Gomuku-Ai-Gamer/
├── Ai/
│ ├── alphabeta.py # Alpha-Beta Pruning algorithm
│ └── minimax.py # Minimax algorithm
│
├── Core/
│ ├── board.py # Board representation and rules
│ ├── game_engine.py # Game engine and logic
│ └── player.py # Player types (human, AI)
│
├── Modes/
│ ├── console_mode.py # Console interface for the game
│ └── gui_mode.py # GUI interface using Tkinter
│
├── Utils/
│ ├── display.py # Board display functions
│ └── move_parser.py # Input parser and validation
│
├── main.py # Entry point (Start Playing here!)
└── README.md # Project documentation


---

##  How to Run and Play the game on your PC

###  Requirements

- Python 3.x
- Tkinter (usually comes with standard Python installations)

Install missing dependencies if needed:

```bash
pip install -r requirements.txt
```

Make sure you are in the **`Gomuku-Ai-Gamer/`** folder, which contains `main.py`.  
For example:

```bash
cd <path/to>/Gomuku-Ai-Gamer  //put your path inside the <>
python main.py
```
Then Chose the **Mode** you want to play in :
**1** for the console Mode, and **2** for the GUI Mode (which is more fun, you know).

After that chose The Game Mode and Board size:
- Human vs Human
- Human vs AI (Minimax)
- AI vs AI

And **finally** tell us , Can you **beat** out game :>

