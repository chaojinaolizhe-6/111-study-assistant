"""打印共享指令版任务的可嵌入片段（供 workflow 工具分轮调用）。

用法：
  python tools/ee-slides-task-slice.py --rounds 5 --offsets        # 只打印各轮字符偏移
  python tools/ee-slides-task-slice.py --rounds 5 --round 1        # 打印第 1 轮的可嵌入 JSON
"""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TASKS = ROOT / "subjects" / "06-电工电子技术" / "课件-AI可读" / "index" / "describe-tasks.json"


def build():
    tasks = json.loads(TASKS.read_text(encoding="utf-8"))["tasks"]
    prompts = [t["prompt"] for t in tasks]
    head = ""
    for i, ch in enumerate(prompts[0]):
        if all(len(p) > i and p[i] == ch for p in prompts):
            head += ch
        else:
            break
    tail = ""
    for i in range(1, min(len(p) for p in prompts) + 1):
        ch = prompts[0][-i]
        if all(p[-i] == ch for p in prompts):
            tail = ch + tail
        else:
            break
    bodies = [p[len(head):len(p) - len(tail)] for p in prompts]
    return head, tail, bodies, [t["label"] for t in tasks]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rounds", type=int, default=5)
    ap.add_argument("--round", type=int, default=0)
    ap.add_argument("--offsets", action="store_true")
    args = ap.parse_args()

    head, tail, bodies, labels = build()
    n = len(bodies)
    per = (n + args.rounds - 1) // args.rounds
    chunks = [bodies[i:i + per] for i in range(0, n, per)]
    lab_chunks = [labels[i:i + per] for i in range(0, n, per)]

    if args.offsets:
        print(json.dumps({
            "shared_head_len": len(head), "shared_tail_len": len(tail),
            "rounds": [{"round": i + 1, "from": i * per, "count": len(c),
                        "label_first": lab_chunks[i][0], "label_last": lab_chunks[i][-1]}
                       for i, c in enumerate(chunks)]}, ensure_ascii=False, indent=1))
        return 0

    idx = args.round - 1
    payload = {"shared_head": head, "shared_tail": tail,
               "batches": [{"label": l, "body": b,
                            "out": f"index/desc/r{args.round}-b{idx * per + j:03d}.json"}
                           for j, (l, b) in enumerate(zip(lab_chunks[idx], chunks[idx]))]}
    print(json.dumps(payload, ensure_ascii=False, separators=(",", ":")))
    print(f"\n[ROUND {args.round}] {len(chunks[idx])} 批 {lab_chunks[idx][0]} … {lab_chunks[idx][-1]}",
          flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
