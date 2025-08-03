from DeckBuilder.genius_api import search_song

song = search_song("Bye Bye Bye", "NSYNC")
print(song.lyrics if song else "No lyrics found.")
