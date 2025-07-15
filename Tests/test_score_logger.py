"""
test_score_logger.py

Unit tests for the score_logger module. These tests verify that:
- Game results are correctly logged to a CSV file
- New logs are appended without overwriting
- The file structure and contents match expectations
"""

import csv
import os
from Utils import score_logger


def test_log_game_result_creates_and_writes(tmp_path):
    """
    Test that log_game_result() creates a new CSV file with a header
    and appends a correctly formatted row when called for the first time.
    """
    test_log_path = tmp_path / "test_highscores.csv"

    # Redirect global LOG_FILE to temp path
    score_logger.LOG_FILE = str(test_log_path)

    # Act
    score_logger.log_game_result(score=25, rounds=5)

    # Assert
    assert test_log_path.exists()

    with open(test_log_path, newline='') as f:
        reader = list(csv.reader(f))
        assert reader[0] == ["timestamp", "rounds", "score"]
        assert len(reader) == 2  # header + 1 data row
        assert reader[1][1:] == ["5", "25"]  # Rounds, Score (timestamp is dynamic)


def test_log_game_result_appends(tmp_path):
    """
    Test that calling log_game_result() multiple times appends new rows
    rather than overwriting the existing file.
    """
    test_log_path = tmp_path / "append_test.csv"
    score_logger.LOG_FILE = str(test_log_path)

    # Act: Log two entries
    score_logger.log_game_result(score=10, rounds=2)
    score_logger.log_game_result(score=15, rounds=3)

    # Assert: 1 header + 2 data rows
    with open(test_log_path, newline='') as f:
        rows = list(csv.reader(f))
        assert len(rows) == 3
        assert rows[0] == ["timestamp", "rounds", "score"]
