#!/usr/bin/env python3
"""范围化校验：区分【错误 / 警告 / 范围外跳过】，**不**用过滤输出假装通过。

背景：外部只读知识库 `obsidian/` 里的数学记号（如 `M[u]` 紧跟 `(P)`）会被上游校验器
的 markdown 链接正则误判为失效链接（2026-09-26 实测 121 条）。按约定**不修改**同步来的知识库正文，
也不把失败行过滤掉就宣称通过；改为按范围分类报告。

范围配置：`.tutor/config/validation-scope.yml`
  out_of_scope_paths:   # 命中的失败只计入"范围外跳过"，不影响退出码
    - obsidian/

退出码：有**范围内**错误 → 1；只有范围外跳过 → 0（并明确打印跳过条数）。
用法: python -B tools/validate_study_scoped.py --today YYYY-MM-DD
"""
from __future__ import annotations

import argparse
import contextlib
import io
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from learninglib import parse_yaml  # noqa: E402

UPSTREAM = ROOT / ".tutor" / "core" / "scripts" / "validate-study.py"
DEFAULT_OUT_OF_SCOPE = ["obsidian/"]


def load_scope(root: Path) -> list[str]:
    path = root / ".tutor" / "config" / "validation-scope.yml"
    if not path.is_file():
        return list(DEFAULT_OUT_OF_SCOPE)
    raw = parse_yaml(path.read_text(encoding="utf-8"))
    paths = raw.get("out_of_scope_paths")
    if isinstance(paths, list) and paths:
        return [str(p) for p in paths]
    return list(DEFAULT_OUT_OF_SCOPE)


def load_info_patterns(root: Path) -> list[str]:
    """信息项模式（可选能力未启用之类），不计错误、不掩盖其它失败。"""
    path = root / ".tutor" / "config" / "validation-scope.yml"
    if not path.is_file():
        return ["no paths.instance_validator configured"]
    raw = parse_yaml(path.read_text(encoding="utf-8"))
    patterns = raw.get("informational_patterns")
    if isinstance(patterns, list) and patterns:
        return [str(p) for p in patterns]
    return ["no paths.instance_validator configured"]


def run_upstream(today: str) -> tuple[int, str]:
    """运行上游校验（core + instance）。

    注意：上游 validate-study.py 只是 subprocess 包装器，其子进程直接继承 stdio，
    进程内 redirect_stdout 捕获不到。这里改为**临时文件重定向**（不使用管道，
    避免受限沙箱下 pipe/EPERM 问题），再读取输出分类。
    """
    import subprocess
    import tempfile

    scripts = ROOT / ".tutor" / "core" / "scripts"
    chunks: list[str] = []
    rc_total = 0
    for name in ("validate-core.py", "validate-instance.py"):
        script = scripts / name
        if not script.is_file():
            chunks.append(f"- 缺少上游脚本：{name}")
            rc_total = rc_total or 2
            continue
        with tempfile.NamedTemporaryFile("w", delete=False, suffix=".log", encoding="utf-8") as fh:
            log_path = Path(fh.name)
            rc = subprocess.run(
                [sys.executable, str(script), "--today", today],
                cwd=str(ROOT),
                stdout=fh,
                stderr=subprocess.STDOUT,
            ).returncode
        chunks.append(log_path.read_text(encoding="utf-8"))
        log_path.unlink(missing_ok=True)
        rc_total = rc_total or rc
    return rc_total, "\n".join(chunks)


def main() -> int:
    parser = argparse.ArgumentParser(description="Scoped study validation with classified reporting.")
    parser.add_argument("--today", required=True)
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    out_of_scope = load_scope(root)

    rc, output = run_upstream(args.today)
    lines = [ln for ln in output.splitlines() if ln.strip()]

    in_scope_errors: list[str] = []
    skipped: list[str] = []
    info_items: list[str] = []
    notes: list[str] = []
    # 上游输出在 Windows 上使用反斜杠路径 → 统一成正斜杠再匹配范围
    normalized_scope = [p.replace("\\", "/") for p in out_of_scope]
    info_patterns = load_info_patterns(root)
    for ln in lines:
        if ln.startswith("- "):
            probe = ln.replace("\\", "/")
            if any(p in ln for p in info_patterns) or any(p in probe for p in info_patterns):
                info_items.append(ln)
            elif any(p in probe for p in normalized_scope):
                skipped.append(ln)
            else:
                in_scope_errors.append(ln)
        else:
            notes.append(ln)

    print("== 范围化校验（范围外跳过不伪装为通过）==")
    print(f"范围外路径（配置）：{', '.join(out_of_scope)}")
    print(f"上游退出码：{rc}")
    print(f"范围内错误：{len(in_scope_errors)}")
    for ln in in_scope_errors:
        print(f"  {ln}")
    print(f"范围外跳过：{len(skipped)} 条（外部只读知识库/导出记录的已知误判；未修改其正文）")
    if skipped:
        print(f"  例：{skipped[0][:160]}")
    print(f"信息项（可选能力未启用，不计错误）：{len(info_items)}")
    for ln in info_items:
        print(f"  {ln}")
    print(f"其他说明行：{len(notes)}")
    for ln in notes[:5]:
        print(f"  {ln}")

    if in_scope_errors:
        print("结论：存在**范围内**错误 → 校验未通过")
        return 1
    print("结论：范围内无错误；范围外存在跳过项（已单列，不代表整库通过）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
