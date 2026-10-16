"""电工学课件 → MinerU 版面解析（GPU）批处理驱动。

教学上要的是「课件每一页在讲什么」，而老师的 PPT 导出件里电路图、波形图、
特性曲线全是位图，纯文本层取不到。本脚本用 MinerU hybrid-engine（本地 GPU，
模型已在 modelscope 缓存）逐册解析，输出每页 markdown、公式 LaTeX、图区裁切图
与 content_list.json，交给 tools/ee-slides-build.py 组装。

用法：
  python tools/ee-slides-run-mineru.py                 # 全部 12 册，跳过已完成的
  python tools/ee-slides-run-mineru.py --decks C4-1 C4-2
  python tools/ee-slides-run-mineru.py --batch-pages 25 --backend hybrid-engine

环境依赖（本机既定配置，勿改动）：
  · GPU Python：D:\\aaa_D_usual\\DSH\\AA教材处理助手\\output\\心理学知识库\\_工具\\venv-gpu
  · MinerU 启动器：同目录 bin\\mineru.bat（强制 CUDA venv，并在 OCR 进程内记录设备）
  · 包装脚本：同目录 run_extract.py（修 NO_PROXY / TEMP / PATH 三个本机坑）
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

import fitz

ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = ROOT / "subjects" / "06-电工电子技术" / "课件"
WORK_DIR = ROOT / "_scratch" / "ee-slides-mineru"

TOOLS = Path(r"D:\aaa_D_usual\DSH\AA教材处理助手\output\心理学知识库\_工具")
WRAPPER = TOOLS / "run_extract.py"
GPU_PY = TOOLS / "venv-gpu" / "Scripts" / "python.exe"

DECK_ORDER = [
    ("C1-1", "Chapter one -1-2026中白上传.pdf"),
    ("C1-2", "Chapter One -2-2026中白上传.pdf"),
    ("C1-3", "Chapter One -3-2026中白上传.pdf"),
    ("C1-4", "Chapter One -4-2026中白上传.pdf"),
    ("C2-1", "Chapter Two-1-2026中白上传.pdf"),
    ("C2-2", "Chapter Two-2-2026中白上传.pdf"),
    ("C3-1", "Chapter Three-1-2026中白上传.pdf"),
    ("C3-2", "Chapter Three-2-2026中白上传.pdf"),
    ("C3-3", "Chapter Three-3-2026中白上传.pdf"),
    ("C4-1", "Chapter Four-1-2026中白上传.pdf"),
    ("C4-2", "Chapter Four-2-2026中白上传.pdf"),
    ("C4-3", "Chapter Four-3-2026中白上传.pdf"),
]


def make_input(deck_id: str, fname: str) -> Path:
    """把源 PDF 复制成 ASCII 名，避开 MinerU 子进程对中文路径的编码坑。"""
    src = SRC_DIR / fname
    dst = WORK_DIR / "input" / f"{deck_id}.pdf"
    dst.parent.mkdir(parents=True, exist_ok=True)
    if not dst.exists() or dst.stat().st_size != src.stat().st_size:
        shutil.copy2(src, dst)
    return dst


def done_marker(deck_id: str) -> Path:
    return WORK_DIR / deck_id / "_DONE.json"


def run_deck(deck_id: str, fname: str, batch_pages: int, backend: str, force: bool) -> dict:
    pdf = make_input(deck_id, fname)
    out = WORK_DIR / deck_id
    marker = done_marker(deck_id)
    if marker.exists() and not force:
        info = json.loads(marker.read_text(encoding="utf-8"))
        print(f"[SKIP] {deck_id} 已完成（{info.get('pages')} 页，{info.get('elapsed_s')}s）", flush=True)
        return info

    if out.exists() and force:
        shutil.rmtree(out)
    out.mkdir(parents=True, exist_ok=True)
    cmd = [str(GPU_PY), str(WRAPPER), "--pdf", str(pdf), "--out", str(out),
           "--mode", "auto", "--backend", backend, "--batch-pages", str(batch_pages)]
    t0 = time.time()
    proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    elapsed = round(time.time() - t0, 1)
    log = (proc.stdout or "") + (proc.stderr or "")
    (out / "runner.log").write_text(log, encoding="utf-8")

    cl = [p for p in out.rglob("*_content_list.json") if "v2" not in p.name]
    doc = fitz.open(pdf)
    npages = doc.page_count
    doc.close()
    # 用 pages/pXXXXX.md 的产出数量判断是否解析完整（run_extract 对短页会标 needs_review，
    # 那是内容质量标记，不是失败）
    produced = len(list((out / "pages").glob("p*.md"))) if (out / "pages").is_dir() else 0
    info = {
        "deck": deck_id, "file": fname, "pages": npages, "pages_produced": produced,
        "content_list": str(cl[0].relative_to(ROOT)).replace("\\", "/") if cl else "",
        "returncode": proc.returncode, "elapsed_s": elapsed,
        "ok": bool(cl) and produced == npages,
    }
    marker.write_text(json.dumps(info, ensure_ascii=False, indent=2), encoding="utf-8")
    flag = "OK" if info["ok"] else "CHECK"
    print(f"[{flag}] {deck_id:<6} {produced}/{npages} 页  {elapsed:>6}s  rc={proc.returncode}", flush=True)
    if not info["ok"]:
        print("      " + log.strip().splitlines()[-1][:160] if log.strip() else "      （无输出）", flush=True)
    return info


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--decks", nargs="*", help="只跑指定课件 id")
    ap.add_argument("--batch-pages", type=int, default=25)
    ap.add_argument("--backend", default="hybrid-engine")
    ap.add_argument("--force", action="store_true", help="忽略已完成标记，重跑")
    args = ap.parse_args()

    if not WRAPPER.exists() or not GPU_PY.exists():
        print(f"[FAIL] 找不到 MinerU 包装脚本或 GPU 解释器：{WRAPPER} / {GPU_PY}", file=sys.stderr)
        return 2

    WORK_DIR.mkdir(parents=True, exist_ok=True)
    results = []
    for deck_id, fname in DECK_ORDER:
        if args.decks and deck_id not in args.decks:
            continue
        if not (SRC_DIR / fname).exists():
            print(f"[SKIP] {deck_id} 缺源文件 {fname}", file=sys.stderr)
            continue
        results.append(run_deck(deck_id, fname, args.batch_pages, args.backend, args.force))

    bad = [r for r in results if not r["ok"]]
    (WORK_DIR / "runner-summary.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[SUMMARY] {len(results) - len(bad)}/{len(results)} 册完整；"
          f"总页数={sum(r['pages'] for r in results)}；总耗时={sum(r['elapsed_s'] for r in results):.0f}s")
    for r in bad:
        print(f"  ⚠ {r['deck']}: {r['pages_produced']}/{r['pages']} 页")
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
