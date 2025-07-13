import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from Game.controller import get_random_lyric, check_guess

class LyricGameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Finish the Lyric")
        self.score = 0
        self.rounds_played = 0

        self.current_lyric = None

        self.lyric_label = tk.Label(root, text="Click 'Next' to begin!", wraplength=400, font=("Arial", 14))
        self.lyric_label.pack(pady=20)

        self.entry = tk.Entry(root, width=50, font=("Arial", 12))
        self.entry.pack(pady=10)

        # Score display
        self.score_label = tk.Label(root, text="Score: 0", font=("Arial", 12))
        self.score_label.pack()

        self.round_label = tk.Label(root, text="Rounds: 0", font=("Arial", 12))
        self.round_label.pack()

        self.submit_button = tk.Button(root, text="Submit Guess", command=self.submit_guess)
        self.submit_button.pack(pady=5)

        self.next_button = tk.Button(root, text="Next Lyric", command=self.load_new_lyric)
        self.next_button.pack(pady=5)

        self.new_game_button = tk.Button(root, text="Start New", command=self.start_new_game)
        self.new_game_button.pack(pady=5)

        self.end_game_button = tk.Button(root, text="End Game", command=self.end_game)
        self.end_game_button.pack(pady=5)

    def start_new_game(self):
        self.score = 0
        self.rounds_played = 0
        self.update_score_labels()
        self.lyric_label.config(text="Click 'Next' to begin!")
        self.entry.delete(0, tk.END)

    def end_game(self):
        summary = f"Game Over!\n\nFinal Score: {self.score}\nRounds Played: {self.rounds_played}"
        messagebox.showinfo("Game Summary", summary)

        # TODO: Log to CSV and generate chart

    def load_new_lyric(self):
        self.current_lyric = get_random_lyric()
        self.lyric_label.config(text=self.current_lyric['lyric_snippet'])
        self.entry.delete(0, tk.END)
        self.update_score_labels()

    def submit_guess(self):
        user_guess = self.entry.get()
        correct_answer = self.current_lyric['next_line']

        if check_guess(user_guess, correct_answer):
            self.score += 5
            messagebox.showinfo("Result", "Correct!")
        else:
            messagebox.showwarning("Result", f"Incorrect. The correct answer was:\n\n{correct_answer}")

        self.rounds_played += 1
        self.update_score_labels()

    def update_score_labels(self):
        self.score_label.config(text=f"Score: {self.score}")
        self.round_label.config(text=f"Rounds: {self.rounds_played}")


