import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from Game.controller import get_random_lyric, check_guess
from Utils.score_logger import plot_game_summary, log_game_result
from Utils.rule_loader import load_game_rules


class LyricGameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Finish the Lyric")
        self.score = 0
        self.rounds_played = 0
        self.round_scores = []  # Tracks score each round
        self.rules = load_game_rules()

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

        if self.round_scores:
            plot_game_summary(self.round_scores)
            log_game_result(self.score, self.rounds_played)

    def load_new_lyric(self):
        self.current_lyric = get_random_lyric()
        self.lyric_label.config(text=self.current_lyric['lyric_snippet'])
        self.entry.delete(0, tk.END)
        self.update_score_labels()

    def submit_guess(self):
        user_guess = self.entry.get()
        correct_answer = self.current_lyric['next_line']

        result = check_guess(user_guess, correct_answer)
        if result:
            score_this_round = 5
            messagebox.showinfo("Result", "Correct!")
        else:
            score_this_round = 0
            if self.rules.get("show_answer", True):
                messagebox.showwarning("Result", f"Incorrect! The correct answer was:\n\n{correct_answer}")
            else:
                messagebox.showwarning("Result", "Incorrect!")

        # Updates
        self.score += score_this_round
        self.round_scores.append(score_this_round)
        self.rounds_played += 1
        self.update_score_labels()

    def update_score_labels(self):
        self.score_label.config(text=f"Score: {self.score}")
        self.round_label.config(text=f"Rounds: {self.rounds_played}")


