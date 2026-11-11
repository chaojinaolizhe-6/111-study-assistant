# -*- coding: utf-8 -*-
"""生成光学期末考试日程卡片（PNG）。仅绘图，不读学习记录。"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).with_name("光学期末考试-20261218.png")

W, H = 840, 1120
BG_TOP = (243, 238, 251)
BG_BOTTOM = (232, 241, 250)
CARD = (255, 255, 255)
BORDER = (214, 199, 236)
INK = (43, 34, 64)
SUB = (106, 96, 128)
ACCENT = (108, 74, 168)

FONT = r"C:\Windows\Fonts\msyh.ttc"
FONT_BD = r"C:\Windows\Fonts\msyhbd.ttc"


def f(size, bold=False):
    return ImageFont.truetype(FONT_BD if bold else FONT, size)


img = Image.new("RGB", (W, H), CARD)
d = ImageDraw.Draw(img)
for y in range(H):
    t = y / (H - 1)
    d.line(
        [(0, y), (W, y)],
        fill=tuple(int(BG_TOP[i] + (BG_BOTTOM[i] - BG_TOP[i]) * t) for i in range(3)),
    )

M = 46
d.rounded_rectangle([M, 60, W - M, H - 60], radius=28, fill=CARD, outline=BORDER, width=2)

cx = W // 2


def center(text, y, font, fill=INK):
    box = d.textbbox((0, 0), text, font=font)
    d.text((cx - (box[2] - box[0]) / 2 - box[0], y), text, font=font, fill=fill)
    return box[3] - box[1]


y = 118
d.text((M + 44, y), "考试日程 · 第 8 场", font=f(24), fill=ACCENT)
y += 46
center("光学期末考试", y, f(46, True))
y += 82
d.line([cx - 60, y, cx + 60, y], fill=BORDER, width=3)
y += 44
center("2026-12-18　周五", y, f(62, True))
y += 96
center("第 16 周 · 3–4 节", y, f(36))
y += 56
center("约 10:00 – 11:40", y, f(32), SUB)
y += 84

# 信息块
d.rounded_rectangle([M + 44, y, W - M - 44, y + 176], radius=18, fill=(248, 245, 253), outline=BORDER, width=1)
d.text((M + 72, y + 26), "考场", font=f(26, True), fill=ACCENT)
d.text((M + 72, y + 68), "待教务处排考后发布", font=f(32), fill=INK)
d.text((M + 72, y + 120), "（群公告原话：具体地点，排考之后教务处会发放）", font=f(21), fill=SUB)

y += 226
lines = [
    "考试范围、题型、开闭卷：尚未公布",
    "同日未登记其它事项：暂无时间冲突",
    "距今（2026-11-11）：37 天",
]
for line in lines:
    d.text((M + 60, y), "· " + line, font=f(27), fill=INK)
    y += 48

y += 26
d.line([M + 44, y, W - M - 44, y], fill=(235, 229, 244), width=2)
y += 28
center("来源：班级群群公告（群主 物理-张老师）· 2026-11-11 记入", y, f(21), SUB)
y += 34
center("事实与不确定性见 plan/考试日程.md §一之三", y, f(21), SUB)

img.save(OUT)
print(OUT)
