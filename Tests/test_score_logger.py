import csv
import os
from Utils import score_logger


def test_log_game_result_creates_and_writes(tmp_path):
    # Redirect LOG_FILE to a temporary file
    test_log_path = tmp_path / "test_highscores.csv"

    # Patch the global LOG_FILE (quick & dirty approach for testing)
    score_logger.LOG_FILE = str(test_log_path)

    # Act: Log a fake result
    score_logger.log_game_result(score=25, rounds=5)

    # Assert: File exists and contains the expected row
    assert test_log_path.exists()

    with open(test_log_path, newline='') as f:
        reader = list(csv.reader(f))
        assert reader[0] == ["timestamp", "rounds", "score"]
        assert len(reader) == 2
        assert reader[1][1:] == ["5", "25"]  # Rounds, Score


def test_log_game_result_appends(tmp_path):
    # Patch path again
    test_log_path = tmp_path / "append_test.csv"
    score_logger.LOG_FILE = str(test_log_path)

    # Write two fake results
    score_logger.log_game_result(score=10, rounds=2)
    score_logger.log_game_result(score=15, rounds=3)

    with open(test_log_path, newline='') as f:
        rows = list(csv.reader(f))
        assert len(rows) == 3  # header + 2 results
