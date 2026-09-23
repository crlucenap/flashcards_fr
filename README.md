![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)
![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-F8D341)
![SQLite](https://img.shields.io/badge/DB-SQLite-003B57?logo=sqlite&logoColor=white)
![Status](https://img.shields.io/badge/status-en%20desarrollo-yellow)

# Quickcards

Desktop app for learning French vocabulary. You type a word while
studying, it gets automatically translated to Spanish and saved as a
card; then you review it in flashcard mode, with no word repeating
until you've seen them all.

<!-- 🎥 Aquí va el GIF o enlace al vídeo de demo -->
<!-- ![demo](docs/demo.gif) -->

## Tech stack

- **Python 3.11**
- **CustomTkinter** — desktop graphical interface
- **SQLite** (`sqlite3`, built into Python) — card persistence
- **MyMemory API** — automatic French → Spanish translation
- **wordfreq** — checks that the word you typed is actually French
  before translating (avoids nonsense translations if you accidentally
  type in another language)

## Features

- ✅ Automatic French → Spanish translation when saving a word
- ✅ Detects words that aren't French or are misspelled, before
  spending an API call
- ✅ Low-confidence translation warning (for typos within French)
- ✅ No duplicate words get saved
- ✅ Review mode with random cards that don't repeat within the same session
- ✅ Restart button once you've reviewed every card
- ✅ Counter showing how many times each word has been reviewed
- ✅ Delete individual cards right from the review card
- ✅ Total saved-cards counter

## What the user can do

1. **Study mode**: type a French word and press "Translate and save"
   (or Enter). The app translates it and adds it to your vocabulary deck.
2. **Review mode**: click the card to flip it and see the translation.
   Use "Next card" to move to the next word without repeating any until
   the deck runs out, and "Start over" to review the whole deck again.
3. **Delete a card**: click the 🗑 icon on the card you're reviewing to
   remove it from the deck

## Keyboard shortcuts

| Shortcut | Action                                  |
|----------|-------------------------------------------|
| `Enter`  | Translates and saves the word (in Study mode) |


## How to run it

```bash
git clone https://github.com/your-username/quickcards.git
cd quickcards
pip install -r requirements.txt
python main.py
```

Requires Python 3.10+ and an internet connection (for automatic translation).

## Video / demo

<!-- Sustituye esto por un enlace a un vídeo corto (Loom, YouTube sin listar,
     o un GIF subido a la carpeta docs/) enseñando la app en uso:
     escribir una palabra, ver que se traduce y guarda, y repasar tarjetas. -->

🎥 *(recording pending)*
