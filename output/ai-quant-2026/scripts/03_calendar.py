"""Step 3 — 交易日历与指数行情（新浪通道）。

交易日历取沪深 300 指数的日线日期：这是最权威的"全市场是否交易"口径，
能自动覆盖春节、国庆等长假与临时休市，比用工作日推算可靠。
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from aq.config import INDEXES
from aq.db import connect, init_db, now_cn
from aq.http import get_text

SINA_K = ("https://money.finance.sina.com.cn/quotes_service/api/json_v2.php/"
          "CN_MarketData.getKLineData")
SINA_SYM = {
    "000300": "sh000300", "000905": "sh000905", "000852": "sh000852",
    "000016": "sh000016", "000985": "sh000985", "399006": "sz399006",
    "000001": "sh000001",
}


def fetch_index(code: str) -> list[dict]:
    sym = SINA_SYM.get(code)
    if not sym:
        return []
    txt = get_text(SINA_K, {"symbol": sym, "scale": 240, "ma": "no", "datalen": 10000},
                   timeout=25, headers={"Referer": "https://finance.sina.com.cn/"})
    txt = txt.strip()
    if not txt.startswith("["):
        return []
    return json.loads(txt)


def main() -> int:
    ap = argparse.ArgumentParser()
    args = ap.parse_args()
    conn = connect()
    init_db(conn)

    all_dates: set[str] = set()
    for code, (_secid, name) in INDEXES.items():
        bars = fetch_index(code)
        rows = []
        prev = None
        for b in bars:
            try:
                d = b["day"][:10]
                o, h, l, c = (float(b["open"]), float(b["high"]),
                              float(b["low"]), float(b["close"]))
                v = float(b.get("volume") or 0)
            except (KeyError, TypeError, ValueError):
                continue
            pct = (c / prev - 1) * 100 if prev else None
            rows.append((code, d, o, h, l, c, v, None, pct))
            prev = c
            all_dates.add(d)
        conn.executemany(
            """INSERT OR REPLACE INTO index_bar(code,date,open,high,low,close,volume,amount,pct_chg)
               VALUES (?,?,?,?,?,?,?,?,?)""", rows)
        conn.commit()
        print(f"[calendar] {code} {name} rows={len(rows)}", flush=True)

    cal = [(d, 1) for d in sorted(all_dates)]
    conn.executemany("INSERT OR REPLACE INTO trade_calendar(date,is_open) VALUES (?,?)", cal)
    conn.commit()
    n = conn.execute("SELECT COUNT(*) c FROM trade_calendar").fetchone()["c"]
    rng = conn.execute("SELECT MIN(date) a, MAX(date) b FROM trade_calendar").fetchone()
    print(f"[calendar] DONE trading_days={n} range={rng['a']}~{rng['b']} {now_cn()}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
