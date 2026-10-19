#!/usr/bin/env python3
"""把「无页码的文本型课程资料」登记进 learning/materials.json（资料读取事实源）。

为什么需要它
------------
`learning/materials.json` 原本只收 PDF：`page_count` ＋ 页码证据，`curriculum.py` 的
章节与单元也把它绑在 `source_pages` 上。但课程设计稿、Markdown 讲义、课程包这类资料
**没有页码**。以前只能二选一：不登记（范围进不了对账），或硬塞页数（等于把设计稿
伪装成已核读页码资料）。

本工具走第三种：`kind=document`。sha256 仍然校验（文件一改就要求重新登记），
位置改用**已核小节标题**表示：默认取正文里 `## ` 开头的标题，也可用 `--sections`
显式给出真正核过的那几节。

用法
----
    python -B tools/register-doc-material.py "subjects/13-AI技术学习/课程包_AI-TECH/courses/C00_编程与开发衔接.md"
    python -B tools/register-doc-material.py <路径> --sections "C00-01 解释器、终端与项目目录" "C00-02 依赖安装、导入与重建"
    python -B tools/register-doc-material.py <路径> --list        # 只看会登记哪些小节，不写文件
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from workspace_lock import LockTimeout, WorkspaceLock, atomic_write_text  # noqa: E402

MATERIALS = Path("learning") / "materials.json"
HEADING = "## "


def extract_sections(path: Path) -> list[str]:
    sections = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith(HEADING):
            title = line[len(HEADING):].strip()
            if title and title not in sections:
                sections.append(title)
    return sections


def dumps_like(data: dict, path: Path) -> str:
    """按目标文件现有的换行约定序列化，避免整文件行尾翻转造成假 diff。"""
    text = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    try:
        if b"\r\n" in path.read_bytes():
            text = text.replace("\n", "\r\n")
    except OSError:
        pass
    return text


def main() -> int:
    parser = argparse.ArgumentParser(description="登记无页码的文本型课程资料（kind=document）")
    parser.add_argument("path", help="工作区相对路径，.md/.txt")
    parser.add_argument("--sections", nargs="+", default=None, help="显式给出已核小节标题（默认取 '## ' 标题）")
    parser.add_argument("--list", action="store_true", dest="list_only", help="只列出小节，不写文件")
    parser.add_argument("--root", default=".")
    parser.add_argument("--note", default=None, help="附加说明")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    rel = args.path.replace("\\", "/")
    if Path(rel).is_absolute() or ".." in Path(rel).parts:
        print("ERROR: 需要工作区相对路径", file=sys.stderr)
        return 2
    target = (root / rel).resolve()
    if not target.is_file():
        print(f"ERROR: 文件不存在：{rel}", file=sys.stderr)
        return 2
    if not target.is_relative_to(root):
        print("ERROR: 文件在工作区之外", file=sys.stderr)
        return 2

    sections = args.sections or extract_sections(target)
    if not sections:
        print(f"ERROR: 未找到 '## ' 标题，且未用 --sections 指定：{rel}", file=sys.stderr)
        return 2
    if len(set(sections)) != len(sections):
        print("ERROR: 小节标题重复，无法唯一对应单元", file=sys.stderr)
        return 2

    if args.list_only:
        print(f"{rel}：{len(sections)} 个小节")
        for s in sections:
            print(f"  - {s}")
        return 0

    digest = hashlib.sha256(target.read_bytes()).hexdigest()
    entry = {
        "path": rel,
        "kind": "document",
        "sha256": digest,
        "page_count": None,
        "sections": sections,
        "note": args.note or "文本型课程资料：sha256 已登记，位置按小节标题对应；不含页码证据，不声称通读全文。",
    }

    try:
        with WorkspaceLock(root / "learning", label="register-doc-material"):
            data = json.loads((root / MATERIALS).read_text(encoding="utf-8"))
            if data.get("schema_version") != 1 or not isinstance(data.get("materials"), list):
                print("ERROR: materials.json 结构不符合预期", file=sys.stderr)
                return 2
            rows = data["materials"]
            for i, row in enumerate(rows):
                if row.get("path") == rel:
                    rows[i] = entry
                    break
            else:
                rows.append(entry)
            atomic_write_text(root / MATERIALS, dumps_like(data, root / MATERIALS))
    except LockTimeout:
        print("ERROR: 拿到写入锁超时，未写入", file=sys.stderr)
        return 1

    print(f"已登记 document 资料：{rel}")
    print(f"  sha256 = {digest}")
    print(f"  小节 {len(sections)} 个：" + "；".join(sections))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
