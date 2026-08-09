import time
from dataclasses import dataclass, field
from typing import Dict, List

@dataclass
class NoteTheme:
    name: str
    display_name: str
    bg_color: str         # Window background
    header_bg: str        # Custom title bar background
    text_color: str       # Text editor color
    accent_color: str     # Header icons & highlights
    border_color: str     # Subtle outline border

THEMES: Dict[str, NoteTheme] = {
    "yellow": NoteTheme(
        name="yellow",
        display_name="Classic Yellow",
        bg_color="#FFF8D6",
        header_bg="#FFF099",
        text_color="#332D00",
        accent_color="#B8860B",
        border_color="#F0E38B",
    ),
    "purple": NoteTheme(
        name="purple",
        display_name="Soft Lavender",
        bg_color="#F3E8FF",
        header_bg="#E9D5FF",
        text_color="#3B0764",
        accent_color="#9333EA",
        border_color="#DDD6FE",
    ),
    "dark": NoteTheme(
        name="dark",
        display_name="Dark Charcoal",
        bg_color="#1E1E2E",
        header_bg="#2D2D3F",
        text_color="#CDD6F4",
        accent_color="#89B4FA",
        border_color="#45475A",
    ),
    "blue": NoteTheme(
        name="blue",
        display_name="Sky Blue",
        bg_color="#E0F2FE",
        header_bg="#BAE6FD",
        text_color="#0C4A6E",
        accent_color="#0284C7",
        border_color="#7DD3FC",
    ),
    "green": NoteTheme(
        name="green",
        display_name="Mint Green",
        bg_color="#DCFCE7",
        header_bg="#BBF7D0",
        text_color="#14532D",
        accent_color="#16A34A",
        border_color="#86EFAC",
    ),
    "pink": NoteTheme(
        name="pink",
        display_name="Rose Pink",
        bg_color="#FFE4E6",
        header_bg="#FECDD3",
        text_color="#881337",
        accent_color="#E11D48",
        border_color="#FDA4AF",
    ),
}

DEFAULT_THEME_NAME = "yellow"

@dataclass
class Note:
    id: int = 0
    title: str = ""
    content: str = ""
    x: int = 150
    y: int = 150
    width: int = 300
    height: int = 320
    theme_name: str = DEFAULT_THEME_NAME
    is_pinned: bool = True
    updated_at: float = field(default_factory=time.time)

    @property
    def theme(self) -> NoteTheme:
        return THEMES.get(self.theme_name, THEMES[DEFAULT_THEME_NAME])
