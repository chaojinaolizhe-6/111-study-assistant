"""Step 1 — 拉取全部财报期数据，建立 point-in-time 财务表与证券主表。

用法:
    python scripts/01_financials.py            # 增量（默认先看 fetch_log）
    python scripts/01_financials.py --force    # 全量重抓
"""
from __future__ import annotations

import argparse
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from aq.config import FIN_START_YEAR
from aq.db import connect, init_db, log_fetch, done_keys, now_cn, upsert
from aq.sources import fin_period, to_secid

FIN_COLS = ["code", "report_date", "notice_date", "eps", "bps", "roe", "revenue",
            "net_profit", "ocf_ps", "gross_margin", "div_yield", "rev_yoy",
            "np_yoy", "data_type", "name"]


def periods(start_year: int) -> list[str]:
    today = date.today().isoformat()
    out = []
    for y in range(start_year, date.today().year + 1):
        for md in ("03-31", "06-30", "09-30", "12-31"):
            p = f"{y}-{md}"
            if p <= today:
                out.append(p)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--workers", type=int, default=4)
    args = ap.parse_args()

    conn = connect()
    init_db(conn)
    ps = periods(FIN_START_YEAR)
    done = set() if args.force else done_keys(conn, "fin_period")
    todo = [p for p in ps if p not in done]
    print(f"[financials] periods total={len(ps)} todo={len(todo)}", flush=True)
    if not todo:
        print("[financials] nothing to fetch")
        return 0

    records: list[dict] = []
    t0 = now_cn()

    def work(p: str) -> tuple[str, list[dict], str | None]:
        try:
            return p, fin_period(p), None
        except Exception as e:  # noqa: BLE001
            return p, [], f"{type(e).__name__}: {e}"

    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = {ex.submit(work, p): p for p in todo}
        for i, f in enumerate(as_completed(futs), 1):
            p, rows, err = f.result()
            if err:
                print(f"  [{i}/{len(todo)}] {p} FAILED {err}", flush=True)
                log_fetch(conn, "fin_period", p, "err", 0, err)
            else:
                records.extend(rows)
                log_fetch(conn, "fin_period", p, "ok" if rows else "empty", len(rows))
                print(f"  [{i}/{len(todo)}] {p} rows={len(rows)}", flush=True)
            conn.commit()

    if not records:
        print("[financials] no records")
        return 1

    # 去重：同一 (code,report_date) 可能因快报/更正出现多行，保留 EITIME 最新的一条
    best: dict[tuple[str, str], dict] = {}
    for r in records:
        k = (r["code"], r["report_date"])
        cur = best.get(k)
        if cur is None or (r.get("eitime") or "") >= (cur.get("eitime") or ""):
            best[k] = r
    print(f"[financials] dedup {len(records)} -> {len(best)}", flush=True)

    fin_rows = [
        (r["code"], r["report_date"], r["notice_date"], r["eps"], r["bps"], r["roe"],
         r["revenue"], r["net_profit"], r["ocf_ps"], r["gross_margin"],
         r["div_yield"], r["rev_yoy"], r["np_yoy"], r["data_type"], r.get("name"))
        for r in best.values()
    ]
    upsert(conn, "fin", FIN_COLS, fin_rows)

    # 证券主表：用最新一期记录的名称/行业
    latest: dict[str, dict] = {}
    for r in best.values():
        c = r["code"]
        if c not in latest or r["report_date"] > latest[c]["report_date"]:
            latest[c] = r
    stock_rows = []
    for code, r in sorted(latest.items()):
        secid = to_secid(code)
        if not secid:
            continue
        exch = "SH" if secid.startswith("1.") else ("BJ" if code[:2] in ("43", "83", "87", "88", "92") else "SZ")
        stock_rows.append((code, secid, exch, r.get("name"), r.get("board"),
                           r.get("board_code"), None, None, 1, now_cn()))
    conn.executemany(
        """INSERT INTO stock(code,secid,exchange,name,board,board_code,list_date,delist_date,is_active,updated_at)
           VALUES (?,?,?,?,?,?,?,?,?,?)
           ON CONFLICT(code) DO UPDATE SET
             name=excluded.name, board=excluded.board, board_code=excluded.board_code,
             updated_at=excluded.updated_at""",
        stock_rows,
    )
    conn.commit()

    n_fin = conn.execute("SELECT COUNT(*) c FROM fin").fetchone()["c"]
    n_stk = conn.execute("SELECT COUNT(*) c FROM stock").fetchone()["c"]
    print(f"[financials] DONE fin={n_fin} stock={n_stk} started={t0} now={now_cn()}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
