import json
import os


def load_game_rules():
    config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../Game/config/game_rules.json"))

    with open(config_path, 'r') as file:
        return json.load(file)
