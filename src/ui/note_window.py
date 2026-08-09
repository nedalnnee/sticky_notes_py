from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QPoint
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTextEdit, QGraphicsDropShadowEffect, QSizeGrip, QHBoxLayout
)

from src.models import Note, THEMES, DEFAULT_THEME_NAME
from src.database import DatabaseManager
from src.ui.styles import get_note_stylesheet
from src.ui.title_bar import TitleBar

class NoteWindow(QWidget):
    new_note_requested = pyqtSignal()
    close_requested = pyqtSignal(int)               # Hide & mark is_open=0 in database
    delete_permanently_requested = pyqtSignal(int)  # Remove completely from database
    note_updated = pyqtSignal()                    # Signal app to sync Notes Library in tray

    def __init__(self, note: Note, db_manager: DatabaseManager):
        super().__init__()
        self.note = note
        self.db_manager = db_manager

        # Set window flags for frameless & translucent background
        self._update_window_flags(self.note.is_pinned)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Content debounced auto-save timer
        self.save_timer = QTimer(self)
        self.save_timer.setSingleShot(True)
        self.save_timer.setInterval(400)
        self.save_timer.timeout.connect(self._persist_content)

        # Geometry save timer
        self.geo_timer = QTimer(self)
        self.geo_timer.setSingleShot(True)
        self.geo_timer.setInterval(500)
        self.geo_timer.timeout.connect(self.save_geometry_state)

        self._init_ui()
        self.apply_theme(self.note.theme_name)
        self.setGeometry(self.note.x, self.note.y, self.note.width, self.note.height)

    def _update_window_flags(self, is_pinned: bool):
        flags = Qt.WindowType.FramelessWindowHint | Qt.WindowType.SubWindow
        if is_pinned:
            flags |= Qt.WindowType.WindowStaysOnTopHint
        self.setWindowFlags(flags)

    def _init_ui(self):
        # Outer layout to hold central widget with drop shadow
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(6, 6, 6, 6)

        # Container widget
        self.central_widget = QWidget(self)
        self.central_widget.setObjectName("CentralWidget")

        # Subtle Drop Shadow Effect
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(0, 4)
        self.central_widget.setGraphicsEffect(shadow)

        central_layout = QVBoxLayout(self.central_widget)
        central_layout.setContentsMargins(0, 0, 0, 0)
        central_layout.setSpacing(0)

        # Custom Title Bar
        self.title_bar = TitleBar(
            self,
            is_pinned=self.note.is_pinned,
            current_theme=self.note.theme,
            initial_title=self.note.display_title
        )
        self.title_bar.new_note_requested.connect(self.new_note_requested.emit)
        self.title_bar.close_note_requested.connect(self._on_close_clicked)
        self.title_bar.delete_permanently_requested.connect(self._on_delete_permanently_clicked)
        self.title_bar.pin_toggled.connect(self._on_pin_toggled)
        self.title_bar.theme_changed.connect(self._on_theme_changed)
        self.title_bar.title_edited.connect(self._on_title_edited)
        central_layout.addWidget(self.title_bar)

        # Text Editor
        self.editor = QTextEdit(self.central_widget)
        self.editor.setObjectName("NoteContent")
        self.editor.setPlaceholderText("Take a note...")
        self.editor.setText(self.note.content)
        self.editor.textChanged.connect(self._on_text_changed)
        central_layout.addWidget(self.editor, 1)

        # Bottom Grip Bar with SizeGrip for resizing
        bottom_bar = QWidget(self.central_widget)
        bottom_layout = QHBoxLayout(bottom_bar)
        bottom_layout.setContentsMargins(0, 0, 4, 4)
        bottom_layout.setSpacing(0)

        bottom_layout.addStretch()
        size_grip = QSizeGrip(bottom_bar)
        size_grip.setFixedSize(14, 14)
        size_grip.setCursor(Qt.CursorShape.SizeFDiagCursor)
        bottom_layout.addWidget(size_grip)

        central_layout.addWidget(bottom_bar)

        outer_layout.addWidget(self.central_widget)
        self.setMinimumSize(200, 180)

    def apply_theme(self, theme_name: str):
        self.note.theme_name = theme_name
        theme = self.note.theme
        stylesheet = get_note_stylesheet(theme)
        self.setStyleSheet(stylesheet)
        if hasattr(self, "title_bar"):
            self.title_bar.update_theme_icons(theme)

    def _on_text_changed(self):
        self.note.content = self.editor.toPlainText()
        self.title_bar.set_title_text(self.note.display_title)
        self.save_timer.start()
        self.note_updated.emit()

    def _on_title_edited(self, new_title: str):
        self.note.title = new_title
        if self.note.id:
            self.db_manager.update_title(self.note.id, new_title)
        self.title_bar.set_title_text(self.note.display_title)
        self.note_updated.emit()

    def _persist_content(self):
        if self.note.id:
            self.db_manager.update_content(self.note.id, self.note.content)

    def _on_theme_changed(self, theme_name: str):
        self.apply_theme(theme_name)
        if self.note.id:
            self.db_manager.update_theme(self.note.id, theme_name)

    def _on_pin_toggled(self, is_pinned: bool):
        self.note.is_pinned = is_pinned
        if self.note.id:
            self.db_manager.update_pinned(self.note.id, is_pinned)

        pos = self.pos()
        size = self.size()

        # Update flags dynamically
        self._update_window_flags(is_pinned)

        # Re-show window with new flags
        self.show()
        self.move(pos)
        self.resize(size)

    def _on_close_clicked(self):
        self.close_requested.emit(self.note.id)

    def _on_delete_permanently_clicked(self):
        self.delete_permanently_requested.emit(self.note.id)

    def save_geometry_state(self):
        geo = self.geometry()
        self.note.x = geo.x()
        self.note.y = geo.y()
        self.note.width = geo.width()
        self.note.height = geo.height()
        if self.note.id:
            self.db_manager.update_geometry(
                self.note.id, self.note.x, self.note.y, self.note.width, self.note.height
            )

    def moveEvent(self, event):
        super().moveEvent(event)
        self.geo_timer.start()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.geo_timer.start()
