# -*- coding: utf-8 -*-
"""Exp32 偏振光：修订数据（2026-10-27）的转录、拟合与分析。"""
import json, math
import numpy as np
from scipy.optimize import curve_fit, minimize_scalar
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

for fam in ["Microsoft YaHei", "SimHei", "Noto Sans CJK SC"]:
    if any(f.name == fam for f in font_manager.fontManager.ttflist):
        plt.rcParams["font.family"] = fam
        break
plt.rcParams["axes.unicode_minus"] = False

INK = "#2b2b33"; VIO = "#6b4c9a"; VIO2 = "#9a7fc4"; GOLD = "#b08a3e"; RED = "#b03a3a"
OUT = "subjects/02-光学/讲义/Exp32-数据处理-20261027"

# ---------------- 1. 修订后的数据 ----------------
malus = [(0, 0.3148), (10, 0.2786), (20, 0.2534), (30, 0.1975),
         (40, 0.1506), (50, 0.1030), (60, 0.0506), (70, 0.0189),
         (80, 0.0016), (90, 0.0027), (100, 0.0223), (110, 0.0535),
         (120, 0.1012), (130, 0.1468), (140, 0.2155), (150, 0.2314),
         (160, 0.2626), (170, 0.2944), (180, 0.3189)]
th = np.array([p[0] for p in malus], float)
I = np.array([p[1] for p in malus], float)

brew = [(40, 0.0180, 0.0048), (45, 0.0438, 0.0050), (50, 0.0465, 0.0002),
        (55, 0.0501, 0.0000), (60, 0.0650, 0.0013), (65, 0.0620, 0.0074),
        (70, 0.0947, 0.0292)]
bi = np.array([b[0] for b in brew], float)
bmax = np.array([b[1] for b in brew], float)
bmin = np.array([b[2] for b in brew], float)
bP = (bmax - bmin) / (bmax + bmin)

qwp_phi = np.array([15, 30, 45, 60, 75, 90], float)
qwp_P = np.abs(np.cos(np.deg2rad(2 * qwp_phi)))
qwp_P[np.abs(qwp_P) < 1e-12] = 0.0

beta0, beta = 90.0, 160.0
theta_half = (beta - beta0) / 2

# ---------------- 2. 马吕斯 ----------------
def malus_model(t, A, t0, B):
    return A * np.cos(np.deg2rad(t - t0)) ** 2 + B

popt, pcov = curve_fit(malus_model, th, I, p0=[0.30, -4, 0.0],
                       bounds=([0.20, -20, 0.0], [0.40, 20, 0.01]), maxfev=50000)
perr = np.sqrt(np.diag(pcov))
fit = malus_model(th, *popt)
res = I - fit
ss_res = float(np.sum(res ** 2)); ss_tot = float(np.sum((I - I.mean()) ** 2))
r2 = 1 - ss_res / ss_tot
rmse = float(np.sqrt(ss_res / len(I)))
A_fit, t0_fit, B_fit = popt
Imax_fit = A_fit + B_fit
Imin_fit = B_fit
P_fit = (Imax_fit - Imin_fit) / (Imax_fit + Imin_fit)
Imax_raw, Imin_raw = float(I.max()), float(I.min())
P_raw = (Imax_raw - Imin_raw) / (Imax_raw + Imin_raw)
ratio_raw = Imax_raw / Imin_raw
i_min_raw = float(th[int(np.argmin(I))])
extinction_fit = (t0_fit + 90) % 180
Ih = Imax_raw / 2
cross = []
for k in range(len(th) - 1):
    if (I[k] - Ih) * (I[k + 1] - Ih) <= 0:
        cross.append(float(th[k] + (Ih - I[k]) * (th[k + 1] - th[k]) / (I[k + 1] - I[k])))
cross = [c for c in cross if 0 <= c <= 180]
if len(cross) >= 2:
    left, right = cross[0], cross[-1]
    mid = (left + right) / 2
    halfwidth = (right - left) / 2
