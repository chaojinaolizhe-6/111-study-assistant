# -*- coding: utf-8 -*-
"""生成电工实验 2/3 的可编辑数据文件（xlsx + md + README）。
所有数值按扫描件逐格转录；存疑格用黄色底标出，并在同表下方写清理由。
"""
import os
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
from openpyxl.utils import get_column_letter

ROOT = r"D:\aaa_D_usual\DSH\111学习助手\电工实验_报告"
os.makedirs(ROOT, exist_ok=True)

HEAD = PatternFill("solid", fgColor="DDEBF7")
WARN = PatternFill("solid", fgColor="FFF2CC")
FREE = PatternFill("solid", fgColor="E2EFDA")
THIN = Side(style="thin", color="808080")
BOX = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)


def put(ws, r, c, v, bold=False, fill=None, fmt=None):
    cell = ws.cell(row=r, column=c, value=v)
    cell.border = BOX
    cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    if bold:
        cell.font = Font(bold=True)
    if fill:
        cell.fill = fill
    if fmt:
        cell.number_format = fmt
    return cell


def note(ws, r, text, ncol):
    c = ws.cell(row=r, column=1, value=text)
    c.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
    c.font = Font(size=9, color="808080")
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=ncol)
    ws.row_dimensions[r].height = 30


def widths(ws, ws_widths):
    for i, w in enumerate(ws_widths, start=1):
        ws.column_dimensions[get_column_letter(i)].width = w


def table(ws, r0, data, warn=(), free_cols=(), numfmt="0.0"):
    """在 ws 的第 r0 行起画表。data[0] 是表头。warn 为 (行,列) 相对 data 的 0-based 坐标。"""
    for i, row in enumerate(data):
        for j, v in enumerate(row):
            cell = put(ws, r0 + i, j + 1, v, bold=(i == 0),
                       fill=(HEAD if i == 0 else (WARN if (i, j) in warn else None)))
            if i > 0 and j > 0 and isinstance(v, (int, float)):
                cell.number_format = numfmt
    # 供填写区（绿色）留空
    for (i, j) in free_cols:
        put(ws, r0 + i, j + 1, None, fill=FREE)


# ============================== 实验 2 ==============================
wb2 = Workbook()
ws = wb2.active
ws.title = "说明"
widths(ws, [22, 90])
rows = [
    ("文件用途", "电工实验二（直流电路）数据识别表，供你核对/直接修改。改完告诉我，我按修改后的数算全部中间量与结果。"),
    ("颜色含义", "黄色 = 我读不准、需要你确认的格子；绿色 = 原始报告里留空、需要你补的格子；蓝色 = 表头。"),
    ("工作表", "2.1.2 电阻测量 / 2.1.3 KVL-KCL / 2.1.4 叠加定理 / 二极管 / 提醒"),
    ("修改方式", "直接改单元格数值即可，不要改表头文字和行列顺序，我按固定坐标读回。"),
]
for i, (k, v) in enumerate(rows, start=1):
    put(ws, i, 1, k, bold=True, fill=HEAD)
    put(ws, i, 2, v)

# ---- 表 2.1.2 ----
ws = wb2.create_sheet("2.1.2 电阻测量")
widths(ws, [16, 11, 11, 11, 11, 11, 11, 11])
d = [
    ["电阻", "R1", "R2", "R3", "R4", "R5", "R0", "RL"],
    ["标称值 /Ω", 510, 1000, 510, 510, 330, 51, 220],
    ["实测值 /Ω", 504.2, 966.6, 503.4, 503.9, 326.1, 51.3, 216.4],
    ["相对误差 /%(待算)", None, None, None, None, None, None, None],
]
table(ws, 1, d, free_cols=[(3, j) for j in range(1, 8)], numfmt="0.0")
note(ws, 6, "相对误差 δ = |实测 − 标称| / 标称 × 100%，由我算，你不用填。", 8)

