from Modes.gui_mode import main as gui_main
from Modes.console_mode import run_console

if __name__ == "__main__":
    mode = input("1. Console\n2. GUI\nChoose: ")
    if mode == "2":
        gui_main()
    else:
        run_console()