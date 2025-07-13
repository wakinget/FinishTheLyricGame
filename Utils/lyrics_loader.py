import pandas as pd

def load_lyrics(filepath: str):
    df = pd.read_excel(filepath, engine="openpyxl")
    df = df.dropna(subset=["lyric_snippet", "next_line"])
    return df.to_dict(orient="records")  # List of dicts
