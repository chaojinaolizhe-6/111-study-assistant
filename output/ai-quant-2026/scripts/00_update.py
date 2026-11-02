"""一键增量更新：把数据层刷新到最新，并在需要时重算因子与模型。

用法
----
    python scripts/00_update.py              # 只更新数据（约 5--40 分钟，视缺口而定）
    python scripts/00_update.py --full       # 更新后重算因子与模型（约 40 分钟）
    python scripts/00_update.py --check      # 只体检，不写库

设计原则
--------
* **幂等**：每个抓取脚本都用 `fetch_log` 记录成功项，重跑只补缺口，不重复下载。
* **可中断**：任何一步 Ctrl-C 后重跑都会从断点继续。
* **先体检后执行**：`--check` 只读，用于判断"要不要更新"。
"""
from __future__ import annotations

import argparse
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PY = sys.executable


def run(script: str, *args: str) -> int:
    t0 = time.time()
    print(f"\n{'=' * 70}\n>>> {script} {' '.join(args)}\n{'=' * 70}", flush=True)
    rc = subprocess.call([PY, str(ROOT / "scripts" / script), *args])
    print(f"<<< {script} 退出码 {rc}  用时 {time.time() - t0:.0f}s", flush=True)
    return rc


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--full", action="store_true", help="更新后重算因子与模型")
    ap.add_argument("--check", action="store_true", help="只体检，不写库")
    args = ap.parse_args()

    if args.check:
        return run("check_db.py", "--verbose")

    steps = [
        ("01_financials.py", []),      # 增量：只补新财报期
        ("02_prices.py", ["--resume"]),  # 增量：只补新股票/失败项
        ("03_calendar.py", []),        # 全量重写（数据量小）
        ("04_valuation.py", []),       # 增量：只补新月份
        ("05_finalize.py", ["--save"]),
        ("09_index_members.py", []),   # 追加一次成分快照
    ]
    for s, a in steps:
        rc = run(s, *a)
        if rc != 0:
            print(f"\n[update] {s} 失败，停止。数据层保持在上一个一致状态，可修复后重跑。")
            return rc

    if args.full:
        for s, a in [("06_factors.py", []), ("07_model.py", []), ("08_report.py", [])]:
            rc = run(s, *a)
            if rc != 0:
                print(f"\n[update] {s} 失败")
                return rc

    print("\n[update] 全部完成。建议接着跑：python scripts/check_db.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
