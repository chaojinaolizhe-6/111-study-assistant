# -*- coding: utf-8 -*-
"""考试日程卡（2026 秋冬）—— 给学习者自己看的日期页。"""
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
fig = plt.figure(figsize=(W, H), dpi=160)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")
ax.add_patch(Rectangle((0, 0), W, H, facecolor="#FBFAF7", edgecolor="none"))

INK, SUB, ACC, RULE = "#1E1B18", "#6B6259", "#5B4380", "#DDD6CA"
LEFT, RIGHT = 0.78, W - 0.78

# ---------- 页头 ----------
cur = H - 0.70
ax.text(LEFT, cur, "2026 秋冬 · 教务系统考试安排", fontsize=10.5, color=SUB)
cur -= 0.46
ax.text(LEFT, cur, "六场考试：日期、考场、还剩几天", fontsize=22, color=INK)
cur -= 0.34
ax.text(LEFT, cur, "今天 2026-11-09（周一）· 全部 凌水主校区 · 1 场已过、5 场待考",
        fontsize=10.2, color=SUB)
cur -= 0.26
ax.plot([LEFT, RIGHT], [cur, cur], color=ACC, lw=1.8)
cur -= 0.30

# ---------- 六行 ----------
rows = [
    ("11-08", "周日", "数学物理方法1", "15:35 – 17:15 · 综153", "已过", False),
    ("11-13", "周五", "大学俄语1 — 基础阅读", "15:35 – 17:15 · 综353", "4 天", True),
    ("11-21", "周六", "微分方程", "10:05 – 11:45 · 综160", "12 天", False),
    ("11-29", "周日", "影视鉴赏", "09:10 – 10:10 · 机房B601", "20 天", False),
    ("12-06", "周日", "马克思主义基本原理", "08:00 – 08:40 · 机房B606", "27 天", False),
    ("12-27", "周日", "中国改革开放史", "14:20 – 15:00 · 机房B606", "48 天", False),
]

ROW_H = 0.94
for i, (md, wd, course, detail, left, hot) in enumerate(rows):
    top = cur - i * ROW_H
    mid = top - ROW_H * 0.52
    if i % 2 == 0:
        ax.add_patch(Rectangle((LEFT - 0.10, top - ROW_H), RIGHT - LEFT + 0.20, ROW_H,
                               facecolor="#F6F2EA", edgecolor="none", zorder=0))
    ax.text(LEFT + 0.02, mid + 0.13, md, fontsize=17.5, color=INK, va="center")
    ax.text(LEFT + 0.02, mid - 0.17, "2026 " + wd, fontsize=8.6, color=SUB, va="center")
    ax.text(LEFT + 1.28, mid + 0.15, course, fontsize=13.2, color=INK, va="center")
    ax.text(LEFT + 1.28, mid - 0.17, detail, fontsize=9.4, color=SUB, va="center")
    col = ACC if hot else ("#9A9188" if left == "已过" else INK)
    ax.text(RIGHT - 0.04, mid, left, fontsize=13.0 if hot else 11.8, color=col,
            ha="right", va="center")

cur = cur - 6 * ROW_H - 0.10
ax.plot([LEFT, RIGHT], [cur, cur], color=RULE, lw=1.2)
cur -= 0.40

# ---------- 必须处理的三件事 ----------
ax.text(LEFT, cur, "三件要先解决的事", fontsize=12.5, color=ACC)
cur -= 0.38

notes = [
    ("11-29 撞车", "大物实验 4.9（08:00–10:00 综一304）与影视鉴赏考试（09:10–10:10）重叠约 50 分钟。"),
    ("11-21 排满", "上午 10:05 微分方程考试、下午 13:30 大物实验 5.3（综205），当天不要再压别的事。"),
    ("两处更正", "数物一原记 11-04、系统显示 11-08（已按系统更正）；马原 12-06 是否被免试口试替代，待核。"),
]
for tag, body in notes:
    ax.text(LEFT + 0.10, cur, tag, fontsize=10.4, color=ACC)
    ax.text(LEFT + 1.45, cur, body, fontsize=9.6, color=INK)
    cur -= 0.38

cur -= 0.10
ax.add_patch(FancyBboxPatch((LEFT, cur - 1.24), RIGHT - LEFT, 1.24,
                            boxstyle="round,pad=0.06,rounding_size=0.08",
                            facecolor="#F3EFE6", edgecolor="none"))
ax.text(LEFT + 0.22, cur - 0.28, "怎么用这张表", fontsize=10.4, color=ACC)
ax.text(LEFT + 0.22, cur - 0.58,
        "① 考前一周起，排期表（plan/schedule.md）会自动把这场考试排进「本周内到期」；",
        fontsize=9.2, color=INK)
ax.text(LEFT + 0.22, cur - 0.84,
        "② 讲义模式下，考试是唯一能把目标升到「迁移通过」的通道；平时只算讲义覆盖。",
        fontsize=9.2, color=INK)
ax.text(LEFT + 0.22, cur - 1.08,
        "③ 完整事实表（含校区、课程库对应、待核对项）见 plan/考试日程.md。",
        fontsize=9.2, color=SUB)

ax.text(W / 2, 0.30, "来源：教务系统「考试安排」截图，2026-11-09 08:04 CST；倒计时按中国时间计算",
        fontsize=8.0, color=SUB, ha="center")

fig.savefig(r"output\考试日程卡-20261109.png", facecolor="#FBFAF7")
print("saved")
