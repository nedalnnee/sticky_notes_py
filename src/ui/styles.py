from src.models import NoteTheme

def get_note_stylesheet(theme: NoteTheme) -> str:
    """Generate dynamic QSS stylesheet for Note Window based on current theme."""
    return f"""
    QWidget#CentralWidget {{
        background-color: {theme.bg_color};
        border: 1px solid {theme.border_color};
        border-radius: 12px;
    }}

    QFrame#TitleBar {{
        background-color: {theme.header_bg};
        border-top-left-radius: 11px;
        border-top-right-radius: 11px;
        border-bottom: 1px solid {theme.border_color};
    }}

    QLabel#TitleLabel {{
        color: {theme.text_color};
        font-family: 'Segoe UI', 'Inter', sans-serif;
        font-size: 13px;
        font-weight: 600;
        padding-left: 6px;
    }}

    QPushButton.TitleBarButton {{
        background-color: transparent;
        border: none;
        border-radius: 4px;
        color: {theme.text_color};
        font-family: 'Segoe UI', sans-serif;
        font-size: 14px;
        font-weight: bold;
        min-width: 24px;
        max-width: 24px;
        min-height: 24px;
        max-height: 24px;
    }}

    QPushButton.TitleBarButton:hover {{
        background-color: rgba(0, 0, 0, 0.08);
    }}

    QPushButton.TitleBarButton:pressed {{
        background-color: rgba(0, 0, 0, 0.16);
    }}

    QPushButton#DeleteButton:hover {{
        background-color: #EF4444;
        color: #FFFFFF;
    }}

    QTextEdit#NoteContent {{
        background-color: transparent;
        color: {theme.text_color};
        font-family: 'Segoe UI', 'Consolas', sans-serif;
        font-size: 14px;
        line-height: 1.4;
        border: none;
        padding: 10px;
        selection-background-color: {theme.accent_color};
        selection-color: #FFFFFF;
    }}

    QScrollBar:vertical {{
        border: none;
        background: transparent;
        width: 8px;
        margin: 4px 2px 4px 2px;
    }}

    QScrollBar::handle:vertical {{
        background: rgba(0, 0, 0, 0.15);
        border-radius: 4px;
        min-height: 20px;
    }}

    QScrollBar::handle:vertical:hover {{
        background: rgba(0, 0, 0, 0.3);
    }}

    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0px;
    }}

    QMenu {{
        background-color: {theme.bg_color};
        border: 1px solid {theme.border_color};
        border-radius: 8px;
        padding: 4px;
    }}

    QMenu::item {{
        color: {theme.text_color};
        font-family: 'Segoe UI', sans-serif;
        font-size: 12px;
        padding: 6px 16px;
        border-radius: 4px;
    }}

    QMenu::item:selected {{
        background-color: {theme.header_bg};
    }}
    """
