"""
controller.py

Provides core game logic for the Finish the Lyric game, including random lyric selection
and answer checking. This module interacts with the loaded lyric deck and contains
pure functions that can be tested independently of the GUI.

Functions:
    get_random_lyric(deck=None): Returns a random lyric entry from the deck.
    check_guess(user_input, correct_answer): Checks if a user's guess is correct.
"""

import os
import random
from Utils.lyrics_loader import load_lyrics

# Default path to the main lyric deck (resolved relative to this file)
LYRICS_FILE = "../Lyrics/Master_Lyric_Deck.xlsx"
_lyrics_deck = load_lyrics(os.path.abspath(os.path.join(os.path.dirname(__file__), LYRICS_FILE)))


def get_random_lyric(deck=None):
    """
    Retrieve a random lyric entry from the given deck or the default lyric deck.

    Args:
        deck (list[dict], optional): A list of lyric entries. Each entry must contain
            at least 'lyric_snippet' and 'next_line' keys. If not provided, the
            function will use the globally loaded deck from the main Excel file.

    Returns:
        dict: A randomly selected lyric entry with keys like 'lyric_snippet' and 'next_line'.
    """
    if deck is None:
        deck = _lyrics_deck
    return random.choice(deck)


def check_guess(user_input: str, correct_answer: str) -> bool:
    """
    Compare the player's guess to the correct answer.

    This check is case-insensitive and ignores leading/trailing whitespace.

    Args:
        user_input (str): The player's input string.
        correct_answer (str): The correct lyric line from the deck.

    Returns:
        bool: True if the guess matches the answer, False otherwise.
    """
    return user_input.strip().lower() == correct_answer.strip().lower()
