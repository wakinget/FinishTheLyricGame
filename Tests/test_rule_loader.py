import json
from Utils.rule_loader import load_game_rules

def test_load_game_rules_reads_valid_json(tmp_path):
    # Arrange: Create temporary game_rules.json
    test_data = {"show_answer": False, "points_per_correct": 10}
    json_path = tmp_path / "game_rules.json"
    with open(json_path, "w") as f:
        json.dump(test_data, f)

    # Act: Load from that custom path
    result = load_game_rules(path=json_path)

    # Assert
    assert isinstance(result, dict)
    assert result["show_answer"] is False
    assert result["points_per_correct"] == 10

def test_load_game_rules_missing_file(tmp_path):
    # Arrange: Point to a path that doesn't exist
    missing_path = tmp_path / "nonexistent.json"

    # Act & Assert
    try:
        load_game_rules(path=missing_path)
        assert False, "Expected FileNotFoundError"
    except FileNotFoundError:
        assert True

