# -*- coding: utf-8 -*-
"""Exp32 addendum: I0, I0/2, I0/3 levels on the Malus curve."""
import json, math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

for fam in ["Microsoft YaHei", "SimHei", "Noto Sans CJK SC"]:
    if any(f.name == fam for f in font_manager.fontManager.ttflist):
        plt.rcParams["font.family"] = fam
        break
plt.rcParams["axes.unicode_minus"] = False

INK = "#2b2b33"; VIO = "#6b4c9a"; GOLD = "#b08a3e"; RED = "#b03a3a"; TEAL = "#2e6e7e"
OUT = "subjects/02-光学/讲义/Exp32-数据处理-20261027"

malus = [(0, 0.3148), (10, 0.2786), (20, 0.2534), (30, 0.1975),
         (40, 0.1506), (50, 0.1030), (60, 0.0506), (70, 0.0189),
         (80, 0.0016), (90, 0.0027), (100, 0.0223), (110, 0.0535),
         (120, 0.1012), (130, 0.1468), (140, 0.2155), (150, 0.2314),
         (160, 0.2626), (170, 0.2944), (180, 0.3189)]
th = np.array([p[0] for p in malus], float)
I = np.array([p[1] for p in malus], float)

with open(f"{OUT}/results.json", encoding="utf-8") as f:
    res = json.load(f)
A = res["malus"]["A"]; t0 = res["malus"]["t0"]; B = res["malus"]["B"]
Imax = float(I.max()); Imin = float(I.min())

def model(t):
    return A * np.cos(np.deg2rad(t - t0)) ** 2 + B

def crossings(level):
    out = []
    for k in range(len(th) - 1):
        if (I[k] - level) * (I[k + 1] - level) <= 0 and I[k] != I[k + 1]:
            out.append(float(th[k] + (level - I[k]) * (th[k + 1] - th[k]) / (I[k + 1] - I[k])))
    return [c for c in out if 0 <= c <= 180]

levels = [
    ("$I_0$", Imax, INK),
    ("$I_0/2$", Imax / 2, GOLD),
    ("$I_0/3$", Imax / 3, RED),
]
info = {}
for name, lv, col in levels:
    cs = crossings(lv)
    phis = []
    for c in cs:
        d = abs(c - (t0 % 180)) % 180
        phis.append(min(d, 180 - d))
    info[name] = {"level": lv, "cross": cs, "phi": phis,
                  "mean_phi": float(np.mean(phis)) if phis else None}

# Figure
fig, ax = plt.subplots(figsize=(6.4, 3.8), dpi=300)
tt = np.linspace(0, 180, 721)
ax.plot(tt, model(tt), color=VIO, lw=1.5, label="拟合 $I=I_0\\cos^2(\\theta-\\theta_0)$")
ax.plot(th, I, "o", ms=4.0, mfc="white", mec=INK, mew=0.9, label="实测")

for (name, lv, col) in levels:
    ax.axhline(lv, color=col, ls="--", lw=0.85, alpha=0.9)
    ax.text(2.0, lv + 0.008, name, color=col, fontsize=8.2, va="bottom")

# vertical markers + labels
label_dx = {"$I_0/2$": [(-2, 10), (2, 10)], "$I_0/3$": [(-2, 10), (2, 10)], "$I_0$": [(2, -12)]}
for name, lv, col in levels:
    cs = info[name]["cross"]
    for j, c in enumerate(cs):
        if name == "$I_0$":
            ax.plot([c, c], [0, lv], color=col, ls=":", lw=0.8, alpha=0.8)
            continue
        ax.plot([c, c], [0, lv], color=col, ls=":", lw=0.8, alpha=0.8)
        dx, dy = label_dx[name][j] if j < len(label_dx[name]) else (2, 8)
        ax.annotate(f"{c:.1f}°", (c, lv), xytext=(dx, dy), textcoords="offset points",
                    fontsize=7.2, color=col)

ax.set_xlim(-3, 184); ax.set_ylim(-0.008, 0.345)
ax.set_xlabel("检偏器转角 $\\theta$ / (°)", fontsize=9)
ax.set_ylabel("光强 $I$ / a.u.", fontsize=9)
ax.set_xticks(range(0, 181, 30)); ax.tick_params(labelsize=8)
ax.legend(fontsize=7.0, loc="upper center", bbox_to_anchor=(0.5, -0.22), ncol=2, frameon=False)
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout(); fig.savefig(f"{OUT}/fig/malus_levels.png", bbox_inches="tight"); plt.close(fig)

print(json.dumps(info, ensure_ascii=False, indent=1))
