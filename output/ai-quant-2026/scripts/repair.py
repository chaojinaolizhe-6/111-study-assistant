"""修复：找出"日志说成功但没有行情"的证券并重抓。

这类"假成功"在批量抓取里很常见：进程被中断时，日志已经写了 ok，
但数据还留在内存缓冲区里没落盘。必须显式核对，否则股票池会静默缺口。
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from aq.db import connect, init_db, now_cn
from aq.panel import load_bars


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=900, help="只检查最近 N 个交易日")
    args = ap.parse_args()

    conn = connect()
    init_db(conn)

    have = {r[0] for r in conn.execute("SELECT DISTINCT code FROM bar")}
    allc = {r[0] for r in conn.execute("SELECT code FROM stock")}
    missing = sorted(allc - have)
    print(f"[repair] 无行情证券 {len(missing)} 只 / 共 {len(allc)}")

    # 按交易所分组统计
    from collections import Counter
    ex = dict(conn.execute("SELECT code, exchange FROM stock"))
    print("  分布:", Counter(ex.get(c, "?") for c in missing).most_common())

    # 最近一个交易日的覆盖率
    last = conn.execute("SELECT MAX(date) FROM bar").fetchone()[0]
    n_last = conn.execute("SELECT COUNT(*) FROM bar WHERE date=?", (last,)).fetchone()[0]
    print(f"[repair] 最新交易日 {last} 有 {n_last} 只股票有行情")

    # 找出日志 ok 但库里没数据 / 数据过短的
    rows = conn.execute("""
        SELECT s.code, l.n_rows, (SELECT COUNT(*) FROM bar b WHERE b.code=s.code) AS actual
        FROM stock s LEFT JOIN fetch_log l ON l.task='bar' AND l.key=s.code
        WHERE l.status='ok'
    """).fetchall()
    fake = [r["code"] for r in rows if (r["actual"] or 0) == 0]
    print(f"[repair] 日志 ok 但无数据: {len(fake)} 只")
    if fake:
        with open(Path(__file__).parent.parent / "data" / "repair_codes.txt", "w") as f:
            f.write(",".join(fake))
        print("  已写入 data/repair_codes.txt，可用 02_prices.py --codes 重抓")
    print(f"[repair] DONE {now_cn()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
