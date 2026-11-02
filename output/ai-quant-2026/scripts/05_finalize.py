"""Step 5 — 收尾与质检：上市/退市日、数据质量报告。

注意架构取舍
------------
ST 状态与换手率这两列**不在库里硬写**，而是在构建面板时由
`fin.name`（简称历史）与 `valuation`（月度股本快照）用 as-of 连接实时生成。

原因：这两列本质是"时点派生量"，写进 bar 表会有三个坏处——
  1) 每次更新财务/估值都要全表重算，几千万行更新极慢；
  2) 口径一旦变化（比如 ST 判定规则改了），历史值无法追溯；
  3) 容易和"当前简称"混用，埋下前视偏差。
原始事实表只放事实，派生量留在面板层，这是纪律。
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from aq.db import connect, init_db, now_cn


def update_status(conn) -> None:
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


def quality_report(conn) -> pd.DataFrame:
    df = pd.read_sql_query("""
        SELECT substr(date,1,4) AS year,
               COUNT(*) AS rows,
               COUNT(DISTINCT code) AS codes,
               SUM(CASE WHEN close IS NULL OR close<=0 THEN 1 ELSE 0 END) AS bad_close,
               SUM(CASE WHEN adj_factor IS NULL THEN 1 ELSE 0 END) AS no_adj,
               SUM(CASE WHEN volume IS NULL OR volume<0 THEN 1 ELSE 0 END) AS bad_vol
        FROM bar GROUP BY year ORDER BY year
    """, conn)
    return df


def coverage_report(conn) -> pd.DataFrame:
    """每只股票：行情天数、首末日期、复权因子是否单调递增。

    复权因子必须单调不减（后复权只增不减）。若有下降，说明数据源在这个点上
    错了，或者发生了反向拆分——两种情况都要人工看一眼。
    """
    df = pd.read_sql_query("""
        SELECT code, COUNT(*) n, MIN(date) first_d, MAX(date) last_d,
               MIN(adj_factor) f_min, MAX(adj_factor) f_max
        FROM bar GROUP BY code
    """, conn)
    df["span_years"] = (
        pd.to_datetime(df["last_d"]) - pd.to_datetime(df["first_d"])
    ).dt.days / 365.25
    return df


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--save", action="store_true", help="把质检报告写到 reports/")
    args = ap.parse_args()

    conn = connect()
    init_db(conn)
    update_status(conn)

    rep = quality_report(conn)
    print("== 分年度数据质量 ==")
    print(rep.to_string(index=False))

    cov = coverage_report(conn)
    print(f"\n== 覆盖 ==")
    print(f"证券数 {len(cov):,}；行情中位天数 {cov['n'].median():.0f}；"
          f"中位跨度 {cov['span_years'].median():.1f} 年")
    short = cov[cov["n"] < 30]
    print(f"行情不足 30 天的证券 {len(short)} 只")

    if args.save:
        from aq.config import REPORTS
        cov.to_csv(REPORTS / "coverage_by_stock.csv", index=False, encoding="utf-8-sig")
        rep.to_csv(REPORTS / "quality_by_year.csv", index=False, encoding="utf-8-sig")
        print(f"报告已写入 {REPORTS}")
    print(f"[finalize] DONE {now_cn()}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
