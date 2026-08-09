import os
from typing import List
from PyQt6.QtCore import pyqtSignal, QObject
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtWidgets import QSystemTrayIcon, QMenu, QMessageBox, QApplication

from src.models import Note

class SystemTrayManager(QObject):
    new_note_requested = pyqtSignal()
    show_all_requested = pyqtSignal()
    hide_all_requested = pyqtSignal()
    note_selected = pyqtSignal(int)      # Emits note_id when user selects a note from library
    exit_requested = pyqtSignal()

    def __init__(self, icon_path: str, parent: QObject = None):
        super().__init__(parent)
        self.icon_path = icon_path
        self.are_notes_visible = True
        self.cached_notes: List[Note] = []

        self._init_tray()

    def _init_tray(self):
        if os.path.exists(self.icon_path):
            self.icon = QIcon(self.icon_path)
        else:
            self.icon = QApplication.style().standardIcon(
                QApplication.style().StandardPixmap.SP_FileIcon
            )

        self.tray_icon = QSystemTrayIcon(self.icon, self)
        self.tray_icon.setToolTip("Sticky Notes")

        # Main Context Menu
        self.menu = QMenu()
        self.menu.aboutToShow.connect(self._rebuild_menu)

        self.tray_icon.setContextMenu(self.menu)
        self.tray_icon.activated.connect(self._on_tray_activated)
        self.tray_icon.show()

    def set_notes_list(self, notes: List[Note]):
        self.cached_notes = notes

    def _rebuild_menu(self):
        self.menu.clear()

        # Action: New Note
        action_new = QAction("New Note", self)
        action_new.triggered.connect(self.new_note_requested.emit)
        self.menu.addAction(action_new)

        # Notes Library Sub-Menu
        library_menu = self.menu.addMenu("Notes Library")
        if not self.cached_notes:
            action_empty = library_menu.addAction("No notes saved")
            action_empty.setEnabled(False)
        else:
            for note in self.cached_notes:
                status_prefix = "● " if note.is_open else "○ "
                title_text = f"{status_prefix}{note.display_title}"
                action = library_menu.addAction(title_text)
                action.triggered.connect(lambda _, nid=note.id: self.note_selected.emit(nid))

        self.menu.addSeparator()

        # Action: Toggle Show/Hide
        toggle_label = "Hide All Notes" if self.are_notes_visible else "Show All Notes"
        action_toggle = QAction(toggle_label, self)
        action_toggle.triggered.connect(self._toggle_visibility)
        self.menu.addAction(action_toggle)

        # Action: About
        action_about = QAction("About Sticky Notes", self)
        action_about.triggered.connect(self._show_about)
        self.menu.addAction(action_about)

        self.menu.addSeparator()

        # Action: Exit
        action_exit = QAction("Exit Sticky Notes", self)
        action_exit.triggered.connect(self.exit_requested.emit)
        self.menu.addAction(action_exit)

    def _on_tray_activated(self, reason: QSystemTrayIcon.ActivationReason):
        if reason in (
            QSystemTrayIcon.ActivationReason.Trigger,
            QSystemTrayIcon.ActivationReason.DoubleClick,
        ):
            self._toggle_visibility()

    def _toggle_visibility(self):
        if self.are_notes_visible:
            self.are_notes_visible = False
            self.hide_all_requested.emit()
        else:
            self.are_notes_visible = True
            self.show_all_requested.emit()

    def _show_about(self):
        QMessageBox.about(
            None,
            "About Sticky Notes",
            "<h3>Sticky Notes v1.1.0</h3>"
            "<p>A lightweight, elegant Windows Sticky Notes application built with PyQt6 & SQLite.</p>"
            "<ul>"
            "<li>Frameless floating windows with custom themes</li>"
            "<li>Always-on-top pin toggle</li>"
            "<li>Notes Library: closed notes are saved & easily re-opened</li>"
            "<li>Seamless Windows System Tray integration</li>"
            "<li>Auto-saving persistence</li>"
            "</ul>"
        )
