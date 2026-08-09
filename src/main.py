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
        self.tray.note_selected.connect(self.open_or_focus_note)
        self.tray.exit_requested.connect(self.quit_app)

    def _sync_tray_library(self):
        all_notes = self.db_manager.get_all_notes()
        self.tray.set_notes_list(all_notes)

    def run(self) -> int:
        all_notes = self.db_manager.get_all_notes()
        if not all_notes:
            # First launch: create welcome note
            welcome_note = Note(
                title="Welcome",
                content="Welcome to Sticky Notes!\n\n"
                        "• Move: Drag from the top header bar\n"
                        "• Resize: Drag the bottom-right corner grip\n"
                        "• Theme: Click the Palette icon to change colors\n"
                        "• Always on Top: Click the Pin icon to keep above apps\n"
                        "• Close Note: Click ✕ to hide (Saved to Notes Library)\n"
                        "• System Tray: Right-click near clock to open Notes Library & restore any note\n\n"
                        "Happy note taking!",
                x=200,
                y=180,
                width=320,
                height=340,
                theme_name=DEFAULT_THEME_NAME,
                is_pinned=True,
                is_open=True,
            )
            welcome_id = self.db_manager.create_note(welcome_note)
            welcome_note.id = welcome_id
            all_notes = [welcome_note]

        self._sync_tray_library()

        # Render only currently open notes
        for note in all_notes:
            if note.is_open:
                self._render_note_window(note)

        return self.app.exec()

    def _render_note_window(self, note: Note) -> NoteWindow:
        win = NoteWindow(note, self.db_manager)
        win.new_note_requested.connect(self.create_new_note)
        win.close_requested.connect(self.close_note_to_library)
        win.delete_permanently_requested.connect(self.delete_note_permanently)
        win.show()
        if note.id:
            self.windows[note.id] = win
        return win

    def create_new_note(self):
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
            is_open=True,
        )
        note_id = self.db_manager.create_note(new_note)
        new_note.id = note_id
        win = self._render_note_window(new_note)
        win.editor.setFocus()
        self._sync_tray_library()

    def open_or_focus_note(self, note_id: int):
        if note_id in self.windows:
            win = self.windows[note_id]
            win.show()
            win.activateWindow()
            win.raise_()
        else:
            # Reopen note from database
            all_notes = self.db_manager.get_all_notes()
            target_note = next((n for n in all_notes if n.id == note_id), None)
            if target_note:
                target_note.is_open = True
                self.db_manager.set_open_status(note_id, True)
                win = self._render_note_window(target_note)
                win.activateWindow()
                self._sync_tray_library()

    def close_note_to_library(self, note_id: int):
        if note_id in self.windows:
            win = self.windows.pop(note_id)
            win.close()
            win.deleteLater()
            self.db_manager.set_open_status(note_id, False)
            self._sync_tray_library()

    def delete_note_permanently(self, note_id: int):
        if note_id in self.windows:
            win = self.windows.pop(note_id)
            win.close()
            win.deleteLater()
        self.db_manager.delete_note(note_id)
        self._sync_tray_library()

    def show_all_notes(self):
        all_notes = self.db_manager.get_all_notes()
        for note in all_notes:
            if not note.is_open:
                self.db_manager.set_open_status(note.id, True)
                note.is_open = True

        for note in all_notes:
            if note.id not in self.windows:
                self._render_note_window(note)
            else:
                self.windows[note.id].show()
                self.windows[note.id].activateWindow()

        self._sync_tray_library()

    def hide_all_notes(self):
        for win in self.windows.values():
            win.hide()

    def quit_app(self):
        for win in self.windows.values():
            win.save_geometry_state()
        self.app.quit()

def main():
    app = StickyNotesApp()
    sys.exit(app.run())

if __name__ == "__main__":
    main()
