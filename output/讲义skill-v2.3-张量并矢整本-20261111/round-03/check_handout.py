# -*- coding: utf-8 -*-
"""本轮讲义静态检查入口。

调用冻结的 lecture-deepdive v2.3.0 的 check_handout.py，对 handout.tex
做 appendix 模式检查，并读取最终 handout.log。退出码沿用检查器：
0 无问题，1 有错误，2 只有人工复核线索。
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent
CHECKER = ROOT.parent / ".dsh" / "skills" / "lecture-deepdive" / "scripts" / "check_handout.py"


def main() -> int:
    if not CHECKER.exists():
        print(f"[E] 找不到冻结检查器：{CHECKER}", file=sys.stderr)
        return 1
    tex = ROOT / "handout.tex"
    log = ROOT / "handout.log"
    if not tex.exists():
        print(f"[E] 找不到 {tex}", file=sys.stderr)
        return 1
    if not log.exists():
        print(f"[E] 找不到 {log}；请先完成两遍 XeLaTeX", file=sys.stderr)
        return 1
    cmd = [
        sys.executable,
        "-B",
        str(CHECKER),
        str(tex),
        "--mode",
        "appendix",
        "--log",
        str(log),
    ]
    print("[运行]", " ".join(cmd))
    result = subprocess.run(cmd, cwd=str(ROOT))
    return int(result.returncode)


if __name__ == "__main__":
    sys.exit(main())
