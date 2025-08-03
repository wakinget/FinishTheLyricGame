import os
from dotenv import load_dotenv
import lyricsgenius

# Load environment variables from .env file
load_dotenv()

# Get Genius API token from environment variable
GENIUS_API_KEY = os.getenv("GENIUS_API_KEY")

# Initialize the Genius API client
# Remove section headers like [Chorus], [Verse], etc.
# Skip non-song results (like interviews)
genius = lyricsgenius.Genius(GENIUS_API_KEY)
genius.remove_section_headers = True
genius.skip_non_songs = True
genius.excluded_terms = ["(Remix)", "(Live)"]

def search_general(query, max_songs=10):
    """
    Search for songs using a general query.

    Args:
        query (str): The search string.
        max_songs (int): Maximum number of songs to return.

    Returns:
        dict: The search results including song metadata.
    """
    try:
        return genius.search_songs(query, per_page=max_songs)
    except Exception as e:
        print(f"Search failed: {e}")
        return None

def search_song(title, artist=None):
    """
    Search for a specific song by title and optionally artist, and fetch lyrics and release year.

    Args:
        title (str): Song title.
        artist (str): Optional artist name.

    Returns:
        object: lyricsgenius Song object with added 'release_year' attribute if available.
    """
    try:
        song = genius.search_song(title, artist)
        if song:
            # Attempt to extract release year from release_date if available
            release_date = getattr(song, 'release_date', None)
            if release_date and isinstance(release_date, str):
                song.release_year = release_date.split('-')[0]  # Extract only the year part
            else:
                song.release_year = ""

            # Extract album name if available
            song.album = getattr(song, 'album', {}).get('name', '') if hasattr(song, 'album') and song.album else ""

            return song
        return None


    except Exception as e:
        print(f"Failed to fetch song: {e}")
        return None
