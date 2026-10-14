#!/usr/bin/env python3
"""make-gemini-index.py — 生成云端 AI（Gemini 等）的「秒读入口」GEMINI-INDEX.md。

为什么需要它
------------
云端 AI 无法读取整个仓库，只能逐个 URL 抓单文件。本脚本把两样东西合进一个文件：
  ① 最关键的当前状态全文（`state/current.md` + `plan/handoff-CURRENT.md`），
     让云端 AI 打开一个 URL 就掌握「学到哪、卡在哪、下一步做什么」；
  ② 仓库内全部受版本控制文件的直达 URL 索引，让它按需抓取其它文件。

⚠ 关键技术细节：LFS 文件必须用 media 域名
------------------------------------------
本仓库大量文件走 Git LFS。`raw.githubusercontent.com` 对 LFS 文件返回的是
**指针文本**（`version https://git-lfs...`），不是真实内容——云端 AI 拿到会
误以为是正文。LFS 文件必须改用：

    https://media.githubusercontent.com/media/<owner>/<repo>/<branch>/<path>

本脚本用 `git check-attr filter` 自动判别，对两类文件分别生成正确 URL。

用法
----
    python -B tools/make-gemini-index.py                    # 生成 GEMINI-INDEX.md
    python -B tools/make-gemini-index.py --base-url https://raw.githubusercontent.com/o/r/main/
    python -B tools/make-gemini-index.py --no-lfs           # 不索引 LFS 文件（索引更精简）
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path
from urllib.parse import quote

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

sys.path.insert(0, str(Path(__file__).resolve().parent))
from timebase import learning_today  # noqa: E402

CN_TZ = timezone(timedelta(hours=8))
OUT_NAME = "GEMINI-INDEX.md"

# 正文内嵌的两份文件：云端 AI 打开本文件即掌握续学上下文
INLINE = ("state/current.md", "plan/handoff-CURRENT.md")

# 索引分组顺序（未列出的目录排在后面）
GROUP_ORDER = [
    ".", "AGENTS.md", "learning", "state", "plan", "subjects",
    "obsidian", ".tutor", ".dsh", "tools", "upload", "mock", "upstream",
]

MAX_FILE_BYTES = 60 * 1024 * 1024   # 单文件超过此值则不索引（云端抓取不现实）


def git(root: Path, args: list[str], raw: bool = False) -> str:
    env = {"GIT_TERMINAL_PROMPT": "0", "LC_ALL": "C.UTF-8"}
    import os

    proc = subprocess.run(
        ["git", *args], cwd=str(root), capture_output=True, text=True,
        encoding="utf-8", errors="replace", env={**os.environ, **env}, timeout=300,
    )
    out = proc.stdout or ""
    return out if raw else out.strip()


def derive_base_url(root: Path) -> str:
    """从 origin 推导 raw 基址。"""
    url = git(root, ["remote", "get-url", "origin"])
    if not url:
        return ""
    if url.startswith("git@github.com:"):
        slug = url.split(":", 1)[1]
    elif "github.com/" in url:
        slug = url.split("github.com/", 1)[1]
    else:
        return ""
    slug = slug.removesuffix(".git").strip("/")
    branch = git(root, ["branch", "--show-current"]) or "main"
    return f"https://raw.githubusercontent.com/{slug}/{branch}/"


def lfs_set(root: Path) -> set[str]:
    out = git(root, ["lfs", "ls-files"])
    return {line.split(maxsplit=2)[-1].strip() for line in out.splitlines() if line.strip()}


def tracked_files(root: Path) -> list[str]:
    out = git(root, ["ls-files", "-z"], raw=True)
    return [f for f in out.split("\0") if f]


def group_of(path: str) -> str:
    return path.split("/", 1)[0] if "/" in path else "."


def build(root: Path, base_url: str, include_lfs: bool) -> str:
    files = tracked_files(root)
    lfs = lfs_set(root)
    raw_base = base_url
    media_base = base_url.replace("raw.githubusercontent.com/", "media.githubusercontent.com/media/")
    today = learning_today()
    now = datetime.now(CN_TZ).strftime("%Y-%m-%d %H:%M")

    lines: list[str] = []
    lines.append("# GEMINI-INDEX · 学习助手云端入口")
    lines.append("")
    lines.append(f"> 自动生成于 {today} {now}（中国时间）。**请勿手工编辑**——"
                 f"每次同步前由 `tools/make-gemini-index.py` 重新生成。")
    lines.append(">")
    lines.append(f"> 仓库：`{base_url.rstrip('/').rsplit('/', 2)[0].replace('https://raw.githubusercontent.com/', '')}`"
                 f"　分支：`{base_url.rstrip('/').rsplit('/', 1)[-1]}`")
    lines.append("")
    lines.append("## 给云端 AI 的读取指引")
    lines.append("")
    lines.append("1. **先读本文件的第 1、2 节**（当前状态事实卡 + 续学入口），它们已内嵌全文，无需再抓 URL。")
    lines.append("2. 需要更多上下文时，从第 3 节索引里挑 URL 抓取，**不要试图抓取全部文件**。")
    lines.append("3. 抓取优先级建议：`AGENTS.md`（教学规则）→ `learning/curriculum.json`（课程范围）"
                 "→ `subjects/<课程>/INDEX.md`（课程导航）→ `obsidian/obsidian知识库/`（教材解构内容）。")
    lines.append("4. ⚠ 标注 `[LFS]` 的文件必须用给出的 **media** URL；用 raw URL 只会拿到指针文本。")
    lines.append("")
    lines.append("---")
    lines.append("")

    # ── 1. 当前状态事实卡 ────────────────────────────────────────────────
    lines.append("## 1. 当前状态（state/current.md 全文）")
    lines.append("")
    for rel in INLINE[:1]:
        p = root / rel
        if p.is_file():
            lines.append(f"<!-- 源文件：{rel} -->")
            lines.append("")
            lines.append(p.read_text(encoding="utf-8", errors="replace").rstrip())
        else:
            lines.append(f"（缺失：{rel}）")
        lines.append("")
    lines.append("---")
    lines.append("")

    # ── 2. 续学入口 ──────────────────────────────────────────────────────
    lines.append("## 2. 续学入口（plan/handoff-CURRENT.md 全文）")
    lines.append("")
    for rel in INLINE[1:]:
        p = root / rel
        if p.is_file():
            lines.append(f"<!-- 源文件：{rel} -->")
            lines.append("")
            lines.append(p.read_text(encoding="utf-8", errors="replace").rstrip())
        else:
            lines.append(f"（缺失：{rel}）")
        lines.append("")
    lines.append("---")
    lines.append("")

    # ── 3. 文件 URL 索引 ────────────────────────────────────────────────
    groups: dict[str, list[str]] = {}
    skipped_lfs = 0
    skipped_big = 0
    for rel in files:
        if rel == OUT_NAME:
            continue
        is_lfs = rel in lfs
        if is_lfs and not include_lfs:
            skipped_lfs += 1
            continue
        p = root / rel
        if p.is_file() and p.stat().st_size > MAX_FILE_BYTES:
            skipped_big += 1
            continue
        groups.setdefault(group_of(rel), []).append(rel)

    def sort_key(g: str) -> tuple[int, str]:
        return (GROUP_ORDER.index(g) if g in GROUP_ORDER else len(GROUP_ORDER), g)

    total = sum(len(v) for v in groups.values())
    lines.append(f"## 3. 文件直达 URL 索引（{total} 个文件）")
    lines.append("")
    lines.append("格式：`相对路径` → URL。标 `[LFS]` 的必须用 media 域名。")
    if skipped_lfs:
        lines.append(f"（另有 {skipped_lfs} 个 LFS 文件未索引；加 `--lfs` 可包含）")
    if skipped_big:
        lines.append(f"（另有 {skipped_big} 个超过 60 MB 的文件未索引）")
    lines.append("")

    for g in sorted(groups, key=sort_key):
        title = "根目录" if g == "." else g
        lines.append(f"### {title}（{len(groups[g])} 个）")
        lines.append("")
        for rel in sorted(groups[g]):
            base = media_base if rel in lfs else raw_base
            url = base + quote(rel)
            tag = " `[LFS]`" if rel in lfs else ""
            lines.append(f"- `{rel}`{tag} → {url}")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## 附：本仓库的结构约定")
    lines.append("")
    lines.append("| 路径 | 含义 |")
    lines.append("|---|---|")
    lines.append("| `AGENTS.md` / `CLAUDE.md` | 教学规则与事实边界（两者强制镜像） |")
    lines.append("| `learning/` | **能力事实源**：作答、订正、困难、目标、题目、课程范围 |")
    lines.append("| `state/current.md` | 跨窗口续学的唯一事实来源 |")
    lines.append("| `plan/` | 排期与续学入口 |")
    lines.append("| `subjects/` | 各课程 INDEX、作业、课堂记录 |")
    lines.append("| `obsidian/obsidian知识库/` | 教材解构成果（markdown，教学用正文） |")
    lines.append("| `.tutor/` | 协议、配置、技能、课件解构缓存 |")
    lines.append("")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="生成云端 AI 秒读入口 GEMINI-INDEX.md")
    parser.add_argument("--root", default=".")
    parser.add_argument("--base-url", default=None, help="raw 基址；默认从 origin 推导")
    parser.add_argument("--out", default=None, help=f"输出文件名，默认 {OUT_NAME}")
    parser.add_argument("--lfs", dest="include_lfs", action="store_true",
                        help="索引中是否包含 LFS 文件（默认包含）")
    parser.add_argument("--no-lfs", dest="include_lfs", action="store_false")
    parser.set_defaults(include_lfs=True)
    args = parser.parse_args()

    root = Path(args.root).resolve()
    base = args.base_url or derive_base_url(root)
    if not base:
        print("[FAIL] 无法确定仓库基址：origin 未配置且未提供 --base-url。")
        return 1
    if not base.endswith("/"):
        base += "/"

    text = build(root, base, args.include_lfs)
    out = root / (args.out or OUT_NAME)
    out.write_text(text, encoding="utf-8", newline="\n")
    print(f"[OK  ] 已生成 {out.name}：{len(text):,} 字符，基址 {base}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
