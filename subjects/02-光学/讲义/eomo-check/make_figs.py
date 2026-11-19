# -*- coding: utf-8 -*-
"""Generate the two quantitative figures for the L4 handout.
No CJK text inside the figures: math/ASCII labels only (font-independent).
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "fig-l4")
plt.rcParams.update({
    "font.size": 10,
    "mathtext.fontset": "cm",
    "axes.linewidth": 0.8,
    "savefig.dpi": 200,
    "savefig.bbox": "tight",
})
VIOLET = "#6B4E8F"
PETAL = "#B79FD0"
CREAM = "#5C606E"

# ---------------------------------------------------------------- fig 1
# Delta n vs E, both normalised to their value at E = +1e6 V/m:
# the point of this figure is parity (odd vs even), not magnitude.
E = np.linspace(-1.2, 1.2, 401)                 # in units of 1e6 V/m
pock = -0.5 * 1.5**3 * 10.6e-12 * E * 1e6       # Delta n for Pockels (one mode)
kerr = 2e-14 * 633e-9 * (E * 1e6)**2            # Delta n for Kerr
pock_n = pock / (0.5 * 1.5**3 * 10.6e-12 * 1e6)   # = -E
kerr_n = kerr / (2e-14 * 633e-9 * 1e12)           # = E^2

fig, ax = plt.subplots(figsize=(4.6, 3.1))
ax.plot(E, pock_n, color=VIOLET, lw=1.8, label=r"Pockels: $\Delta n \propto E$")
ax.plot(E, kerr_n, color=PETAL, lw=1.8, label=r"Kerr: $\Delta n \propto E^{2}$")
ax.axhline(0, color=CREAM, lw=0.6)
ax.axvline(0, color=CREAM, lw=0.6)
ax.axhline(1, color=CREAM, lw=0.4, ls=":")
ax.set_xlabel(r"$E\ (10^{6}\ \mathrm{V/m})$")
ax.set_ylabel(r"$\Delta n\,/\,\Delta n(E_{0})$")
ax.set_ylim(-1.8, 1.8)
ax.set_xlim(-1.25, 1.25)
ax.annotate(r"$\Delta n(-E)=-\Delta n(+E)$", xy=(-1.18, -1.55), fontsize=8,
            color=VIOLET, ha="left", va="center")
ax.annotate(r"$\Delta n(-E)=+\Delta n(+E)$", xy=(0.02, 1.55), fontsize=8,
            color="#8a72ad", ha="left", va="center")
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.26), ncol=2,
          frameon=False, fontsize=9)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
fig.savefig(os.path.join(OUT, "fig1-dn-vs-E.png"))
plt.close(fig)

# ---------------------------------------------------------------- fig 2
# T = sin^2(pi V / 2 Vpi)
v = np.linspace(0, 2.0, 601)             # in units of Vpi
T = np.sin(np.pi * v / 2) ** 2

fig, ax = plt.subplots(figsize=(5.6, 2.9))
ax.plot(v, T, color=VIOLET, lw=1.8)
ax.axhline(0.5, color=PETAL, lw=0.8, ls="--")
ax.axvline(0.5, color=PETAL, lw=0.8, ls="--")
pts = [(0.0, 0.0, "null\n$V=0$"),
       (0.5, 0.5, "quadrature\n$V=V_\\pi/2$"),
       (1.0, 1.0, "peak\n$V=V_\\pi$"),
       (1.5, 0.5, "quadrature\n$V=3V_\\pi/2$")]
for x, y, lab in pts:
    ax.plot([x], [y], "o", ms=5, color=VIOLET)
    ax.annotate(lab, xy=(x, y), xytext=(4, -14 if y > 0.9 else 10),
                textcoords="offset points", fontsize=8, color=CREAM,
                ha="left" if x < 1.2 else "right")
ax.annotate("linear region", xy=(0.5, 0.5), xytext=(0.72, 0.24), fontsize=8,
            color="#8a72ad",
            arrowprops=dict(arrowstyle="->", lw=0.8, color="#8a72ad"))
ax.set_xlabel(r"$V/V_{\pi}$")
ax.set_ylabel(r"$T=I_{\mathrm{out}}/I_{\mathrm{in}}$")
ax.set_xlim(-0.02, 2.02)
ax.set_ylim(-0.03, 1.10)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
fig.savefig(os.path.join(OUT, "fig2-transmission.png"))
plt.close(fig)

print("wrote fig1-dn-vs-E.png, fig2-transmission.png")
print("Pockels dn at E=1e6:", pock[np.argmin(abs(E - 1.0))])
print("Kerr dn at E=1e6:", kerr[np.argmin(abs(E - 1.0))])
