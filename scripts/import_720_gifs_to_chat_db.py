#!/usr/bin/env python3
"""
将 720 目录下的 .gif 写入 backend/data/chat.db 的新表（与应用主库一致）。
不依赖项目内其它模块；仅用标准库。

默认 GIF 目录：优先 <项目根>/720，否则 <项目根>/../720。

用法（在项目根 vts-create 下）:
  python scripts/import_720_gifs_to_chat_db.py

可选:
  python scripts/import_720_gifs_to_chat_db.py --db path/to/chat.db --gif-dir path/to/720
"""

from __future__ import annotations

import argparse
import sqlite3
import sys
from pathlib import Path

TABLE_NAME = "stickers_gif_720"


def _project_root() -> Path:
    return Path(__file__).resolve().parent.parent


def _resolve_gif_dir(explicit: Path | None, root: Path) -> Path:
    if explicit is not None:
        if not explicit.is_dir():
            sys.exit(f"GIF 目录不存在: {explicit}")
        return explicit
    for candidate in (root / "720", root.parent / "720"):
        if candidate.is_dir():
            return candidate
    sys.exit(
        "未找到 720 目录。请将文件夹放在项目根下的 720/，"
        "或使用 --gif-dir 指定路径。"
    )


def _resolve_db_path(explicit: Path | None, root: Path) -> Path:
    if explicit is not None:
        p = explicit
    else:
        p = root / "backend" / "data" / "chat.db"
    p.parent.mkdir(parents=True, exist_ok=True)
    return p


def main() -> None:
    root = _project_root()
    parser = argparse.ArgumentParser(description="导入 720 下 GIF 到 chat.db")
    parser.add_argument(
        "--db",
        type=Path,
        default=None,
        help="SQLite 文件路径，默认 backend/data/chat.db",
    )
    parser.add_argument(
        "--gif-dir",
        type=Path,
        default=None,
        help="含 GIF 的目录，默认自动查找 720",
    )
    args = parser.parse_args()

    gif_dir = _resolve_gif_dir(args.gif_dir, root)
    db_path = _resolve_db_path(args.db, root)

    gifs = sorted(gif_dir.glob("*.gif"))
    if not gifs:
        sys.exit(f"目录中无 .gif 文件: {gif_dir}")

    conn = sqlite3.connect(db_path)
    try:
        conn.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_name TEXT NOT NULL,
                relative_path TEXT NOT NULL UNIQUE
            )
            """
        )
        conn.execute(
            f"CREATE INDEX IF NOT EXISTS idx_{TABLE_NAME}_file_name "
            f"ON {TABLE_NAME}(file_name)"
        )

        for path in gifs:
            rel = Path(path).resolve().relative_to(root.resolve())
            rel_posix = rel.as_posix()
            conn.execute(
                f"""
                INSERT INTO {TABLE_NAME} (file_name, relative_path)
                VALUES (?, ?)
                ON CONFLICT(relative_path) DO UPDATE SET
                    file_name = excluded.file_name
                """,
                (path.name, rel_posix),
            )

        conn.commit()
    finally:
        conn.close()

    print(f"数据库: {db_path}")
    print(f"GIF 目录: {gif_dir}")
    print(f"表 {TABLE_NAME}: 已写入/更新 {len(gifs)} 行。")


if __name__ == "__main__":
    main()
