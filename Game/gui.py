import tkinter as tk
from tkinter import messagebox
from Game.controller import get_random_lyric, check_guess

class LyricGameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Finish the Lyric")

        self.current_lyric = None

        self.lyric_label = tk.Label(root, text="Click 'Next' to begin!", wraplength=400, font=("Arial", 14))
        self.lyric_label.pack(pady=20)

        self.entry = tk.Entry(root, width=50, font=("Arial", 12))
        self.entry.pack(pady=10)

        self.submit_button = tk.Button(root, text="Submit Guess", command=self.submit_guess)
        self.submit_button.pack(pady=5)

        self.next_button = tk.Button(root, text="Next Lyric", command=self.load_new_lyric)
        self.next_button.pack(pady=5)

    def load_new_lyric(self):
        self.current_lyric = get_random_lyric()
        self.lyric_label.config(text=self.current_lyric['lyric_snippet'])
        self.entry.delete(0, tk.END)

    def submit_guess(self):
        user_guess = self.entry.get()
        correct_answer = self.current_lyric['next_line']
        if check_guess(user_guess, correct_answer):
            messagebox.showinfo("Result", "Correct!")
        else:
            messagebox.showwarning("Result", f"Incorrect. The correct answer was:\n\n{correct_answer}")
