# -*- coding: utf-8 -*-
"""生成并自校验 round-04/delivery-manifest.json。

原则：
 - 所有字节数与哈希在写入时现算，不硬编码；
 - 页数从最终 handout.pdf 读取，断言条数/检查结论从“现跑一次脚本并读它的汇总行”得到，
   不沿用旧数字；
 - 写完后重新读回 JSON，逐条核对文件存在、bytes 与 sha256 是否仍一致，不一致即非零退出。
"""
from __future__ import annotations

import datetime
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

import fitz

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent
PARENT = ROOT.parent


def sha(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def entry(p: Path, rel: str) -> dict:
    return {"path": rel, "bytes": p.stat().st_size, "sha256": sha(p)}


def run(args: list[str]) -> tuple[int, str]:
    r = subprocess.run([sys.executable, "-B", *args], cwd=str(ROOT),
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def main() -> int:
    # ---------- 现跑三个脚本，取真实结论 ----------
    v_code, v_out = run(["verify_handout.py"])
    c_code, c_out = run(["check_handout.py"])
    l_code, l_out = run(["layout_audit.py"])

    def grab(out: str, pat: str) -> str | None:
        m = re.search(pat, out)
        return m.group(0) if m else None

    v_sum = grab(v_out, r"合计断言 \d+ 条，失败 \d+ 条")
    c_sum = grab(c_out, r"合计：错误 \d+ 条，人工复核线索 \d+ 条")
    pages = fitz.open(ROOT / "handout.pdf").page_count
    tex = (ROOT / "handout.tex").read_text(encoding="utf-8")
    log = (ROOT / "handout.log").read_text(encoding="utf-8", errors="replace")

    stats = {
        "pdf_pages": pages,
        "verify_summary": v_sum,
        "verify_exit_code": v_code,
        "check_handout_summary": c_sum,
        "check_handout_exit_code": c_code,
        "layout_audit_exit_code": l_code,
        "figures": tex.count("\\begin{tikzpicture}"),
        "figure_captions": tex.count("\\figcap{"),
        "exercises": len(re.findall(r"\\practice\{P\d+\}", tex)),
        "answer_blocks": len(re.findall(r"\\answerstart\{P\d+\}", tex)),
        "answer_continuations": len(re.findall(r"\\answercontinue\{P\d+\}", tex)),
        "xelatex_passes": 2,
        "overfull_hbox": len(re.findall(r"Overfull \\hbox", log)),
        "overfull_vbox": len(re.findall(r"Overfull \\vbox", log)),
        "missing_character": len(re.findall(r"Missing character", log)),
        "underfull_hbox": len(re.findall(r"Underfull \\hbox", log)),
        "undefined_references": len(re.findall(r"LaTeX Warning: Reference", log)),
        "rendered_pages": len(list((ROOT / "rendered").glob("page-*.png"))),
        "figures_same_page": len(re.findall(r"图本体 p\d+、图注 p\d+", l_out)),
        "tables_rule_same_page": len(re.findall(r"上粗线 y=", l_out)),
        "continuation_markers_at_page_top": len(re.findall(r"的续解标记在实际续页页首", v_out)),
    }

    # ---------- 本轮输出 ----------
    outputs = []
    named = ["handout.tex", "handout.pdf", "handout.log", "handout.aux",
             "preparation.json", "source-map.json", "revision-response.json",
             "verification.txt", "verify_handout.py", "check_handout.py",
             "layout_audit.py", "render_pages.py", "make_source_map.py", "make_manifest.py"]
    for rel in named:
        p = ROOT / rel
        if p.exists():
            outputs.append(entry(p, "round-04/" + rel))
    outidx = ROOT / "rendered" / "index.txt"
    if outidx.exists():
        outputs.append(entry(outidx, "round-04/rendered/index.txt"))
    for p in sorted((ROOT / "rendered").glob("page-*.png")):
        outputs.append(entry(p, "round-04/rendered/" + p.name))

    # ---------- 原始输入与追加基础文件 ----------
    inputs = []
    for rel in ["inputs/TM2026-Topic8-P1.pdf", "inputs/RIT-Whelan-notes10-tensor.pdf",
                "inputs/baseline-full-v2.2.2.tex", "inputs/baseline-full-v2.2.2.pdf",
                "inputs/accepted-mainline-v2.3.tex", "inputs/accepted-mainline-v2.3.pdf",
                "inputs/accepted-mainline-selection.json",
                "inputs/learner-background-confirmed-20261114.json",
                "inputs/learner-background-full.json", "inputs/prior-learner-background.json"]:
        p = PARENT / rel
        if p.exists():
            p_input = entry(p, rel)
            p_input["kind"] = ("learner_addendum_2026-11-14"
                               if "confirmed-20261114" in rel else
                               ("learner_background" if "learner-background" in rel else "source"))
            inputs.append(p_input)

    # ---------- 冻结规则 ----------
    frozen = []
    skill = PARENT / ".dsh" / "skills" / "lecture-deepdive"
    for p in sorted(skill.rglob("*")):
        if p.is_file():
            frozen.append(entry(p, ".dsh/skills/lecture-deepdive/" + p.relative_to(skill).as_posix()))
    agent = ROOT / "AGENTS.md"
    if agent.exists():
        frozen.append(entry(agent, "AGENTS.md"))
    for p in sorted((PARENT / "tools").glob("*.py")):
        frozen.append(entry(p, "tools/" + p.name))

    # ---------- 前几轮旧稿（应保持不变） ----------
    prev = []
    for rel in ["round-01/handout.tex", "round-01/handout.pdf", "round-01/verification.txt",
                "round-01/preparation.json", "round-01/source-map.json",
                "round-01/delivery-manifest.json",
                "round-02/handout.tex", "round-02/handout.pdf", "round-02/verification.txt",
                "round-02/preparation.json", "round-02/source-map.json",
                "round-02/revision-response.json", "round-02/delivery-manifest.json",
                "round-03/handout.tex", "round-03/handout.pdf", "round-03/handout.log",
                "round-03/verification.txt", "round-03/preparation.json",
                "round-03/source-map.json", "round-03/revision-response.json",
                "round-03/delivery-manifest.json"]:
        p = PARENT / rel
        if p.exists():
            prev.append(entry(p, rel))

    # ---------- 本轮所依据的审核证据（工作区外，只读） ----------
    review_root = Path("D:/aaa_D_usual/CODEX/AI-SKILL/reviews/lecture-full-20261111")
    review = []
    for rel in ["r3-final-reconciliation.json", "math-r3-working-review.json",
                "math-r3-final-review.json", "source-reading-r3-working-review.json",
                "source-reading-r3-metadata-review.json", "source-reading-r3-final-review.json",
                "visual-r3-working-review.json", "visual-r3-final-review.json",
                "round-03-integrity.json"]:
        p = review_root / rel
        if p.exists():
            item = entry(p, str(p.as_posix()))
            review.append(item)

    manifest = {
        "generated_at_utc": datetime.datetime.now(datetime.timezone.utc)
                                    .strftime("%Y-%m-%dT%H:%M:%S+00:00"),
        "round": "round-04",
        "kind": "第三轮审核返工稿（编辑起点 round-03，只处理其复审后仍存在的问题），不是从零生成",
        "book": "从张量到并矢：二次型主轴、并矢运算与三处力学落点",
        "skill": {"name": "lecture-deepdive", "version": "2.3.0",
                  "frozen_copy": ".dsh/skills/lecture-deepdive/"},
        "stats_source": "页数来自 handout.pdf；断言/检查结论来自写入时现跑的脚本；"
                        "其余计数来自 handout.tex 与 handout.log",
        "stats": stats,
        "outputs": outputs,
        "inputs": inputs,
        "frozen_rules": frozen,
        "previous_rounds_untouched": prev,
        "review_evidence_read_only": review,
        "notes": [
            "本清单不证明内容正确或页面已目视；脚本结论的覆盖范围见 round-04/verification.txt。",
            "round-01、round-02、round-03 只读保留；上面记录的是写入时刻的哈希。",
            "没有运行 git、同步、学习记录收尾；没有修改真实 learning/state/plan/config；没有对外发送消息。",
            "审核证据目录在工作区之外，只读取、不修改；这里只记路径与哈希，便于核对依据。",
        ],
    }

    out = ROOT / "delivery-manifest.json"
    out.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[ok] 写入 {out}")

    # ---------- 自校验：重新读回并逐条核对 ----------
    data = json.loads(out.read_text(encoding="utf-8"))
    problems = []
    for group in ("outputs", "inputs", "frozen_rules", "previous_rounds_untouched",
                  "review_evidence_read_only"):
        for item in data[group]:
            path = item["path"]
            if path.startswith("round-04/"):
                p = ROOT / path[len("round-04/"):]
            elif Path(path).is_absolute():
                p = Path(path)
            else:
                p = PARENT / path
            if not p.exists():
                problems.append(f"缺失：{item['path']}")
                continue
            if p.stat().st_size != item["bytes"]:
                problems.append(f"字节数变了：{item['path']}")
            if sha(p) != item["sha256"]:
                problems.append(f"哈希变了：{item['path']}")
    print(f"[check] 输出 {len(data['outputs'])} 项、输入 {len(data['inputs'])} 项、"
          f"冻结规则 {len(data['frozen_rules'])} 项、旧稿 {len(data['previous_rounds_untouched'])} 项、"
          f"审核证据 {len(data['review_evidence_read_only'])} 项")
    print(f"[check] 页数 {data['stats']['pdf_pages']}；{data['stats']['verify_summary']}；"
          f"{data['stats']['check_handout_summary']}")
    if v_code != 0 or c_code != 0 or l_code != 0:
        problems.append(f"脚本退出码异常：verify={v_code}, check={c_code}, layout={l_code}")
    if problems:
        print("自校验失败：")
        for x in problems:
            print(" -", x)
        return 1
    print("自校验通过：清单里的每个路径都存在，bytes 与 sha256 与磁盘一致。")
    return 0


if __name__ == "__main__":
    sys.exit(main())


