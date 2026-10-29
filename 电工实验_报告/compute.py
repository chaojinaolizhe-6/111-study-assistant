# -*- coding: utf-8 -*-
"""从已冻结的源数据 xlsx 读取数值，计算全部中间量与结果。
只读源文件，不改动；输出 计算结果.json 与 计算用表.xlsx（新文件）。
"""
import json
import os

import numpy as np
import openpyxl

ROOT = r"D:\aaa_D_usual\DSH\111学习助手\电工实验_报告"
F2 = os.path.join(ROOT, "实验2_直流电路数据.xlsx")
F3 = os.path.join(ROOT, "实验3_交流电路数据.xlsx")

wb2 = openpyxl.load_workbook(F2, data_only=True)
wb3 = openpyxl.load_workbook(F3, data_only=True)

R = {}


def grab(ws, r, c0, c1):
    return [ws.cell(row=r, column=c).value for c in range(c0, c1 + 1)]


# ---------------- 表 2.1.2 ----------------
ws = wb2["2.1.2 电阻测量"]
nom = grab(ws, 2, 2, 8)
mea = grab(ws, 3, 2, 8)
names = ["R1", "R2", "R3", "R4", "R5", "R0", "RL"]
err = [abs(m - n) / n * 100 for n, m in zip(nom, mea)]
R["r_meas"] = dict(zip(names, mea))
R["t212"] = {"names": names, "nominal": nom, "measured": mea, "error": err}

# ---------------- 电路正演模型 ----------------
Rm = R["r_meas"]
R1, R2, R3, R4, R5 = (Rm["R1"], Rm["R2"], Rm["R3"], Rm["R4"], Rm["R5"])


def solve(us1, us2):
    """节点法。V_D=0, V_F=V_E+U_S1, V_C=V_B-U_S2（两电源正极分别在 F 端与 B 端）。"""
    A = np.array([
        [1 / R1 + 1 / R2 + 1 / R3, -1 / R2, -1 / R1],
        [-1 / R2, 1 / R2 + 1 / R5, 0.0],
        [-1 / R1, 0.0, 1 / R1 + 1 / R4],
    ])
    b = np.array([us1 / R1, us2 / R5, -us1 / R1])
    vA, vB, vE = np.linalg.solve(A, b)
    vC, vF = vB - us2, vE + us1
    return {
        "I1": (vF - vA) / R1 * 1000,
        "I2": (vB - vA) / R2 * 1000,
        "I3": vA / R3 * 1000,
        "U_AB": vA - vB,
        "U_CD": vC,
        "U_AD": vA,
        "U_DE": -vE,
        "U_FA": vF - vA,
        "_v": dict(vA=vA, vB=vB, vC=vC, vE=vE, vF=vF),
    }


# ---------------- 表 2.1.3 ----------------
ws = wb2["2.1.3 KVL-KCL"]
cols = ["U_S1", "U_S2", "I1", "I2", "I3", "U_AB", "U_CD", "U_AD", "U_DE", "U_FA"]
meas = dict(zip(cols, grab(ws, 2, 2, 11)))
calc = solve(meas["U_S1"], meas["U_S2"])
rel = {k: abs(meas[k] - calc[k]) / abs(calc[k]) * 100 for k in cols[2:]}
R["t213"] = {"cols": cols, "meas": meas,
             "calc": {k: calc[k] for k in cols[2:]},
             "rel": rel, "node_v": calc["_v"]}

# ---------------- 表 2.1.4 ----------------
ws = wb2["2.1.4 叠加定理"]
cases = ["U_S1 单独", "U_S2 单独", "共同作用", "2U_S2"]
rows = {c: dict(zip(cols, grab(ws, 2 + i, 2, 11))) for i, c in enumerate(cases)}
theory = {c: solve(rows[c]["U_S1"], rows[c]["U_S2"]) for c in cases}
sum_res = {k: (rows["U_S1 单独"][k] + rows["U_S2 单独"][k]) - rows["共同作用"][k] for k in cols}
hom_res = {k: 2 * rows["U_S2 单独"][k] - rows["2U_S2"][k] for k in cols}
R["t214"] = {"cases": cases, "meas": rows,
             "theory": {c: {k: theory[c][k] for k in cols[2:]} for c in cases},
             "sum_res": sum_res, "hom_res": hom_res,
             "sum_row": {k: rows["U_S1 单独"][k] + rows["U_S2 单独"][k] for k in cols},
             "double_row": {k: 2 * rows["U_S2 单独"][k] for k in cols}}

# ---------------- 二极管 ----------------
ws = wb2["二极管"]
dio = [grab(ws, r, 1, 3) for r in range(2, 6)]
R["diode"] = {"rows": dio,
              "sum": dio[0][2] + dio[1][2],
              "both": dio[2][2],
              "res": dio[0][2] + dio[1][2] - dio[2][2],
              "double": 2 * dio[1][2],
              "hom_res": 2 * dio[1][2] - dio[3][2]}

