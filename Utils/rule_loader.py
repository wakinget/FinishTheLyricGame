"""
rule_loader.py

Loads configuration rules for the Finish the Lyric game from a JSON file.

The rules define gameplay behavior such as whether to show the correct answer,
bonus scoring, hint availability, and other toggles.
"""

import json
import os


def load_game_rules(path=None):
    """
    Load game rules from a JSON configuration file.

    If no path is provided, the function loads the default file located at
    'Game/config/game_rules.json' (resolved relative to this file).

    Args:
        path (str, optional): The full or relative path to the JSON rules file.
            If None, a default internal path is used.

    Returns:
        dict: A dictionary of game rule settings. Example:
            {
                "show_answer": true,
                "points_per_correct": 5,
                "artist_bonus": 1,
                "hint_cost": 2
            }

    Raises:
        FileNotFoundError: If the specified file does not exist.
        json.JSONDecodeError: If the file is not valid JSON.
    """
    if path is None:
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../Game/config/game_rules.json"))

    with open(path, 'r') as file:
        return json.load(file)
