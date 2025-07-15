import json
import os


def load_game_rules(path=None):
    if path is None:
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../Game/config/game_rules.json"))
    with open(path, 'r') as file:
        return json.load(file)
