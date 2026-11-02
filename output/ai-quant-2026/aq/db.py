"""SQLite 读写封装。"""
from __future__ import annotations

import sqlite3
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Iterable, Sequence

from .config import DB_PATH

CN_TZ = timezone(timedelta(hours=8))


def now_cn() -> str:
    return datetime.now(CN_TZ).strftime("%Y-%m-%d %H:%M:%S")


def connect(path: Path | str = DB_PATH, fast: bool = False) -> sqlite3.Connection:
    conn = sqlite3.connect(str(path), timeout=60.0)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    # 批量导入时 synchronous=OFF 能快 3~5 倍；进程崩溃最多丢掉最后一批，
    # 而抓取日志本身支持按股票断点续抓，重跑即可，不存在数据错乱。
    conn.execute("PRAGMA synchronous=OFF" if fast else "PRAGMA synchronous=NORMAL")
    conn.execute("PRAGMA temp_store=MEMORY")
    conn.execute("PRAGMA cache_size=-400000")
    return conn


def init_db(conn: sqlite3.Connection, create_indexes: bool = True) -> None:
    schema = (Path(__file__).with_name("schema.sql")).read_text(encoding="utf-8")
    if not create_indexes:
        # 批量导入阶段先不建二级索引，否则每行插入都要维护一棵 B 树
        schema = "\n".join(l for l in schema.splitlines()
                           if not l.strip().upper().startswith("CREATE INDEX"))
    conn.executescript(schema)
    _migrate(conn)
    if create_indexes:
        build_indexes(conn)
    conn.commit()


def build_indexes(conn: sqlite3.Connection) -> None:
    """导入完成后一次性建索引。"""
    conn.execute("CREATE INDEX IF NOT EXISTS idx_bar_date ON bar(date)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_fin_notice ON fin(notice_date)")
    conn.commit()


# 后续版本新增的列，老库自动补齐，避免每次改表都要删库重来
_MIGRATIONS = [
    ("fin", "name", "TEXT"),
    ("bar", "is_st", "INTEGER"),
    ("bar", "trade_status", "INTEGER"),
]


def _migrate(conn: sqlite3.Connection) -> None:
    for table, col, typ in _MIGRATIONS:
        cols = {r["name"] for r in conn.execute(f"PRAGMA table_info({table})")}
        if cols and col not in cols:
            conn.execute(f"ALTER TABLE {table} ADD COLUMN {col} {typ}")


def upsert(conn: sqlite3.Connection, table: str, columns: Sequence[str],
           rows: Iterable[Sequence[Any]], *, chunk: int = 5000) -> int:
    """INSERT OR REPLACE 批量写入。返回写入行数。"""
    cols = ",".join(columns)
    ph = ",".join("?" * len(columns))
    sql = f"INSERT OR REPLACE INTO {table} ({cols}) VALUES ({ph})"
    n = 0
    buf: list[Sequence[Any]] = []
    for r in rows:
        buf.append(r)
        if len(buf) >= chunk:
            conn.executemany(sql, buf)
            n += len(buf)
            buf.clear()
    if buf:
        conn.executemany(sql, buf)
        n += len(buf)
    conn.commit()
    return n


def set_meta(conn: sqlite3.Connection, key: str, value: str) -> None:
    conn.execute("INSERT OR REPLACE INTO meta(key,value) VALUES (?,?)", (key, str(value)))
    conn.commit()


def get_meta(conn: sqlite3.Connection, key: str, default: str | None = None) -> str | None:
    row = conn.execute("SELECT value FROM meta WHERE key=?", (key,)).fetchone()
    return row["value"] if row else default


def log_fetch(conn: sqlite3.Connection, task: str, key: str, status: str,
              n_rows: int = 0, err: str | None = None) -> None:
    conn.execute(
        "INSERT OR REPLACE INTO fetch_log(task,key,status,n_rows,ts,err) VALUES (?,?,?,?,?,?)",
        (task, key, status, n_rows, now_cn(), err),
    )


def done_keys(conn: sqlite3.Connection, task: str) -> set[str]:
    cur = conn.execute(
        "SELECT key FROM fetch_log WHERE task=? AND status IN ('ok','empty')", (task,)
    )
    return {r["key"] for r in cur.fetchall()}
