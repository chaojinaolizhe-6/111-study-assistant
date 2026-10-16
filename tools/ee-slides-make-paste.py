"""把课件 AI 可读层合成「可直接粘贴给网页 AI」的整册纯文本。

为什么需要
----------
网页 AI 的抓取常被限制（例如只允许已收录域名 / 直链白名单），`raw.githubusercontent.com`
与仓库地址都可能被拒。此时最稳的办法不是换域名，而是**把内容变成一段文本**：
用户复制粘贴（或作为附件上传）即可，不依赖任何网络抓取。

产物（`paste/`，纯文本，无 LFS）：
  README.md           这一层是什么、怎么用、先看哪一册
  00-目录.md          12 册的页数 / 体量 / 一句话主题，用来挑要粘哪一册
  <deck>.md           整册串读：每页「出处锚点 + 正文 + 图上标注 + 图区视觉通读 + 读图要点」

单册 27–59 KB（约 8k–18k tokens），一次会话粘 1–2 册最稳；四章各自合计 62–172 KB。

用法：
  python tools/ee-slides-make-paste.py            # 重建 paste/
  python tools/ee-slides-make-paste.py --check    # 只报告体量，不写文件
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LAYER = ROOT / "subjects" / "06-电工电子技术" / "课件-AI可读"
OUT = ROOT / "paste"

DECK_ORDER = ["C1-1", "C1-2", "C1-3", "C1-4", "C2-1", "C2-2",
              "C3-1", "C3-2", "C3-3", "C4-1", "C4-2", "C4-3"]

DECK_NOTE = {
    "C1-1": "电路的功能与组成、电路模型、参考点与参考方向、实际电源与电源变换（KVL 引入）",
    "C1-2": "电位例题、电源/负载判别（发出还是吸收功率）、实际电源与电源变换复习",
    "C1-3": "基尔霍夫定律（KCL p11–p17、KVL p18–p25）、支路电流法、叠加定理引入",
    "C1-4": "叠加定理例题 E1–E5、等效电源定理（戴维南/诺顿）",
    "C2-1": "正弦交流电路基本概念（2.1 起）",
    "C2-2": "相量与阻抗",
    "C3-1": "3.1 半导体基础、3.2 二极管",
    "C3-2": "3.3 稳压电源结构、3.4 整流电路、3.5 滤波电路",
    "C3-3": "3.6 稳压电路（稳压管、三端集成稳压器 78XX/79XX）",
    "C4-1": "4.1 双极型晶体管：基本概念、三种工作模式、特性曲线、主要参数",
    "C4-2": "4.2 放大电路原理、4.3 静态分析（直流通路、失真）",
    "C4-3": "4.4 动态分析：性能指标、微变等效电路",
}

HEADER = """# 电工电子技术课件 · {deck}（{deck_title}）

> 来源：老师课件 `{source}`，共 {pages} 页。每页的 `[课件id p页号]` 就是该 PDF 的物理页号，
> 与课件页码一致，可以直接用来回指原页。
> 内容构成：课件正文（公式为 LaTeX）+ 页面文字层补充（画在图里的元件名与极性，顺序仅是版面位置）
> + 图区内容（对电路图/波形图/特性曲线的文字转写，含拓扑、极性、参考方向与坐标刻度）。
> 边界：这是课件的**忠实转写**，不是讲义、不含习题答案；公式若与原始页面图不一致，以 Page 图为准。
> 本册主题：{note}

"""

README = """# paste/ · 可直接粘贴给网页 AI 的课件正文

网页 AI 的抓取常被限制（只允许已收录域名、禁止直链等），`raw.githubusercontent.com`
与仓库地址都可能被拒。这一层就是为此准备的：**纯文本、无需抓取、复制粘贴或作为附件上传即可用**。

## 怎么用

1. 先看 `00-目录.md`，里面是 12 册的页数、体量与一句话主题。
2. 挑一册（单册 27–59 KB，约 8k–18k tokens），整份粘给网页 AI；一次会话建议 1–2 册，避免超上下文。
3. 要它做事时，直接引用页码，例如「按 [C3-2 p14] 到 [C3-2 p24] 讲整流电路」——
   文件里的页锚点与课件物理页一一对应。

## 按章打包（体量参考）

| 章 | 含哪几册 | 合计 |
|---|---|---|
| 第一章 直流电路 | C1-1 … C1-4 | 约 172 KB |
| 第二章 正弦交流电路 | C2-1、C2-2 | 约 62 KB |
| 第三章 直流稳压电源 | C3-1 … C3-3 | 约 157 KB |
| 第四章 基本放大电路 | C4-1 … C4-3 | 约 97 KB |

全库合计约 488 KB。若某次任务范围明确（例如只讲第四章），只粘对应的一册最省。

## 重新生成

内容由课件 AI 可读层（`subjects/06-电工电子技术/课件-AI可读/`）合成，改层后重跑：

