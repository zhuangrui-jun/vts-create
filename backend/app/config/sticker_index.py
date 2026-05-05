import os
import random
from pathlib import Path
from sqlalchemy import text
from app.db.database import get_session_factory

KEYWORDS_FILE = Path(__file__).resolve().parent.parent.parent.parent / "scripts" / "sticker_keyword_output" / "unique_keywords.txt"


def _ensure_keywords_table():
    factory = get_session_factory()
    db = factory()
    try:
        db.execute(text("""
            CREATE TABLE IF NOT EXISTS unique_keywords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                keyword TEXT UNIQUE NOT NULL
            )
        """))
        db.commit()

        # Load from txt if table is empty
        count = db.execute(text("SELECT COUNT(*) FROM unique_keywords")).scalar()
        if count == 0 and KEYWORDS_FILE.exists():
            with open(KEYWORDS_FILE, "r", encoding="utf-8") as f:
                keywords = [line.strip() for line in f if line.strip()]
            for kw in keywords:
                db.execute(
                    text("INSERT OR IGNORE INTO unique_keywords (keyword) VALUES (:kw)"),
                    {"kw": kw},
                )
            db.commit()
    finally:
        db.close()


def _tokenize(text: str) -> list[str]:
    """Extract all 2-4 char substrings from text."""
    tokens = []
    for size in (4, 3, 2):
        for i in range(len(text) - size + 1):
            tokens.append(text[i:i + size])
    return tokens


def match_sticker(user_message: str) -> tuple[str, str] | None:
    _ensure_keywords_table()

    factory = get_session_factory()
    db = factory()
    try:
        tokens = _tokenize(user_message)

        # Try to find matching keywords, prefer longer matches
        best_keyword = None
        best_len = 0
        for token in tokens:
            row = db.execute(
                text("SELECT keyword FROM unique_keywords WHERE keyword = :kw"),
                {"kw": token},
            ).fetchone()
            if row and len(token) > best_len:
                best_keyword = row[0]
                best_len = len(token)

        # Search stickers by keyword (top 3 random), or random 5 if no match
        if best_keyword:
            rows = db.execute(
                text(
                    "SELECT file_name, relative_path FROM stickers_gif_720 "
                    "WHERE file_name LIKE :pat ORDER BY RANDOM() LIMIT 3"
                ),
                {"pat": f"%{best_keyword}%"},
            ).fetchall()
        else:
            rows = db.execute(
                text(
                    "SELECT file_name, relative_path FROM stickers_gif_720 "
                    "ORDER BY RANDOM() LIMIT 5"
                ),
            ).fetchall()

        if rows:
            pick = random.choice(rows)
            return pick[0], pick[1]
        return None
    finally:
        db.close()
