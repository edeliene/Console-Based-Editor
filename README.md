# Console-Based Text Editor (Multi-Line)

A simple console-based text editor written in Python that simulates basic Vim-style editing through command-based input.  
This project demonstrates core concepts in data structures, string manipulation, and command parsing by building a lightweight text editor from scratch.

---

## Overview

This editor operates entirely in the terminal using text commands instead of a graphical interface or real-time key detection.

It supports multi-line editing, cursor navigation, word-level operations, and basic text manipulation. The goal of this project is to explore how text editors manage state (content, cursor position, and lines) using simple data structures.

---

## Features

### Cursor Movement
- `h` / `l` → move left / right
- `j` / `k` → move up / down between lines
- `^` / `$` → move to start / end of line
- `w` / `b` / `e` → word-based navigation

---

### Text Editing
- `i <text>` → insert text before cursor
- `a <text>` → append text after cursor
- `I <text>` → insert at beginning of line
- `A <text>` → append at end of line

---

### Deletion Commands
- `x` → delete character at cursor
- `X` → delete character before cursor
- `dw` → delete word starting at cursor
- `de` → delete to end of word
- `db` → delete previous word
- `dc` → delete word/whitespace at cursor
- `dd` → delete current line

---

### Word Operations
- `sw` → swap current word with next word
- `sb` → swap current word with previous word

---

### Multi-Line Features
- `o` → insert new line below
- `O` → insert new line above
- `J` / `K` → move current line down / up
- `;` → toggle line indicator (current line marker)

---

### Utility Commands
- `?` → show help menu
- `.` → toggle cursor highlight
- `LineNumber` → jump to a specific line
- `q` → quit editor

---

## How to Run

Make sure you have Python 3 installed.

```bash
python editor.py
```

---

## How It Works

The editor is built around three main components:

- `content` – the active line currently being edited
- `lines` – a list storing all lines in the editor
- `cursor_pos` – the current cursor position within the active line

### Execution Flow

1. Read a command from the user
2. Parse the command into an action and optional argument
3. Update the editor state (text, cursor position, or lines)
4. Re-render the editor content in the console

This design simulates how a text editor manages its internal state while remaining entirely terminal-based.

---

## Limitations

The current version of the editor has the following limitations:

- Command-based input only (no real-time keypress handling)
- No undo/redo functionality
- No file saving or loading support
- No clipboard or copy/paste system
- No syntax highlighting

---

## Contributing

Contributions are welcome. Feel free to:

- Fork the repository
- Experiment with new features
- Improve existing functionality
- Submit pull requests
- Report bugs or suggest enhancements through GitHub Issues

---

## 📄 License

This project was developed as part of the **CSC1002 – Computational Laboratory** course and is intended for educational and learning purposes.