```powershell
python tools/ee-slides-make-paste.py
```
"""


def load() -> tuple[list[dict], dict]:
    rows = [json.loads(l) for l in (LAYER / "index" / "pages.jsonl")
            .read_text(encoding="utf-8").splitlines() if l.strip()]
    desc = json.loads((LAYER / "index" / "figure-descriptions.json").read_text(encoding="utf-8"))
    return rows, desc


def render_deck(deck: str, rows: list[dict], desc: dict, compact: bool = False) -> str:
    """整册串读。compact=True 时省去「图上标注」碎片。

    图上标注（`＋ − uO RL` 这类版面文字）是从页面图上抄下来的短碎片，顺序只是版面位置；
    图区描述已经把同一张图讲成通顺的句子，因此两者信息高度重叠。体量紧张时留图区描述、
    去掉碎片，仍能看懂电路，读取量少约六分之一。
    """
    head = rows[0]
    out = [HEADER.format(deck=deck, deck_title=head.get("deck_title", ""), source=head["source"],
                         pages=len(rows), note=DECK_NOTE.get(deck, ""))]
    cur_sec = None
    for r in rows:
        sec = (r.get("section_no") or "").strip()
        if sec and sec != cur_sec:
            title = (r.get("section") or "").strip()
            title = title[len(sec):].strip() if title.startswith(sec) else title
            out.append(f"## {sec} {title}".rstrip() + "\n")
            cur_sec = sec
        page_title = (r.get("title") or "").strip()
        line = f"### [{deck} p{r['page']}]"
        if page_title and page_title != (r.get("section") or "").strip():
            line += f" {page_title}"
        out.append(line + "\n")
        body = (r.get("text") or "").strip()
        if body:
            # 逐页正文里 MinerU 会在图的位置留一行占位（「（此位置版面为图…）」）；
            # 粘贴稿下方已有专门的「图区内容」，这行纯属噪音，去掉。
            keep = [ln for ln in body.splitlines()
                    if not ln.strip().startswith("（此位置版面为图")]
            body = "\n".join(keep).strip()
        if body:
            out.append(body + "\n")
        labels = r.get("labels") or []
        if labels and not compact:
            out.append("图上标注（版面文字片段，仅供识别元件与坐标轴）：" + "；".join(labels) + "\n")
        entry = desc.get(f"{deck}#{r['page']}") or {}
        figs = entry.get("figures") or []
        n_fig = max(len(figs), int(r.get("figures") or 0))
        if n_fig:
            out.append(f"图区内容（共 {n_fig} 处版面图区）：\n")
            for f in figs:
                out.append(f"- {f.strip()}\n")
        reading = (entry.get("reading") or "").strip()
        if reading:
            out.append("读图要点：" + reading + "\n")
        out.append("")
    return "\n".join(out).rstrip() + "\n"


def render_index(rows: list[dict], sizes: dict[str, int]) -> str:
    parts = [README, "\n## 分册一览\n",
             "| 文件 | 页数 | 体量 | 主题 |", "|---|---|---|---|"]
    for deck in DECK_ORDER:
        n = sum(1 for r in rows if r["deck"] == deck)
        parts.append(f"| `{deck}.md` | {n} | {sizes.get(deck, 0) / 1024:.0f} KB | "
                     f"{DECK_NOTE.get(deck, '')} |")
    parts += ["", f"合计 {sum(sizes.values()) / 1024:.0f} KB。", ""]
    return "\n".join(parts)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--compact", action="store_true",
                    help="同时生成 compact/ 精简档（省去与图区描述重复的图上标注碎片）")
    args = ap.parse_args()

    rows, desc = load()
    by_deck: dict[str, list[dict]] = {d: [] for d in DECK_ORDER}
    for r in rows:
        by_deck.setdefault(r["deck"], []).append(r)

    texts, sizes = {}, {}
    for deck in DECK_ORDER:
        rs = by_deck.get(deck) or []
        if not rs:
            print(f"[SKIP] {deck} 无可读层数据", file=sys.stderr)
            continue
        texts[deck] = render_deck(deck, rs, desc)
        sizes[deck] = len(texts[deck].encode("utf-8"))

    compact_texts, compact_sizes = {}, {}
    if args.compact or args.check:
        for deck in DECK_ORDER:
            rs = by_deck.get(deck) or []
            if not rs:
                continue
            compact_texts[deck] = render_deck(deck, rs, desc, compact=True)
            compact_sizes[deck] = len(compact_texts[deck].encode("utf-8"))

    if args.check:
        for deck in sizes:
            print(f"  {deck:<6} {sizes[deck] / 1024:>6.1f} KB   compact {compact_sizes[deck] / 1024:>6.1f} KB")
        print(f"[CHECK] 完整档 {sum(sizes.values()) / 1024:.0f} KB；"
              f"精简档 {sum(compact_sizes.values()) / 1024:.0f} KB")
        return 0

    OUT.mkdir(exist_ok=True)
    for deck, text in texts.items():
        (OUT / f"{deck}.md").write_text(text, encoding="utf-8", newline="\n")
    (OUT / "00-目录.md").write_text(render_index(rows, sizes), encoding="utf-8", newline="\n")
    (OUT / "README.md").write_text(README, encoding="utf-8", newline="\n")
    print(f"[OK] 生成 {len(texts)} 册 + 目录 + README → {OUT}")
    for deck in DECK_ORDER:
        if deck in sizes:
            print(f"  {deck}.md  {sizes[deck] / 1024:>6.1f} KB")

    if args.compact:
        cdir = OUT / "compact"
        cdir.mkdir(exist_ok=True)
        for deck, text in compact_texts.items():
            (cdir / f"{deck}.md").write_text(text, encoding="utf-8", newline="\n")
        print(f"[OK] 精简档 → {cdir}（合计 {sum(compact_sizes.values()) / 1024:.0f} KB）")

    print(f"[TOTAL] 完整档 {sum(sizes.values()) / 1024:.0f} KB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
