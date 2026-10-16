"""生成「图区视觉通读」任务表，并把 agent 结果合并回课件 AI 可读层。

为什么需要这一层
----------------
课件里 90% 的信息画在图上（电路拓扑、极性、波形、特性曲线），文字层与
MinerU 都取不到「谁和谁串联、二极管朝哪边、波形削掉了哪半周」。这一层让
能看图的 AI 逐页读 `assets/<deck>/p###.jpg`，把图读成受控 JSON，写回
`index/figure-descriptions.json`，再由 ee-slides-build.py refresh 落到正文。

用法：
  python tools/ee-slides-merge-descriptions.py tasks  --out <层目录> --batches 6 [--decks C4-1]
  python tools/ee-slides-merge-descriptions.py merge  --out <层目录> --result <结果.json> [...]
  python tools/ee-slides-merge-descriptions.py status --out <层目录>

结果 JSON 形状（agent 返回的数组，或 {"pages":[...]}）：
  [{"deck":"C3-2","page":14,"figures":["图1：…"],"figure_reading":"…"}, ...]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUT = ROOT / "subjects" / "06-电工电子技术" / "课件-AI可读"

INSTRUCTION = """任务：把电工学课件页面**读成文字**，让不能看图的 AI 也知道图上画了什么。

用 read_image 逐张读取（必须真看图，禁止凭标题或文字层猜测）：
{image_list}

文字层背景（仅供定位术语，不能替代看图）：
{page_text}

只输出一个 JSON 对象（无代码围栏、无解释）：
{{"pages":[{{"deck":"<课件id>","page":<页号>,"figures":["图1：…"],"figure_reading":"…"}}]}}

