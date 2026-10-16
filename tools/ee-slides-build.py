"""电工学课件 → 网页 AI 可读结构化层（组装阶段）。

上游：MinerU（hybrid-engine，GPU）把每个课件 PDF 解析成
      pages/pXXXXX.md + raw/.../input_content_list.json + images/*.jpg
本脚本把它们组装成 GitHub / 网页 AI 都能直接读的一层：

  slides/index/pages.jsonl     一行一页的机器可读索引（主键 deck+page）
  slides/index/manifest.json   构建元数据（源文件 sha256、页数、图数、token 估算）
  slides/text/<deck>-p###.md   逐页正文（frontmatter + 正文 + 图区描述）
  slides/assets/<deck>/p###.jpg  整页扫描图（150 dpi，版面事实的最终依据）

设计约束（按重要性）：
  1. **页码必须等于 PDF 物理页**。MinerU 的 content_list 用 page_idx（子 PDF 内的位置），
     组装时按顺序映射回原 PDF 页，错位会让所有页码引用失效。
  2. 母版噪声（水印「大连理工大学」、Logo、页码）单独归档到 noise 字段，不进正文。
  3. 公式保留 LaTeX（MinerU 已转好），不做二次改写。
  4. 本脚本不写「图形语义描述」——那是视觉通读阶段的产物，通过 merge 子命令回填。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

import fitz

ROOT = Path(__file__).resolve().parent.parent
SUBJECT = ROOT / "subjects" / "06-电工电子技术"
SRC_DIR = SUBJECT / "课件"
OUT_DIR = SUBJECT / "课件-AI可读"
WORK_DIR = ROOT / "_scratch" / "ee-slides-mineru"

RENDER_DPI = 150
JPEG_QUALITY = 78

DECK_ORDER = [
    ("C1-1", "Chapter one -1-2026中白上传.pdf", "第一章 直流电路（一）"),
    ("C1-2", "Chapter One -2-2026中白上传.pdf", "第一章 直流电路（二）"),
    ("C1-3", "Chapter One -3-2026中白上传.pdf", "第一章 直流电路（三）"),
    ("C1-4", "Chapter One -4-2026中白上传.pdf", "第一章 直流电路（四）"),
    ("C2-1", "Chapter Two-1-2026中白上传.pdf", "第二章 正弦交流电路（一）"),
    ("C2-2", "Chapter Two-2-2026中白上传.pdf", "第二章 正弦交流电路（二）"),
    ("C3-1", "Chapter Three-1-2026中白上传.pdf", "第三章 直流稳压电源（一）"),
    ("C3-2", "Chapter Three-2-2026中白上传.pdf", "第三章 直流稳压电源（二）"),
    ("C3-3", "Chapter Three-3-2026中白上传.pdf", "第三章 直流稳压电源（三）"),
    ("C4-1", "Chapter Four-1-2026中白上传.pdf", "第四章 基本放大电路（一）"),
    ("C4-2", "Chapter Four-2-2026中白上传.pdf", "第四章 基本放大电路（二）"),
    ("C4-3", "Chapter Four-3-2026中白上传.pdf", "第四章 基本放大电路（三）"),
]

WATERMARK_RE = re.compile(r"^(大连理工大学|DALIAN UNIVERSITY OF TECHNOLOGY|Dalian University of Technology)$")
NOISE_TYPES = {"header", "footer", "page_number", "aside_text"}
KEEP_TYPES = {"text", "equation", "image", "chart", "table", "code", "list"}


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def norm_key(s: str) -> str:
    return re.sub(r"[\s\u3000]+", "", s).strip().lower()


def est_tokens(text: str) -> int:
    cjk = sum(1 for c in text if "\u2e80" <= c <= "\u9fff")
    other = len(text) - cjk
    return int(cjk * 1.05 + other / 3.5) + 1


def strip_ws(s: str) -> str:
    s = re.sub(r"[ \t]{2,}", " ", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()


EXERCISE_RE = re.compile(
    r"(\bE\s?\d+\b)|(\bExample\b)|(\bExercise\b)|(\bTry to find\b)|(\bGiven that\b)|"
    r"(\bQuestions?\s*:)|(\bDetermine\b)|(\bCalculate\b)|(\bFind\b)",
    re.I,
)
# 常见元件/电量记号里被 PDF 拆成「字母 + 空格 + 下标」的合并规则（只在下标位置合并）
SYMBOL_MERGE = [
    re.compile(r"\bU\s(?=S\b|CE\b|BE\b|CC\b|BB\b|AB\b|BC\b|O\b|i\b|o\b|I\b|Z\b|[1-4]\b)"),
    re.compile(r"\bI\s(?=S\b|C\b|B\b|E\b|CEO\b|CM\b|Z\b|L\b|R\b|O\b|[1-4]\b)"),
    re.compile(r"\bR\s(?=S\b|C\b|B\b|E\b|L\b|[1-4]\b)"),
    re.compile(r"\bC\s(?=S\b|E\b|B\b|C\b|L\b|O\b|[1-4]\b)"),
    re.compile(r"\bP\s(?=CM\b|Cu\b|C\b|O\b|L\b)"),
    re.compile(r"\bT\s(?=r\b|r1\b|r2\b)"),
]


def tidy_label(s: str) -> str:
    s = s.replace("\u00a0", " ").replace("\n", " ")
    for rx in SYMBOL_MERGE:
        prev = None
        while prev != s:
            prev = s
            s = rx.sub("", s)
    return re.sub(r"[ \t]{2,}", " ", s).strip()


def page_labels(page) -> list[str]:
    """用 PyMuPDF 另取一遍页面文字层，作为「图上标注」补充。

    为什么需要：MinerU 的版面模型会把画在图里的短标注（＋、−、uO、RL、b、I）
    判成 header/footer 丢掉，而**电路图的元件名与极性恰恰全在这些碎片里**。
    这里只取非页眉/页脚区、去水印、去纯数字的碎片，按位置排序并用 ｜ 连接，
    作为独立小节保留，绝不混进正文段落。
    """
    h = page.rect.height
    blocks = []
    for b in page.get_text("dict", flags=fitz.TEXTFLAGS_TEXT).get("blocks", []):
        if b.get("type") != 0:
            continue
        yc = (b["bbox"][1] + b["bbox"][3]) / 2
        if yc < h * 0.14 or yc > h * 0.93:
            continue
        txt = " ".join(s["text"] for ln in b.get("lines", []) for s in ln.get("spans", []))
        txt = tidy_label(txt)
        if not txt or len(txt) > 90:
            continue
        if re.fullmatch(r"\d{1,3}", txt) or WATERMARK_RE.match(txt.replace(" ", "")):
            continue
        blocks.append((round(b["bbox"][1] / 14.0), b["bbox"][0], txt))
    rows: dict[int, list[str]] = {}
    for row_key, x, txt in sorted(blocks):
        rows.setdefault(row_key, []).append(txt)
    merged = []
    for row_key in sorted(rows):
        uniq = []
        for t in rows[row_key]:
            if t not in uniq:
                uniq.append(t)
        merged.append(" ｜ ".join(uniq))
    return merged[:24]


def block_md(block: dict) -> tuple[str, str]:
    """返回 (markdown, 类别)。类别用于统计与检索：text/equation/image/..."""
    kind = block.get("type", "text")
    if kind in NOISE_TYPES:
        return "", "noise"
    text = block.get("text") or block.get("content") or ""
    if kind == "equation":
        eq = strip_ws(text)
        if not eq:
            return "", "noise"
        return (eq if eq.startswith("$$") else f"$$\n{eq}\n$$"), "equation"
    if kind in ("image", "chart"):
        # 图区裁切图**不进本层**：MinerU 的裁切含大量装饰块与重复，
        # 而整页扫描图 assets/<deck>/p###.jpg 已完整保留版面事实。
        # 这里只留一句提示，指明该位置有图，正文与图形语义由视觉通读补齐。
        cap = block.get("image_caption") or block.get("chart_caption") or []
        cap = " ｜ ".join(cap) if isinstance(cap, list) else str(cap)
        note = f"（此位置版面为{'图' if kind == 'image' else '图表'}"
        note += f"：{cap.strip()}）" if cap.strip() else "，见整页扫描图）"
        return note, "image"
    if kind == "table":
        body = block.get("table_body") or text
        cap = block.get("table_caption") or []
        cap = " ｜ ".join(cap) if isinstance(cap, list) else str(cap)
        return (f"{cap}\n\n{body}" if cap.strip() else body), "table"
    body = strip_ws(text)
    if not body:
        return "", "noise"
    level = block.get("text_level")
    if kind == "text" and isinstance(level, int) and level > 0:
        return f"{'#' * min(level + 1, 6)} {body}", "heading"
    return body, "text"


def find_content_list(work: Path) -> Path | None:
    cands = sorted(work.rglob("*_content_list.json"))
    cands = [c for c in cands if "v2" not in c.name]
    return cands[0] if cands else None


def build_deck(deck_id: str, fname: str, work_root: Path, out: Path, dry: bool) -> dict:
    pdf = SRC_DIR / fname
    doc = fitz.open(pdf)
    npages = doc.page_count

    # MinerU 产物布局有两种：<work>/<deck>/（批处理驱动）与 <work>/（单册直跑）。
    # 两种都试，避免"目录不存在 → 正文全空"这种静默失败。
    work = work_root / deck_id
    cl_path = find_content_list(work) if work.exists() else None
    if cl_path is None and work_root.exists():
        cl_path = find_content_list(work_root)
    blocks_by_page: dict[int, list[dict]] = {}
    warnings: list[str] = []
    if cl_path is None:
        warnings.append("未找到 MinerU content_list，正文层为空")
    else:
        blocks = json.loads(cl_path.read_text(encoding="utf-8"))
        for b in blocks:
            idx = b.get("page_idx")
            if not isinstance(idx, int) or not (0 <= idx < npages):
                warnings.append(f"page_idx 越界块，已丢弃：{b.get('type')}")
                continue
            blocks_by_page.setdefault(idx, []).append(b)

    records = []
    text_dir = out / "text"
    if not dry:
        text_dir.mkdir(parents=True, exist_ok=True)

    for idx, page in enumerate(doc):
        page_no = idx + 1
        raw_blocks = blocks_by_page.get(idx, [])
        pieces, kinds, noise = [], Counter(), []
        for b in raw_blocks:
            txt = strip_ws(b.get("text") or "")
            if b.get("type") in NOISE_TYPES or WATERMARK_RE.match(txt.replace(" ", "")):
                if txt and len(txt) <= 60:
                    noise.append(txt)
                continue
            md, kind = block_md(b)
            kinds[kind] += 1
            if md:
                pieces.append(md)
        body = "\n\n".join(pieces)
        labels = page_labels(page) if not dry else []

        title = ""
        for b in raw_blocks:
            if b.get("type") == "text" and b.get("text_level"):
                title = strip_ws(b["text"])
                break
        if not title:
            for b in raw_blocks:
                t = strip_ws(b.get("text") or "")
                if b.get("type") == "text" and t and not WATERMARK_RE.match(t.replace(" ", "")):
                    title = t.replace("\n", " ")[:80]
                    break

        section_no, section = "", ""
        m = re.search(r"\b(\d+\.\d+(?:\.\d+)?)\b", body)
        if m:
            section_no = m.group(1)
            line = next((l for l in body.splitlines() if section_no in l), "")
            section = re.sub(r"^#+\s*", "", line).strip()[:90]
        title_zh = DECK_TITLE_ZH.get(deck_id, "")
        has_exercise = bool(re.search(r"\b(E\s?\d+|Example|Exercise|Try to find|Given that)\b", body, re.I))
        ex_label = ""
        me = re.search(r"\bE\s?(\d+)\b", body)
        if me:
            ex_label = f"E{me.group(1)}"

        page_jpg = f"assets/{deck_id}/p{page_no:03d}.jpg"
        if not dry:
            dst = out / page_jpg
            dst.parent.mkdir(parents=True, exist_ok=True)
            pix = page.get_pixmap(dpi=RENDER_DPI, alpha=False)
            pix.save(str(dst), jpg_quality=JPEG_QUALITY)

        src_rel = f"subjects/06-电工电子技术/课件/{fname}"

        records.append({
            "deck": deck_id,
            "deck_title": title_zh,
            "page": page_no,
            "source": src_rel,
            "section_no": section_no,
            "section": section,
            "title": title.replace("\n", " "),
            "exercise": has_exercise,
            "exercise_label": ex_label,
            "kinds": dict(kinds),
            "text": body,
            "labels": labels,
            "noise": sorted(set(noise)),
            "chars": len(body),
            "tokens_est": est_tokens(body) + est_tokens(" ".join(labels)),
            "page_image": page_jpg,
            "md": f"text/{deck_id}-p{page_no:03d}.md",
            "figures": kinds.get("image", 0) + kinds.get("chart", 0),
        })
    doc.close()
    return {
        "deck": deck_id,
        "file": fname,
        "deck_title": DECK_TITLE_ZH.get(deck_id, ""),
        "pages": npages,
        "sha256": sha256_file(pdf),
        "size_bytes": pdf.stat().st_size,
        "content_list": (str(cl_path.resolve().relative_to(ROOT)).replace("\\", "/")
                         if cl_path and cl_path.resolve().is_relative_to(ROOT) else (str(cl_path) if cl_path else "")),
        "warnings": warnings,
        "records": records,
    }


DECK_TITLE_ZH = {d[0]: d[2] for d in DECK_ORDER}

FENCE = "````"

USAGE_DOC = """## 这是什么

