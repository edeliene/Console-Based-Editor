# Console Text Editor (Vim-like in Python)

A lightweight console-based text editor implemented in Python, inspired by Vim-style modal editing and command navigation.

This project demonstrates how a simple text editor can be built from scratch using core data structures and string manipulation—without external libraries or GUI frameworks.

---

## ✨ Features

### Cursor Movement
- `h / l` → move left / right
- `j / k` → move up / down between lines
- `^ / $` → jump to start / end of line
- `w / b / e` → word-based navigation

### Text Editing
- `i / a` → insert before / after cursor
- `I / A` → insert at beginning / end of line
- `x / X` → delete character at / before cursor

### Word Operations
- `dw` → delete to next word
- `de` → delete to end of word
- `db` → delete previous word
- `dc` → delete word or whitespace at cursor

### Word Swapping
- `sw` → swap current word with next word
- `sb` → swap current word with previous word

### Multi-line Editing
- `o / O` → insert new line below / above
- `dd` → delete current line
- `J / K` → move line up / down
- `;` → toggle line cursor indicator

### Utility
- `?` → show help menu
- `.` → toggle cursor highlight
- `q` → quit editor
- `LineNumber` → jump to a specific line

---

## How to Run

Make sure you have Python 3 installed.

```bash
python editor.py
