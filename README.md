# 🎶 Finish the Lyric Game

A Python-based desktop game where players test their lyrical memory by completing lines from popular songs. The game presents a lyric snippet from a randomly selected song, and players must guess the next line. Features include scoring, round tracking, visual summaries, and rule customization.

---

## 🧩 Features

- 🎵 Randomly selected lyric snippets from an Excel-based deck
- ✍️ Free-form text input with case- and whitespace-insensitive matching
- 🧮 Scoring system: +5 points per correct guess
- 📊 End-of-game summary chart (per-round + cumulative score)
- 🗃 Score logging to a CSV high score file
- ⚙️ Configurable game rules via JSON (e.g., show/hide correct answer)
- 🖼 Simple Tkinter GUI for easy gameplay
- ✅ Unit tests for core modules (controller, logger, rules, etc.)

---

## 🎮 How to Play

1. Launch the game.
2. Click **"Next Lyric"** to begin.
3. Read the lyric snippet and type the next line into the text box.
4. Click **"Submit Guess"** to check your answer and update your score.
5. Click **"Start New"** to reset the game at any time.
6. When you're done, click **"End Game"** to log your score and view a visual summary.

---

## 🛠 Installation

### Requirements

- Python 3.9+
- pandas
- openpyxl
- matplotlib
- pytest (for testing)

### Installation Steps

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/FinishTheLyricGame.git
   cd FinishTheLyricGame
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## 🚀 Running the Game

From the project root, run:
```bash
python Game/main.py
```

Make sure you have a valid lyrics deck located at:
```
Lyrics/Master_Lyric_Deck.xlsx
```
Each row should contain at least:
- `lyric_snippet`
- `next_line`

Optional columns include: `song_title`, `artist`, `genre`, `release_year`.

---

## ⚙️ Game Configuration

You can customize gameplay behavior by editing the JSON config file:

**`Game/config/game_rules.json`**
```json
{
  "show_answer": true,
  "points_per_correct": 5,
  "artist_bonus": 1,
  "hint_cost": 2
}
```

---

## 📈 Score Logging

Each game session is logged to:
```
Game/config/highscores.csv
```

Logged fields:
- Timestamp
- Rounds played
- Final score

---

## 🧪 Running Tests

All core modules are tested using `pytest`.

To run all tests:
```bash
pytest
```

Tests are located in the `/tests` directory and cover:
- Game logic (`controller`)
- Rule loading
- Score logging
- Lyric deck loading

---

## 🛣 Roadmap

Planned features include:
- 🎁 Bonus guesses for artist and song title
- 💡 Hint system (at point cost)
- 🎮 Menu screen to select game mode or rules
- 🧠 Fuzzy matching or partial credit scoring
- 🌐 Web or mobile port

---

## 🤝 Contributions

All contributions are welcome — from new decks to features or UI improvements.  
Please fork the repo and open a pull request with a clear description of your changes.

---

## 📄 License

MIT License (or specify your own)

---

## 👤 Author

Dylan McKeithen
