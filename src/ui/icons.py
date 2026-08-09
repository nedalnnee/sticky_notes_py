import os
import sys
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon, QPixmap, QPainter, QColor
from PyQt6.QtSvg import QSvgRenderer

def get_assets_dir() -> str:
    # Handle PyInstaller _MEIPASS path resolution vs standard directory structure
    base_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    return os.path.join(base_dir, "assets")

def load_svg_icon(icon_name: str, color_hex: str = None, size: int = 16) -> QIcon:
    """
    Load an SVG vector icon from assets/icons/, optionally tinting it to match current theme text color.
    """
    assets_dir = get_assets_dir()
    svg_path = os.path.join(assets_dir, "icons", f"{icon_name}.svg")

    if not os.path.exists(svg_path):
        return QIcon()

    if not color_hex:
        return QIcon(svg_path)

    # Render SVG onto transparent QPixmap and tint with requested color_hex
    renderer = QSvgRenderer(svg_path)
    if not renderer.isValid():
        return QIcon(svg_path)

    pixmap = QPixmap(size * 2, size * 2)  # High DPI 2x scaling
    pixmap.fill(Qt.GlobalColor.transparent)

    painter = QPainter(pixmap)
    renderer.render(painter)
    painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
    painter.fillRect(pixmap.rect(), QColor(color_hex))
    painter.end()

    icon = QIcon()
    icon.addPixmap(pixmap)
    return icon
