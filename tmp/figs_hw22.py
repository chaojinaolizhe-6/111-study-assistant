# -*- coding: utf-8 -*-
"""生成 Lecture 22-23 讲义所需的四张矢量图（PDF）+ PNG 预览（v2）。"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.patches import Circle
from scipy.integrate import solve_ivp

CJK = FontProperties(fname=r"C:\Windows\Fonts\msyh.ttc")

VIOLET = "#6B4E8F"
DEEP = "#3F2C5C"
PETAL = "#B79FD0"
GRAY = "#5C606E"
CREAM = "#FCF9F2"
RULE = "#D9CFE6"

plt.rcParams.update({
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "axes.unicode_minus": False,
    "font.size": 9,
    "axes.edgecolor": GRAY,
    "axes.linewidth": 0.6,
    "xtick.color": GRAY,
    "ytick.color": GRAY,
    "xtick.labelsize": 7.5,
    "ytick.labelsize": 7.5,
    "text.color": DEEP,
    "mathtext.fontset": "dejavusans",
})

OUT = os.path.join("subjects", "03-微分方程", "讲义", "figs-hw22")
os.makedirs(OUT, exist_ok=True)


def save(fig, name):
    fig.savefig(os.path.join(OUT, name + ".pdf"), bbox_inches="tight", pad_inches=0.02)
    fig.savefig(os.path.join(OUT, name + ".png"), dpi=170, bbox_inches="tight", pad_inches=0.02)
    plt.close(fig)


def field(A, X, Y):
    return A[0, 0] * X + A[0, 1] * Y, A[1, 0] * X + A[1, 1] * Y


def traj_linear(A, x0, times):
    sol = solve_ivp(lambda t, z: A @ z, (times[0], times[-1]), x0,
                    t_eval=times, rtol=1e-9, atol=1e-11)
    return sol.y[0], sol.y[1]


def panel(A, ax, L, seeds, T):
    X, Y = np.meshgrid(np.linspace(-L, L, 220), np.linspace(-L, L, 220))
    U, V = field(A, X, Y)
    ax.streamplot(X, Y, U, V, color=RULE, linewidth=0.5, arrowsize=0.45,
                  density=0.85, zorder=1)

    times = np.linspace(-T, T, 1100)
    for ang, r0 in seeds:
        x0 = r0 * np.array([np.cos(ang), np.sin(ang)])
        xs, ys = traj_linear(A, x0, times)
        m = (np.abs(xs) <= L * 1.04) & (np.abs(ys) <= L * 1.04)
        ax.plot(np.where(m, xs, np.nan), np.where(m, ys, np.nan),
                color=VIOLET, lw=0.95, zorder=3, solid_capstyle="round")

    w = np.linalg.eigvals(A)
    if np.max(np.abs(w.imag)) < 1e-9:
        vals, vecs = np.linalg.eig(A)
        for i in range(len(vals)):
            v = np.real(vecs[:, i])
            v = v / np.linalg.norm(v) * L * 1.03
            ax.plot([-v[0], v[0]], [-v[1], v[1]], ls=(0, (4, 3)), lw=0.85,
                    color=PETAL, zorder=2)

    ax.plot(0, 0, "o", ms=3.6, color=DEEP, zorder=5)
    ax.set_xlim(-L, L)
    ax.set_ylim(-L, L)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.set_xlabel(r"$x$", labelpad=0.5)
    ax.set_ylabel(r"$y$", labelpad=0.5)


def ring(n, r0, r1=None, phase=0.13):
    if r1 is None:
        return [(2 * np.pi * k / n + phase, r0) for k in range(n)]
    return [(2 * np.pi * k / n + phase, r0 + (r1 - r0) * k / max(n - 1, 1)) for k in range(n)]


def fig_kinds():
    fig, axes = plt.subplots(2, 3, figsize=(9.6, 6.6))
    spec = [
        (np.array([[3, 2], [1, 4]], float), 1.55, "(a) 不稳定结点", r"$\lambda=2,\,5$",
         ring(9, 0.62), 0.38),
        (np.array([[1, 0], [0, -1]], float), 1.55, "(b) 鞍点", r"$\lambda=\pm1$",
         ring(8, 1.25), 1.55),
        (np.array([[-1, 2], [-2, -1]], float), 1.55, "(c) 稳定焦点", r"$\lambda=-1\pm2i$",
         ring(9, 1.30), np.pi),
        (np.array([[0, 1], [-1, 0]], float), 1.55, "(d) 中心", r"$\lambda=\pm i$",
         ring(11, 0.22, 1.35), 2 * np.pi),
        (np.array([[-1, 0], [0, -1]], float), 1.35, "(e) 临界结点", r"$\lambda=-1$（二重）",
         ring(12, 1.45), 2.2),
        (np.array([[-1, 0], [0, -2]], float), 1.55, "(f) 稳定结点", r"$\lambda=-1,\,-2$",
         ring(9, 1.45), 2.6),
    ]
    for ax, (A, L, title, sub, seeds, T) in zip(axes.ravel(), spec):
        panel(A, ax, L, seeds, T)
        ax.set_title(title, fontproperties=CJK, fontsize=10.5, color=DEEP, pad=4)
        ax.text(0.5, -0.128, sub, transform=ax.transAxes, ha="center", va="top",
                fontsize=8.5, fontproperties=CJK)
    fig.subplots_adjust(wspace=0.22, hspace=0.34)
    save(fig, "fig1-kinds")


def fig_taud():
    from matplotlib.patches import Polygon

    fig, ax = plt.subplots(figsize=(6.9, 5.0))
    xl, xr, yb, yt = -7.6, 7.6, -4.2, 11.5
    par = lambda x: x ** 2 / 4.0
    xs = np.linspace(0, xl, 200)

    def band(pts, color, z):
        ax.add_patch(Polygon(pts, closed=True, facecolor=color, edgecolor="none", zorder=z))

    band([(xl, yb), (xr, yb), (xr, 0), (xl, 0)], "#E9E1F4", 0.4)                       # 鞍点
    band([(0, 0)] + list(zip(xs, par(xs))) + [(xl, 0)], "#F0EAF8", 0.5)               # 稳定结点
    xsr = np.linspace(0, xr, 200)
    band([(0, 0)] + list(zip(xsr, par(xsr))) + [(xr, 0)], "#FBF8FE", 0.5)             # 不稳定结点
    band(list(zip(xs, par(xs))) + [(xl, yt), (0, yt)], "#D5C4EB", 0.55)               # 稳定焦点
    band(list(zip(xsr, par(xsr))) + [(xr, yt), (0, yt)], "#FAF5FE", 0.55)             # 不稳定焦点
    band([(-0.055, 0), (0.055, 0), (0.055, yt), (-0.055, yt)], "#BBA3DC", 0.6)        # 中心

    ax.plot([xl, xr], [0, 0], color=GRAY, lw=1.0, zorder=2)
    ax.plot([0, 0], [yb, yt], color=GRAY, lw=1.0, zorder=2)
    ax.plot(np.linspace(xl, xr, 601), par(np.linspace(xl, xr, 601)), color=VIOLET, lw=1.4, zorder=2)
    ax.set_xlim(xl, xr)
    ax.set_ylim(yb, yt)
    ax.set_xlabel(r"$\tau=\operatorname{tr}A$", fontsize=10)
    ax.set_ylabel(r"$\Delta=\det A$", fontsize=10)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)

    lab = dict(fontproperties=CJK, fontsize=9.5, color=DEEP, ha="center", va="center")
    ax.text(-5.6, 3.0, "稳定结点", **lab)
    ax.text(5.6, 3.0, "不稳定结点", **lab)
    ax.text(-2.9, 8.4, "稳定焦点", **lab)
    ax.text(3.0, 8.4, "不稳定焦点", **lab)
    ax.text(0, -2.3, "鞍点（恒不稳定）", **lab)
    ax.annotate("中心\n（稳定、非渐近）", xy=(0, 6.4), xytext=(1.5, 10.1),
                fontproperties=CJK, fontsize=9, color=DEEP, ha="left", va="center",
                arrowprops=dict(arrowstyle="-|>", color=VIOLET, lw=0.9,
                                connectionstyle="arc3,rad=0.28"))
    ax.text(4.4, 5.0, r"$\Delta=\tau^{2}/4$", fontsize=8.6, color=VIOLET, rotation=50)

    pts = [
        (7.0, 10.0, "①", (0.0, 0.70)),
        (-2.0, 1.0, "②", (-0.10, -1.05)),
        (-2.0, 5.0, "③", (0.50, 0.35)),
        (1.5, 0.5, "④", (0.62, -0.72)),
    ]
    for x, y, tag, off in pts:
        ax.plot([x], [y], "o", ms=5.4, mfc="white", mec=DEEP, mew=1.2, zorder=6)
        ax.plot([x], [y], "o", ms=1.8, color=DEEP, zorder=7)
        ax.annotate(tag, xy=(x, y), xytext=(x + off[0] * 1.15, y + off[1] * 1.15),
                    fontsize=11, color=DEEP, ha="center", va="center", zorder=8)
    ax.text(0.015, 0.03, "作业①–④与第 2 题的线性部分都落在这张图上",
            transform=ax.transAxes, ha="left", va="bottom", fontproperties=CJK,
            fontsize=8.2, color=GRAY)
    save(fig, "fig2-taud")


def fig_epsdelta():
    fig, axes = plt.subplots(1, 2, figsize=(8.4, 3.6))
    eps, delta = 1.0, 0.50

    def rings(ax):
        ax.add_patch(Circle((0, 0), eps, fill=False, ls=(0, (5, 3)), lw=1.0, color=VIOLET))
        ax.add_patch(Circle((0, 0), delta, fill=False, ls=(0, (2, 2)), lw=1.0, color=PETAL))
        ax.plot(0, 0, "o", ms=3.2, color=DEEP)
        ax.text(eps * 0.72, eps * 0.70, r"$\varepsilon$", fontsize=10, color=VIOLET)
        ax.text(delta * 0.60, -delta * 0.92, r"$\delta$", fontsize=10, color=VIOLET)

    # (a) 稳定焦点：起点在 delta 内，轨线留在 eps 内并趋于原点
    ax = axes[0]
    rings(ax)
    A = np.array([[-0.34, 2.0], [-2.0, -0.34]])
    times = np.linspace(0, 13.0, 2200)
    for ang in np.linspace(0, 2 * np.pi, 5, endpoint=False):
        xs, ys = traj_linear(A, 0.48 * np.array([np.cos(ang), np.sin(ang)]), times)
        ax.plot(xs, ys, color=DEEP, lw=0.95)
    ax.set_title("(a) 稳定：从 $\\delta$ 内出发，永不跑出 $\\varepsilon$",
                 fontproperties=CJK, fontsize=9.4, color=DEEP, pad=5)
    ax.text(0.015, 0.035, "$t\\to\\infty$ 时趋于原点（渐近稳定）", transform=ax.transAxes,
            fontsize=8.6, color=GRAY, fontproperties=CJK)

    # (b) 不稳定：起点很小，仍然越界
    ax = axes[1]
    rings(ax)
    B = np.array([[0.55, 0.25], [0.25, 0.60]])
    times = np.linspace(0, 4.2, 2000)
    for ang in np.linspace(0, 2 * np.pi, 7, endpoint=False):
        xs, ys = traj_linear(B, 0.06 * np.array([np.cos(ang), np.sin(ang)]), times)
        m = np.hypot(xs, ys) <= 1.58
        ax.plot(np.where(m, xs, np.nan), np.where(m, ys, np.nan), color=DEEP, lw=0.95)
    ax.plot(0.06, 0, "o", ms=2.6, color=VIOLET, zorder=6)
    ax.annotate("起点（$0.06\\ll\\delta$）", xy=(0.06, 0), xytext=(0.10, -0.62),
                fontsize=8.2, color=VIOLET, fontproperties=CJK,
                arrowprops=dict(arrowstyle="-", color=PETAL, lw=0.8))
    ax.set_title("(b) 不稳定：起点再近，也能跑出 $\\varepsilon$",
                 fontproperties=CJK, fontsize=9.4, color=DEEP, pad=5)
    ax.text(0.015, 0.035, "无论 $\\delta$ 取多小，总有一条轨线越界", transform=ax.transAxes,
            fontsize=8.6, color=GRAY, fontproperties=CJK)

    for ax in axes:
        ax.set_xlim(-1.62, 1.62)
        ax.set_ylim(-1.62, 1.62)
        ax.set_aspect("equal")
        ax.set_xticks([])
        ax.set_yticks([])
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
        ax.set_xlabel(r"$x$", labelpad=0.5)
        ax.set_ylabel(r"$y$", labelpad=0.5)
    fig.subplots_adjust(wspace=0.16)
    save(fig, "fig3-epsdelta")


def hw2_field(X, Y):
    P = X - X ** 2 - X * Y
    Q = 0.5 * Y - 0.75 * X * Y - 0.25 * Y ** 2
    return P, Q


def hw2_traj(z0, T):
    def rhs(t, z):
        P, Q = hw2_field(np.array([z[0]]), np.array([z[1]]))
        return [float(P[0]), float(Q[0])]

    sol = solve_ivp(rhs, (0, T), z0, t_eval=np.linspace(0, T, 1500),
                    rtol=1e-9, atol=1e-11)
    return sol.y


def fig_hw2():
    fig, axes = plt.subplots(1, 2, figsize=(9.4, 4.1),
                             gridspec_kw={"width_ratios": [1.18, 1.0]})

    ax = axes[0]
    X, Y = np.meshgrid(np.linspace(-0.55, 1.75, 400), np.linspace(-0.55, 2.45, 400))
    U, V = hw2_field(X, Y)
    ax.streamplot(X, Y, U, V, color=RULE, linewidth=0.5, arrowsize=0.45, density=1.15, zorder=1)
    seeds = [(-0.4, 0.1), (-0.3, 1.0), (0.15, -0.35), (0.85, 2.3), (1.55, 1.9),
             (1.2, -0.3), (0.35, 1.55), (1.5, 0.6), (0.05, 2.2), (1.62, 0.15)]
    for z0 in seeds:
        ys = hw2_traj(np.array(z0, float), 12.0)
        ax.plot(ys[0], ys[1], color=VIOLET, lw=0.85, zorder=3)
    pts = [(0, 0, "不稳定结点", (0.14, 0.26), "o"),
           (1, 0, "稳定结点", (0.02, -0.36), "o"),
           (0, 2, "稳定结点", (0.10, 0.26), "o"),
           (0.5, 0.5, "鞍点", (0.24, 0.20), "X")]
    for x, y, name, off, mk in pts:
        ax.plot(x, y, mk, ms=6.6 if mk == "X" else 5.2, color=DEEP,
                mfc=CREAM if mk == "X" else DEEP, mew=1.1, zorder=6)
        ax.annotate(name, xy=(x, y), xytext=(x + off[0], y + off[1]),
                    fontproperties=CJK, fontsize=8.6, color=DEEP, zorder=7)
    ax.set_xlim(-0.55, 1.75)
    ax.set_ylim(-0.55, 2.45)
    ax.set_xlabel(r"$x_1$", labelpad=0.5)
    ax.set_ylabel(r"$x_2$", labelpad=0.5)
    ax.set_title("(a) 第 2 题系统的全局相图", fontproperties=CJK, fontsize=9.6, color=DEEP, pad=5)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)

    ax = axes[1]
    L = 0.42
    X, Y = np.meshgrid(np.linspace(-L, L, 260), np.linspace(-L, L, 260))
    U, V = hw2_field(X, Y)
    ax.streamplot(X, Y, U, V, color=RULE, linewidth=0.5, arrowsize=0.45, density=0.95, zorder=1)
    for ang in np.linspace(0, 2 * np.pi, 12, endpoint=False):
        z0 = 0.055 * np.array([np.cos(ang), np.sin(ang)])
        ys = hw2_traj(z0, 3.2)
        m = (np.abs(ys[0]) <= L * 1.06) & (np.abs(ys[1]) <= L * 1.06)
        ax.plot(np.where(m, ys[0], np.nan), np.where(m, ys[1], np.nan),
                color=VIOLET, lw=0.85, zorder=3)
    ax.plot([0, 0], [-L, L], ls=(0, (4, 3)), color=PETAL, lw=0.9, zorder=2)
    ax.plot(0, 0, "o", ms=5.2, color=DEEP, zorder=6)
    ax.set_xlim(-L, L)
    ax.set_ylim(-L, L)
    ax.set_aspect("equal")
    ax.set_xlabel(r"$x_1$", labelpad=0.5)
    ax.set_ylabel(r"$x_2$", labelpad=0.5)
    ax.set_title("(b) 原点放大：沿 $x_2$ 轴增长较慢", fontproperties=CJK,
                 fontsize=9.6, color=DEEP, pad=5)
    ax.text(0.03, 0.94, "小扰动都被推离原点", transform=ax.transAxes,
            fontproperties=CJK, fontsize=8.4, color=GRAY, va="top")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)

    fig.subplots_adjust(wspace=0.26)
    save(fig, "fig4-hw2")


if __name__ == "__main__":
    fig_kinds()
    fig_taud()
    fig_epsdelta()
    fig_hw2()
    print("figures written")
