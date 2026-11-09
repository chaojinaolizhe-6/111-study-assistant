# -*- coding: utf-8 -*-
"""光学作业二 三题判据卡（给学习者自己写作业用）。"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch, Rectangle

FONT = "C:/Windows/Fonts/simhei.ttf"
font_manager.fontManager.addfont(FONT)
FAM = font_manager.FontProperties(fname=FONT).get_name()
plt.rcParams["font.family"] = FAM
plt.rcParams["axes.unicode_minus"] = False

W, H = 8.27, 11.69
fig = plt.figure(figsize=(W, H), dpi=150)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")
ax.add_patch(Rectangle((0, 0), W, H, facecolor="#FBFAF7", edgecolor="none"))

INK, SUB, ACC, RULE = "#1E1B18", "#6B6259", "#5B4380", "#D8D2C8"
LEFT, XLAB, XBODY, RIGHT = 0.72, 1.02, 1.62, W - 0.72

# ---------- 页头 ----------
cur = H - 0.55
ax.text(LEFT, cur, "光学 · 第五章 光的干涉", fontsize=10.5, color=SUB)
cur -= 0.36
ax.text(LEFT, cur, "作业二：三题怎么自己写", fontsize=21, color=INK)
cur -= 0.28
ax.text(LEFT, cur, "判据 + 你讲义里的位置；不是抄同学的答案页", fontsize=9.8, color=SUB)
cur -= 0.20
ax.plot([LEFT, RIGHT], [cur, cur], color=ACC, lw=1.6)
cur -= 0.46


def block(cur, tag, title, rows, where):
    top = cur
    ax.text(XLAB, cur, tag, fontsize=10.8, color=ACC)
    cur -= 0.33
    ax.text(XLAB, cur, title, fontsize=13.2, color=INK)
    cur -= 0.34
    for label, body in rows:
        ax.text(XLAB, cur, label, fontsize=9.5, color=ACC)
        ax.text(XBODY, cur, body, fontsize=9.5, color=INK)
        cur -= 0.35
    cur -= 0.12
    ax.text(XLAB, cur, where, fontsize=8.7, color=SUB)
    ax.add_patch(FancyBboxPatch((LEFT, cur - 0.14), 0.085, top - cur + 0.26,
                                boxstyle="square,pad=0", facecolor=ACC, edgecolor="none"))
    return cur - 0.46


cur = block(cur, "① 云母片盖住一条缝", "光程差变成 (n-1)h，问厚度",
            [["判据", "ΔL = (n-1)h = mλ，m 就是条纹移过的条数"],
             ["关键", "λ = 550 nm 要写进式子；“零级移到第 8 条明纹”即 m = 8"],
             ["结果", "h = 8×550 nm ÷ 0.58 = 7 586 nm ≈ 7.59 μm"]],
            "讲义：第五章-杨氏双缝与云母片 §9（给了三条独立路线）")

cur = block(cur, "② 迈克尔逊移镜数条纹", "镜移 h，光程差变 2h，每 λ/2 过一条",
            [["判据", "h = N·λ/2；N 是“间隔数”，不是“看到的条数”"],
             ["关键", "数到 11 条 = 10 个间隔 → N = 10；题面若写“移过 11 条”则 N = 11"],
             ["结果", "N = 10、λ = 600 nm → h = 3.0 μm（取 N = 11 得 3.3 μm，差 10%）"]],
            "讲义：第五章-薄膜与迈克尔逊 §5.2（等厚调节与计数约定）")

cur = block(cur, "③ 等倾环三问（课件 p53）", "同一个式子 2d·cos i = (m - 1/2)λ 的三种问法",
            [["Q1", "固定 m：d↓ → cos i↑ → i↓ → 环半径 r↓，逐条缩进中心后消失"],
             ["Q2", "|di/dm| = λ/(2d·sin i)：d↓ → 角间距↑ → 环变疏、视场里环数↓"],
             ["Q3", "d = 0 几何光程差为 0，分束板“一外一内”差 π → 零级暗纹铺满视场"]],
            "讲义：第五章-薄膜与迈克尔逊 §8.5（三问合一块讲）")

# ---------- 扣分点 ----------
cur += 0.06
ax.plot([LEFT, RIGHT], [cur, cur], color=RULE, lw=1.0)
cur -= 0.30
ax.text(LEFT, cur, "老师最容易扣分的地方", fontsize=10.8, color=ACC)
cur -= 0.34
for t in ["① 不写 λ，也不说“8 条”从哪来 —— 式子和答案都像抄的。",
          "② 把“数到 11 条”当 11 个间隔 —— 差 0.3 μm，10% 的错。",
          "③ 用 2d·cos i = mλ 讲 Q1/Q2 —— 那是暗环口径，亮环是 (m - 1/2)λ。"]:
    ax.text(LEFT + 0.14, cur, t, fontsize=9.4, color=INK)
    cur -= 0.33

ax.text(W / 2, 0.50, "参数复核：8 × 550 / 0.58 = 7.586 μm；10 × 600 / 2 = 3.0 μm",
        fontsize=8.2, color=SUB, ha="center")

fig.savefig(r"output\光学作业二-三题判据卡-20261105.png", facecolor="#FBFAF7")
print("saved, cursor bottom =", round(cur, 2))