# ---- 表 2.1.3 ----
ws = wb2.create_sheet("2.1.3 KVL-KCL")
widths(ws, [14, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10])
d = [
    ["量", "U_S1/V", "U_S2/V", "I1/mA", "I2/mA", "I3/mA",
     "U_AB/V", "U_CD/V", "U_AD/V", "U_DE/V", "U_FA/V"],
    ["实测值", 5.9, 12.1, 1.8, 60.9, 9, -6.0, -1.9, 4.0, 0.9, 0.9],
    ["计算值(待算)", 6.0, 12.0, None, None, None, None, None, None, None, None],
    ["相对误差/%(待算)", None, None, None, None, None, None, None, None, None, None],
]
table(ws, 1, d, warn={(1, 3), (1, 4)}, free_cols=[(2, j) for j in range(2, 11)], numfmt="0.0")
note(ws, 6, "⚠ I2 格：纸上写「6 0 . 9」，其中 0 是红笔后补；I3 格只剩一个「.9」。"
            "电路理论算出 I2≈6.1 mA、I3≈8.1 mA，所以很可能是 I2=6.0、I3=9（也可能是 I2=6.09、I3 空）。请改成正确值。", 11)
note(ws, 7, "参考：U_AB/U_CD/U_AD/U_DE/U_FA 用实测电阻正演得 −5.94 / −2.00 / 4.06 / 0.97 / 0.97，与实测吻合，可放心。", 11)

# ---- 表 2.1.4 ----
ws = wb2.create_sheet("2.1.4 叠加定理")
widths(ws, [22, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10])
d = [
    ["工况", "U_S1/V", "U_S2/V", "I1/mA", "I2/mA", "I3/mA",
     "U_AB/V", "U_CD/V", "U_AD/V", "U_DE/V", "U_FA/V"],
    ["U_S1 单独作用", 12.0, 0, 8.6, -2.4, 6.2, 2.9, 0.7, 3.2, 4.3, 4.3],
    ["U_S2 单独作用", 0, 6.0, -1.2, 3.6, 2.4, -3.6, -1.1, 1.2, -0.6, -0.6],
    ["U_S1、U_S2 共同作用", 12.0, 6.0, 7.4, 1.2, 8.6, -0.7, -0.4, 4.4, 3.7, 3.7],
    ["2U_S2 单独作用（齐次性）", 0, 12.0, -2.4, 7.2, 4.8, -7.2, -2.2, 2.4, -1.2, -1.2],
]
table(ws, 1, d, numfmt="0.0")
note(ws, 6, "自检：第1行 + 第2行 = 第3行；第2行 × 2 = 第4行（实测值确实满足，可直接用于验证叠加与齐次性）。", 11)

# ---- 二极管 ----
ws = wb2.create_sheet("二极管")
widths(ws, [14, 14, 14])
d = [
    ["U_S1/V", "U_S2/V", "I3/mA"],
    [12.0, 0, 7.8],
    [0, 6.0, -1.3],
    [12.0, 6.0, 1.5],
    [0, 12.0, -2.8],
]
table(ws, 1, d, numfmt="0.0")
note(ws, 7, "R3 换成 1N4007 后测 I3：7.8 + (−1.3) = 6.5 ≠ 1.5，说明叠加定理对非线性元件不成立。", 3)

wb2.save(os.path.join(ROOT, "实验2_直流电路数据.xlsx"))

# ============================== 实验 3 ==============================
wb3 = Workbook()
ws = wb3.active
ws.title = "说明"
widths(ws, [22, 90])
rows = [
    ("文件用途", "电工实验三（交流电路）数据识别表，供你核对/直接修改。"),
    ("颜色含义", "黄色 = 读不准、需确认；绿色 = 原报告留空待补。"),
    ("工作表", "3-1 等效变换 / 3-2 日光灯 / 3-3 电压三角形 / 3-4 点火电压"),
]
for i, (k, v) in enumerate(rows, start=1):
    put(ws, i, 1, k, bold=True, fill=HEAD)
    put(ws, i, 2, v)

