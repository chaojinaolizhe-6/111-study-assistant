# -*- coding: utf-8 -*-
"""版面与阅读定位检查：读 PDF 文字层，报告章节标题所在页、孤行风险、练习/详解页码。

不代替目视验收；只检查可自动化的页位与文字连续性。
输出：layout-report.txt（同时打印）
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PDF = HERE / "handout.pdf"
OUT = HERE / "layout-report.txt"

CHAPTERS = [
    ("§0 路线图", "路线图：三个坎，以及全篇唯一的主线"),
    ("§0 起点", "起点：六个动作与一句话"),
    ("§1", "二次型与主轴：椭球、特征值、谱定理"),
    ("§2", "张量与并矢：对象、写法、运算"),
    ("§3", "旋转算子与角速度"),
    ("§4", "落点一：转动惯量张量"),
    ("§5", "落点二：欧拉方程与对称陀螺"),
    ("§6", "落点三：应力张量"),
    ("§7", "独立练习"),
    ("§8", "易错点、速查与三句话"),
    ("附录 A", "练习详解"),
    ("附录 B", "指标与记号速查"),
    ("附录 C", "来源对应、补充与选读清单"),
]
SUB_MARKERS = ["2.1", "2.2", "2.3", "2.5", "4.5", "5.1", "5.3", "6.4"]
PRACTICE_RE = re.compile(r"练习\s*(P\d+)")
ANSWER_RE = re.compile(r"(P\d+)\s*详解")
CONTINUE_RE = re.compile(r"(P\d+)\s*续解")


def body_lines(page) -> list[str]:
    """去掉页眉（专题·张量与并矢 / 理论力学）与页脚（: 页码 :）。"""
    out = []
    for ln in page.get_text().splitlines():
        s = ln.strip()
        if not s:
            continue
        if s.startswith("专题") or s == "理论力学" or re.fullmatch(r":\s*\d+\s*:", s):
            continue
        out.append(s)
    return out


def norm(t: str) -> str:
    return re.sub(r"\s+", "", t)


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    try:
        import fitz
    except ImportError:
        print("需要 PyMuPDF", file=sys.stderr)
        return 2
    doc = fitz.open(PDF)
    bodies = [body_lines(p) for p in doc]
    flattened = [norm("".join(lines)) for lines in bodies]
    lines_out: list[str] = []
    say = lines_out.append

    say("=" * 78)
    say("版面与阅读定位检查（PDF 文字层，不是目视验收）")
    say("=" * 78)
    say(f"PDF：{PDF.name}；页数：{doc.page_count}")
    say("")

    say("## 章节标题页位与同页正文量")
    orphan = []
    for label, title in CHAPTERS:
        hits = [i + 1 for i, t in enumerate(flattened) if title in t]
        detail = []
        for p in hits:
            t = flattened[p - 1]
            pos = t.find(title)
            after = t[pos + len(title):]
            detail.append(f"p{p} 后随 {len(after)} 字")
            if len(after) < 60:
                orphan.append((label, p, len(after)))
        say(f"- {label}：「{title}」 -> {hits if hits else '未找到'}" + (f"（{'；'.join(detail)}）" if detail else ""))
    say("")
    if orphan:
        say("## 疑似标题孤行（标题后同页正文不足 60 字）")
        for label, p, n in orphan:
            say(f"- {label}：p{p}，后随仅 {n} 字")
    else:
        say("## 标题孤行检查：未发现“标题后同页正文不足 60 字”的章节标题。")
    say("")

    say("## 小节标记出现页（前 8 页）")
    for sub in SUB_MARKERS:
        hits = [i + 1 for i, t in enumerate(flattened) if sub in t]
        say(f"- {sub}: {hits[:8]}")
    say("")

    say("## 练习题干与详解页位")
    practice, answers, cont = {}, {}, {}
    for i, t in enumerate(flattened):
        for m in PRACTICE_RE.finditer(t):
            practice.setdefault(m.group(1), []).append(i + 1)
        for m in ANSWER_RE.finditer(t):
            answers.setdefault(m.group(1), []).append(i + 1)
        for m in CONTINUE_RE.finditer(t):
            cont.setdefault(m.group(1), []).append(i + 1)
    for pid in [f"P{i}" for i in range(1, 13)]:
        say(f"- {pid}: 题干 {practice.get(pid)}；详解 {answers.get(pid)}；续解 {cont.get(pid)}")
    say("")

    say("## 图所在页（按图号）")
    for k in range(1, 9):
        hits = [i + 1 for i, t in enumerate(flattened) if f"图{k}" in t]
        say(f"- 图 {k}: {hits}")
    say("")

    say("## 每页正文首尾（已去页眉页脚）")
    for i, raw in enumerate(bodies):
        first = raw[0][:50] if raw else "(空页)"
        last = raw[-1][:50] if raw else ""
        say(f"p{i+1:02d}: 首「{first}」 尾「{last}」")
    say("")
    say("说明：本报告只依据 PDF 文字层，不能判断字体、重叠、图内标号是否被遮挡；")
    say("目视验收仍需支持图像输入的审核者完成。")
    OUT.write_text("\n".join(lines_out) + "\n", encoding="utf-8")
    print("\n".join(lines_out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