老师的电工学课件是 PPT 导出的 PDF：**电路图、波形图、特性曲线全是位图**，
纯文字层取不到，而图恰恰是这门课的全部信息。这一层把每页拆成
「可检索正文（公式为 LaTeX）+ 图上标注 + 整页扫描图 + 图区 AI 视觉通读」，
让网页 AI 不必打开 PDF 就能读到页码级的内容，并能把每一句话回指到 `[课件-页码]`。

## 读取顺序（AI 用）

1. `index/INDEX.md`（本文件）→ 知道有哪些册、哪些页、怎么取。
2. `index/manifest.json` → 每册页数 / 源文件 sha256 / 统计（判断完整性）。
3. **按需取页**，不要整库读入：
   - 云端 AI：抓 `text/<deck>-p###.md` 单页（约 0.3–1 KB），或用
     `media.githubusercontent.com` 抓 `assets/<deck>/p###.jpg`（LFS）。
   - 本地 AI：直接 `grep` `index/pages.jsonl` 定位页码，再读对应 `text/*.md`
     和 `assets/*/p###.jpg`；需要整章上下文时读 `chapters/<deck>.md`。

## 页码引用规范

正文里写 `[C3-2 p14]` 就唯一指向 `Chapter Three-2-2026中白上传.pdf` 第 14 页。
物理页号 == PPT 页码 == `assets` 里的文件名编号，三者一致，不会有印刷页码偏移问题。

