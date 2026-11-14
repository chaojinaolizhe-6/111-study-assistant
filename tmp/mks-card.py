# -*- coding: utf-8 -*-
"""生成「马原口试 · 七大思维原理锚点」学习卡（PNG）。"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1600, 2000
BG = "#FFFFFF"
INK = "#12263A"
GRAY = "#6B7280"
LINE = "#E5E7EB"
CARD = "#FBFBFA"
ACCENT = "#C8452D"

LAYER = {
    1: ("#1F4E79", "认识 · 引擎"),
    2: ("#1F4E79", "认识 · 引擎"),
    3: ("#2E7D6F", "结构 · 骨架"),
    4: ("#2E7D6F", "结构 · 骨架"),
    5: ("#B7791F", "动力 · 推进"),
    6: ("#9B2C2C", "边界 · 护栏"),
    7: ("#9B2C2C", "边界 · 护栏"),
}

ITEMS = [
    (1, "辩证思维", "第一章第二节 · 对立统一规律",
     "矛盾既对立又统一，是事物发展的根本动力；抓主要矛盾，坚持两点论与重点论。",
     "卖得好与被围堵，是同一个矛盾的两面。"),
    (2, "历史思维", "第三章 · 社会存在与社会意识",
     "社会存在决定社会意识，生产力是最终决定力量；把当下放回过程中定位。",
     "市场换技术 → 合资跟随 → 换道超车。"),
    (3, "系统思维", "第一章第二节 · 联系的普遍性",
     "事物作为系统存在：整体性、结构性、层次性、开放性；整体大于部分之和。",
     "卖得越多，充电桩、电网、回收都跟着疼。"),
    (4, "战略思维", "第一章 · 主要矛盾；第二章 · 规律与能动性",
     "主要矛盾定主攻方向；尊重规律与发挥能动性相统一；落实到敢做取舍。",
     "放弃内燃机追赶，把资源压到电池电驱。"),
    (5, "创新思维", "第一章 · 否定之否定；第二章 · 理论/实践创新互动",
     "辩证否定即扬弃：既克服又保留；实践没止境，创新也没有止境。",
     "磷酸铁锂 → 三元 → 固态，一路被否定又被修正。"),
    (6, "法治思维", "第三章 · 上层建筑；第六章 · 社会主义法治",
     "经济基础决定上层建筑，上层建筑反作用：把经济关系固化为规则，给出预期。",
     "欧盟把竞争优势用规则重新定义一遍。"),
    (7, "底线思维", "第一章 · 质量互变的「度」",
     "量变积累到关节点引起质变，所以要把握「度」；先算最坏可能，再决定走不走。",
     "技术、产能、安全，三条线不能碰。"),
]

F_TITLE = ImageFont.truetype(r"C:\Windows\Fonts\msyhbd.ttc", 48)
F_SUB = ImageFont.truetype(r"C:\Windows\Fonts\msyh.ttc", 25)
F_NAME = ImageFont.truetype(r"C:\Windows\Fonts\msyhbd.ttc", 34)
F_TAG = ImageFont.truetype(r"C:\Windows\Fonts\msyh.ttc", 19)
F_BODY = ImageFont.truetype(r"C:\Windows\Fonts\msyh.ttc", 23)
F_CASE = ImageFont.truetype(r"C:\Windows\Fonts\msyh.ttc", 21)
F_NOTE = ImageFont.truetype(r"C:\Windows\Fonts\msyh.ttc", 21)
F_NOTEB = ImageFont.truetype(r"C:\Windows\Fonts\msyhbd.ttc", 22)

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)


def wrap(text, font, maxw):
    lines, cur = [], ""
    for ch in text:
        if ch == "\n":
            lines.append(cur)
            cur = ""
            continue
        if d.textlength(cur + ch, font=font) <= maxw:
            cur += ch
        else:
            lines.append(cur)
            cur = ch
    if cur:
        lines.append(cur)
    return lines


# 顶部
d.text((60, 62), "马原口试 · 七大思维 × 2023 版教材锚点", font=F_TITLE, fill=INK)
d.text((62, 140), "每个思维只记三样：教材落点 / 一句话原理 / 一个案例镜头。口诀背下来，稿子自然长出来。",
       font=F_SUB, fill=GRAY)
d.line([(60, 200), (W - 60, 200)], fill=INK, width=3)

M, GAP = 60, 34
BW = (W - 2 * M - GAP) // 2
BH = 372
TOP = 248

for idx, (num, name, tag, body, case) in enumerate(ITEMS):
    col, row = idx % 2, idx // 2
    x = M + col * (BW + GAP)
    y = TOP + row * (BH + 30)
    color, layer = LAYER[num]

    d.rounded_rectangle([x, y, x + BW, y + BH], radius=14, fill=CARD, outline=LINE, width=2)
    d.rounded_rectangle([x, y, x + 9, y + BH], radius=5, fill=color)

    d.text((x + 40, y + 26), name, font=F_NAME, fill=INK)
    d.text((x + 40, y + 76), f"教材：{tag}", font=F_TAG, fill=GRAY)

    # 层级标签（右上）
    tw = d.textlength(layer, font=F_TAG)
    d.text((x + BW - 30 - tw, y + 30), layer, font=F_TAG, fill=color)

    by = y + 118
    for ln in wrap(body, F_BODY, BW - 90)[:3]:
        d.text((x + 40, by), ln, font=F_BODY, fill=INK)
        by += 34

    d.line([(x + 40, y + BH - 78), (x + BW - 40, y + BH - 78)], fill=LINE, width=1)
    d.text((x + 40, y + BH - 64), "镜头｜", font=F_CASE, fill=ACCENT)
    d.text((x + 108, y + BH - 64), case, font=F_CASE, fill="#374151")

# 第 8 格：警示框
x = M + (BW + GAP)
y = TOP + 3 * (BH + 30)
d.rounded_rectangle([x, y, x + BW, y + BH], radius=14, fill="#FFF8F0", outline="#E8C9A8", width=2)
d.text((x + 40, y + 26), "最容易翻车的一处", font=F_NOTEB, fill="#9B2C2C")
note = ("教材第一章第三节只列「五种」思维能力：辩证、历史、战略、底线、创新。"
        "系统与法治是从总书记表述扩出来的两项——系统落在第一章第二节（联系的普遍性），"
        "法治落在第三章（上层建筑）与第六章（社会主义法治）。")
ny = y + 72
for ln in wrap(note, F_NOTE, BW - 80):
    d.text((x + 40, ny), ln, font=F_NOTE, fill="#4B3A2A")
    ny += 32
d.text((x + 40, y + BH - 64), "被问「教材哪一页」时，就这么答。", font=F_CASE, fill="#9B2C2C")

# 页脚
d.line([(60, H - 86), (W - 60, H - 86)], fill=LINE, width=2)
d.text((60, H - 66), "红线：矛盾＝既对立又统一（不是「对立」）；否定＝扬弃（不是推倒重来）；系统≠整体（还有结构、层次、开放）。",
       font=F_TAG, fill=GRAY)

out = r"D:\aaa_D_usual\DSH\111学习助手\output\马原口试-七大思维原理锚点卡-20261113.png"
img.save(out, "PNG")
print(out)
