#!/usr/bin/env python3
"""生成一张模拟作业照片 PNG（纯标准库），用于验证 作业/ 目录的图片读取通道。

仅用于模拟验证：图片内容是灰色底 + 黑色"文字行"，不代表任何真实题目。
"""
import struct
import zlib
from pathlib import Path


def chunk(tag: bytes, data: bytes) -> bytes:
    return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)


def make_png(path: Path, width: int = 320, height: int = 200) -> None:
    rows = bytearray()
    line_h = 24
    gap = 18
    start_y = 30
    n_lines = 5
    for y in range(height):
        row = bytearray([0])  # filter type 0
        for x in range(width):
            dark = (
                start_y <= y < start_y + line_h
                or any(start_y + i * (line_h + gap) <= y < start_y + i * (line_h + gap) + line_h for i in range(1, n_lines))
            ) and 40 <= x < width - 40
            row.append(30 if dark else 220)
        rows += row
    ihdr = struct.pack(">IIBBBBB", width, height, 8, 0, 0, 0, 0)
    png = (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", ihdr)
        + chunk(b"IDAT", zlib.compress(bytes(rows), 9))
        + chunk(b"IEND", b"")
    )
    path.write_bytes(png)
    print(f"wrote {path} ({len(png)} bytes)")


if __name__ == "__main__":
    out = Path(__file__).resolve().parent / "subjects" / "01-mock-diffeq" / "作业" / "mock-hw1-photo-模拟照片.png"
    make_png(out)
