# DeckBuilder/__main__.py
from .deck_builder_gui import DeckBuilderApp
import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    app = DeckBuilderApp(root)
    root.mainloop()
