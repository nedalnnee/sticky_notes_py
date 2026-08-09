import sys
import os
from typing import Dict

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication

# Adjust path when running directly or as PyInstaller executable
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models import Note, DEFAULT_THEME_NAME
from src.database import DatabaseManager
from src.ui.note_window import NoteWindow
from src.tray import SystemTrayManager

class StickyNotesApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setQuitOnLastWindowClosed(False)

        # Asset path resolution
        self.base_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.icon_path = os.path.join(self.base_dir, "assets", "app_icon.ico")

        if os.path.exists(self.icon_path):
            self.app.setWindowIcon(QIcon(self.icon_path))

        # Database initialization
        self.db_manager = DatabaseManager()

        # Windows map: note_id -> NoteWindow
        self.windows: Dict[int, NoteWindow] = {}

        # System Tray Manager
        self.tray = SystemTrayManager(self.icon_path)
        self.tray.new_note_requested.connect(self.create_new_note)
        self.tray.show_all_requested.connect(self.show_all_notes)
        self.tray.hide_all_requested.connect(self.hide_all_notes)
        self.tray.exit_requested.connect(self.quit_app)

    def run(self) -> int:
        notes = self.db_manager.get_all_notes()
        if not notes:
            # First launch: create welcome note
            welcome_note = Note(
                title="Welcome",
                content="Welcome to Sticky Notes!\n\n"
                        "• Drag from header bar to move\n"
                        "• Resize from bottom-right corner\n"
                        "• Click ● to change color theme\n"
                        "• Click ★ to pin always on top\n"
                        "• Minimizes to Windows System Tray\n\n"
                        "Enjoy writing notes!",
                x=200,
                y=180,
                width=320,
                height=340,
                theme_name=DEFAULT_THEME_NAME,
                is_pinned=True,
            )
            welcome_id = self.db_manager.create_note(welcome_note)
            welcome_note.id = welcome_id
            notes = [welcome_note]

        for note in notes:
            self._render_note_window(note)

        return self.app.exec()

    def _render_note_window(self, note: Note) -> NoteWindow:
        win = NoteWindow(note, self.db_manager)
        win.new_note_requested.connect(self.create_new_note)
        win.delete_requested.connect(self.delete_note)
        win.show()
        if note.id:
            self.windows[note.id] = win
        return win

    def create_new_note(self):
        # Stagger position slightly for new notes
        count = len(self.windows)
        offset = (count * 25) % 200

        new_note = Note(
            content="",
            x=220 + offset,
            y=200 + offset,
            width=300,
            height=300,
            theme_name=DEFAULT_THEME_NAME,
            is_pinned=True,
        )
        note_id = self.db_manager.create_note(new_note)
        new_note.id = note_id
        win = self._render_note_window(new_note)
        win.editor.setFocus()

    def delete_note(self, note_id: int):
        if note_id in self.windows:
            win = self.windows.pop(note_id)
            win.close()
            win.deleteLater()
            self.db_manager.delete_note(note_id)

    def show_all_notes(self):
        for win in self.windows.values():
            win.show()
            win.activateWindow()

    def hide_all_notes(self):
        for win in self.windows.values():
            win.hide()

    def quit_app(self):
        # Save geometry of all open windows before quit
        for win in self.windows.values():
            win.save_geometry_state()
        self.app.quit()

def main():
    app = StickyNotesApp()
    sys.exit(app.run())

if __name__ == "__main__":
    main()
