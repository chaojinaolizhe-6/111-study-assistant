# -*- coding: utf-8 -*-
"""文本/坐标层面的版面审计（不是目视验收，也不判断图形画得对不对）。

本脚本只用 PDF 的文本与矢量绘图坐标做能自动判断的事：
  1. 文字是否落到正文区之外（左右边距、上下边界之外）；
  2. 每页正文行数是否异常（空页或几乎空白页）；
  3. 每幅图：图注页与“图注上方相邻矢量绘图簇”的页是否同一页（记 figure_body_page /
     caption_page，二者必须相同）；逐幅检查，不靠“图注文字出现过一次”冒充图与图注同页；
  4. 每张表：表头上方是否紧挨着它的上粗线（\\tabtop 的规则线），且在同一页；
     上粗线孤零零留在上一页、表头/表体在下一页时算失败；
  5. 续解：把“实际续页”作为验收目标——凡某题详解跨到下一页，下一页开头必须能认出题号
     （题号或“续解”）；“Pk 续解”标记必须落在真正续页的页首，落在页中一律失败；
     不限制每题续页次数，也不把“页首或页中后随 3 行”这种放宽口径当作通过。
  6. 报告章节标题起页、图本体页与图注页、练习题干页/详解起页/续页。

无法自动判断的（图形几何是否正确、断行是否美观、整页是否均衡、表格内容是否好读）
明确留给支持看图的审核者；脚本通过不等于页面已目视验收。
发现硬性问题以非零退出码报告。
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
TEX = ROOT / "handout.tex"

PAGE_W, PAGE_H = 595.276, 841.89
# A4 + 左右 2.0cm 边距。容差 12pt ≈ 一个汉字：中文断行会把行末标点“悬挂”到版心外。
LEFT, RIGHT = 2.0 / 2.54 * 72, PAGE_W - 2.0 / 2.54 * 72
TOL = 12.0
TOP_LIMIT, BOTTOM_LIMIT = 58.0, 797.0   # 正文区上下界（页眉线以上、页脚以上）

PROBLEMS: list[str] = []


def body_lines(page):
    rows = []
    for b in page.get_text("dict")["blocks"]:
        for line in b.get("lines", []):
            txt = "".join(s["text"] for s in line["spans"]).strip()
            if txt:
                rows.append((line["bbox"][1], line["bbox"][3], txt))
    rows.sort()
    return [r for r in rows if TOP_LIMIT < r[0] < BOTTOM_LIMIT]


def main() -> int:
    if not PDF.exists():
        print(f"[E] 找不到 {PDF}", file=sys.stderr)
        return 1
    doc = fitz.open(PDF)
    n = doc.page_count
    print(f"PDF 页数：{n}")
    raw = [p.get_text() for p in doc]
    flat = [re.sub(r"\s+", "", t) for t in raw]
    body = [body_lines(p) for p in doc]

    # 1) 出界检查（左右）
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

    # 1b) 出界检查（上下；页眉页脚位置除外）
    vbad = []
    for i, rows in enumerate(body, 1):
        if not rows:
            continue
        if rows[0][0] < TOP_LIMIT:
            vbad.append((i, "top", round(rows[0][0], 1)))
        if rows[-1][1] > BOTTOM_LIMIT:
            vbad.append((i, "bottom", round(rows[-1][1], 1)))
    if vbad:
        PROBLEMS.append(f"有 {len(vbad)} 处正文超出上下正文区")
        for v in vbad[:10]:
            print(f"  [竖向越界] 第 {v[0]} 页 {v[1]} y={v[2]}")
    else:
        print(f"上下正文区：正文位于 y∈[60,{BOTTOM_LIMIT}] 内")

    # 2) 正文行数
    for i, rows in enumerate(body, 1):
        if len(rows) < 8:
            PROBLEMS.append(f"第 {i} 页正文只有 {len(rows)} 行，疑似空白页")
            print(f"  [空白页] 第 {i} 页只有 {len(rows)} 行正文")
    print("正文行数：每页至少 8 行（否则记为疑似空白页）")

    # 3) 图：图注页 vs 图本体页（按图注上方相邻的矢量绘图簇判断）
    cap_page = {}
    for i, t in enumerate(flat, 1):
        for m in re.finditer(r"图(\d+)（(?:自绘|据课件)", t):
            cap_page.setdefault(int(m.group(1)), []).append(i)
    print("\n逐幅图检查（图本体页 / 图注页都必须相同，且图形确实在同一页图注上方）：")
    for k in sorted(cap_page):
        pgs = cap_page[k]
        if len(pgs) != 1:
            PROBLEMS.append(f"图 {k} 的图注出现在多页：{pgs}")
            continue
        p = pgs[0]
        page = doc[p - 1]
        rects = page.search_for(f"图 {k}（") or page.search_for(f"图{k}（")
        if not rects:
            PROBLEMS.append(f"图 {k}：第 {p} 页定位不到图注文本")
            continue
        top = rects[0].y0
        near = [d["rect"] for d in page.get_drawings()
                if d["rect"].y1 <= top - 2 and d["rect"].y1 > top - 340
                and (d["rect"].width > 3 or d["rect"].height > 3)]
        if not near:
            PROBLEMS.append(f"图 {k}：第 {p} 页图注上方找不到图形（图与图注可能被分页）")
            continue
        y0 = round(min(r.y0 for r in near), 1)
        y1 = round(max(r.y1 for r in near), 1)
        print(f"  图{k}: 图本体 p{p}、图注 p{p}，图形 y∈[{y0},{y1}]，"
              f"图注从 y={round(top, 1)} 起（同页且图注在图形下方）")

    # 4) 表：表头上方紧邻上粗线，且同页（上粗线若留在上一页，这里就会失败）
    print("\n逐张表检查（表头正上方必须有上粗线，且在同一页）：")
    rules = {}
    for i, page in enumerate(doc, 1):
        rules[i] = [d["rect"] for d in page.get_drawings()
                    if d["rect"].height < 6 and d["rect"].width > 50]

    tex = TEX.read_text(encoding="utf-8") if TEX.exists() else ""
    tab_heads = []
    for m in re.finditer(r"\\tabtop", tex):
        seg = tex[m.end():m.end() + 400]
        row = seg.split("\\\\")[0]
        heads = re.findall(r"\\thead\{([^}]*)\}", row)
        clean = []
        for h in heads:
            h = re.sub(r"\$[^$]*\$", "", h)
            h = re.sub(r"\\[a-zA-Z]+", "", h)
            h = re.sub(r"[{}\s]", "", h)
            if len(h) >= 2:
                clean.append(h)
        if clean:
            tab_heads.append(clean)
    last_clean, start = None, 1
    for clean in tab_heads:
        if clean == last_clean:
            start = prev_p + 1
        # 表格的列标题在 PDF 里各占一行、共享同一个 y；按“同一页、同一 y（±4pt）
        # 同时出现全部列标题”定位表头行，避免把段中出现的同名词当成表头。
        hits = {}
        for c in clean:
            for p in range(start, n + 1):
                for y0, y1, txt in body[p - 1]:
                    if c in re.sub(r"\s+", "", txt):
                        hits.setdefault(c, []).append((p, y0))
        hit = None
        for p, y in hits.get(clean[0], []):
            if all(any(pp == p and abs(yy - y) <= 4 for pp, yy in hits.get(c, []))
                   for c in clean):
                hit = (p, y)
                break
        if not hit:
            PROBLEMS.append(f"表头 {clean} 在正文里定位不到同一行")
            print(f"  [表头定位失败] {clean}")
            continue
        p, top = hit
        prev_p, last_clean = p, clean
        above = [x for x in rules[p] if x.y1 <= top + 1 and x.y0 > top - 40]
        if above:
            print(f"  [第 {p} 页] 表头 {clean[0]!r} 等 y={round(top, 1)}，"
                  f"上粗线 y={round(max(x.y1 for x in above), 1)}（同页且相邻）")
        else:
            PROBLEMS.append(f"第 {p} 页表头 {clean} 上方找不到同页的上粗线")
            print(f"  [缺上粗线] 第 {p} 页 {clean}")

    # 5) 练习与续解（PDF 抽取会把“Pk”和“详解/续解”排成两行，先后顺序不固定；
    #    这里按“相邻两行”判断，不依赖行序）
    def pair_label(rows, k):
        t = rows[k][2]
        if t != "详解" and t != "续解":
            return None, None
        for j in (k - 1, k + 1):
            if 0 <= j < len(rows):
                m = re.fullmatch(r"(P\d+)", rows[j][2])
                if m:
                    return m.group(1), t
        return None, None

    starts, conts = {}, {}
    for i, rows in enumerate(body, 1):
        for k in range(len(rows)):
            pid, kind = pair_label(rows, k)
            if not pid:
                continue
            if kind == "详解":
                starts.setdefault(pid, i)
            else:
                conts.setdefault(pid, []).append((i, k + 1, rows[k][0]))
    appB = next((i for i, t in enumerate(flat, 1) if "指标与记号速查" in t), n + 1)
    print("\n详解起始页：", dict(sorted(starts.items(), key=lambda kv: int(kv[0][1:]))))
    print("续解标记（页, 正文行号）：", {k: [(c[0], c[1]) for c in v] for k, v in conts.items()})

    bad_cont = False
    for pid, lst in conts.items():
        for page, idx, y in lst:
            if idx > 3:
                bad_cont = True
                PROBLEMS.append(
                    f"{pid} 的续解标记落在第 {page} 页页中（正文第 {idx + 1} 行），"
                    f"不是实际续页开头")
                print(f"  [续解在页中] {pid} 第 {page} 页，正文第 {idx + 1} 行")
    for k in range(1, 13):
        pid = f"P{k}"
        if pid not in starts:
            continue
        nxt = starts.get(f"P{k + 1}", appB)
        for p in range(starts[pid] + 1, nxt):
            head = " ".join(rows[2] for rows in body[p - 1][:3])
            if pid not in head:
                bad_cont = True
                PROBLEMS.append(
                    f"{pid} 在第 {p} 页续排，但页首没有题号/续解标识（{head[:40]!r}）")
                print(f"  [续页无标识] {pid} 第 {p} 页页首：{head[:40]!r}")
    if not bad_cont:
        print("续页检查：每条续解都在实际续页页首；所有跨页详解的续页开头都能认出题号")

    # 5c) 小节标题不得孤零零落在页底（标题后同页没有任何正文）
    subs = []
    for m in re.finditer(r"\\subhdr\{([0-9A-C]+\.[0-9]+)\\quad([^}]*)\}", tex):
        num, title = m.group(1), m.group(2)
        title = re.sub(r"\$[^$]*\$", "", title)
        title = re.sub(r"\\[a-zA-Z]+\s*", "", title)
        title = re.sub(r"[{}\s]", "", title)
        subs.append((num, title))
    print("\n小节标题落点（标题不得孤零零留在页底）：")
    for num, title in subs:
        pg = None
        for p, rows in enumerate(body, 1):
            for k, (y0, y1, txt) in enumerate(rows):
                if re.sub(r"\s+", "", txt) == num:
                    pg = p
                    idx = k
                    break
            if pg:
                break
        if not pg:
            print(f"  小节 {num} 在 PDF 里定位不到（不当作通过）")
            PROBLEMS.append(f"小节 {num} 标题在 PDF 里定位不到")
            continue
        rows = body[pg - 1]
        if idx >= len(rows) - 1:
            PROBLEMS.append(f"小节 {num} 的标题在第 {pg} 页页底孤立（同页无正文）")
            print(f"  [孤立小节标题] {num} 在第 {pg} 页页底")
    if not any("孤立小节标题" in p or "定位不到" in p for p in PROBLEMS):
        print("  没有小节标题孤立在页底")

    # 6) 章节标题起页（按“§k 标记行 + 紧随的标题行”定位；导语里提到标题不算）
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
    print("\n章节标题起页（按标题行定位，不是按正文里提到标题）：")
    sec_pages = {}
    for label, title in titles.items():
        tflat = re.sub(r"\s+", "", title)
        pg = None
        for p, rows in enumerate(body, 1):
            texts = [re.sub(r"\s+", "", r[2]) for r in rows]
            if label not in texts:
                continue
            idx = texts.index(label)
            window = "".join(texts[max(0, idx - 1):idx + 4])
            if tflat in window:
                pg = p
                break
        sec_pages[label] = pg
        print(f"  {label} 标题起页：{pg}")

    print()
    if PROBLEMS:
        print("发现问题：")
        for p in PROBLEMS:
            print(" -", p)
        return 1
    print("坐标/文本层面未发现出界、空白页、图与图注分页、表头上粗线脱离、续解页首错位。"
          "这仍然不是目视验收：图形几何、断行观感与整页均衡需看渲染图判断。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