# ---------------- 等效变换（属实验二） ----------------
ws = wb3["3-1 等效变换"]
eq1 = grab(ws, 2, 3, 4)
eq2 = grab(ws, 3, 3, 4)
US_SRC, IS_SRC, R0, RLm = 6.0, 103.5, Rm["R0"], Rm["RL"]
R["equiv"] = {
    "us_src": US_SRC, "is_src": IS_SRC, "R0": R0, "RL": RLm,
    "fig1": {"U": eq1[0], "I": eq1[1]},
    "fig2": {"U": eq2[0], "I": eq2[1]},
    "R_loop": RLm + R0,
    "I_theory1": US_SRC / (R0 + RLm) * 1000,
    "U_theory1": US_SRC * RLm / (R0 + RLm),
    "I_theory2": IS_SRC * R0 / (R0 + RLm),
    "U_theory2": IS_SRC * R0 / (R0 + RLm) * RLm / 1000,
    "IS_theory": US_SRC / R0 * 1000,
    "US_from_IS": IS_SRC * R0 / 1000,
    "R_port1": eq1[0] / (eq1[1] / 1000),
    "R_port2": eq2[0] / (eq2[1] / 1000),
}

# ---------------- 日光灯 ----------------
ws = wb3["3-2 日光灯"]
hdr = grab(ws, 1, 1, 14)
fl = [grab(ws, r, 1, 14) for r in range(2, 8)]
f = 50.0
w = 2 * np.pi * f
rowsfl = []
for row in fl:
    (C, U, UR, UL, I, IC, IL, P, PLR, PC, ccalc, cmeas, PL, PR) = row
    S = U * I / 1000                      # V·A
    cos_calc = P / S if S else None
    Q = np.sqrt(max(S ** 2 - P ** 2, 0))
    IC_th = w * C * 1e-6 * U * 1000        # mA
    rowsfl.append(dict(C=C, U=U, UR=UR, UL=UL, I=I, IC=IC, IL=IL, P=P,
                       PLR=PLR, PC=PC, cos_calc=cos_calc, cos_meas=cmeas,
                       S=S, Q=Q, IC_th=IC_th, PL=PL, PR=PR,
                       dev=abs(cos_calc - cmeas) / cmeas * 100 if cmeas else None))
R["fluor"] = {"hdr": hdr, "rows": rowsfl, "f": f,
              "Imin_row": min(rowsfl, key=lambda d: d["I"])["C"],
              "cos_max": max(rowsfl, key=lambda d: d["cos_meas"])["C"]}

# 最佳补偿电容（按 C=0 行的感性无功估算）
base = rowsfl[0]
phi0 = np.degrees(np.arccos(base["cos_calc"]))
C_opt = base["P"] * np.tan(np.radians(phi0)) / (w * base["U"] ** 2) * 1e6
R["fluor"]["phi0_deg"] = phi0
R["fluor"]["C_opt"] = C_opt
R["fluor"]["IC_need"] = base["IL"] * np.sin(np.radians(phi0))

# ---------------- 电压三角形 ----------------
ws = wb3["3-3 电压三角形"]
vt = [grab(ws, r, 2, 4) for r in range(2, 5)]
vrows = []
for j, cap in enumerate(["1", "2", "4.7"]):
    UR, UC, U = vt[0][j], vt[1][j], vt[2][j]
    Uth = np.hypot(UR, UC)
    vrows.append(dict(C=cap, UR=UR, UC=UC, U=U, U_calc=Uth,
                      dev=(Uth - U) / U * 100,
                      phi=np.degrees(np.arctan2(UC, UR))))
R["vtri"] = {"rows": vrows}

# ---------------- 点火电压 ----------------
R["ignition"] = str(wb3["3-4 点火电压"].cell(row=2, column=1).value)

with open(os.path.join(ROOT, "计算结果.json"), "w", encoding="utf-8") as fh:
    json.dump(R, fh, ensure_ascii=False, indent=1, default=float)

# ---------- 控制台摘要 ----------
print("R errors:", [round(e, 2) for e in err])
print("2.1.3 calc:", {k: round(v, 2) for k, v in R["t213"]["calc"].items()})
print("2.1.3 rel%:", {k: round(v, 1) for k, v in rel.items()})
print("2.1.4 sum_res:", {k: round(v, 2) for k, v in sum_res.items()})
print("2.1.4 hom_res:", {k: round(v, 2) for k, v in hom_res.items()})
print("diode:", R["diode"])
print("equiv:", {k: (round(v, 2) if isinstance(v, float) else v) for k, v in R["equiv"].items()})
for r_ in rowsfl:
    print("fluor C=%.1f  S=%.1f  cos_calc=%.3f  cos_meas=%.3f  Q=%.1f  IC_th=%.0f"
          % (r_["C"], r_["S"], r_["cos_calc"], r_["cos_meas"], r_["Q"], r_["IC_th"]))
print("phi0=%.1f deg  C_opt=%.2f uF  IC_need=%.0f mA" % (phi0, C_opt, R["fluor"]["IC_need"]))
for r_ in vrows:
    print("vtri C=%s  U_calc=%.1f  U=%.1f  dev=%.2f%%  phi=%.1f" % (r_["C"], r_["U_calc"], r_["U"], r_["dev"], r_["phi"]))
print("ignition:", R["ignition"])
