"""
test_rule_loader.py

Unit tests for the rule_loader module. These tests verify that:
- Game rules are correctly loaded from a JSON file
- Missing files raise the appropriate error
"""

import json
from Utils.rule_loader import load_game_rules


def test_load_game_rules_reads_valid_json(tmp_path):
    """
    Test that load_game_rules() correctly loads a well-formed JSON file
    and returns a dictionary with the expected key-value pairs.

    Args:
        tmp_path (pathlib.Path): A pytest fixture that provides a temporary directory.
    """
    # Arrange: Create a temporary game_rules.json with test data
    test_data = {"show_answer": False, "points_per_correct": 10}
    json_path = tmp_path / "game_rules.json"
    with open(json_path, "w") as f:
        json.dump(test_data, f)

    # Act: Load from that custom path
    result = load_game_rules(path=json_path)

    # Assert: Values match what was written
    assert isinstance(result, dict)
    assert result["show_answer"] is False
    assert result["points_per_correct"] == 10


def test_load_game_rules_missing_file(tmp_path):
    """
    Test that load_game_rules() raises a FileNotFoundError
    when the specified JSON path does not exist.

    Args:
        tmp_path (pathlib.Path): A pytest fixture that provides a temporary directory.
    """
    # Arrange: Define a path that does not point to any file
    missing_path = tmp_path / "nonexistent.json"

    # Act & Assert
    try:
        load_game_rules(path=missing_path)
        assert False, "Expected FileNotFoundError"
    except FileNotFoundError:
        assert True
