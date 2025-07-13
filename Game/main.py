import tkinter as tk
from Game.gui import LyricGameGUI

def start_game():
    root = tk.Tk()
    app = LyricGameGUI(root)
    root.mainloop()

if __name__ == "__main__":
    start_game()
