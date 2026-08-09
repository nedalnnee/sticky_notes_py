from PyQt6.QtCore import Qt, QPoint, QSize, pyqtSignal
from PyQt6.QtWidgets import (
    QFrame, QHBoxLayout, QLabel, QPushButton, QMenu, QWidget, QMessageBox, QInputDialog
)

from src.models import THEMES, NoteTheme
from src.ui.icons import load_svg_icon

class TitleBar(QFrame):
    # Signals
    new_note_requested = pyqtSignal()
    close_note_requested = pyqtSignal()            # Hide/close note (keeps in library)
    delete_permanently_requested = pyqtSignal()     # Delete permanently from database
    pin_toggled = pyqtSignal(bool)
    theme_changed = pyqtSignal(str)
    title_edited = pyqtSignal(str)

    def __init__(self, parent: QWidget, is_pinned: bool = True, current_theme: NoteTheme = None, initial_title: str = "Sticky Note"):
        super().__init__(parent)
        self.setObjectName("TitleBar")
        self.parent_window = parent
        self.is_pinned = is_pinned
        self.current_theme = current_theme or THEMES["yellow"]
        self._drag_position = QPoint()
        self._is_dragging = False

        self._init_ui(initial_title)
        self.update_theme_icons(self.current_theme)

    def _init_ui(self, initial_title: str):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 4, 8, 4)
        layout.setSpacing(4)

        icon_size = QSize(14, 14)

        # New Note (+) button
        self.btn_add = QPushButton()
        self.btn_add.setToolTip("New Note")
        self.btn_add.setProperty("class", "TitleBarButton")
        self.btn_add.setIconSize(icon_size)
        self.btn_add.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_add.clicked.connect(self.new_note_requested.emit)
        layout.addWidget(self.btn_add)

        # Dynamic Title Label
        self.lbl_title = QLabel(initial_title)
        self.lbl_title.setObjectName("TitleLabel")
        self.lbl_title.setToolTip("Double-click or use Options menu to edit custom title")
        layout.addWidget(self.lbl_title, 1)

        # Theme & Options button
        self.btn_color = QPushButton()
        self.btn_color.setToolTip("Options & Color Themes")
        self.btn_color.setProperty("class", "TitleBarButton")
        self.btn_color.setIconSize(icon_size)
        self.btn_color.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_color.clicked.connect(self._show_color_menu)
        layout.addWidget(self.btn_color)

        # Pin / Always on top button
        self.btn_pin = QPushButton()
        self.btn_pin.setProperty("class", "TitleBarButton")
        self.btn_pin.setIconSize(icon_size)
        self.btn_pin.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_pin.clicked.connect(self._toggle_pin)
        layout.addWidget(self.btn_pin)

        # Permanent Trash Delete button (with confirmation)
        self.btn_trash = QPushButton()
        self.btn_trash.setObjectName("DeleteButton")
        self.btn_trash.setProperty("class", "TitleBarButton")
        self.btn_trash.setIconSize(icon_size)
        self.btn_trash.setToolTip("Delete Note Permanently")
        self.btn_trash.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_trash.clicked.connect(self._confirm_delete_permanently)
        layout.addWidget(self.btn_trash)

        # Close button (Hides note to library)
        self.btn_delete = QPushButton()
        self.btn_delete.setObjectName("CloseButton")
        self.btn_delete.setProperty("class", "TitleBarButton")
        self.btn_delete.setIconSize(icon_size)
        self.btn_delete.setToolTip("Close Note (Saved in Notes Library)")
        self.btn_delete.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_delete.clicked.connect(self.close_note_requested.emit)
        layout.addWidget(self.btn_delete)

        self.setFixedHeight(34)

    def set_title_text(self, title_text: str):
        self.lbl_title.setText(title_text)

    def update_theme_icons(self, theme: NoteTheme):
        self.current_theme = theme
        color = theme.text_color

        self.btn_add.setIcon(load_svg_icon("plus", color))
        self.btn_color.setIcon(load_svg_icon("palette", color))
        self.btn_trash.setIcon(load_svg_icon("trash", color))
        self.btn_delete.setIcon(load_svg_icon("close", color))
        self._update_pin_icon()

    def set_pinned(self, is_pinned: bool):
        self.is_pinned = is_pinned
        self._update_pin_icon()

    def _update_pin_icon(self):
        color = self.current_theme.text_color
        if self.is_pinned:
            self.btn_pin.setIcon(load_svg_icon("pin_filled", color))
            self.btn_pin.setToolTip("Pinned (Always on Top)")
        else:
            self.btn_pin.setIcon(load_svg_icon("pin_outline", color))
            self.btn_pin.setToolTip("Unpinned (Standard Window)")

    def _toggle_pin(self):
        self.set_pinned(not self.is_pinned)
        self.pin_toggled.emit(self.is_pinned)

    def _show_color_menu(self):
        menu = QMenu(self)

        action_title = menu.addAction("Edit Note Title...")
        action_title.triggered.connect(self._prompt_edit_title)

        menu.addSeparator()

        # Color palettes header
        menu.addSection("Color Themes")
        for theme_key, theme_obj in THEMES.items():
            action = menu.addAction(f"  {theme_obj.display_name}")
            action.triggered.connect(lambda _, key=theme_key: self.theme_changed.emit(key))

        menu.addSeparator()

        # Delete permanently option
        action_delete = menu.addAction("Delete Permanently...")
        action_delete.triggered.connect(self._confirm_delete_permanently)

        menu.exec(self.btn_color.mapToGlobal(QPoint(0, self.btn_color.height())))

    def _prompt_edit_title(self):
        current_custom_title = self.parent_window.note.title if hasattr(self.parent_window, "note") else ""
        text, ok = QInputDialog.getText(
            self,
            "Custom Note Title",
            "Enter custom title (leave empty to auto-extract first 2 words):",
            text=current_custom_title
        )
        if ok:
            self.title_edited.emit(text.strip())

    def _confirm_delete_permanently(self):
        reply = QMessageBox.question(
            self,
            "Delete Note",
            "Are you sure you want to permanently delete this note?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.delete_permanently_requested.emit()

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._prompt_edit_title()
            event.accept()
        else:
            super().mouseDoubleClickEvent(event)

    # Dragging logic
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._is_dragging = True
            self._drag_position = event.globalPosition().toPoint() - self.parent_window.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self._is_dragging and event.buttons() == Qt.MouseButton.LeftButton:
            self.parent_window.move(event.globalPosition().toPoint() - self._drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._is_dragging = False
            if hasattr(self.parent_window, "save_geometry_state"):
                self.parent_window.save_geometry_state()
            event.accept()
