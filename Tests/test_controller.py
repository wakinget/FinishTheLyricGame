from Game import controller

def test_check_guess_exact_match():
    assert controller.check_guess("Let it be", "Let it be")

def test_check_guess_case_insensitive():
    assert controller.check_guess("LET IT BE", "let it be")

def test_check_guess_with_whitespace():
    assert controller.check_guess("  Let it be  ", "let it be")

def test_check_guess_incorrect():
    assert not controller.check_guess("Hello", "Goodbye")

def test_get_random_lyric_has_expected_fields():
    lyric = controller.get_random_lyric()
    assert isinstance(lyric, dict)
    assert "lyric_snippet" in lyric
    assert "next_line" in lyric

def test_get_random_lyric_from_custom_deck():
    fake_deck = [{"lyric_snippet": "Hey", "next_line": "Jude"}]
    result = controller.get_random_lyric(fake_deck)
    assert result["lyric_snippet"] == "Hey"
    assert result["next_line"] == "Jude"

