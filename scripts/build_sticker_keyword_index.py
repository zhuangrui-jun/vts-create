#!/usr/bin/env python3
"""
从 chat.db 的 stickers_gif_720 读取 file_name，去掉 .gif 后仅按「-」切分，
关键词存入 set 去重，写入文本（每行一词）。输出中不会出现 .gif。

用法（在项目根 vts-create 下）:
  python scripts/build_sticker_keyword_index.py

可选:
  python scripts/build_sticker_keyword_index.py --db path/to/chat.db -o path/to/keywords.txt
"""

from __future__ import annotations

import argparse
import sqlite3
import sys
from pathlib import Path

TABLE_NAME = "stickers_gif_720"
DEFAULT_OUT = "scripts/sticker_keyword_output/unique_keywords.txt"


def _project_root() -> Path:
    return Path(__file__).resolve().parent.parent


def _resolve_db_path(explicit: Path | None, root: Path) -> Path:
    if explicit is not None:
        return explicit
    return root / "backend" / "data" / "chat.db"


def stem_without_gif(file_name: str) -> str:
    """去掉扩展名，保证不参与切分的字符串里不含 .gif。"""
    name = file_name.strip()
    lower = name.lower()
    if lower.endswith(".gif"):
        return name[: -4].strip()
    return name


def collect_keywords_from_filename(file_name: str) -> list[str]:
    stem = stem_without_gif(file_name)
    parts = stem.split("-")
    out: list[str] = []
    for p in parts:
        t = p.strip()
        if not t or ".gif" in t.lower():
            continue
        out.append(t)
    return out


def main() -> None:
    root = _project_root()
    parser = argparse.ArgumentParser(
        description="按「-」从贴纸文件名切词，去重后写入文本文件（无 .gif）"
    )
    parser.add_argument(
        "--db",
        type=Path,
        default=None,
        help="SQLite 路径，默认 backend/data/chat.db",
    )
    parser.add_argument(
        "-o",
        "--out",
        type=Path,
        default=None,
        help=f"输出文件路径，默认 {DEFAULT_OUT}（相对项目根）",
    )
    args = parser.parse_args()

    db_path = _resolve_db_path(args.db, root)
    out_path = (root / DEFAULT_OUT) if args.out is None else args.out
    if not out_path.is_absolute():
        out_path = root / out_path

    if not db_path.is_file():
        sys.exit(f"数据库文件不存在: {db_path}")

    conn = sqlite3.connect(db_path)
    try:
        cur = conn.execute(
            f"SELECT file_name FROM {TABLE_NAME} ORDER BY id"
        )
        rows = [str(r[0]) for r in cur.fetchall()]
    finally:
        conn.close()

    if not rows:
        sys.exit(f"表 {TABLE_NAME} 无数据")

    keywords: set[str] = set()
    for file_name in rows:
        for kw in collect_keywords_from_filename(file_name):
            keywords.add(kw)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        "\n".join(sorted(keywords)) + "\n",
        encoding="utf-8",
    )

    print(f"数据库: {db_path}")
    print(f"贴纸文件数: {len(rows)}")
    print(f"不重复关键词数: {len(keywords)}")
    print(f"已写入: {out_path}")


if __name__ == "__main__":
    main()
