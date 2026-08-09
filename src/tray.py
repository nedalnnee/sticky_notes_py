import os
from PyQt6.QtCore import pyqtSignal, QObject
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtWidgets import QSystemTrayIcon, QMenu, QMessageBox, QApplication

class SystemTrayManager(QObject):
    new_note_requested = pyqtSignal()
    show_all_requested = pyqtSignal()
    hide_all_requested = pyqtSignal()
    exit_requested = pyqtSignal()

    def __init__(self, icon_path: str, parent: QObject = None):
        super().__init__(parent)
        self.icon_path = icon_path
        self.are_notes_visible = True

        self._init_tray()

    def _init_tray(self):
        if os.path.exists(self.icon_path):
            self.icon = QIcon(self.icon_path)
        else:
            # Fallback to standard window icon
            self.icon = QApplication.style().standardIcon(
                QApplication.style().StandardPixmap.SP_FileIcon
            )

        self.tray_icon = QSystemTrayIcon(self.icon, self)
        self.tray_icon.setToolTip("Sticky Notes")

        # Context Menu
        self.menu = QMenu()

        # Action: New Note
        self.action_new = QAction("New Note", self)
        self.action_new.triggered.connect(self.new_note_requested.emit)
        self.menu.addAction(self.action_new)

        self.menu.addSeparator()

        # Action: Toggle Show/Hide
        self.action_toggle_visibility = QAction("Hide All Notes", self)
        self.action_toggle_visibility.triggered.connect(self._toggle_visibility)
        self.menu.addAction(self.action_toggle_visibility)

        # Action: About
        self.action_about = QAction("About Sticky Notes", self)
        self.action_about.triggered.connect(self._show_about)
        self.menu.addAction(self.action_about)

        self.menu.addSeparator()

        # Action: Exit
        self.action_exit = QAction("Exit Sticky Notes", self)
        self.action_exit.triggered.connect(self.exit_requested.emit)
        self.menu.addAction(self.action_exit)

        self.tray_icon.setContextMenu(self.menu)

        # Handle Tray Icon Click
        self.tray_icon.activated.connect(self._on_tray_activated)
        self.tray_icon.show()

    def _on_tray_activated(self, reason: QSystemTrayIcon.ActivationReason):
        if reason in (
            QSystemTrayIcon.ActivationReason.Trigger,
            QSystemTrayIcon.ActivationReason.DoubleClick,
        ):
            self._toggle_visibility()

    def _toggle_visibility(self):
        if self.are_notes_visible:
            self.are_notes_visible = False
            self.action_toggle_visibility.setText("Show All Notes")
            self.hide_all_requested.emit()
        else:
            self.are_notes_visible = True
            self.action_toggle_visibility.setText("Hide All Notes")
            self.show_all_requested.emit()

    def _show_about(self):
        QMessageBox.about(
            None,
            "About Sticky Notes",
            "<h3>Sticky Notes v1.0</h3>"
            "<p>A lightweight, elegant Windows Sticky Notes application built with PyQt6 & SQLite.</p>"
            "<ul>"
            "<li>Frameless floating windows with custom themes</li>"
            "<li>Always-on-top pin toggle</li>"
            "<li>Seamless Windows System Tray integration</li>"
            "<li>Auto-saving persistence</li>"
            "</ul>"
        )
