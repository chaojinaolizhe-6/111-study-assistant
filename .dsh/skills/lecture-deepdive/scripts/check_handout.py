# -*- coding: utf-8 -*-
r"""check_handout.py —— 讲义交付前的「一题一块」自动检查。

用法：
    python -B .dsh/skills/lecture-deepdive/scripts/check_handout.py [file.tex ...]
    不带参数时扫描 subjects/**/*.tex。

检查项（对应 SKILL.md 硬性约束 13 与步骤 5 清单）：
  1. 每个「第 N 题」详解块的开头若干行内必须有题干：`\qstem` 或「题面／题目／已知／求」；
  2. 每个「例 N」块同样要有题面（例题可以不用 \qstem，但题干不能缺席）；
  3. 出现「作业汇总／题面照抄」字样而全文没有「答案／详解」→ 作业只抄了题面，没有解；
  4. 正文出现裸 ✓ ✗（lmroman 缺字，应写 $\checkmark$）；
  5. 警告：\qstem 没写课件页码；\qstem 前没加 \qbreak（可能被跨页拆开）。

退出码：0 全通过；1 有错误；2 只有警告。
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

HEAD_RE = re.compile(r"^\s*\\(?:subhdr|hdr)\{(.*)\}\s*$")
PROBLEM_RE = re.compile(r"第\s*\d+\s*题")
EXAMPLE_RE = re.compile(r"例\s*\d+")
STEM_MARKERS = (r"\qstem{", "题面", "题目", "已知", "求：", "求 ", "题：", "？", "?")
LOOKAHEAD = 12  # 标题后看几行


def split_blocks(text: str) -> list[tuple[str, list[str]]]:
    lines = text.splitlines()
    heads = [(i, m.group(1)) for i, line in enumerate(lines) if (m := HEAD_RE.match(line))]
    blocks: list[tuple[str, list[str]]] = []
    for k, (i, title) in enumerate(heads):
        j = heads[k + 1][0] if k + 1 < len(heads) else len(lines)
        blocks.append((title, lines[i:j]))
    return blocks


def has_stem(lines: list[str]) -> bool:
    head = "\n".join(lines[1 : 1 + LOOKAHEAD])
    return any(m in head for m in STEM_MARKERS)


def check_file(path: Path) -> tuple[list[str], list[str]]:
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    warns: list[str] = []

    for title, body in split_blocks(text):
        if PROBLEM_RE.search(title) and not has_stem(body):
            errors.append(f"题块「{title}」开头看不到题干（既无 \\qstem，也无题面／题目／已知）")

        if r"\qstem" in "\n".join(body):
            if not re.search(r"\\qstem\{\s*[（(]\s*课件", "\n".join(body)):
                warns.append(f"题块「{title}」的题干没写课件页码（应为「（课件 pXX 第 N 题）」开头）")
            start = text.index("\n".join(body))
            if not text[:start].rstrip().endswith(r"\qbreak"):
                warns.append(f"题块「{title}」的 \\qstem 前没有 \\qbreak，可能被跨页拆开")

    if re.search(r"(作业汇总|题面照抄|题面成组)", text) and not re.search(r"(答案|详解)", text):
        errors.append("作业只有题面（「作业汇总／题面照抄」），全文没有答案或详解")

    for no, line in enumerate(text.splitlines(), 1):
        if "✓" in line:
            errors.append(f"第 {no} 行有裸 ✓（lmroman 缺字），改为 $\\checkmark$")
        if "✗" in line:
            errors.append(f"第 {no} 行有裸 ✗，改用文字或 $\\times$")

    return errors, warns


def main(argv: list[str]) -> int:
    files = [Path(p) for p in argv[1:]] or sorted(Path("subjects").rglob("*.tex"))
    if not files:
        print("没有找到 .tex 文件")
        return 2

    total_err = total_warn = 0
    for path in files:
        try:
            errors, warns = check_file(path)
        except (UnicodeDecodeError, OSError) as exc:
            print(f"[跳过] {path}：{exc}")
            continue
        if not errors and not warns:
            print(f"[通过] {path.name}")
            continue
        print(f"[检查] {path}")
        for e in errors:
            print(f"   ✗ {e}")
        for w in warns:
            print(f"   ! {w}")
        total_err += len(errors)
        total_warn += len(warns)

    print(f"\n合计：错误 {total_err} 条，警告 {total_warn} 条")
    if total_err:
        return 1
    return 2 if total_warn else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