else:
    left = right = mid = halfwidth = float("nan")

# ---------------- 3. 布儒斯特 ----------------
idx = int(np.argmax(bP))
iB_peak = float(bi[idx])
n_peak = math.tan(math.radians(iB_peak))
xs3 = bi[idx - 1:idx + 2]; ys3 = bP[idx - 1:idx + 2]
coef = np.polyfit(xs3, ys3, 2)
iB_par = float(-coef[1] / (2 * coef[0]))
P_vertex = float(np.polyval(coef, iB_par))
n_par = math.tan(math.radians(iB_par))

def fresnel(n, ang):
    a = np.deg2rad(ang); ct = np.cos(a); st = np.sin(a)
    st2 = st / n; ct2 = np.sqrt(1 - st2 ** 2)
    rs = (ct - n * ct2) / (ct + n * ct2)
    rp = (n * ct - ct2) / (n * ct + ct2)
    return rs ** 2, rp ** 2

sel = (bi >= 45) & (bi <= 60)
def fres_obj(n):
    rs, rp = fresnel(n, bi[sel])
    return float(np.sum(((rs - rp) / (rs + rp) - bP[sel]) ** 2))
n_fit = float(minimize_scalar(fres_obj, bounds=(1.2, 1.9), method="bounded").x)
iB_fit = math.degrees(math.atan(n_fit))
def fres_obj_all(n):
    rs, rp = fresnel(n, bi)
    return float(np.sum(((rs - rp) / (rs + rp) - bP) ** 2))
n_all = float(minimize_scalar(fres_obj_all, bounds=(1.2, 1.9), method="bounded").x)

d_I = 0.0005
dP = np.sqrt((2 * bmin * d_I) ** 2 + (2 * bmax * d_I) ** 2) / (bmax + bmin) ** 2
dn = (1 / math.cos(math.radians(iB_peak))) ** 2 * math.radians(2.0)

