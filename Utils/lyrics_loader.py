"""
lyrics_loader.py

Loads a lyric deck from an Excel file and returns a clean, structured list
of lyric entries suitable for use in the lyric guessing game.
"""

import pandas as pd


def load_lyrics(filepath: str):
    """
    Load a lyric deck from an Excel (.xlsx) file.

    The file must contain at least the columns 'lyric_snippet' and 'next_line'.
    Rows with missing values in those columns will be excluded.

    Args:
        filepath (str): The path to the Excel file containing the lyric deck.

    Returns:
        list[dict]: A list of dictionaries, where each dictionary represents
            a lyric entry with keys like:
            {
                "lyric_snippet": "Some lyric...",
                "next_line": "The next line...",
                "song_title": "Title",
                "artist": "Artist Name",
                ...
            }
    """
    df = pd.read_excel(filepath, engine="openpyxl")
    df = df.dropna(subset=["lyric_snippet", "next_line"])
    return df.to_dict(orient="records")  # List of lyric entries
