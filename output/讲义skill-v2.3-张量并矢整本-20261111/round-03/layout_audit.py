# -*- coding: utf-8 -*-
"""文本/坐标层面的版面审计（不是目视验收）。

本脚本只用 PDF 的文本坐标做能自动判断的事：
  1. 是否有文字落到正文区之外（左右边距、页眉页脚之外）；
  2. 每页正文行数是否异常（空页或几乎空白页）；
  3. 图注页、题号页、续解页的实际页码；
  4. 图注与其引用文字是否在同一页或相邻页。
它无法判断图形几何是否正确、断行是否美观，也不能代替看渲染图。
发现硬性问题（文字出界、空白正文页）以非零退出码报告。
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import fitz

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent
PDF = ROOT / "handout.pdf"

# 版面：A4 + 左右 2.0cm 边距。
# 容差 12pt ≈ 一个汉字：中文断行会把行末标点“悬挂”到版心外，这是正常排版，
# 不算越界；只有超过一个汉字宽度才当作真正的出界。
PAGE_W, PAGE_H = 595.276, 841.89
LEFT, RIGHT = 2.0 / 2.54 * 72, PAGE_W - 2.0 / 2.54 * 72
TOL = 12.0

PROBLEMS: list[str] = []


def main() -> int:
    doc = fitz.open(PDF)
    n = doc.page_count
    print(f"PDF 页数：{n}")
    flat, raw = [], []
    for i, page in enumerate(doc, 1):
        raw.append(page.get_text())
        flat.append(re.sub(r"\s+", "", raw[-1]))

    # 1) 出界检查
    worst = []
    for i, page in enumerate(doc, 1):
        for b in page.get_text("dict")["blocks"]:
            for line in b.get("lines", []):
                for span in line["spans"]:
                    if not span["text"].strip():
                        continue
                    x0, y0, x1, y1 = span["bbox"]
                    over = max(LEFT - x0, x1 - RIGHT)
                    if over > TOL:
                        worst.append((round(over, 2), i, span["text"][:32]))
    worst.sort(reverse=True)
    if worst:
        PROBLEMS.append(f"有 {len(worst)} 个文本片段超出左右正文区")
        for w in worst[:10]:
            print(f"  [越界 {w[0]}pt] 第 {w[1]} 页：{w[2]!r}")
    else:
        print("左右正文区：没有文本片段越界（容差 12pt，即允许行末标点悬挂）")

    appA = next((i for i, t in enumerate(flat, 1) if "附录A" in t and "练习详解" in t), None)

    # 2) 正文行数
    for i, t in enumerate(raw, 1):
        lines = [s for s in t.splitlines() if s.strip()]
        body = [s for s in lines if not re.match(r"^: ?\d+ ?:$", s.strip())]
        if len(body) < 8:
            PROBLEMS.append(f"第 {i} 页正文只有 {len(body)} 行，疑似空白页")
            print(f"  [空白页] 第 {i} 页只有 {len(body)} 行正文")
    print("正文行数：每页至少 8 行（否则记为疑似空白页）")

    # 3) 图注页
    fig_pages = {}
    for i, t in enumerate(flat, 1):
        for m in re.finditer(r"图(\d+)(?:（自绘|（据课件)", t):
            fig_pages.setdefault(int(m.group(1)), []).append(i)
    print("图注所在页：", {k: v for k, v in sorted(fig_pages.items())})
    for k, v in sorted(fig_pages.items()):
        if len(v) != 1:
            PROBLEMS.append(f"图 {k} 的图注出现在多页：{v}")

    # 4) 图引用与图注的页距
    ref_ok = True
    for k, v in sorted(fig_pages.items()):
        fp = v[0]
        refs = [i for i, t in enumerate(flat, 1) if re.search(rf"图{k}(?!\d)", t)]
        near = [p for p in refs if p != fp]
        far = [p for p in near if abs(p - fp) > 3 and not (appA and p >= appA)]
        print(f"  图 {k}：图注第 {fp} 页，另在 {near} 出现引用"
              + (f"，其中正文中远离图注的 {far}" if far else ""))
        if far:
            ref_ok = False
    if not ref_ok:
        PROBLEMS.append("有图被远处文字引用（超过 3 页）")

    # 5) 题号与续解页
    starts, conts = {}, {}
    for i, t in enumerate(raw, 1):
        lines = [s.strip() for s in t.splitlines() if s.strip()]
        for k in range(len(lines) - 1):
            m = re.fullmatch(r"(P\d+)", lines[k])
            if not m:
                continue
            pid = m.group(1)
            if lines[k + 1] == "详解" and pid not in starts:
                starts[pid] = i
            if lines[k + 1] == "续解":
                after = len([s for s in lines[k + 2:] if not re.match(r"^: ?\d+ ?:$", s)])
                at_top = k + 1 <= 3
                conts.setdefault(pid, []).append((i, at_top, after))
    print("详解起始页：", dict(sorted(starts.items(), key=lambda kv: int(kv[0][1:]))))
    print("续解位置：", {k: [(c[0], "页首" if c[1] else "页中", f"后随 {c[2]} 行") for c in v]
                        for k, v in conts.items()})
    for k, v in conts.items():
        if len(v) != 1:
            PROBLEMS.append(f"{k} 的续解标题出现 {len(v)} 次：{v}")
        for page, at_top, after in v:
            if not at_top and after < 3:
                PROBLEMS.append(f"{k} 的续解标题在第 {page} 页页中且后随内容不足 3 行（像孤立标题）")

    # 6) 章节起始页（按实际标题文字定位，不按 "§k" 字样，因为导语里也会提到）
    titles = {
        "§0": "起点：矢量、矩阵与换基",
        "§1": "二次型与主轴：椭球、特征值、谱定理",
        "§2": "张量与并矢：对象、写法、运算",
        "§3": "旋转算子与角速度",
        "§4": "落点一：转动惯量张量",
        "§5": "落点二：输运定理、欧拉方程与对称陀螺",
        "§6": "落点三：应力张量",
        "§7": "独立练习",
        "§8": "易错点、速查与三句话",
        "附录A": "练习详解",
        "附录B": "指标与记号速查",
        "附录C": "来源对应、补充与自补推导",
    }
    for label, title in titles.items():
        pg = next((i for i, t in enumerate(flat, 1) if re.sub(r"\s+", "", title) in t), None)
        print(f"  {label} 标题首次出现于第 {pg} 页")

    print()
    if PROBLEMS:
        print("发现问题：")
        for p in PROBLEMS:
            print(" -", p)
        return 1
    print("坐标/文本层面未发现出界、空白页、图注重复或续解标题错位。"
          "这仍然不是目视验收：图形几何、断行观感与整页均衡需看渲染图判断。")
    return 0


if __name__ == "__main__":
    sys.exit(main())

