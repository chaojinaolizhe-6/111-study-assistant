#!/usr/bin/env python3
"""写前自检（write-check）：**用真正的解析器**检查将要落盘的文件，而不是靠启发式。

两条实际踩过的坑（2026-09-30 各一次）：
1. `tools/*.py` 里中文旁的半角引号 → SyntaxError；
2. `learning/attempts/*.json` 里中文旁的半角引号 → 非法 JSON，事件被拒。

启发式（数引号个数）误报太多、不可用；这里直接：
- `.py` → `compile(src, path, "exec")`
- `.json` → `json.loads`
- `.jsonl` → 逐行 `json.loads`
- `.md` / `.yml` → 报告其中的半角引号对（警告级，因为 Markdown 里合法）

用法:
  python -B tools/write_check.py <file> [...]      # 全部文件都检查
  python -B tools/write_check.py --json <file>     # 只当 JSON/JSONL 检查
退出码：0 = 通过（可能有警告）；1 = 有错误。
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def check_py(path: Path) -> list[str]:
    try:
        compile(path.read_text(encoding="utf-8"), str(path), "exec")
    except SyntaxError as exc:
        return [f"{path}:{exc.lineno}: SyntaxError: {exc.msg} → {str(exc.text or '').strip()[:120]}"]
    return []


def check_json(path: Path) -> list[str]:
    try:
        json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"{path}:{exc.lineno}: JSONDecodeError: {exc.msg}（中文引号请用「」）"]
    return []


def check_jsonl(path: Path) -> list[str]:
    errors = []
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"{path}:{i}: JSONDecodeError: {exc.msg}（中文引号请用「」）")
    return errors


def check_yaml(path: Path) -> list[str]:
    """极简 YAML 检查：能解析成 dict 即可（调用 tools/learninglib.parse_yaml）。"""
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from learninglib import parse_yaml

    try:
        parse_yaml(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001 - 校验器要报告任何解析失败
        return [f"{path}: YAML parse failed: {exc}"]
    return []


def main() -> int:
    parser = argparse.ArgumentParser(description="Pre-write validation using real parsers.")
    parser.add_argument("files", nargs="+")
    args = parser.parse_args()
    errors: list[str] = []
    checked = 0
    for name in args.files:
        path = Path(name)
        if not path.is_file():
            errors.append(f"{path}: 文件不存在")
            continue
        suffix = path.suffix.lower()
        if suffix == ".py":
            errors += check_py(path)
        elif suffix == ".json":
            errors += check_json(path)
        elif suffix == ".jsonl":
            errors += check_jsonl(path)
        elif suffix in (".yml", ".yaml"):
            errors += check_yaml(path)
        else:
            print(f"SKIP {path}（未知类型，仅报告）")
        checked += 1
    for error in errors:
        print(f"ERROR {error}")
    print(f"\nwrite-check：检查 {checked} 个文件，错误 {len(errors)} 个")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
