from PyQt6.QtCore import Qt, QPoint, pyqtSignal
from PyQt6.QtWidgets import (
    QFrame, QHBoxLayout, QLabel, QPushButton, QMenu, QWidget
)

from src.models import THEMES, NoteTheme

class TitleBar(QFrame):
    # Signals
    new_note_requested = pyqtSignal()
    delete_requested = pyqtSignal()
    pin_toggled = pyqtSignal(bool)
    theme_changed = pyqtSignal(str)

    def __init__(self, parent: QWidget, is_pinned: bool = True):
        super().__init__(parent)
        self.setObjectName("TitleBar")
        self.parent_window = parent
        self.is_pinned = is_pinned
        self._drag_position = QPoint()
        self._is_dragging = False

        self._init_ui()

    def _init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 4, 8, 4)
        layout.setSpacing(4)

        # New Note (+) button
        self.btn_add = QPushButton("+")
        self.btn_add.setToolTip("New Note")
        self.btn_add.setProperty("class", "TitleBarButton")
        self.btn_add.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_add.clicked.connect(self.new_note_requested.emit)
        layout.addWidget(self.btn_add)

        # Spacer/Title Drag region label
        self.lbl_title = QLabel("Sticky Note")
        self.lbl_title.setObjectName("TitleLabel")
        layout.addWidget(self.lbl_title, 1)

        # Theme color picker button
        self.btn_color = QPushButton("●")
        self.btn_color.setToolTip("Change Color Theme")
        self.btn_color.setProperty("class", "TitleBarButton")
        self.btn_color.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_color.clicked.connect(self._show_color_menu)
        layout.addWidget(self.btn_color)

        # Pin / Always on top button
        self.btn_pin = QPushButton("★" if self.is_pinned else "☆")
        self.btn_pin.setToolTip("Pinned (Always on Top)" if self.is_pinned else "Unpinned (Standard Window)")
        self.btn_pin.setProperty("class", "TitleBarButton")
        self.btn_pin.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_pin.clicked.connect(self._toggle_pin)
        layout.addWidget(self.btn_pin)

        # Delete button
        self.btn_delete = QPushButton("✕")
        self.btn_delete.setObjectName("DeleteButton")
        self.btn_delete.setProperty("class", "TitleBarButton")
        self.btn_delete.setToolTip("Delete Note")
        self.btn_delete.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_delete.clicked.connect(self.delete_requested.emit)
        layout.addWidget(self.btn_delete)

        self.setFixedHeight(34)

    def set_pinned(self, is_pinned: bool):
        self.is_pinned = is_pinned
        self.btn_pin.setText("★" if self.is_pinned else "☆")
        self.btn_pin.setToolTip("Pinned (Always on Top)" if self.is_pinned else "Unpinned (Standard Window)")

    def _toggle_pin(self):
        self.set_pinned(not self.is_pinned)
        self.pin_toggled.emit(self.is_pinned)

    def _show_color_menu(self):
        menu = QMenu(self)
        for theme_key, theme_obj in THEMES.items():
            action = menu.addAction(f"  {theme_obj.display_name}")
            action.triggered.connect(lambda _, key=theme_key: self.theme_changed.emit(key))
        menu.exec(self.btn_color.mapToGlobal(QPoint(0, self.btn_color.height())))

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
            # Signal parent to persist new geometry
            if hasattr(self.parent_window, "save_geometry_state"):
                self.parent_window.save_geometry_state()
            event.accept()