`figures` 每条以「图N：」开头，依次交代：①图形类型（电路图/波形图/特性曲线/结构示意/方框图/表格）
②元件与标注（照抄图上符号：Tr、D/VD、RL、C、L、u2、uO、β、IB、UCE）③连接关系或拓扑（谁串谁并、
二极管阳极阴极各接哪、回路怎么走、处在整流器与负载之间的什么位置）④极性、参考方向、坐标轴刻度
（如 ωt 轴上的 π/2π/3π、虚线 √2U2）⑤图形说明的动作或过程（如「正半周导通电流路径」「电容充放电削平脉动」）。
页面上的公式、文字气泡、黄色高亮结论写进对应条目末尾并标明是版面文字。
`figure_reading`：一句话说明这页的图在讲什么机制、读图该盯住哪里；不要展开成讲课。
读不清就写「分辨率不足，未能辨认」，**绝不编造元件、数值或连接**。中英并存写成「二极管 D（diode）」。
不要写教学建议或学习方法。纯文字页写 `"figures":[]`，`figure_reading` 只列这页有哪些文字块。"""


def load_rows(out: Path) -> list[dict]:
    pages = out / "index" / "pages.jsonl"
    if not pages.exists():
        print(f"[FAIL] 缺少 {pages}", file=sys.stderr)
        sys.exit(2)
    return [json.loads(l) for l in pages.read_text(encoding="utf-8").splitlines() if l.strip()]


def cmd_tasks(args) -> int:
    out = Path(args.out)
    rows = load_rows(out)
    if args.decks:
        rows = [r for r in rows if r["deck"] in args.decks]
    if args.pages:
        lo, hi = (int(x) for x in args.pages.split("-"))
        rows = [r for r in rows if lo <= r["page"] <= hi]

    # 待描述页：有图区、或正文几乎为空的页（图占满整页）；可选包含全部页
    todo = rows if args.all_pages else [
        r for r in rows if (r.get("figures") or len(r.get("text", "").strip()) < 60)
    ]
    batches = [todo[i:i + args.batches] for i in range(0, len(todo), args.batches)]
    tasks = []
    for i, group in enumerate(batches):
        imgs, ctx = [], []
        for r in group:
            img = out / r["page_image"]
            imgs.append(f"- {img}   （课件 {r['deck']} 第 {r['page']} 页）")
            body = (r.get("text") or "").strip()
            ctx.append(f"── {r['deck']} p{r['page']} "
                       f"[{r.get('section_no','')} {r.get('section','')}] "
                       f"{r.get('title','')}\n{body[:1200] if body else '（文字层为空）'}")
        prompt = INSTRUCTION.format(image_list="\n".join(imgs), page_text="\n\n".join(ctx))
        tasks.append({
            "id": f"batch-{i:03d}",
            "label": f"读图 {group[0]['deck']} p{group[0]['page']}"
                     + (f"–p{group[-1]['page']}" if len(group) > 1 else ""),
            "decks": sorted({r["deck"] for r in group}),
            "pages": [{"deck": r["deck"], "page": r["page"]} for r in group],
            "prompt": prompt,
        })
    payload = {"tasks": tasks}
    out_path = Path(args.tasks_out) if args.tasks_out else out / "index" / "describe-tasks.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[TASKS] 待描述 {len(todo)}/{len(rows)} 页 → {len(tasks)} 个批次；写入 {out_path}")
    return 0


def read_json_tolerant(p: Path):
    """读 agent 写出的 JSON：可能带 UTF-8 BOM（write 工具的默认行为之一）。"""
    raw = p.read_text(encoding="utf-8-sig")
    return json.loads(raw)


def extract_pages(blob) -> list[dict]:
    if isinstance(blob, dict):
        blob = blob.get("pages") or blob.get("results") or []
    if isinstance(blob, str):
        try:
            text = blob.lstrip("\ufeff").strip()
            if text.startswith("```"):
                text = re.sub(r"^```[a-zA-Z]*\n|\n```$", "", text)
            return extract_pages(json.loads(text))
        except json.JSONDecodeError:
            return []
    return [b for b in blob if isinstance(b, dict) and "deck" in b and "page" in b]


def cmd_merge(args) -> int:
    out = Path(args.out)
    desc_path = out / "index" / "figure-descriptions.json"
    store = json.loads(desc_path.read_text(encoding="utf-8")) if desc_path.exists() else {}
    added = 0
    skipped: list[str] = []
    for path in args.result:
        p = Path(path)
        if not p.is_absolute():
            p = (ROOT / p) if (ROOT / p).exists() else Path.cwd() / p
        # 直接展开目录：读图 agent 的产物统一落在 index/desc/
        files = sorted(p.glob("*.json")) if p.is_dir() else [p]
        for f in files:
            try:
                blob = read_json_tolerant(f)
            except (OSError, json.JSONDecodeError) as exc:
                skipped.append(f"{f.name}: {exc}")
                continue
            for entry in extract_pages(blob):
                deck, page = entry["deck"], int(entry["page"])
                figs = entry.get("figures") or []
                if isinstance(figs, str):
                    figs = [figs]
                key = f"{deck}#{page}"
                store[key] = {
                    "description": entry.get("description") or entry.get("figure_description") or "",
                    "reading": entry.get("figure_reading") or entry.get("reading") or "",
                    "figures": [x for x in figs if isinstance(x, str)],
                    "source": f.name,
                }
                added += 1
    desc_path.parent.mkdir(parents=True, exist_ok=True)
    desc_path.write_text(json.dumps(store, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"[MERGE] 本次写入 {added} 页；库内合计 {len(store)} 页 → {desc_path}")
    if skipped:
        print("[SKIP] " + "；".join(skipped[:5]))
    return 0


def cmd_status(args) -> int:
    out = Path(args.out)
    rows = load_rows(out)
    desc_path = out / "index" / "figure-descriptions.json"
    store = json.loads(desc_path.read_text(encoding="utf-8")) if desc_path.exists() else {}
    need = [r for r in rows if (r.get("figures") or len(r.get("text", "").strip()) < 60)]
    have = [r for r in need if f"{r['deck']}#{r['page']}" in store]
    per = {}
    for r in rows:
        k = r["deck"]
        per.setdefault(k, [0, 0])
        if (r.get("figures") or len(r.get("text", "").strip()) < 60):
            per[k][1] += 1
            if f"{r['deck']}#{r['page']}" in store:
                per[k][0] += 1
    print(f"[STATUS] 需要描述 {len(need)} 页；已有 {len(have)} 页；缺 {len(need) - len(have)} 页")
    for k, (a, b) in sorted(per.items()):
        flag = "✅" if a == b else ("…" if a else "－")
        print(f"  {flag} {k}: {a}/{b}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)
    t = sub.add_parser("tasks")
    t.add_argument("--out", default=str(DEFAULT_OUT))
    t.add_argument("--batches", type=int, default=6, help="每个 agent 负责多少页")
    t.add_argument("--decks", nargs="*")
    t.add_argument("--pages", help="只取某页段，如 1-20")
    t.add_argument("--all-pages", action="store_true", help="连纯文字页也描述")
    t.add_argument("--tasks-out", help="任务文件输出路径")
    t.set_defaults(func=cmd_tasks)
    m = sub.add_parser("merge")
    m.add_argument("--out", default=str(DEFAULT_OUT))
    m.add_argument("--result", nargs="+", required=True, help="agent 结果 JSON 路径")
    m.set_defaults(func=cmd_merge)
    s = sub.add_parser("status")
    s.add_argument("--out", default=str(DEFAULT_OUT))
    s.set_defaults(func=cmd_status)
    args = ap.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
