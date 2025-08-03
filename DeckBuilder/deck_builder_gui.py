import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
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
        self.deck_listbox.bind("<<ListboxSelect>>", self.on_deck_select)

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.deck_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.deck_listbox.config(yscrollcommand=scrollbar.set)

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill="x", pady=5)

        edit_btn = ttk.Button(btn_frame, text="Edit Selected", command=self.edit_selected_entry)
        edit_btn.pack(side="left", padx=5)

        delete_btn = ttk.Button(btn_frame, text="Delete Selected", command=self.delete_selected_entry)
        delete_btn.pack(side="left", padx=5)

        export_btn = ttk.Button(btn_frame, text="Export to CSV", command=self.export_to_csv)
        import_btn = ttk.Button(btn_frame, text="Import from CSV", command=self.import_from_csv)
        import_btn.pack(side="right", padx=5)
        export_btn.pack(side="right", padx=5)

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
        if song:
            self.selected_song['release_year'] = getattr(song, 'release_year', '')
            self.selected_song['album'] = getattr(song.album, 'name', '') if hasattr(song, 'album') and song.album else ''
        if song and song.lyrics:
            self.lyrics_text.insert("1.0", song.lyrics)
        else:
            self.lyrics_text.insert("1.0", "Lyrics not found.")

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
            "lyric_snippet": prompt,
            "next_line": answer,
            "release_year": self.selected_song.get('release_year', ''),
            "album": self.selected_song.get('album', '')
        }
        self.deck_entries.append(entry)
        display_text = f"{entry['song_title']} — {entry['lyric_snippet']} → {entry['next_line']}"
        self.deck_listbox.insert(tk.END, display_text)

        self.prompt_entry.delete("1.0", tk.END)
        self.answer_entry.delete("1.0", tk.END)

    def on_deck_select(self, event):
        selection = self.deck_listbox.curselection()
        if not selection:
            return
        index = selection[0]
        entry = self.deck_entries[index]
        self.prompt_entry.delete("1.0", tk.END)
        self.answer_entry.delete("1.0", tk.END)
        self.prompt_entry.insert("1.0", entry['lyric_snippet'])
        self.answer_entry.insert("1.0", entry['next_line'])

    def edit_selected_entry(self):
        selection = self.deck_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select an entry to edit.")
            return

        index = selection[0]
        new_prompt = self.prompt_entry.get("1.0", tk.END).strip()
        new_answer = self.answer_entry.get("1.0", tk.END).strip()

        if not new_prompt or not new_answer:
            messagebox.showwarning("Missing Input", "Please provide both a prompt and an answer.")
            return

        self.deck_entries[index]['lyric_snippet'] = new_prompt
        self.deck_entries[index]['next_line'] = new_answer

        display_text = f"[EDITED] {self.deck_entries[index]['song_title']} — {new_prompt} → {new_answer}"
        self.deck_listbox.delete(index)
        self.deck_listbox.insert(index, display_text)

    def delete_selected_entry(self):
        selection = self.deck_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select an entry to delete.")
            return
        index = selection[0]
        self.deck_listbox.delete(index)
        del self.deck_entries[index]

    def import_from_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if not file_path:
            return

        try:
            with open(file_path, mode="r", newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self.deck_entries.append(row)
                    display_text = f"{row['song_title']} — {row['lyric_snippet']} → {row['next_line']}"
                    self.deck_listbox.insert(tk.END, display_text)
            messagebox.showinfo("Import Successful", f"Deck imported from {file_path}")
        except Exception as e:
            messagebox.showerror("Import Failed", str(e))

    def export_to_csv(self):
        if not self.deck_entries:
            messagebox.showinfo("No Data", "There is nothing to export.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if not file_path:
            return

        try:
            with open(file_path, mode="w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=["lyric_snippet", "next_line", "song_title", "artist", "release_year", "album"])
                writer.writeheader()
                writer.writerows(self.deck_entries)
            messagebox.showinfo("Export Successful", f"Deck exported to {file_path}")
        except Exception as e:
            messagebox.showerror("Export Failed", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = DeckBuilderApp(root)
    root.mainloop()
