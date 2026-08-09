<div align="center">

# 📌 Sticky Notes

**A modern, lightweight Windows Sticky Notes application built with PyQt6 & SQLite.**

![Python Version](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)
![Framework](https://img.shields.io/badge/GUI-PyQt6-green?logo=qt&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows-0078D6?logo=windows&logoColor=white)
![License](https://img.shields.io/badge/License-PolyForm%20Noncommercial-red)

</div>

---

## 🌟 Overview

**Sticky Notes** is a desktop application designed to stay easily accessible on your screen. It features frameless floating note windows, always-on-top pin capabilities, customizable pastel & dark color themes, and automatic SQLite database saving.

The application runs directly in the **Windows System Tray** (notification area), allowing you to quickly create, hide, or show notes without cluttering your taskbar.

---

## ✨ Features

- 📌 **Always-on-Top Toggle**: Pin notes to float above all active applications (browsers, IDEs, games) or unpin to behave like standard windows.
- 🎨 **6 Theme Palettes**: Classic Yellow, Soft Lavender, Dark Charcoal, Sky Blue, Mint Green, and Rose Pink.
- 🖱️ **Frameless & Draggable**: Sleek header bar with smooth click-and-drag window movement.
- 📐 **Dynamic Resize Grip**: Built-in size grip handle at the bottom-right corner for easy resizing.
- 💾 **SQLite Persistence**: Auto-saves note content, screen position $(X, Y)$, dimensions $(\text{Width}, \text{Height})$, theme, and pin states in real-time (`%APPDATA%\StickyNotesApp\notes.db`).
- 🔔 **Windows System Tray**: Minimizes directly to the taskbar tray with right-click actions (*New Note*, *Show/Hide All*, *About*, *Exit*).
- 📦 **Standalone Executable**: Easily packageable into a single self-contained `StickyNotes.exe` via PyInstaller.

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.9+** installed on Windows.
- [uv](https://github.com/astral-sh/uv) (recommended) or standard `pip`.

### Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/sticky_notes.git
   cd sticky_notes
   ```

2. **Set Up Environment & Dependencies**:
   Using `uv`:
   ```bash
   uv venv
   uv pip install --python .venv pyqt6 pillow pyinstaller
   ```
   Or standard `pip`:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   pip install pyqt6 pillow pyinstaller
   ```

3. **Run the Application**:
   ```bash
   .venv\Scripts\python -m src.main
   ```

---

## 📦 Building Standalone `.exe`

To package the application into a standalone Windows executable (`dist/StickyNotes.exe`):

```bash
.venv\Scripts\python build.py
```

The compiled binary will be generated at `dist/StickyNotes.exe` and is ready to be moved anywhere or configured to launch on Windows startup.

---

## 📂 Project Architecture

```
sticky_notes/
├── .github/
│   └── ISSUE_TEMPLATE/
│       ├── bug_report.md
│       └── feature_request.md
├── assets/
│   ├── app_icon.ico                 # Application window and system tray icon
│   ├── app_icon.png                 # High-resolution PNG logo
│   └── generate_assets.py           # Pillow script to generate vector icons
├── src/
│   ├── __init__.py
│   ├── main.py                      # Application entry point & window manager
│   ├── database.py                  # SQLite database manager & auto-save CRUD
│   ├── models.py                    # Note models & theme color definitions
│   ├── tray.py                      # Windows System Tray manager
│   └── ui/
│       ├── __init__.py
│       ├── note_window.py           # Frameless floating sticky note window
│       ├── title_bar.py             # Custom title bar (drag, pin, color picker, delete)
│       └── styles.py                # Dynamic QSS stylesheets & design tokens
├── build.py                         # PyInstaller build automation script
├── pyproject.toml                   # Package metadata & dependencies
├── CONTRIBUTING.md                  # Guidelines for contributors
├── LICENSE                          # PolyForm Noncommercial License 1.0.0
└── README.md                        # Project documentation
```

---

## 📄 License

This project is licensed under the **PolyForm Noncommercial License 1.0.0**.

- ✅ **Free** for personal, educational, and non-commercial use.
- ❌ **Strictly Non-Commercial / Not For Sale**: You may not sell, sublicense, or monetize this software or derivative works.

For full license terms, see the [LICENSE](file:///c:/Users/dell/Desktop/sticky_notes/LICENSE) file.
