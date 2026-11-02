"""数据库巡检：行数、覆盖范围、缺口与质量告警。

用法: python scripts/check_db.py [--verbose]
"""
from __future__ import annotations

import argparse
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from aq.config import DB_PATH


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    q = lambda s, p=(): conn.execute(s, p).fetchone()  # noqa: E731

    print(f"DB: {DB_PATH}  ({DB_PATH.stat().st_size / 1e6:.1f} MB)")

    for t in ("stock", "bar", "fin", "valuation", "index_bar", "index_member", "trade_calendar", "fetch_log", "meta"):
        try:
            n = q(f"SELECT COUNT(*) c FROM {t}")["c"]
            print(f"  {t:16s} {n:>10,}")
        except sqlite3.Error:
            print(f"  {t:16s} (缺失)")

    r = q("SELECT MIN(date) a, MAX(date) b, COUNT(DISTINCT code) n, COUNT(*) c FROM bar")
    if r and r["c"]:
        print(f"\n行情区间 {r['a']} ~ {r['b']}  codes={r['n']}  rows={r['c']:,}")

    r = q("SELECT MIN(notice_date) a, MAX(notice_date) b FROM fin")
    print(f"财报公告日 {r['a']} ~ {r['b']}")

    print("\n抓取状态:")
    for row in conn.execute(
            "SELECT task, status, COUNT(*) n FROM fetch_log GROUP BY task, status ORDER BY task, status"):
        print(f"  {row['task']:12s} {row['status']:6s} {row['n']:>6,}")

    todo = q("SELECT COUNT(*) c FROM stock s WHERE NOT EXISTS "
             "(SELECT 1 FROM bar b WHERE b.code=s.code)")["c"]
    print(f"\n无行情记录的证券: {todo}")

    if args.verbose:
        print("\n按年份:")
        for row in conn.execute(
                "SELECT substr(date,1,4) y, COUNT(*) n, COUNT(DISTINCT code) c FROM bar GROUP BY y"):
            print(f"  {row['y']}  rows={row['n']:>9,} codes={row['c']:>5,}")
    conn.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
