import tkinter as tk
from tkinter import ttk, messagebox
from DeckBuilder.genius_api import search_general, search_song

class DeckBuilderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lyric Deck Builder")
        self.root.geometry("800x900")

        self.deck_entries = []  # Stores final prompt-answer pairs

        self._build_search_section()
        self._build_search_results()
        self._build_lyric_viewer()
        self._build_snippet_entry()
        self._build_song_deck_preview()

    def _build_search_section(self):
        frame = ttk.LabelFrame(self.root, text="Search Songs")
        frame.pack(fill="x", padx=10, pady=10)

        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(frame, textvariable=self.search_var, width=50)
        search_entry.pack(side="left", padx=5)

        search_btn = ttk.Button(frame, text="Search", command=self.perform_search)
        search_btn.pack(side="left", padx=5)

    def _build_search_results(self):
        frame = ttk.LabelFrame(self.root, text="Search Results")
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.results_listbox = tk.Listbox(frame, height=10)
        self.results_listbox.pack(side="left", fill="both", expand=True)
        self.results_listbox.bind("<<ListboxSelect>>", self.on_result_select)

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.results_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.results_listbox.config(yscrollcommand=scrollbar.set)

        self.add_btn = ttk.Button(self.root, text="+ Add to Deck", command=self.add_selected_to_deck)
        self.add_btn.pack(pady=5)

    def _build_lyric_viewer(self):
        frame = ttk.LabelFrame(self.root, text="Lyrics Viewer")
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        fetch_btn = ttk.Button(frame, text="Fetch Lyrics", command=self.fetch_lyrics)
        fetch_btn.pack(anchor="w", padx=5, pady=5)

        self.lyrics_text = tk.Text(frame, wrap="word", height=15)
        self.lyrics_text.pack(fill="both", expand=True, padx=5, pady=5)
        self.lyrics_text.insert("1.0", "Lyrics will appear here...")

    def _build_snippet_entry(self):
        frame = ttk.LabelFrame(self.root, text="Add Prompt → Answer Pair")
        frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(frame, text="Lyric Snippet (Prompt):").pack(anchor="w")
        self.prompt_entry = tk.Text(frame, height=2, wrap="word")
        self.prompt_entry.pack(fill="x", padx=5, pady=2)

        ttk.Label(frame, text="Next Line (Answer):").pack(anchor="w")
        self.answer_entry = tk.Text(frame, height=2, wrap="word")
        self.answer_entry.pack(fill="x", padx=5, pady=2)

        add_btn = ttk.Button(frame, text="Add Prompt → Answer", command=self.store_snippet_pair)
        add_btn.pack(pady=5)

    def _build_song_deck_preview(self):
        frame = ttk.LabelFrame(self.root, text="Deck Preview")
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.deck_listbox = tk.Listbox(frame, height=10)
        self.deck_listbox.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.deck_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.deck_listbox.config(yscrollcommand=scrollbar.set)

    def perform_search(self):
        query = self.search_var.get()
        if not query:
            messagebox.showwarning("Missing Input", "Please enter a search query.")
            return

        self.results_listbox.delete(0, tk.END)
        self.search_results = search_general(query)

        if not self.search_results:
            messagebox.showinfo("No Results", "No songs found.")
            return

        for hit in self.search_results['hits']:
            song = hit['result']
            title = song['title']
            artist = song['primary_artist']['name']
            self.results_listbox.insert(tk.END, f"{title} — {artist}")

    def on_result_select(self, event):
        selection = self.results_listbox.curselection()
        if not selection:
            return
        index = selection[0]
        hit = self.search_results['hits'][index]['result']
        self.selected_song = {
            'title': hit['title'],
            'artist': hit['primary_artist']['name']
        }

    def fetch_lyrics(self):
        self.lyrics_text.delete("1.0", tk.END)
        if not hasattr(self, 'selected_song'):
            self.lyrics_text.insert("1.0", "No song selected!")
            return

        title = self.selected_song['title']
        artist = self.selected_song['artist']
        song = search_song(title, artist)
        if song and song.lyrics:
            self.lyrics_text.insert("1.0", song.lyrics)
        else:
            self.lyrics_text.insert("1.0", "Lyrics not found.")

    def add_selected_to_deck(self):
        if not hasattr(self, 'selected_song'):
            messagebox.showwarning("No Selection", "Please select a song first.")
            return

        title = self.selected_song['title']
        artist = self.selected_song['artist']
        self.deck_listbox.insert(tk.END, f"{title} — {artist}")

    def store_snippet_pair(self):
        if not hasattr(self, 'selected_song'):
            messagebox.showwarning("No Song Selected", "Please select a song before adding a lyric snippet.")
            return

        prompt = self.prompt_entry.get("1.0", tk.END).strip()
        answer = self.answer_entry.get("1.0", tk.END).strip()

        if not prompt or not answer:
            messagebox.showwarning("Missing Input", "Please provide both a prompt and an answer.")
            return

        entry = {
            "song_title": self.selected_song['title'],
            "artist": self.selected_song['artist'],
            "prompt": prompt,
            "answer": answer
        }
        self.deck_entries.append(entry)
        display_text = f"{entry['song_title']} — {entry['prompt']} → {entry['answer']}"
        self.deck_listbox.insert(tk.END, display_text)

        # Clear input fields
        self.prompt_entry.delete("1.0", tk.END)
        self.answer_entry.delete("1.0", tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = DeckBuilderApp(root)
    root.mainloop()
