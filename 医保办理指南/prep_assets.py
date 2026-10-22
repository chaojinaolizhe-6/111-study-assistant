# -*- coding: utf-8 -*-
"""清理群图片：去掉二维码图右侧的杂线，并统一白边。"""
from pathlib import Path
from PIL import Image

base = Path(__file__).resolve().parent / "assets"
pair = Image.open(base / "qr-pair.png").convert("RGB")
w, h = pair.size
clean = pair.crop((8, 0, 466, h))          # 去掉右侧 2px 竖线杂色
canvas = Image.new("RGB", (clean.size[0] + 16, clean.size[1] + 12), "white")
canvas.paste(clean, (8, 6))
canvas.save(base / "qr-pair-clean.png")
print("pair clean:", canvas.size)

picc = Image.open(base / "picc.png").convert("RGB")
print("picc:", picc.size)
