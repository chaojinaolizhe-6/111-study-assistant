"""按段打印读图任务的 prompt 数组，供 workflow 工具分块调用使用。

workflow 脚本本身没有文件系统权限，任务文本必须先由工具调用带进去。
为控制单次调用体积，这里只输出 prompt 字符串数组，并按 --from/--count 分段。
"""
import argparse
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TASKS = ROOT / "subjects" / "06-电工电子技术" / "课件-AI可读" / "index" / "describe-tasks.json"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--from", dest="start", type=int, default=0)
    ap.add_argument("--count", type=int, default=1)
    ap.add_argument("--mode", choices=["full", "shared", "chunk"], default="full",
                    help="full=完整任务数组；shared=抽出公共指令后每批只留 label+prompt；"
                         "chunk=只输出 prompt 字符串数组")
    args = ap.parse_args()

    tasks = json.loads(TASKS.read_text(encoding="utf-8"))["tasks"]
    chunk = tasks[args.start:args.start + args.count]

    if args.mode == "chunk":
        payload = [t["prompt"] for t in chunk]
    elif args.mode == "shared":
        # 所有批次的 prompt = 公共指令 + 各自的图列表与文字层背景。
        # 抽取最长公共前后缀，避免把同一段说明重复 84 遍。
        prompts = [t["prompt"] for t in chunk]
        head = os.path.commonprefix(prompts)
        tail = os.path.commonprefix([p[::-1] for p in prompts])[::-1]
        bodies = [p[len(head):len(p) - len(tail)] for p in prompts]
        payload = {"shared_head": head, "shared_tail": tail,
                   "batches": [{"label": t["label"], "body": b} for t, b in zip(chunk, bodies)]}
    else:
        payload = [{"label": t["label"], "prompt": t["prompt"]} for t in chunk]

    print(json.dumps(payload, ensure_ascii=False, separators=(",", ":")))
    print(f"\n[CHUNK] mode={args.mode} {args.start}..{args.start + len(chunk) - 1} / {len(tasks)}",
          flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
