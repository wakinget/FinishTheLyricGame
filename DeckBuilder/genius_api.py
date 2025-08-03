import os
from dotenv import load_dotenv
import lyricsgenius

# Load environment variables from .env file
load_dotenv()

# Try to get the API key from environment
api_key = os.getenv("GENIUS_API_KEY")

# Optional fallback prompt
if not api_key:
    print("⚠️ No Genius API key found in .env")
    api_key = input("Please enter your Genius API key: ")

# Initialize the Genius client
genius = lyricsgenius.Genius(api_key)

# Optional: Clean up results
genius.skip_non_songs = True
genius.remove_section_headers = True
genius.excluded_terms = ["(Remix)", "(Live)"]

# Example usage
def search_song(title, artist=None):
    return genius.search_song(title, artist)

def search_general(query, max_songs=10):
    return genius.search_songs(query, per_page=max_songs)