ws = wb3.create_sheet("3-1 等效变换")
widths(ws, [28, 20, 10, 10, 24])
d = [
    ["电路", "电源取值", "U/V", "I/mA", "说明"],
    ["图一（电压源 + R0 串联）", "U_S = 6.0 V", 4.1, 19.2, "R0=51Ω，RL=220Ω"],
    ["图二（电流源 + R0 并联）", "I_S = 103.5 mA", 4.1, 19.2, "R0=51Ω，RL=220Ω"],
]
table(ws, 1, d, warn={(1, 1)}, numfmt="0.0")
note(ws, 5, "⚠ 图上「60V」按 6.0 V 读：只有 6 V / (51+220)Ω ≈ 19.2 mA、19.2mA×220Ω ≈ 4.1 V 才对得上实测；且 6 V/51Ω ≈ 117.6 mA 与 103.5 mA 同量级。", 5)

ws = wb3.create_sheet("3-2 日光灯")
widths(ws, [10] + [10] * 10)
d = [
    ["C/μF", "U/V", "U_R/V", "U_L/V", "I/mA", "I_C/mA",
     "P/W", "P_R/W", "P_L/W", "cosφ计算", "cosφ实测"],
    [0.0, 219.6, 194.5, 56.7, 313.4, 0, 27.2, 24.4, 28.9, 0.0, 0.426],
    [1.0, 219.6, 194.5, 56.7, 274.8, 43.2, 307.9, 28.4, 28.9, 0.0, 0.485],
    [2.0, 219.6, 194.5, 56.7, 198.5, 139.9, 306.9, 26.4, 28.9, 0.0, 0.678],
    [3.7, 219.6, 194.5, 56.7, 143.7, 304.2, 306.9, 28.2, 28.8, 0.0, 0.989],
    [4.7, 219.6, 194.5, 56.7, 134.9, 346.9, 307.5, 24.2, 28.9, 0.0, 0.904],
    [5.7, 219.6, 194.5, 56.7, 222.3, 443.5, 308.1, 29.2, 28.9, 0.0, 0.630],
]
table(ws, 1, d, warn={(i, 6) for i in range(2, 7)}, free_cols=[(i, 9) for i in range(1, 7)], numfmt="0.0")
note(ws, 9, "⚠ P 列：纸上写 307.9 / 306.9 / 306.9 / 307.5 / 308.1。"
            "但 cosφ = P/(U·I) 反推 P ≈ 30.7 W 才自洽（如 219.6×0.2223×0.630 = 30.8 W），疑小数点整体右移一位。", 11)
note(ws, 10, "I 列按 mA 读（表头写作 I/A，但 313.4 A 不可能，0.313 A 才对）。cosφ计算列原报告填 0.0，实际需按 P/(UI) 算。", 11)
note(ws, 11, "P_R / P_L 两列我不确定对应哪条支路（表头顺序为 P、P_R、P_L），数值照抄，含义请你确认。", 11)

ws = wb3.create_sheet("3-3 电压三角形")
widths(ws, [12, 12, 12, 12])
d = [
    ["", "1 μF", "2 μF", "4.7 μF"],
    ["U_R/V", 219.1, 218.9, 215.2],
    ["U_C/V", 19.9, 23.3, 43.8],
    ["U/V", 220.1, 220.1, 220.1],
]
table(ws, 1, d, numfmt="0.0")
note(ws, 6, "自检：√(U_R² + U_C²) = 220.0 / 220.1 / 219.6，与实测 U 一致，电压三角形成立。", 4)

ws = wb3.create_sheet("3-4 点火电压")
put(ws, 1, 1, "日光灯点火电压", bold=True, fill=HEAD)
put(ws, 2, 1, "173.3 V")
widths(ws, [22])

wb3.save(os.path.join(ROOT, "实验3_交流电路数据.xlsx"))
print("ok")
