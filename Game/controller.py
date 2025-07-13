import random
from Utils.lyrics_loader import load_lyrics

LYRICS_FILE = "../Lyrics/Master_Lyric_Deck.xlsx"
_lyrics_deck = load_lyrics(LYRICS_FILE)

def get_random_lyric():
    return random.choice(_lyrics_deck)

def check_guess(user_input: str, correct_answer: str) -> bool:
    return user_input.strip().lower() == correct_answer.strip().lower()
