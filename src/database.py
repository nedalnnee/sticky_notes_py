import os
import sqlite3
import time
from typing import List, Optional
from src.models import Note, DEFAULT_THEME_NAME

def get_db_path() -> str:
    """Return path to SQLite database file stored in AppData/StickyNotes."""
    appdata = os.getenv("APPDATA")
    if not appdata:
        appdata = os.path.expanduser("~")
    data_dir = os.path.join(appdata, "StickyNotesApp")
    os.makedirs(data_dir, exist_ok=True)
    return os.path.join(data_dir, "notes.db")

class DatabaseManager:
    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or get_db_path()
        self.init_db()

    def get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS notes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT DEFAULT '',
                    content TEXT DEFAULT '',
                    x INTEGER DEFAULT 150,
                    y INTEGER DEFAULT 150,
                    width INTEGER DEFAULT 300,
                    height INTEGER DEFAULT 320,
                    theme_name TEXT DEFAULT 'yellow',
                    is_pinned INTEGER DEFAULT 1,
                    updated_at REAL
                )
            """)
            conn.commit()

    def get_all_notes(self) -> List[Note]:
        notes = []
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM notes ORDER BY id ASC")
            rows = cursor.fetchall()
            for row in rows:
                note = Note(
                    id=row["id"],
                    title=row["title"] or "",
                    content=row["content"] or "",
                    x=row["x"],
                    y=row["y"],
                    width=row["width"],
                    height=row["height"],
                    theme_name=row["theme_name"] or DEFAULT_THEME_NAME,
                    is_pinned=bool(row["is_pinned"]),
                    updated_at=row["updated_at"] or time.time(),
                )
                notes.append(note)
        return notes

    def create_note(self, note: Note) -> int:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO notes (title, content, x, y, width, height, theme_name, is_pinned, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                note.title,
                note.content,
                note.x,
                note.y,
                note.width,
                note.height,
                note.theme_name,
                1 if note.is_pinned else 0,
                time.time()
            ))
            conn.commit()
            return cursor.lastrowid

    def update_geometry(self, note_id: int, x: int, y: int, width: int, height: int):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE notes SET x = ?, y = ?, width = ?, height = ?, updated_at = ? WHERE id = ?
            """, (x, y, width, height, time.time(), note_id))
            conn.commit()

    def update_content(self, note_id: int, content: str):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE notes SET content = ?, updated_at = ? WHERE id = ?
            """, (content, time.time(), note_id))
            conn.commit()

    def update_theme(self, note_id: int, theme_name: str):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE notes SET theme_name = ?, updated_at = ? WHERE id = ?
            """, (theme_name, time.time(), note_id))
            conn.commit()

    def update_pinned(self, note_id: int, is_pinned: bool):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE notes SET is_pinned = ?, updated_at = ? WHERE id = ?
            """, (1 if is_pinned else 0, time.time(), note_id))
            conn.commit()

    def delete_note(self, note_id: int):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM notes WHERE id = ?", (note_id,))
            conn.commit()