results = {
    "malus": {
        "A": float(A_fit), "t0": float(t0_fit), "B": float(B_fit),
        "A_err": float(perr[0]), "t0_err": float(perr[1]), "B_err": float(perr[2]),
        "Imax": Imax_raw, "Imin": Imin_raw, "P": float(P_raw),
        "ratio": float(ratio_raw), "R2": float(r2), "RMSE": rmse,
        "i_min_raw": i_min_raw, "extinction_fit": float(extinction_fit),
        "half": [left, right], "mid": float(mid), "halfwidth": float(halfwidth),
        "n": int(len(I)),
    },
    "brewster": {
        "iB_peak": iB_peak, "n_peak": float(n_peak), "iB_par": iB_par,
        "P_vertex": P_vertex, "n_par": float(n_par),
        "n_fit": n_fit, "iB_fit": float(iB_fit), "n_all": n_all,
        "angles": bi.tolist(), "P": bP.tolist(), "dP": dP.tolist(),
        "dn": float(dn), "iB_nominal": float(math.degrees(math.atan(1.52))),
    },
    "qwp": {"phi": qwp_phi.tolist(), "P": qwp_P.tolist()},
    "hwp": {"beta0": beta0, "beta": beta, "theta": theta_half},
}
with open(f"{OUT}/results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

# ---------------- 4. 图 ----------------
fig, ax = plt.subplots(figsize=(6.0, 3.6), dpi=300)
tt = np.linspace(0, 180, 721)
ax.plot(tt, malus_model(tt, *popt), color=VIO, lw=1.6,
        label="拟合 $I=I_0\\cos^2(\\theta-\\theta_0)+I_{min}$")
ax.plot(th, I, "o", ms=4.2, mfc="white", mec=INK, mew=0.9, label="实测")
ax.axhline(Ih, color=GOLD, ls="--", lw=0.8)
ax.text(2, Ih + 0.006, "$I_{max}/2$", color=GOLD, fontsize=7.5)
ax.axvline(85, color=RED, ls=":", lw=0.9)
ax.text(86.5, 0.28, "消光 $85^\\circ$ 附近", color=RED, fontsize=7.2)
ax.annotate("$I_{max}=0.3189$", (180, 0.3189), xytext=(-44, -14), textcoords="offset points",
            fontsize=7, color=INK)
ax.annotate("$I_{min}=0.0016$", (80, 0.0016), xytext=(-10, 22), textcoords="offset points",
            fontsize=7, color=INK)
ax.set_xlim(-3, 183); ax.set_ylim(-0.006, 0.35)
ax.set_xlabel("检偏器转角 $\\theta$ / (°)", fontsize=9)
ax.set_ylabel("光强 $I$ / a.u.", fontsize=9)
ax.set_xticks(range(0, 181, 30)); ax.tick_params(labelsize=8)
ax.legend(fontsize=7.0, loc="upper right", frameon=False)
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout(); fig.savefig(f"{OUT}/fig/malus.png", bbox_inches="tight"); plt.close(fig)

fig, ax = plt.subplots(figsize=(6.0, 3.6), dpi=300)
ax.errorbar(bi, bP, yerr=dP, fmt="o", ms=4.5, color=VIO, ecolor=VIO2,
            capsize=2, lw=0.9, label="实测 $P$")
aa = np.linspace(39, 71, 400)
Rs, Rp = fresnel(n_fit, aa)
ax.plot(aa, (Rs - Rp) / (Rs + Rp), color=GOLD, lw=1.1, ls="--",
        label=f"菲涅耳 $n={n_fit:.3f}$（45°–60° 拟合）")
ax.axvline(iB_peak, color=RED, ls=":", lw=0.9)
ax.text(iB_peak + 0.7, 0.62, f"$i_B={iB_peak:.0f}^\\circ$", color=RED, fontsize=8)
ax.set_xlim(39, 71); ax.set_ylim(0.35, 1.06)
ax.set_xlabel("入射角 $i$ / (°)", fontsize=9)
ax.set_ylabel("偏振度 $P$", fontsize=9)
ax.tick_params(labelsize=8)
ax.legend(fontsize=6.8, loc="lower right", frameon=False)
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout(); fig.savefig(f"{OUT}/fig/brewster.png", bbox_inches="tight"); plt.close(fig)

fig, ax = plt.subplots(figsize=(5.4, 2.9), dpi=300)
ph = np.linspace(0, 90, 361)
ax.plot(ph, np.abs(np.cos(np.deg2rad(2 * ph))), color=VIO, lw=1.5)
ax.plot(qwp_phi, qwp_P, "o", ms=4, mfc="white", mec=INK, mew=0.9)
for x, y, s in [(15, 0.866, "椭圆"), (30, 0.5, "椭圆"), (45, 0, "圆"),
                (60, 0.5, "椭圆"), (75, 0.866, "椭圆"), (90, 1, "线")]:
    ax.annotate(s, (x, y), textcoords="offset points", xytext=(3, 6), fontsize=7, color=INK)
ax.set_xlabel("λ/4 光轴与 P1 夹角 $\\varphi$ / (°)", fontsize=9)
ax.set_ylabel("理论 $P=|\\cos 2\\varphi|$", fontsize=9)
ax.set_xlim(0, 92); ax.set_ylim(-0.03, 1.08); ax.tick_params(labelsize=8)
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout(); fig.savefig(f"{OUT}/fig/qwp.png", bbox_inches="tight"); plt.close(fig)

import csv
with open(f"{OUT}/data.csv", "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f)
    w.writerow(["table", "x", "y1", "y2", "y3"])
    for a, v in malus:
        w.writerow(["malus", a, v, "", ""])
    for a, mx, mn in brew:
        w.writerow(["brewster", a, mx, mn, (mx - mn) / (mx + mn)])
    for a, p in zip(qwp_phi, qwp_P):
        w.writerow(["qwp", a, "", "", p])

print(json.dumps(results, ensure_ascii=False, indent=1))
