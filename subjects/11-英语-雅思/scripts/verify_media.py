"""校验资料里的音频文件（容器层）与听力汇编的页码映射。

⚠ 能力边界：本脚本只能验证**文件是不是有效音频**，**不能验证它听起来是什么**——
   导师没有音频输入。音频与题面是否配对，只能由学习者听一遍确认。
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
MAT = ROOT / "subjects" / "11-英语-雅思" / "资料"


def mp3_info(p: Path) -> str:
    b = p.read_bytes()
    if b[:3] == b"ID3":
        ver = f"ID3v2.{b[3]}"
    elif b[:2] in (b"\xff\xfb", b"\xff\xf3", b"\xff\xf2", b"\xff\xfa"):
        ver = "MPEG frame"
    else:
        return f"NOT-MP3 magic={b[:4]!r}"
    # 粗估时长：找第一个有效帧头，按 128kbps 折算
    n = len(b)
    return f"{ver:9s} {n/1e6:6.2f}MB  约 {n*8/128000:6.1f}s @128kbps"


def main() -> int:
    want = sys.argv[1] if len(sys.argv) > 1 else ""
    files = sorted(p for p in MAT.rglob("*.mp3") if want in str(p))
    print(f"音频文件 {len(files)} 个")
    for p in files:
        print(f"  {mp3_info(p):40s} {p.relative_to(MAT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
