# 电工实验 2 / 3 数据与报告工程

## 交付文件

| 文件 | 说明 |
|---|---|
| **电工实验二三_报告填写指南_中英双版.pdf** | 主交付物，13 页。每个填写项先给**英文**（可直接抄进报告），再给**中文**对照。 |
| **实验2_数据与计算.xlsx** | 实验二 6 张表：2.1.2 电阻（含 δ）、2.1.3 KVL/KCL（含计算值与 δ）、2.1.4 叠加、2.1.4 校验、二极管、**等效变换** |
| **实验3_数据与计算.xlsx** | 实验三：日光灯（含 cosφ 计算列）、3-2 分析（S/Q/I_C/偏差）、电压三角形、3-3 校验、点火电压 |
| 实验2_直流电路数据.xlsx | **源数据（未改动）** |
| 实验3_交流电路数据.xlsx | **源数据（未改动）** |
| _备份/ | 你确认时的源数据副本 + SHA256 校验值 |

## PDF 的双语约定

- `EN` 蓝标段落 = **报告里要写的内容**（英文，可原样照抄）。
- `中` 灰标段落 = 中文对照，用于理解与答辩解释。
- 表格用实验册原始英文行名：Measured / Calculated / Relative error，
  表下附行名对照（实测 / 计算 / 相对误差）。

## 结构（按实验册页码）

- **实验册第 1--5 页 = Experiment 2**：Preliminary Work → Fig. 2.1.1 → Table 2.1.2 / 2.1.3 / 2.1.4 →
  1N4007 diode → **第 3--4 页第 3 节 equivalent transformation** → Discussion（第 5 页）。
- **实验册第 6--8 页 = Experiment 3**：Preliminary Work → fluorescent-lamp wiring & data →
  ignition voltage → voltage triangle。

因此“等效变换”已从实验三移到实验二的《实验2_数据与计算.xlsx》“等效变换”表；
《实验3_数据与计算.xlsx》保留源表 3-1 并在“说明”页注明归属。

## 计算口径

- 相对误差：δ = |X_meas − X_calc| / |X_calc| × 100%（电阻表以标称值为参考）。
- 电路正演：节点电压法，V_D = 0，电源正极在 F 端与 B 端；
  方向 I₁: F→A，I₂: B→A，I₃: A→D。
- 有效数字：U、I 1 位小数；相对误差 1--2 位小数。

## 重新生成

```powershell
python compute.py             # 源数据 → 计算结果.json
python build_pdf_bilingual.py # → report_guide_bi.tex → PDF（中英双版）
python fill_xlsx.py           # → 两份“数据与计算” xlsx
```

源数据 xlsx 一旦改动，重跑以上三步即可同步更新全部结果与 PDF。
`build_pdf.py`、`build_data.py` 为早期中文单语版脚本，保留备查，可删。
