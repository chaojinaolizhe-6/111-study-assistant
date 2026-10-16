"""电工学课件视觉通读：按分段打印 agent 提示（含各自输出路径）。

用法：
  python tools/ee-slides-task-prompt.py --start 0 --count 2 [--no-context]
"""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LAYER = ROOT / "subjects" / "06-电工电子技术" / "课件-AI可读"
TASKS = LAYER / "index" / "describe-tasks.json"

READ = """任务：把电工学课件页面**读成文字**，让不能看图的 AI 也知道图上画了什么。

用 read_image 逐张读取（必须真看图，禁止凭标题或文字层猜测）：
{images}

"""

CTX_BLOCK = """文字层背景（仅供定位术语，不能替代看图）：
{context}

"""

RESULT = """最后一步（必须做）：用 write 工具把上面那个 JSON 对象原样写进
{out_path}
（只写 JSON 本身）。写成功后只回复一行 `{ack}`，不要复述内容。"""


def build_prompt(task: dict, out_rel: str, ack: str, with_context: bool) -> str:
    body = task["prompt"]
    marker = body.index("文字层背景")
    images = body[:marker].split("：\n", 1)[1].rstrip("\n")
    rest = body[marker:]
    ctx_end = rest.index("只输出一个 JSON 对象")
    context = rest[len("文字层背景（仅供定位术语，不能替代看图）：\n"):ctx_end].rstrip("\n")
    tail = rest[ctx_end:].rstrip("\n")
    prompt = READ.format(images=images)
    if with_context:
        prompt += CTX_BLOCK.format(context=context)
    prompt += tail + "\n\n" + RESULT.format(
        out_path=str(LAYER / out_rel), ack=ack)
    return prompt


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", type=int, default=0)
    ap.add_argument("--count", type=int, default=2)
    ap.add_argument("--round", type=int, default=1)
    ap.add_argument("--no-context", dest="context", action="store_false")
    ap.set_defaults(context=True)
    args = ap.parse_args()

    tasks = json.loads(TASKS.read_text(encoding="utf-8"))["tasks"]
    chunk = tasks[args.start:args.start + args.count]
    batches = []
    for j, t in enumerate(chunk):
        idx = args.start + j
        out_rel = f"index/desc/r{args.round}-b{idx:03d}.json"
        ack = f"OK {idx}"
        batches.append({
            "label": t["label"], "out": out_rel, "ack": ack,
            "prompt": build_prompt(t, out_rel, ack, args.context),
        })
    print(json.dumps({"batches": batches}, ensure_ascii=False, separators=(",", ":")))
    print(f"\n[CHUNK] round={args.round} {args.start}..{args.start + len(batches) - 1}"
          f" context={args.context}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
