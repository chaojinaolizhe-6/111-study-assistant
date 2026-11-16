# -*- coding: utf-8 -*-
"""生成并自校验 round-01/delivery-manifest.json。

原则：
 - 所有字节数与哈希在写入时现算，不硬编码；
 - 页数从最终 handout.pdf 读取；断言条数与检查结论来自写入时现跑的脚本；
 - 写入后重新读回 JSON，逐条核对路径、bytes、sha256；不一致即非零退出；
 - 清单不包含自身，避免循环哈希。
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
TASK = ROOT.parent
BASELINE = TASK.parent / "讲义skill-v2.3-张量并矢整本-20261111"
REVIEW = Path("D:/aaa_D_usual/CODEX/AI-SKILL/reviews/lecture-full-20261111")


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
    # ---------- 现跑检查，取真实结论 ----------
    ov_code, ov_out = run(["check_overview.py"])
    pg_code, pg_out = run(["check_pages.py"])
    ch_code, ch_out = run([str(TASK / ".dsh" / "skills" / "lecture-deepdive" / "scripts" /
                              "check_handout.py"), "handout.tex", "--mode", "appendix",
                          "--log", "handout.log"])
    la_code, la_out = run(["layout_audit.py"])

    def grab(out: str, pat: str) -> str | None:
        m = re.search(pat, out)
        return m.group(0) if m else None

    pdf = fitz.open(ROOT / "handout.pdf")
    pages = pdf.page_count
    tex = (ROOT / "handout.tex").read_text(encoding="utf-8")
    log = (ROOT / "handout.log").read_text(encoding="utf-8", errors="replace")
    aux = (ROOT / "handout.aux").read_text(encoding="utf-8")

    stats = {
        "pdf_pages": pages,
        "xelatex_passes": 2,
        "overview_figure_page": 1,
        "tikzpictures": tex.count("\\begin{tikzpicture}"),
        "figure_captions": tex.count("\\figcap{"),
        "exercises": len(re.findall(r"\\practice\{P\d+\}", tex)),
        "answer_starts": len(re.findall(r"\\answerstart\{P\d+\}", tex)),
        "answer_continuations": len(re.findall(r"\\answercontinue\{P\d+\}", tex)),
        "overfull_hbox": len(re.findall(r"Overfull \\hbox", log)),
        "overfull_vbox": len(re.findall(r"Overfull \\vbox", log)),
        "missing_character": len(re.findall(r"Missing character", log)),
        "underfull_hbox": len(re.findall(r"Underfull \\hbox", log)),
        "undefined_references": len(re.findall(r"(?:LaTeX Warning: Reference|undefined references)", log, re.I)),
        "rendered_pages": len(list((ROOT / "rendered").glob("page-*.png"))) - 1,
        "rendered_hi_res_page1": (ROOT / "rendered" / "page-001-hi.png").exists(),
        "check_overview_summary": grab(ov_out, r"合计断言 \d+ 条，失败 \d+ 条"),
        "check_overview_exit": ov_code,
        "check_pages_summary": grab(pg_out, r"合计断言 \d+ 条，失败 \d+ 条"),
        "check_pages_exit": pg_code,
        "check_handout_summary": grab(ch_out, r"合计：错误 \d+ 条，人工复核线索 \d+ 条"),
        "check_handout_exit": ch_code,
        "layout_audit_exit": la_code,
        "figures_same_page": len(re.findall(r"图本体 p\d+、图注 p\d+", la_out)),
        "tables_rule_same_page": len(re.findall(r"上粗线 y=", la_out)),
        "continuations_at_page_top": len(re.findall(r"\(\d+, 1\)", la_out)),
        "answer_label_pages": {k: int(v) for k, v in
                               re.findall(r"\\newlabel\{ans:(P\d+)\}\{\{\}\{(\d+)\}", aux)},
    }

    # ---------- 本轮输出 ----------
    outputs = []
    named = ["handout.tex", "handout.pdf", "handout.log", "handout.aux",
             "verification.txt", "revision-response.json", "source-diff.txt",
             "check_overview.py", "check_pages.py", "layout_audit.py",
             "render_pages.py", "make_manifest.py"]
    for rel in named:
        p = ROOT / rel
        if p.exists():
            outputs.append(entry(p, "round-01/" + rel))
    idx = ROOT / "rendered" / "index.txt"
    if idx.exists():
        outputs.append(entry(idx, "round-01/rendered/index.txt"))
    for p in sorted((ROOT / "rendered").glob("page-*.png")):
        outputs.append(entry(p, "round-01/rendered/" + p.name))

    # ---------- 只读基线 ----------
    baseline = []
    for rel in ["round-04/handout.tex", "round-04/handout.pdf"]:
        p = BASELINE / rel
        if p.exists():
            item = entry(p, "D:/aaa_D_usual/DSH/111学习助手/output/讲义skill-v2.3-张量并矢整本-20261111/" + rel)
            item["kind"] = "accepted_baseline"
            baseline.append(item)
    for rel in ["inputs/TM2026-Topic8-P1.pdf", "inputs/RIT-Whelan-notes10-tensor.pdf"]:
        p = BASELINE / rel
        if p.exists():
            item = entry(p, "D:/aaa_D_usual/DSH/111学习助手/output/讲义skill-v2.3-张量并矢整本-20261111/" + rel)
            item["kind"] = "book_source_read_only"
            baseline.append(item)
    acc = REVIEW / "final-acceptance.json"
    if acc.exists():
        item = entry(acc, str(acc.as_posix()))
        item["kind"] = "acceptance_evidence_read_only"
        baseline.append(item)

    # ---------- 冻结规则与图依赖 ----------
    frozen = []
    skill = TASK / ".dsh" / "skills" / "lecture-deepdive"
    for p in sorted(skill.rglob("*")):
        if p.is_file():
            frozen.append(entry(p, "task/.dsh/skills/lecture-deepdive/" + p.relative_to(skill).as_posix()))
    for p, rel in [(TASK / "AGENTS.md", "task/AGENTS.md"),
                   (TASK / "tools" / "verify_math.py", "task/tools/verify_math.py")]:
        if p.exists():
            frozen.append(entry(p, rel))

    manifest = {
        "generated_at_utc": datetime.datetime.now(datetime.timezone.utc)
                                    .strftime("%Y-%m-%dT%H:%M:%S+00:00"),
        "round": "round-01",
        "kind": "开篇主线概览修订稿：基线为已验收 round-04，只新增图 0 与相应版本说明，正文逐行保留",
        "book": "从张量到并矢：二次型主轴、并矢运算与三处力学落点",
        "skill": {"name": "lecture-deepdive", "version": "2.3.1",
                  "frozen_copy": "task/.dsh/skills/lecture-deepdive/"},
        "stats_source": "页数/标签页来自 handout.pdf 与 handout.aux；断言与检查结论来自写入时现跑的脚本；"
                        "其余计数来自 handout.tex 与 handout.log",
        "stats": stats,
        "outputs": outputs,
        "baseline_read_only": baseline,
        "frozen_rules_and_figure_dependencies": frozen,
        "notes": [
            "图 0 只用 LaTeX/TikZ 原生绘制，不依赖外部图片；主题文件是上表规则副本中的 assets/theme-violet.tex。",
            "本清单不含自身哈希，避免循环；写入后重新读回并逐条核对 bytes/sha256。",
            "本清单不证明内容正确或页面已目视；检查覆盖范围见 round-01/verification.txt。",
            "没有运行 git、同步、学习记录收尾；没有修改真实 learning/state/plan/config；没有对外发送消息。",
        ],
    }

    out = ROOT / "delivery-manifest.json"
    out.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[ok] 写入 {out}")

    # ---------- 自校验 ----------
    data = json.loads(out.read_text(encoding="utf-8"))
    problems = []
    for group in ("outputs", "baseline_read_only", "frozen_rules_and_figure_dependencies"):
        for item in data[group]:
            p = Path(item["path"])
            if not p.is_absolute():
                p = TASK / item["path"][len("task/"):] if item["path"].startswith("task/") else ROOT / item["path"][len("round-01/"):]
            if not p.exists():
                problems.append(f"缺失：{item['path']} -> {p}")
                continue
            if p.stat().st_size != item["bytes"]:
                problems.append(f"字节数变了：{item['path']}")
            if sha(p) != item["sha256"]:
                problems.append(f"哈希变了：{item['path']}")
    if any(item["path"].endswith("delivery-manifest.json") for g in
           ("outputs", "baseline_read_only", "frozen_rules_and_figure_dependencies") for item in data[g]):
        problems.append("清单包含自身")
    print(f"[check] 输出 {len(data['outputs'])} 项、只读基线 {len(data['baseline_read_only'])} 项、"
          f"规则与图依赖 {len(data['frozen_rules_and_figure_dependencies'])} 项")
    print(f"[check] 页数 {data['stats']['pdf_pages']}；{data['stats']['check_overview_summary']}；"
          f"{data['stats']['check_pages_summary']}；{data['stats']['check_handout_summary']}")
    if ov_code != 0 or pg_code != 0 or ch_code != 0 or la_code != 0:
        problems.append(f"脚本退出码异常：overview={ov_code}, pages={pg_code}, "
                        f"check_handout={ch_code}, layout={la_code}")
    if problems:
        print("自校验失败：")
        for x in problems:
            print(" -", x)
        return 1
    print("自校验通过：清单内每个路径都存在，bytes 与 sha256 与磁盘一致，且不含自身。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
