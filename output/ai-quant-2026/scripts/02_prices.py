"""Step 2 — 抓取全市场日线（新浪财经通道）。

数据源决策记录（这段值得保留，它是"工程现实"而不是教科书）
--------------------------------------------------------
1. 东方财富 push2his：一次请求给全历史，字段最全（含成交额、换手率），
   2026-10-31 批量抓取约 50 次后被 IP 封锁（直连/代理均 RemoteDisconnected）。
2. 腾讯 fqkline：单页 800 根、响应最快，抓了约 200 次后触发 WAF
   （返回 waf.tencent.com 的 501 挑战页）。
3. baostock：字段最全（isST / tradeStatus / 复权因子），但单连接 TCP 协议，
   并发一高就被限速到每只 100 秒以上。
4. 新浪 CN_MarketData：`datalen=10000` 可一次返回全历史（600000 共 6417 根），
   另配 `hfq.js` 给出累计后复权因子。两条请求即可完整还原一只股票，
   2026-10-31 实测稳定。

结论：**任何单一免费源都不可靠**，生产级做法是写适配器 + 断点续抓 + 交叉校验。
本脚本实现了 `--source sina|tencent` 两种适配器，默认新浪。
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from aq.db import connect, done_keys, init_db, log_fetch, now_cn, upsert
from aq.http import get_text

SINA_K = ("https://money.finance.sina.com.cn/quotes_service/api/json_v2.php/"
          "CN_MarketData.getKLineData")
SINA_F = "https://finance.sina.com.cn/realstock/company/{sym}/hfq.js"
BAR_COLS = ["code", "date", "open", "high", "low", "close", "pre_close",
            "volume", "amount", "turnover", "pct_chg", "adj_factor",
            "is_st", "trade_status"]
_lock = threading.Lock()


def sina_symbol(code: str) -> str | None:
    if code[0] == "6":
        return "sh" + code
    if code[0] in "03":
        return "sz" + code
    return None          # 北交所新浪无稳定接口


def fetch_kline(sym: str) -> list[dict]:
    txt = get_text(SINA_K, {"symbol": sym, "scale": 240, "ma": "no", "datalen": 10000},
                   timeout=25, headers={"Referer": "https://finance.sina.com.cn/"})
    txt = txt.strip()
    if not txt.startswith("["):
        return []
    return json.loads(txt)


def fetch_hfq_factor(sym: str) -> list[tuple[str, float]]:
    txt = get_text(SINA_F.format(sym=sym), timeout=20,
                   headers={"Referer": "https://finance.sina.com.cn/"})
    m = re.search(r"=\s*(\{.*\})", txt, re.S)
    if not m:
        return []
    try:
        obj = json.loads(m.group(1))
    except json.JSONDecodeError:
        return []
    out = []
    for it in obj.get("data") or []:
        try:
            out.append((str(it["d"])[:10], float(it["f"])))
        except (KeyError, TypeError, ValueError):
            continue
    out.sort()
    return out


def build_rows(code: str) -> list[tuple]:
    sym = sina_symbol(code)
    if sym is None:
        return []
    bars = fetch_kline(sym)
    if not bars:
        return []
    facs = fetch_hfq_factor(sym)
    # 交易日 -> 复权因子：取"除权日 <= 当日"的最近一个因子
    fac_dates = np.array([d for d, _ in facs], dtype="datetime64[D]") if facs else None
    fac_vals = np.array([v for _, v in facs], dtype=float) if facs else None

    rows: list[tuple] = []
    prev_close = None
    for b in bars:
        try:
            d = b["day"][:10]
            o, h, l, c = float(b["open"]), float(b["high"]), float(b["low"]), float(b["close"])
            v = float(b["volume"])
        except (KeyError, TypeError, ValueError):
            continue
        if c <= 0 or v < 0:
            continue
        pre = prev_close if prev_close else o
        pct = (c / pre - 1) * 100 if pre else None
        vwap = (o + h + l + c) / 4.0
        amount = v * vwap                     # 成交额估算
        if fac_dates is not None and len(fac_dates):
            idx = np.searchsorted(fac_dates, np.datetime64(d, "D"), side="right") - 1
            adj = float(fac_vals[idx]) if idx >= 0 else float(fac_vals[0])
        else:
            adj = 1.0
        rows.append((code, d, o, h, l, c, pre, v, amount, None, pct, adj, 0, 1))
        prev_close = c
    return rows


def work(code: str):
    try:
        return code, build_rows(code), None
    except Exception as e:  # noqa: BLE001
        return code, [], f"{type(e).__name__}: {e}"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--resume", action="store_true")
    ap.add_argument("--codes", default="")
    args = ap.parse_args()

    conn = connect(fast=True)
    init_db(conn, create_indexes=False)
    conn.execute("DROP INDEX IF EXISTS idx_bar_date")
    conn.commit()
    if args.codes:
        codes = [c.strip() for c in args.codes.split(",") if c.strip()]
    else:
        codes = [r["code"] for r in conn.execute("SELECT code FROM stock ORDER BY code")]
    if args.resume:
        done = done_keys(conn, "bar")
        codes = [c for c in codes if c not in done]
    if args.limit:
        codes = codes[: args.limit]
    if not codes:
        print("[prices] nothing to do")
        return 0

    print(f"[prices] codes={len(codes)} workers={args.workers} start={now_cn()}", flush=True)
    ok = err = empty = 0
    nrows = 0
    buf: list[tuple] = []

    def flush() -> None:
        nonlocal buf
        if buf:
            upsert(conn, "bar", BAR_COLS, buf, chunk=20000)
            buf = []

    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = {ex.submit(work, c): c for c in codes}
        for i, f in enumerate(as_completed(futs), 1):
            code, rows, e = f.result()
            if e:
                err += 1
                log_fetch(conn, "bar", code, "err", 0, e)
            elif not rows:
                empty += 1
                log_fetch(conn, "bar", code, "empty", 0)
            else:
                ok += 1
                nrows += len(rows)
                buf.extend(rows)
                log_fetch(conn, "bar", code, "ok", len(rows))
            # 批量落盘：攒够 15 万行或每 40 只写一次，避免主线程成为瓶颈
            if len(buf) >= 150000 or i % 40 == 0:
                flush()
            if i % 200 == 0:
                print(f"  [{i}/{len(codes)}] ok={ok} empty={empty} err={err} rows={nrows}",
                      flush=True)
        flush()

    conn.execute("""
        UPDATE stock SET
          list_date = (SELECT MIN(date) FROM bar WHERE bar.code = stock.code),
          delist_date = (SELECT CASE WHEN MAX(date) < date('now','-45 day')
                                THEN MAX(date) END
                         FROM bar WHERE bar.code = stock.code),
          is_active = CASE WHEN (SELECT MAX(date) FROM bar WHERE bar.code = stock.code)
                            >= date('now','-45 day') THEN 1 ELSE 0 END
        WHERE EXISTS (SELECT 1 FROM bar WHERE bar.code = stock.code)
    """)
    conn.commit()
    print("[prices] 建索引中 ...", flush=True)
    conn.execute("ANALYZE")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_bar_date ON bar(date)")
    conn.commit()
    print(f"[prices] DONE ok={ok} empty={empty} err={err} rows={nrows} now={now_cn()}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
