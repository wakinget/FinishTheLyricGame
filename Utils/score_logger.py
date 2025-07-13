import csv
from datetime import datetime
import os
import matplotlib.pyplot as plt


LOG_FILE = os.path.join(os.path.dirname(__file__), "../Game/config/highscores.csv")
LOG_FILE = os.path.abspath(LOG_FILE)
def log_game_result(score: int, rounds: int):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_row = [timestamp, rounds, score]

    file_exists = os.path.exists(LOG_FILE)

    with open(LOG_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["timestamp", "rounds", "score"])  # header
        writer.writerow(new_row)

def plot_game_summary(round_scores):
    total_score = sum(round_scores)
    average_score = total_score / len(round_scores)
    rounds = list(range(1, len(round_scores) + 1))
    cumulative_scores = [sum(round_scores[:i+1]) for i in range(len(round_scores))]

    fig, ax1 = plt.subplots(figsize=(10, 6))

    ax1.bar(rounds, round_scores, color='skyblue', label='Score per Round')
    ax2 = ax1.twinx()
    ax2.plot(rounds, cumulative_scores, color='red', marker='o', label='Cumulative Score')

    ax1.set_xlabel('Round')
    ax1.set_ylabel('Score per Round', color='skyblue')
    ax2.set_ylabel('Cumulative Score', color='red')
    plt.title(f"Game Summary\nTotal: {total_score} | Average per Round: {average_score:.2f}")

    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')
    plt.tight_layout()
    plt.show()
