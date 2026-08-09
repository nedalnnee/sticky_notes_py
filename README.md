# Sticky Notes (Python / PyQt6) 📌

A modern, best-practice Windows Sticky Notes application with system tray support, frameless floating windows, customizable theme palettes, auto-save persistence, and standalone `.exe` packaging.

---

## Key Features

- 📌 **Always on Top Toggle**: Pin notes so they sit above all open applications (browsers, IDEs, games) or unpin to behave like standard windows.
- 🎨 **6 Theme Palettes**: Classic Yellow, Soft Lavender, Dark Charcoal, Sky Blue, Mint Green, and Rose Pink.
- 🖱️ **Frameless & Draggable**: Custom sleek title bar with smooth click-and-drag.
- 📐 **Resizable Grip**: Bottom-right size grip handle for dynamic note sizing.
- 💾 **SQLite Auto-Save**: Auto-saves text content, position (X, Y), width, height, theme, and pin status.
- 🔔 **Windows System Tray**: Minimizes to the notification area tray (icon menu: *New Note*, *Show/Hide All*, *About*, *Exit*).
- 📦 **Single Executable**: Packageable into a self-contained `StickyNotes.exe` via PyInstaller.

---

## Quick Start

### 1. Requirements & Installation

Ensure Python 3.9+ is installed. Use `uv` or standard `pip`:

```bash
# Create virtual environment
uv venv

# Install dependencies
uv pip install --python .venv pyqt6 pillow pyinstaller
```

### 2. Run the Application

```bash
.venv\Scripts\python -m src.main
```

### 3. Build Standalone `.exe`

Run the build automation script:

```bash
.venv\Scripts\python build.py
```

The compiled standalone executable will be located at: `dist/StickyNotes.exe`.

---

## Project Architecture

```
sticky_notes/
├── assets/
│   ├── app_icon.ico
│   ├── app_icon.png
│   └── generate_assets.py
├── src/
│   ├── __init__.py
│   ├── main.py              # Application lifecycle & window manager
│   ├── database.py          # SQLite database schema & auto-save CRUD
│   ├── models.py            # Data models & theme color definitions
│   ├── tray.py              # Windows System Tray manager
│   └── ui/
│       ├── __init__.py
│       ├── note_window.py   # Frameless sticky note main window
│       ├── title_bar.py     # Custom header bar with action buttons
│       └── styles.py        # QSS stylesheets & color themes
├── build.py                 # PyInstaller build automation script
├── pyproject.toml           # Package metadata & dependencies
└── README.md
```
