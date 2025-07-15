"""
test_controller.py

Unit tests for the Game.controller module. These tests validate:
- Lyric matching logic (case, whitespace, correctness)
- Structure and behavior of get_random_lyric() with both default and custom decks
"""

from Game import controller


def test_check_guess_exact_match():
    """
    Test that check_guess() returns True for an exact match.
    """
    assert controller.check_guess("Let it be", "Let it be")


def test_check_guess_case_insensitive():
    """
    Test that check_guess() is case-insensitive.
    """
    assert controller.check_guess("LET IT BE", "let it be")


def test_check_guess_with_whitespace():
    """
    Test that check_guess() trims leading/trailing whitespace before comparing.
    """
    assert controller.check_guess("  Let it be  ", "let it be")


def test_check_guess_incorrect():
    """
    Test that check_guess() returns False for a clearly wrong guess.
    """
    assert not controller.check_guess("Hello", "Goodbye")


def test_get_random_lyric_has_expected_fields():
    """
    Test that get_random_lyric() returns a dictionary containing
    the required keys from the default deck.
    """
    lyric = controller.get_random_lyric()
    assert isinstance(lyric, dict)
    assert "lyric_snippet" in lyric
    assert "next_line" in lyric


def test_get_random_lyric_from_custom_deck():
    """
    Test that get_random_lyric() can return a result from a provided custom deck.
    """
    fake_deck = [{"lyric_snippet": "Hey", "next_line": "Jude"}]
    result = controller.get_random_lyric(fake_deck)
    assert result["lyric_snippet"] == "Hey"
    assert result["next_line"] == "Jude"