## 一行一页的机器可读索引

`index/pages.jsonl` 每行一个 JSON 对象，字段：

| 字段 | 含义 |
|---|---|
| `deck` / `page` | 课件 id（C1-1…C4-3）与物理页号 |
| `source` | 原始 PDF 路径（仓库内相对路径） |
| `section_no` / `section` | 该页命中的小节号与 running head 标题 |
| `title` | 页面标题（MinerU 标题层级或首个文本框） |
| `exercise` / `exercise_label` | 是否例题/习题页，及题号（如 E1） |
| `kinds` | 各类块计数：text / equation / image / table |
| `text` | 该页正文（含 LaTeX 公式，与 `text/*.md` 同源） |
| `noise` | 已剔除的母版噪声（水印、页码等） |
| `tokens_est` | 正文 token 估算，便于挑选阅读预算 |
| `page_image` | 整页扫描图（LFS，用 media URL 取） |
| `figures` | 该页 MinerU 判定的图区数量（0 表示纯文字页） |
| `figure_description` | 图区 AI 视觉通读（电路拓扑/波形/曲线读法），可能为空 |
| `md` | 对应的逐页 markdown |

## 目录结构

| 路径 | 内容 |
|---|---|
| `index/INDEX.md` | 本文件：导航与用法 |
| `index/manifest.json` | 构建元数据与统计 |
| `index/pages.jsonl` | 一行一页的机器可读索引 |
| `chapters/<deck>.md` | 整册串读全文（含目录表） |
| `text/<deck>-p###.md` | 逐页正文（最长被引用单元） |
| `assets/<deck>/p###.jpg` | 整页扫描图（150 dpi，版面事实的最终依据；**不另存图区裁切**） |

