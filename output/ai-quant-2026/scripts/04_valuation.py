"""Step 4 — 估值快照：流通市值、总股本、PE/PB/PS、行业。

为什么单独做这一步
------------------
流通股本决定了"换手率"，而换手率是 A 股最强的因子族之一。
但日频行情接口（新浪）并不提供股本，腾讯/东财行情又容易被限流。

东财数据中心有一张 `RPT_VALUEANALYSIS_DET` 表，按「交易日」给出全市场每只股票的
    TOTAL_MARKET_CAP / NOTLIMITED_MARKETCAP_A / TOTAL_SHARES / FREE_SHARES_A
    PE_TTM / PB_MRQ / PS_TTM / PCF_OCF_TTM / BOARD_NAME
覆盖 2018-01 至今。股本变动一年只有几次，因此**每月取一个快照**再用前向填充
还原到日频，误差只出现在送转/增发发生后的一个月内，完全够用。

按「日期」查（每天一次、每次 12 页）比按「股票」查（每只 5 页 x 5589 只）
少两个数量级的请求数，这是这一层的关键设计取舍。
"""
from __future__ import annotations

import argparse
import calendar
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from aq.db import connect, init_db, log_fetch, now_cn
from aq.http import get_json

URL = "https://datacenter-web.eastmoney.com/api/data/v1/get"
COLS = ("SECURITY_CODE,TRADE_DATE,TOTAL_MARKET_CAP,NOTLIMITED_MARKETCAP_A,"
        "CLOSE_PRICE,TOTAL_SHARES,FREE_SHARES_A,PE_TTM,PB_MRQ,PS_TTM,"
        "PCF_OCF_TTM,BOARD_NAME")
PAGE = 500


def fetch_day(date: str) -> tuple[str, list[tuple], str | None]:
    rows: list[tuple] = []
    page = 1
    pages = 1
    try:
        while page <= pages:
            j = get_json(URL, {
                "reportName": "RPT_VALUEANALYSIS_DET",
                "columns": COLS,
                "pageNumber": page,
                "pageSize": PAGE,
                "sortColumns": "SECURITY_CODE",
                "sortTypes": 1,
                "filter": f"(TRADE_DATE='{date}')",
                "source": "WEB",
                "client": "WEB",
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
                rows.append((
                    code, date,
                    r.get("TOTAL_MARKET_CAP"), r.get("NOTLIMITED_MARKETCAP_A"),
                    r.get("CLOSE_PRICE"), r.get("TOTAL_SHARES"),
                    r.get("FREE_SHARES_A"), r.get("PE_TTM"), r.get("PB_MRQ"),
                    r.get("PS_TTM"), r.get("PCF_OCF_TTM"), r.get("BOARD_NAME"),
                ))
            page += 1
    except Exception as e:  # noqa: BLE001
        return date, rows, f"{type(e).__name__}: {e}"
    return date, rows, None


def month_starts(conn, start: str = "2018-01-01", end: str = "2026-12-31") -> list[str]:
    days = [r[0] for r in conn.execute(
        "SELECT date FROM trade_calendar WHERE date>=? AND date<=? ORDER BY date",
        (start, end))]
    if not days:
        return []
    firsts: dict[str, str] = {}
    for d in days:
        firsts.setdefault(d[:7], d)
    return sorted(firsts.values())


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--start", default="2018-01-01")
    args = ap.parse_args()

    conn = connect()
    init_db(conn)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS valuation (
            code TEXT NOT NULL, date TEXT NOT NULL,
            total_mv REAL, float_mv REAL, close REAL,
            total_shares REAL, free_shares REAL,
            pe_ttm REAL, pb_mrq REAL, ps_ttm REAL, pcf_ttm REAL,
            board TEXT,
            PRIMARY KEY (code, date)
        ) WITHOUT ROWID
    """)
    conn.commit()

    dates = month_starts(conn, start=args.start)
    if not dates:
        print("[valuation] trade_calendar 为空，先跑 03_calendar.py")
        return 1
    done = {r[0] for r in conn.execute("SELECT DISTINCT date FROM valuation")}
    todo = [d for d in dates if d not in done]
    print(f"[valuation] snapshots total={len(dates)} todo={len(todo)} "
          f"range={dates[0]}~{dates[-1]}", flush=True)
    if not todo:
        print("[valuation] nothing to do")
        return 0

    ok = err = 0
    nrows = 0
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = [ex.submit(fetch_day, d) for d in todo]
        for i, f in enumerate(as_completed(futs), 1):
            d, rows, e = f.result()
            if e:
                err += 1
                log_fetch(conn, "valuation", d, "err", len(rows), e)
            else:
                ok += 1
                nrows += len(rows)
                log_fetch(conn, "valuation", d, "ok" if rows else "empty", len(rows))
            if rows:
                conn.executemany(
                    """INSERT OR REPLACE INTO valuation
                       (code,date,total_mv,float_mv,close,total_shares,free_shares,
                        pe_ttm,pb_mrq,ps_ttm,pcf_ttm,board)
                       VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""", rows)
                conn.commit()
            if i % 10 == 0:
                print(f"  [{i}/{len(todo)}] ok={ok} err={err} rows={nrows}", flush=True)

    n = conn.execute("SELECT COUNT(*) c FROM valuation").fetchone()["c"]
    print(f"[valuation] DONE ok={ok} err={err} rows={n} now={now_cn()}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
