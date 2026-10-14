#!/usr/bin/env python3
"""session-close-and-sync.py — 收尾 + 同步的唯一包装入口。

为什么要有它
------------
`tools/session-close.py` 是本工作区的**收尾唯一入口**（12 步，含一致性核对）。
用户明确要求**不修改它的本体**。因此本脚本作为外层包装，把「收尾」与「同步」
串成一个动作，同时补上原设计缺失的 C3 兜底：

    收尾通过  → 生成 GEMINI-INDEX → 推送到 main
    收尾失败  → 把当前状态提交并推送到 wip/broken-state 分支（故障备份）

C3 是什么：原设计规定「session-close 全部通过之后才同步」，
于是**恰恰在出问题时反而没有备份**——与备份目的相悖。
这里用独立分支兜底：main 保持干净可用，故障现场另存一份。

用法
----
    python -B tools/session-close-and-sync.py
    python -B tools/session-close-and-sync.py --today 2026-10-14
    python -B tools/session-close-and-sync.py --no-sync      # 只收尾，不同步
    python -B tools/session-close-and-sync.py --carry-over plan/today-<昨天>.md

退出码：0 收尾通过（同步成功与否另报）／1 收尾失败（已尝试故障备份）。

⚠ 本脚本不修改任何学习数据；入账与订正仍走各自的专用工具。
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

sys.path.insert(0, str(Path(__file__).resolve().parent))
from timebase import learning_today  # noqa: E402

BROKEN_BRANCH = "wip/broken-state"


def run_script(script: Path, args: list[str], root: Path, capture: bool = False) -> tuple[int, str]:
    if not script.is_file():
        return 127, f"脚本不存在：{script}"
    proc = subprocess.run(
        [sys.executable, "-B", str(script), "--root", str(root), *args],
        cwd=str(root),
        capture_output=capture,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=1800,
    )
    out = (proc.stdout or "") if capture else ""
    return proc.returncode, out


def git(root: Path, args: list[str], check: bool = False) -> tuple[int, str]:
    env = dict(os.environ)
    env["GIT_TERMINAL_PROMPT"] = "0"
    env["GCM_INTERACTIVE"] = "never"
    env["LC_ALL"] = "C.UTF-8"
    proc = subprocess.run(
        ["git", *args], cwd=str(root), capture_output=True, text=True,
        encoding="utf-8", errors="replace", env=env, timeout=1800,
    )
    out = ((proc.stdout or "") + (proc.stderr or "")).strip()
    if check and proc.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} 失败：{out}")
    return proc.returncode, out


def backup_broken_state(root: Path, today: str) -> None:
    """收尾失败时的故障备份：提交当前现场并推到 wip/broken-state。

    main 分支保持不动（用 --soft 撤销本地提交），避免把半成品状态混进主线。
    """
    print()
    print("[兜底] 收尾未通过 → 尝试把当前现场备份到 " + BROKEN_BRANCH)

    rc, _ = git(root, ["add", "-A"])
    if rc != 0:
        print("[WARN] git add 失败，跳过故障备份。")
        return

    rc, out = git(root, ["commit", "-m", f"{today} WIP 故障备份（session-close 未通过）"])
    if rc != 0:
        print(f"[INFO] 无变更可备份（{out.splitlines()[-1] if out else ''}）")
        return

    rc, out = git(root, ["push", "-f", "origin", f"HEAD:refs/heads/{BROKEN_BRANCH}"])
    if rc == 0:
        print(f"[OK  ] 故障现场已备份到远端分支 {BROKEN_BRANCH}（main 未受影响）")
    else:
        print(f"[WARN] 故障备份推送失败：{out.splitlines()[-1] if out else out}")

    # 撤销本地提交，保留改动在工作区（不污染 main）
    rc, _ = git(root, ["reset", "--soft", "HEAD~1"])
    if rc == 0:
        print("[INFO] 已撤销本地提交，改动仍留在工作区。")
    else:
        print("[WARN] 撤销本地提交失败——main 上多了一个 WIP 提交，请手工 git reset --soft HEAD~1。")


def main() -> int:
    parser = argparse.ArgumentParser(description="收尾 + 同步的唯一包装入口（不改 session-close.py 本体）")
    parser.add_argument("--root", default=".")
    parser.add_argument("--today", default=None)
    parser.add_argument("--carry-over", default=None, help="昨日清单路径（结转未完成项）")
    parser.add_argument("--no-sync", action="store_true", help="只收尾，不做任何 git 操作")
    parser.add_argument("--no-index", action="store_true", help="不重新生成 GEMINI-INDEX.md")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    today = args.today or learning_today()

    # ── 1. 收尾（唯一入口，本体不动）──────────────────────────────────
    print("=" * 66)
    print("步骤 1/3  会话收尾（tools/session-close.py）")
    print("=" * 66)
    close_args: list[str] = ["--today", today]
    if args.carry_over:
        close_args += ["--carry-over", args.carry_over]
    rc_close, _ = run_script(root / "tools" / "session-close.py", close_args, root)

    if rc_close != 0:
        print()
        print(f"[FAIL] 收尾未全部通过（退出码 {rc_close}）——**不声称已保存完整**。")
        if not args.no_sync:
            backup_broken_state(root, today)
        return 1

    print()
    print("[OK  ] 收尾 12 步全部通过。")

    if args.no_sync:
        print("[INFO] --no-sync：跳过索引生成与同步。")
        return 0

    # ── 2. 生成云端 AI 秒读入口 ────────────────────────────────────────
    print()
    print("=" * 66)
    print("步骤 2/3  生成 GEMINI-INDEX.md")
    print("=" * 66)
    if args.no_index:
        print("[INFO] --no-index：跳过。")
    else:
        rc_idx, out = run_script(
            root / "tools" / "make-gemini-index.py", [], root, capture=True
        )
        print(out.strip() or f"[WARN] 生成脚本退出码 {rc_idx}")
        if rc_idx != 0:
            print("[WARN] GEMINI-INDEX 生成失败——继续同步，但云端入口可能是旧的。")

    # ── 3. 同步 ────────────────────────────────────────────────────────
    print()
    print("=" * 66)
    print("步骤 3/3  同步到 GitHub（tools/git-sync.py）")
    print("=" * 66)
    rc_sync, _ = run_script(root / "tools" / "git-sync.py", [], root)
    if rc_sync != 0:
        print()
        print(f"[WARN] 收尾已通过，但同步失败（退出码 {rc_sync}）。本地数据完好，可稍后重跑。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
