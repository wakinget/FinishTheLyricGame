"""
score_logger.py

Handles logging of game results to a CSV file and visualizing performance using Matplotlib.

This module allows you to persist player scores after each session and to
generate a summary chart that includes per-round scores and cumulative score tracking.

Functions:
    log_game_result(score, rounds): Logs a game result to a CSV file.
    plot_game_summary(round_scores): Displays a summary chart of a completed game.
"""

import csv
from datetime import datetime
import os
import matplotlib.pyplot as plt

# Absolute path to the high scores CSV log file
LOG_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "../Game/config/highscores.csv"))


def log_game_result(score: int, rounds: int):
    """
    Append a single game result to the highscores CSV log file.

    If the file does not exist, a header row will be created.

    Args:
        score (int): The total score achieved during the game.
        rounds (int): The number of rounds played in the game.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_row = [timestamp, rounds, score]

    file_exists = os.path.exists(LOG_FILE)

    with open(LOG_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["timestamp", "rounds", "score"])  # Write header
        writer.writerow(new_row)


def plot_game_summary(round_scores):
    """
    Display a summary chart of the game's round-by-round performance.

    The chart includes:
    - A bar chart of each round's score
    - A line plot of cumulative score over time
    - A title summarizing total and average score

    Args:
        round_scores (list[int]): A list of integers representing the score earned in each round.
    """
    total_score = sum(round_scores)
    average_score = total_score / len(round_scores)
    rounds = list(range(1, len(round_scores) + 1))
    cumulative_scores = [sum(round_scores[:i + 1]) for i in range(len(round_scores))]

    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Bar chart: score per round
    ax1.bar(rounds, round_scores, color='skyblue', label='Score per Round')

    # Line chart: cumulative score
    ax2 = ax1.twinx()
    ax2.plot(rounds, cumulative_scores, color='red', marker='o', label='Cumulative Score')

    # Labels and layout
    ax1.set_xlabel('Round')
    ax1.set_ylabel('Score per Round', color='skyblue')
    ax2.set_ylabel('Cumulative Score', color='red')
    plt.title(f"Game Summary\nTotal: {total_score} | Average per Round: {average_score:.2f}")

    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')
    plt.tight_layout()
    plt.show()
