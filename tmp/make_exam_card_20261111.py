# -*- coding: utf-8 -*-
"""生成一张「考试日程更新」卡片：理论力学期中（第13周待定）。"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1500
M = 76
BG = (251, 248, 243)
INK = (34, 32, 37)
MUTED = (105, 99, 112)
ACCENT = (107, 78, 155)
ACCENT_LIGHT = (241, 235, 248)
RULE = (222, 214, 232)

FONT_DIR = Path("C:/Windows/Fonts")
F_BOLD = str(FONT_DIR / "msyhbd.ttc")
F_REG = str(FONT_DIR / "msyh.ttc")


def font(path, size):
    return ImageFont.truetype(path, size)


img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

# 顶部色带
d.rectangle([0, 0, W, 10], fill=ACCENT)

y = 78
d.text((M, y), "考试日程 · 新增一场", font=font(F_REG, 38), fill=MUTED)
y += 72

d.text((M, y), "理论力学 期中考试", font=font(F_BOLD, 76), fill=INK)
y += 116

# 周次高亮框
box_top = y
box_h = 250
d.rounded_rectangle([M, box_top, W - M, box_top + box_h], radius=24, fill=ACCENT_LIGHT)
inner_x = M + 44
ty = box_top + 38
d.text((inner_x, ty), "暂定 第 13 周", font=font(F_BOLD, 52), fill=ACCENT)
ty += 78
d.text((inner_x, ty), "2026-11-23（周一） ~ 11-29（周日）", font=font(F_REG, 40), fill=INK)
ty += 62
d.text((inner_x, ty), "具体日期 / 时段 / 考场：待定", font=font(F_REG, 36), fill=MUTED)
y = box_top + box_h + 46

# 副信息
d.text((M, y), "距今 12–18 天　·　班级 物国际2502　·　来源标记 M3229",
       font=font(F_REG, 32), fill=MUTED)
y += 58
d.line([M, y, W - M, y], fill=RULE, width=2)
y += 44

items = [
    ("1", "「暂定」不是定。",
     "消息来自 QQ 群简报，当时 QQ 离线，只整理了归档内容；\n离线期间的新消息没有补齐，考前必须再核实一次。"),
    ("2", "这场排在结课之后。",
     "课表里理论力学是第 1–12 周（11-22 结课），\n第 13 周已无正常排课，它落在结课后那一周。"),
    ("3", "若落在 11-29，那天已经很满。",
     "大物实验 4.9　08:00–10:00\n影视鉴赏机考　09:10–10:10\n电工综合设计实验一　13:00–16:00"),
]

for num, head, body in items:
    circle_d = ImageDraw.Draw(img)
    circle_d.ellipse([M, y + 4, M + 46, y + 50], fill=ACCENT)
    tw = d.textlength(num, font=font(F_BOLD, 30))
    d.text((M + 23 - tw / 2, y + 8), num, font=font(F_BOLD, 30), fill=(255, 255, 255))
    d.text((M + 66, y), head, font=font(F_BOLD, 38), fill=INK)
    y += 54
    for line in body.split("\n"):
        d.text((M + 66, y), line, font=font(F_REG, 32), fill=MUTED)
        y += 46
    y += 30

d.line([M, y, W - M, y], fill=RULE, width=2)
y += 30
d.text((M, y), "已记入 plan/考试日程.md 与 plan/inputs.yml", font=font(F_REG, 30), fill=MUTED)
y += 42
d.text((M, y), "（排期里 due 11-23 是占位，不是考试日期）", font=font(F_REG, 30), fill=MUTED)

out = Path("output/考试日程更新-理力期中-20261111.png")
out.parent.mkdir(parents=True, exist_ok=True)
img.save(out)
print("saved", out, out.stat().st_size, "bytes; used height", y + 30)