## 事实边界（重要）

- 这一层是**课件的忠实转写**，不是讲义、不是答案。图区描述里凡属推断的读法，
  写在「读图要点」中，供教学核对，**不能当作已经学会的证据**。
- 公式来自 MinerU 的版面识别；若与 `assets/<deck>/p###.jpg` 不一致，
  **以页面图为准**，并把差异记进 `subjects/06-电工电子技术/课件/INDEX.md`。
- 页码级覆盖 = 全部页；内容级理解仍需按页核对，课件上的手写补充、口头说明不在本层内。
"""


def render_page_md(r: dict) -> str:
    """逐页 markdown：frontmatter + 正文 + 页面文字层补充 + 图区描述 + 整页图链接。"""
    desc = r.get("figure_description") or ""
    reading = r.get("figure_reading") or ""
    labels = r.get("labels") or []
    parts = [r.get("text", "").strip() or "_（MinerU 未提取到正文，回看页面图）_"]
    if labels:
        parts.append("### 页面文字层补充（图上标注）\n\n"
                     "> 这一节来自 PDF 文字层原样碎片，是画在图里的元件名、极性与坐标标签；\n"
                     "> 顺序只是版面位置，不代表语义关系，需要结合图看。\n\n"
                     + "\n".join(f"- {l}" for l in labels))
    if desc:
        block = ["## 图区内容（AI 视觉通读）", ""]
        n_fig = r.get("figures") or 0
        for i in range(1, n_fig + 1):
            block.append(f"- 图{i}")
        if n_fig:
            block.append("")
        block += [desc, ""]
        if reading:
            block += [f"**读图要点**：{reading}", ""]
        parts.append("\n".join(block).rstrip())
    lines = [
        "---",
        f"deck: {r['deck']}",
        f"deck_title: {r.get('deck_title', '')}",
        f"page: {r['page']}",
        f"source: {r['source']}",
        f"section_no: {re.sub(r'[:#]', ' ', r.get('section_no') or '')}",
        f"section: {re.sub(r'[:#]', ' ', r.get('section') or '')}",
        f"title: {re.sub(r'[:#]', ' ', r.get('title') or '')}",
        f"exercise: {'true' if r.get('exercise') else 'false'}",
        f"exercise_label: {r.get('exercise_label', '')}",
        f"page_image: {r['page_image']}",
        "---",
        "",
        f"> 出处：`{r['source']}` 第 {r['page']} 页　引用写法 `[{r['deck']} p{r['page']}]`",
        "",
        "\n\n".join(parts),
        "",
        f"![整页扫描 p{r['page']}]({r['page_image']})",
        "",
    ]
    return "\n".join(lines)


def render_chapter_md(deck_id: str, rows: list[dict]) -> str:
    head = rows[0]
    lines = [
        f"# {deck_id} · {head.get('deck_title', '')}",
        "",
        f"> 源文件：`{head['source']}`　共 {len(rows)} 页",
        f"> 课件 id `{deck_id}`；引用写法 `[{deck_id} p12]`（页码即 PDF 物理页）",
        "",
        "## 本册目录",
        "",
        "| 页 | 小节 | 标题 | 例题 | 图区 |",
        "|---|---|---|---|---|",
    ]
    for r in rows:
        title = r.get("title", "").replace("|", "／")[:56]
        sec = (r.get("section_no", "") + " " + r.get("section", "")).strip().replace("|", "／")[:40]
        ex = r.get("exercise_label", "") if r.get("exercise") else ""
        lines.append(f"| p{r['page']} | {sec} | {title} | {ex} | {r.get('figures') or 0} |")
    lines += ["", "---", ""]
    for r in rows:
        lines.append(f"## p{r['page']}"
                     + (f" · {r.get('section_no')}" if r.get("section_no") else "")
                     + (f" · {r.get('title')}" if r.get("title") else ""))
        lines.append("")
        if r.get("text", "").strip():
            lines.append(r["text"].strip())
            lines.append("")
        if r.get("figure_description"):
            lines.append("**图区内容（AI 视觉通读）**")
            lines.append("")
            for fig in r.get("figure_list") or []:
                lines.append(f"- {fig}")
            if r.get("figure_list"):
                lines.append("")
            lines.append(r["figure_description"])
            if r.get("figure_reading"):
                lines.append("")
                lines.append(f"读图要点：{r['figure_reading']}")
            lines.append("")
        lines.append(f"（整页图：`{r['page_image']}`）")
        lines.append("")
    return "\n".join(lines)


def render_index_md(man: dict, rows: list[dict]) -> str:
    t = man["totals"]
    lines = [
        "# 电工电子技术 课件 · AI 可读层",
        "",
        f"> 生成方式：{man['pipeline']}　生成日期：{man.get('date', '')}",
        f"> 覆盖：{t['decks']} 册 / {t['pages']} 页（物理页全覆盖）/ "
        f"{t['figures']} 处版面图区；"
        f"{t.get('described_pages', 0)} 页已附 AI 视觉通读图区描述",
        f"> 小节归属：{t.get('section_filled_pages', 0)}/{t['pages']} 页有小节号"
        f"（其中 {t.get('section_detected_pages', 0)} 页是课件自己印了小节标题，其余按页序向前传播）",
        f"> 正文规模：≈{t['tokens_est']:,} tokens（整库）；含例题/习题标记的页 {t['exercise_pages']} 页",
        "",
        USAGE_DOC,
        "---",
        "",
        "## 分册一览",
        "",
        "| 课件 id | 页数 | 源文件（原件不在仓库，见课件 INDEX） | 整册串读 |",
        "|---|---|---|---|",
    ]
    for d in man["decks"]:
        lines.append(f"| `{d['deck']}` | {d['pages']} | `{d['file']}` | `chapters/{d['deck']}.md` |")
    lines += [
        "",
        "## 逐页去向",
        "",
        "| 课件 | 逐页正文 | 整页扫描图 |",
        "|---|---|---|",
    ]
    for d in man["decks"]:
        n = d["pages"]
        lines.append(f"| `{d['deck']}` | `text/{d['deck']}-p001.md` … `-p{n:03d}.md` | "
                     f"`assets/{d['deck']}/p001.jpg` … `p{n:03d}.jpg` |")
    lines += [
        "",
        "## 页码 → 小节 快查（按课件分节）",
        "",
    ]
    by_deck: dict[str, list[dict]] = {}
    for r in rows:
        by_deck.setdefault(r["deck"], []).append(r)
    for deck_id, rs in by_deck.items():
        lines += [f"### {deck_id} {rs[0].get('deck_title', '')}", "",
                  "| 小节 | 页范围 | 页数 |", "|---|---|---|"]
        groups: list[tuple[str, list[int]]] = []
        for r in rs:
            key = (r.get("section_no", "") + " " + r.get("section", "")).strip() or "（未标注小节）"
            if groups and groups[-1][0] == key:
                groups[-1][1].append(r["page"])
            else:
                groups.append((key, [r["page"]]))
        for key, pages in groups:
            span = f"p{pages[0]}" + (f"–p{pages[-1]}" if len(pages) > 1 else "")
            lines.append(f"| {key.replace('|', '／')} | {span} | {len(pages)} |")
        lines.append("")
    ex = [r for r in rows if r.get("exercise")]
    lines += [
        "## 例题 / 习题页清单",
        "",
        f"共 {len(ex)} 页带例题或习题标记（`exercise: true`）。",
        "",
        "| 课件 | 页 | 题号 | 标题 |",
        "|---|---|---|---|",
    ]
    for r in ex:
        lines.append(f"| `{r['deck']}` | p{r['page']} | {r.get('exercise_label', '')} | "
                     f"{r.get('title', '').replace('|', '／')[:60]} |")
    lines.append("")
    return "\n".join(lines)



def propagate_sections(rows: list[dict]) -> int:
    """把每册内已识别的小节号向前传播，直到出现下一个节号。

    为什么需要：MinerU 只在真有标题框的页上给出小节号，而课件是「一页推进一个小节」，
    例如 C1-1 p17 标 1.4、p18 没有标题框但仍在 1.4 里。不传播的话「页码→小节」表
    会出现大片「未标注小节」，AI 无法按节取页。

    传播是**只读推断**：不编造节号，只沿用上一页已确认的节号；每页另存
    `section_detected` 说明该页是否真的印了标题，供核对。
    """
    n = 0
    for deck in {r["deck"] for r in rows}:
        cur_no, cur_title = "", ""
        for r in sorted((x for x in rows if x["deck"] == deck), key=lambda x: x["page"]):
            # refresh 路径下 rows 来自 pages.jsonl，节号已被上次传播改写过，
            # 因此用落盘的 section_detected 作为「该页自己印过标题」的判据。
            inherited = bool(r.get("_inherited_section"))
            if r.get("section_detected") is None:
                r["section_detected"] = bool(r.get("section_no")) and not inherited
            raw = (r.get("section_no") or "").strip() if not inherited else ""
            if raw:
                cur_no, cur_title = raw, r.get("section") or ""
            elif cur_no:
                if r.get("section_no") != cur_no:
                    n += 1
                r["section_no"], r["section"] = cur_no, cur_title
                r["_inherited_section"] = True
    return n


def write_layer(out: Path, results: list[dict], rows: list[dict]) -> dict:
    """写 pages.jsonl / manifest.json / text / chapters / index/INDEX.md。"""
    from datetime import datetime, timezone, timedelta
    (out / "index").mkdir(parents=True, exist_ok=True)
    (out / "chapters").mkdir(parents=True, exist_ok=True)
    (out / "text").mkdir(parents=True, exist_ok=True)

    filled = propagate_sections(rows)
    print(f"[SECTION] 小节号向前传播，补全 {filled} 页；"
          f"课件自己印了小节标题的页 {sum(1 for r in rows if r.get('section_detected'))}/{len(rows)}")
    # 先传播再渲染：渲染物（逐页 frontmatter / 整册目录 / INDEX）必须与 pages.jsonl 同值
    for r in rows:
        r.pop("_inherited_section", None)
        r["figure_list"] = [f"图{i}" for i in range(1, (r.get("figures") or 0) + 1)]
        (out / r["md"]).write_text(render_page_md(r), encoding="utf-8")

    by_deck: dict[str, list[dict]] = {}
    for r in rows:
        by_deck.setdefault(r["deck"], []).append(r)
    for deck_id, rs in by_deck.items():
        (out / "chapters" / f"{deck_id}.md").write_text(render_chapter_md(deck_id, rs), encoding="utf-8")

    manifest = {
        "generated_by": "tools/ee-slides-build.py",
        "pipeline": "MinerU hybrid-engine（本地 GPU 版面解析）→ 本脚本组装",
        "date": datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%d"),
        "source_dir": "subjects/06-电工电子技术/课件/",
        "output_dir": "subjects/06-电工电子技术/课件-AI可读/",
        "render_dpi": RENDER_DPI,
        "jpeg_quality": JPEG_QUALITY,
        "decks": [{k: v for k, v in r.items() if k != "records"} for r in results],
        "totals": {
            "decks": len(results),
            "pages": sum(r["pages"] for r in results),
            "figures": sum((r.get("figures") or 0) for r in rows),
            "figure_labels_ok": sum(1 for r in rows if r.get("figure_labels_ok")),
            "exercise_pages": sum(1 for r in rows if r.get("exercise")),
            "tokens_est": sum(r.get("tokens_est", 0) for r in rows),
            "with_description": sum(1 for r in rows if r.get("figure_description")),
            "with_reading": sum(1 for r in rows if r.get("figure_reading")),
            "described_pages": sum(1 for r in rows
                                   if r.get("figure_description") or r.get("figure_reading")),
            "section_detected_pages": sum(1 for r in rows if r.get("section_detected")),
            "section_filled_pages": sum(1 for r in rows if r.get("section_no")),
            "source_bytes": sum(r.get("size_bytes", 0) for r in results),
        },
    }
    (out / "index" / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    with (out / "index" / "pages.jsonl").open("w", encoding="utf-8", newline="\n") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    (out / "index" / "INDEX.md").write_text(render_index_md(manifest, rows), encoding="utf-8")
    return manifest


def cmd_build(args) -> int:
    out = Path(args.out)
    (out / "index").mkdir(parents=True, exist_ok=True)
    results, all_records = [], []
    for deck_id, fname, _ in DECK_ORDER:
        if args.decks and deck_id not in args.decks:
            continue
        pdf = SRC_DIR / fname
        if not pdf.exists():
            print(f"[SKIP] 缺源文件 {fname}", file=sys.stderr)
            continue
        res = build_deck(deck_id, fname, Path(args.work), out, args.dry)
        all_records.extend(res.pop("records"))
        results.append(res)
        print(f"[OK] {deck_id:<6} {res['pages']:>3}页  "
              f"正文≈{sum(r['tokens_est'] for r in all_records if r['deck']==deck_id):>6}tok  "
              f"图区{sum((r['figures'] or 0) for r in all_records if r['deck']==deck_id):>3}  {fname}", flush=True)

    # 回填已有的图形描述（若存在），保证重跑不丢；用 load_desc 统一形状
    desc = load_desc(out)
    if desc:
        for r in all_records:
            entry = desc.get(f"{r['deck']}#{r['page']}")
            if entry:
                r["figure_description"] = entry["description"]
                r["figure_reading"] = entry["reading"]
        print(f"[MERGE] 复用已有图形描述 {len(desc)} 条")

    if not args.dry:
        man = write_layer(out, results, all_records)
        print(f"[DONE] {man['totals']}")
    return 0


def load_desc(out: Path) -> dict:
    """读取描述文件，兼容两种形状。

    读图 agent 的产物形状：`{reading, figures:[逐图描述], source}`，
    正文就是 `figures` 里各条按顺序拼接；早期/手写产物可能是 `{description, reading}`。
    """
    desc_path = out / "index" / "figure-descriptions.json"
    if not desc_path.exists():
        return {}
    raw = json.loads(desc_path.read_text(encoding="utf-8"))
    norm = {}
    for key, val in raw.items():
        if isinstance(val, str):
            norm[key] = {"description": val, "reading": "", "figures": []}
            continue
        if not isinstance(val, dict):
            continue
        figs = val.get("figures") or []
        if isinstance(figs, str):
            figs = [figs]
        figs = [f for f in figs if isinstance(f, str) and f.strip()]
        desc = (val.get("description") or val.get("figure_description") or "").strip()
        norm[key] = {
            "description": desc or "\n\n".join(figs),
            "reading": (val.get("reading") or val.get("figure_reading") or "").strip(),
            "figures": figs,
        }
    return norm


def cmd_refresh(args) -> int:
    """把 figure-descriptions.json 回填进逐页/整册 markdown 与 INDEX。"""
    out = Path(args.out)
    desc = load_desc(out)
    if not desc:
        print(f"[FAIL] 缺少或为空：{out / 'index' / 'figure-descriptions.json'}", file=sys.stderr)
        return 2
    pages_path = out / "index" / "pages.jsonl"
    man_path = out / "index" / "manifest.json"
    rows = [json.loads(l) for l in pages_path.read_text(encoding="utf-8").splitlines() if l.strip()]
    man = json.loads(man_path.read_text(encoding="utf-8"))
    hit = 0
    for r in rows:
        entry = desc.get(f"{r['deck']}#{r['page']}")
        if entry and entry["description"]:
            r["figure_description"] = entry["description"]
            r["figure_reading"] = entry["reading"]
            if entry["figures"]:
                r["figure_labels_ok"] = True
            hit += 1
    man["totals"]["with_description"] = hit
    man["totals"]["figure_labels_ok"] = sum(1 for r in rows if r.get("figure_labels_ok"))
    man_path.write_text(json.dumps(man, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_layer(out, man["decks"], rows)
    print(f"[REFRESH] 回填 {hit} 页图形描述；INDEX/逐页/整册 markdown 已重建")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build", help="从 MinerU 产物组装 AI 可读层")
    b.add_argument("--work", default=str(WORK_DIR))
    b.add_argument("--out", default=str(OUT_DIR))
    b.add_argument("--decks", nargs="*")
    b.add_argument("--dry", action="store_true")
    b.set_defaults(func=cmd_build)
    r = sub.add_parser("refresh", help="把图形描述回填进 text/*.md")
    r.add_argument("--out", default=str(OUT_DIR))
    r.set_defaults(func=cmd_refresh)
    args = ap.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
