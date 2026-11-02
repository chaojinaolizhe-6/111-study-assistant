"""Step 9 — 指数成分股快照（沪深300 / 上证50 / 中证500 / 中证1000 等）。

设计要点
--------
`index_member` 存的是**成分区间**而不是单次快照：
    in_date  = 该股票被观察到属于该指数的最早日期
    out_date = 最后一次被观察到仍属于该指数的日期（仍在成分内则留空）

于是「某日成分股」= `in_date <= t AND (out_date IS NULL OR out_date > t)`。

这样做的意义：**免费源只给当期成分，不给历史成分**。如果直接用"今天的成分"
回测 2015 年的沪深300增强策略，你买入的是十年后才被纳入的股票——
这是指数增强研究里最经典的幸存者偏差。

本脚本每次运行追加一次快照：
  * 新进成分 -> 新增一行，in_date = 快照日
  * 退出成分 -> 把 out_date 设为快照日
  * 持续在成分 -> 不动
因此只要定期（例如每季度）跑一次，成分历史会自然积累起来。
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from aq.db import connect, init_db, log_fetch, now_cn
from aq.http import get_json

URL = "https://datacenter-web.eastmoney.com/api/data/v1/get"

# TYPE 编码与指数的对应关系由「成分数量 + 样本股票」交叉确认（2026-10-31 实测）
TYPE_MAP = {
    "000300": (1, "沪深300"),
    "000016": (2, "上证50"),
    "000905": (3, "中证500"),
    "000688": (4, "科创50"),
    "000852": (7, "中证1000"),
    "899050": (10, "北证50"),
}
PAGE = 500


def fetch_snapshot(type_id: int) -> tuple[str, list[tuple]]:
    rows: list[tuple] = []
    page, pages = 1, 1
    snap = ""
    while page <= pages:
        j = get_json(URL, {
            "reportName": "RPT_INDEX_TS_COMPONENT",
            "columns": "SECURITY_CODE,SECURITY_NAME_ABBR,MAXTRADEDATE,WEIGHT,INDUSTRY",
            "pageNumber": page, "pageSize": PAGE,
            "filter": f'(TYPE="{type_id}")',
            "source": "WEB", "client": "WEB",
        }, timeout=25)
        res = j.get("result") or {}
        pages = int(res.get("pages") or 0)
        data = res.get("data") or []
        if not data:
            break
        for r in data:
            code = r.get("SECURITY_CODE")
            if not code:
                continue
            d = str(r.get("MAXTRADEDATE") or "")[:10]
            snap = max(snap, d)
            rows.append((code, r.get("SECURITY_NAME_ABBR"), d, r.get("WEIGHT")))
        page += 1
    return snap, rows


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--indexes", default="000300,000016,000905,000852,000688,899050")
    args = ap.parse_args()
    wanted = [x.strip() for x in args.indexes.split(",") if x.strip()]

    conn = connect()
    init_db(conn)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS index_member_detail (
            index_code TEXT NOT NULL, code TEXT NOT NULL, snap_date TEXT NOT NULL,
            name TEXT, weight REAL, industry TEXT,
            PRIMARY KEY (index_code, code, snap_date)
        ) WITHOUT ROWID
    """)
    conn.commit()

    for idx in wanted:
        if idx not in TYPE_MAP:
            print(f"[members] 未知指数 {idx}，跳过")
            continue
        tid, name = TYPE_MAP[idx]
        try:
            snap, rows = fetch_snapshot(tid)
        except Exception as e:  # noqa: BLE001
            print(f"[members] {idx} {name} 抓取失败 {type(e).__name__}: {e}")
            log_fetch(conn, "index_member", idx, "err", 0, str(e))
            continue
        if not rows:
            print(f"[members] {idx} {name} 空结果")
            log_fetch(conn, "index_member", idx, "empty", 0)
            continue

        # 明细快照（用于日后回溯权重与行业变化）
        conn.executemany(
            """INSERT OR REPLACE INTO index_member_detail
               (index_code,code,snap_date,name,weight,industry) VALUES (?,?,?,?,?,?)""",
            [(idx, c, snap, n, w, None) for c, n, _d, w in rows])

        new_codes = {c for c, _n, _d, _w in rows}
        # 1) 以前在成分内、这次不在 -> 记为退出
        old = {r["code"] for r in conn.execute(
            "SELECT code FROM index_member WHERE index_code=? AND out_date IS NULL", (idx,))}
        gone = old - new_codes
        for c in gone:
            conn.execute(
                "UPDATE index_member SET out_date=? WHERE index_code=? AND code=? AND out_date IS NULL",
                (snap, idx, c))
        # 2) 新进或持续在内 -> upsert（已在则保留原 in_date）
        for c in sorted(new_codes):
            conn.execute(
                """INSERT INTO index_member(index_code,code,in_date,out_date) VALUES (?,?,?,NULL)
                   ON CONFLICT(index_code,code,in_date) DO NOTHING""", (idx, c, snap))
        conn.commit()
        n_in = conn.execute(
            "SELECT COUNT(*) FROM index_member WHERE index_code=? AND out_date IS NULL",
            (idx,)).fetchone()[0]
        log_fetch(conn, "index_member", idx, "ok", len(rows))
        print(f"[members] {idx} {name:8s} 快照 {snap} 成分 {len(rows):4d} "
              f"新进 {len(new_codes - old):3d} 退出 {len(gone):3d} 当前在册 {n_in}")

    tot = conn.execute("SELECT COUNT(*) FROM index_member").fetchone()[0]
    print(f"[members] DONE 区间记录 {tot} 条  {now_cn()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
