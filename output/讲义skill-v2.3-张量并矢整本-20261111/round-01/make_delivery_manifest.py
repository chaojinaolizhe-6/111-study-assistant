# -*- coding: utf-8 -*-
"""生成本轮交付清单（相对工作目录的路径、bytes、SHA256）。

在 round-01 目录下运行：python -B make_delivery_manifest.py
清单只列最终产物；临时提取/编译中间文件已清理。
"""
from __future__ import annotations

import datetime
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ROUND = ROOT / "round-01"


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def main() -> int:
    output_files = [
        "round-01/handout.tex",
        "round-01/handout.pdf",
        "round-01/handout.log",
        "round-01/preparation.json",
        "round-01/source-map.json",
        "round-01/verification.txt",
        "round-01/check_handout.py",
        "round-01/verify_handout.py",
        "round-01/render_pages.py",
        "round-01/make_delivery_manifest.py",
        "round-01/rendered/index.txt",
    ]
    rendered = sorted((ROUND / "rendered").glob("page-*.png"), key=lambda p: p.name)
    output_files += [str(p.relative_to(ROOT)).replace("\\", "/") for p in rendered]

    outputs = []
    for rel in output_files:
        p = ROOT / rel
        if not p.exists():
            raise SystemExit(f"缺少产物：{rel}")
        outputs.append({"path": rel, "bytes": p.stat().st_size, "sha256": sha(p)})

    input_files = [
        "inputs/TM2026-Topic8-P1.pdf",
        "inputs/RIT-Whelan-notes10-tensor.pdf",
        "inputs/baseline-full-v2.2.2.pdf",
        "inputs/baseline-full-v2.2.2.tex",
        "inputs/accepted-mainline-v2.3.pdf",
        "inputs/accepted-mainline-v2.3.tex",
        "inputs/learner-background-full.json",
        "inputs/prior-learner-background.json",
        "inputs/accepted-mainline-selection.json",
        ".dsh/skills/lecture-deepdive/SKILL.md",
        ".dsh/skills/lecture-deepdive/assets/theme-violet.tex",
        ".dsh/skills/lecture-deepdive/scripts/check_handout.py",
        "AGENTS.md",
    ]
    inputs = {}
    for rel in input_files:
        p = ROOT / rel
        if not p.exists():
            raise SystemExit(f"缺少输入：{rel}")
        inputs[rel] = {"bytes": p.stat().st_size, "sha256": sha(p)}

    manifest = {
        "generated_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "working_directory": str(ROOT),
        "round": "round-01",
        "book": "从张量到并矢：二次型主轴、并矢运算与三处力学落点",
        "skill": {"name": "lecture-deepdive", "version": "2.3.0"},
        "summary": {
            "pdf_pages": 57,
            "exercises": 12,
            "figures": 11,
            "verify_assertions": 157,
            "verify_failures": 0,
            "check_handout_errors": 0,
            "check_handout_warnings": 0,
            "xelatex_passes": 2,
            "overfull_hbox": 0,
            "missing_character": 0,
            "undefined_references": 0,
            "underfull_hbox": 3,
        },
        "outputs": outputs,
        "input_hashes": inputs,
        "checks": {
            "compile": "xelatex -halt-on-error -interaction=nonstopmode handout.tex，两遍退出码 0，57 页",
            "static": "python -B check_handout.py，appendix 模式，错误 0、人工线索 0",
            "math_and_structure": "python -B verify_handout.py，157 条断言、失败 0",
            "pages_rendered": "python -B render_pages.py，57 页 PNG 与 index.txt",
        },
        "visual_acceptance": {
            "dsh_visual_inspection": False,
            "reason": "当前模型 deepseek-v4-flash 不声明图像输入；read_image 返回 model does not declare image input。已保存逐页 PNG，交协调器目视复核。",
            "rendered_pages": 57,
        },
        "user_trial_reading": False,
        "mastery_claimed": False,
        "notes": [
            "本清单只列最终产物；临时提取/编译中间文件已清理。",
            "handout.log 有 3 处 Underfull hbox（badness 3930/10000/4779），不是溢出或缺字，已如实记录。",
            "source-map.json 的页码取自最终 handout.aux；若再改正文需重新生成。",
            "inputs 与规则文件均为只读；本清单记录其哈希以便复核。",
        ],
    }
    out = ROUND / "delivery-manifest.json"
    out.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote {out} bytes={out.stat().st_size} outputs={len(outputs)} inputs={len(inputs)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
