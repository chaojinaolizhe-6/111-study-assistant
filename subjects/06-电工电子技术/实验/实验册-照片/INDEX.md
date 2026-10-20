---
# 该文件夹是纸质实验册照片存放处，本文件供校验脚本识别目录（scripts 要求每个 subject 子目录有 INDEX.md）
---

# 纸质实验册照片（电工学实验A1，2026-09-29 上传 8 张）

- 材料：8 张手机照片 `册-p01 ~ 册-p08`（原图 1773×2364，来自学习者 2026-09-29 10:03 拍摄）
- 读取状态（2026-09-29）：①文件已登记 ✅ ②无需渲染 ✅ ③**内容已阅读（8/8）** ✅ ④关键页已逐项核验 ✅
- 读入方式：当次会话视觉模型**直读原图**（可读图，实测通过）
- **照片覆盖范围**：实验册**最前面几页**（清单、上课须知、安全规则）+ **"2. DC Circuit Experiment"的 1–5 页**
- ⚠ **没有覆盖**：`1. Multisim Simulation Experiment`（今天实验1）的正文页 —— **[待确认] 它在册子的哪几页**

---

## p01｜List of Experiments（实验清单）—— **重要：填掉了"实验2–8 内容未知"**

| # | Experiment | Operation Full Marks |
|---|-----------|---------------------|
| 1 | Multisim Simulation Experiment | **10** |
| 2 | DC Circuit Experiment | 5 |
| 3 | AC Circuit Experiment | 5 |
| 4 | DC Stabilized Power Supply Experiment | 5 |
| 5 | Transistor Single-Stage Amplifier Circuit Experiment | 10 |
| 6 | Integrated Operational Amplifier Experiment | **25** |
| 7 | Integrated Logic Gate and Combinational Logic Function Devices Experiment | 10 |
| 8 | Trigger and Counter Experiment | 10 |
| — | Additional Items | — |

表头列：`Operation Full Marks` ｜ `Preparation (Total 5 points)` ｜ `Operation` ｜ `Discussion of Results (10+5 points)` ｜ `Score`

> **Tip（册上原文）**：*Once the electronic report of the Experiment 1 is complete, please print it out and submit it along with this report.*
> → 即：**实验1 的报告＝电子版（docx）**，做完后**打印**，与**这本纸质册**一同提交。纸质册里**没有**实验1 的正文页。
>
> ⚠ 推论（**待与老师核实**）：**"Preparation" 单独占 5 分** → 预习是**计分项**，与《上课须知》"没有预习报告不允许做实验"互相印证。

## p02｜电工学实验上课须知（中文）—— **电子版里完全没有的硬规定**

> 原文要点（逐条摘录，非改写）

**一、选课要求**
- 实验选课前需确认已在教务选课系统中选择该课程（否则没成绩）。实验实施**网上选课**，请按选课时间上课；
  有特殊情况需事先请假；**无故缺课不上者不得补做，缺实验者不得成绩**。

**二、预习要求**
1. **课前认真阅读实验教程，完成预习报告内容。** 设计性实验和综合性实验课前预习时还要完成必要的**电路设计和实验方案设计**，提前画出电路图、标注所用元器件参数值等。注意实验内容有**必做实验和选做实验**；
2. 绘制电路原理图时应**明确标注出元器件的参数值，用铅笔、直尺**作图；
3. 记录实验数据时，应**明确标注实验数据的单位**；
4. 画图时，应标注**坐标轴、参考点、坐标参数及单位、波形参数**等完整信息；
5. **没有预习报告或预习报告不合格者不允许做实验。**

**三、实验课上要求**
1. 严格遵守《电工学实验室安全操作规则》；
2. **独立完成实验，抄袭数据、编造数据均记 0 分，严禁带他人实验报告进入实验室**；
3. 实验中不许擅自离开实验操作岗位；发现仪器异常或故障应立即**切断电源**停止实验，报告指导教师；
4. 实验完毕应将仪器设备归位，不得将实验室物品带出教室；
5. **所有实验记录均需指导教师确认批改，否则无效**；
6. 实验结束后需关闭实验台所有电源、整理实验台、清扫实验室。

**四、实验报告**
1. **实验报告统一提交**，没有按要求提交报告者不得成绩，**抄袭报告记 0 分**；
2. 为环保，**实验报告双面打印**。

**五、其他**
1. **上课必须携带实验报告和教材：《电工学实验教程第2版》，高等教育出版社，刘凤春主编。**
   **强电实验，为规范实验操作，不带教材不允许进实验室。**

## p03｜GENERAL LABORATORY SAFETY RULES（英文安全规则）
与 p02 的"三、实验课上要求"同源，英文版共 16 条。要点：禁止饮食/吸烟；必须穿包脚鞋；进入实验室前须熟悉灭火器、急救箱、应急断电开关与疏散通道；
**没有教师在场不得操作**；通电前须由 TA 检查接线并经同组同学确认；**50 V 交流／50 V 直流以上均属危险电压**；改接线路前必须先断电并断开电源连线；
不得使用破损导线；发现设备异常立即报告并停用。

## p04｜"2. DC Circuit Experiment" 第 1 页 —— I. Preliminary Work
- 要求：读教材 **Section 2.1**；课前按所有实验项目**画出电路图**；按需**准备表格**或剪贴教材上可剪的表格；学习**万用表、直流电压表、直流电流表**的用法（第 8 章）；
  学习**直流稳压电源与电流源**的操作。并回答 4 个问题：
  1. 基尔霍夫定律与元件的**线性/非线性**性质有关吗？**叠加定理**呢？
  2. 电压源**不用时**应如何存放：开路还是短路？电流源呢？
  3. 测电压时，电压表应与被测支路**串联还是并联**？接反会有什么后果？
  4. **相对误差**怎么算？既然实际测量中拿不到"真值"，相对误差应如何计算？

## p05｜第 2 页 —— II. Experimental Procedure / 1. Verification of Kirchhoff's Laws
- 读教材 Section 2.1.4；**画出实验原理图（须标注元件参数值）** → `Figure 2.1.1 a) Experimental Circuit`（照片中为空白，待在册上或报告上画）
- **(1) 测量电阻值（测量数据保留一位小数）** → `Table 2.1.2 Resistance-measurement Data`：列为 R₁…R₇，行为 `Nominal Value/Ω`、`Measured Value/Ω`、`Relative Error`
- **(2) 验证基尔霍夫定律**（画表或剪贴教材表格）：`Experimental conditions: U_S1 = ___ V, U_S2 = ___ V` → `Table 2.1.3 Data Record for Verification of Kirchhoff's Laws`（保留一位小数）

## p06｜第 3 页 —— 2. 叠加定理 / 3. 电源等效变换
- **2. Verification of the Superposition Theorem**：读 Section 2.1.4；`U_S1 = ___ V, U_S2 = ___ V`
  - (1) 验证叠加定理 → `Table 2.1.4 Data Record for Superposition Theorem Experiment`
  - (2) **把 R₃ 换成 1N4007 二极管**，选一个电压或电流参量测量，检验叠加定理是否仍成立（保留一位小数）
- **3. Verification of Equivalent-transformation Conditions for Voltage Sources and Current Sources**
  —— **课前**按教材 **Section 3.1** 自行设计实验电路、数据表格与测试步骤（逐条）

## p07｜第 4 页 —— 记录三栏（空白待填）
(1) Experimental schematic diagram (specify component parameter values) ／ (2) Brief description of experimental procedures ／ (3) Experimental data recording

## p08｜第 5 页 —— Discussion of Results
- 总要求：**凡计算题都要写出公式并代入数值**（适用于所有实验）
1. 用表 2.1.3 的计算值与测量值**算相对误差**并填入表 2.1.3；
2. 在原理图中**选一个节点**，用表 2.1.3 的数据**验证 KCL**；
3. 从表 2.1.4 取**一组数据**，计算检验**叠加性与齐性**是否满足；
4. 从表 2.1.4 取一组数据，计算说明**电阻功率能否用叠加定理计算**；
5. **把 R₃ 换成二极管后，叠加定理还成立吗？**

---

## 实验3（AC Circuit）—— 2026-10-20 学习者补拍 3 张

> 来源：学习者 2026-10-20 补拍（此前工作区**只有** p01–p08，全是实验2 的 DC Circuit；实验3 页面确实缺失，上一版报告路线图因缺页而按实验2 骨架误推，已作废）。
> 三张已入库，**页码未统一编号**（页脚只见一个 "9"），故按内容命名：
> `册-实验3-01-接线与图2.3.3-表234-235.jpg`｜`册-实验3-02-启辉值与电压三角形.jpg`｜`册-实验3-03-Discussion-5问-页9.jpg`
> 读取状态：①已登记 ✅ ②无需渲染 ✅ ③内容已阅读 3/3 ✅ ④关键句已逐条转录 ✅（直读原图 + 旋转裁切局部复核）

### 实验3-01｜II. Experimental Procedure 起页 + 图 2.3.3

- `II. Experimental Procedure` → `1. Wiring and Measurement of a Fluorescent-lamp Circuit`
- `Read Section 2.3.5 of the textbook and complete the following experiment.`
- `Draw the experimental schematic diagram.`（**学习者已手绘**：调压器 L1/L2/L3/N → 过流保护 → S₁ → 镇流器 → 灯管＋启辉器 S；电容支路带多个投切开关）
- `Figure 2.3.3 Schematic Diagram of Fluorescent Lamp Circuit`
- `(1) Wire the fluorescent-lamp circuit according to the schematic. **Do not turn on the power yourself!!** Check the circuit yourself first, then ask the teacher to turn on the power. Measure and record data into Table 2.3.4 and Table 2.3.5.`

> ⚠ 本页两条硬规则：**①不许自己合闸，须自查后请老师合闸；②数据填表 2.3.4 与表 2.3.5**。本页**没有**表 2.3.3，也没有三表法内容。

### 实验3-02｜启辉电压 + 电压三角形

- `(2) Determination of the ignition voltage in fluorescent lamp circuit.`
- `Operate as described on Page 36 of the textbook. Record the ignition voltage: ______ V.`
- `2. Experimental Verification of Voltage-triangle Relationships`
- `Draw your designed circuit diagram and data-recording table, and record experimental data.`

> ⚠ 册上写 `Page 36`，但教材第 2 版 **p.36 是 §2.3.3 原理页**，启辉值测定步骤在 **§2.3.5 第 3 条，书 p.39 = PDF p.52** —— 页码不一致。
> ⚠ II-2 是**设计要求**：电路图 + 数据记录表都要自己设计，不是抄教材表。

### 实验3-03｜Discussion of Results（页脚标 **9**，共 **5 问**）

1. `Calculate the power factor of the fluorescent lamp circuit using data from Table 2.3.4. Show your calculation process.`
2. `Complete power-factor calculations for Table 2.3.5.`
3. `According to data in Table 2.3.5: which physical quantities change as capacitance varies, and how do they change? Which quantities remain constant?`
4. `…total circuit current decreases until it reaches its minimum value. At this point the circuit is ______ (resistive / inductive / capacitive). When capacitance exceeds a certain value, the total circuit current ______ (rises / falls / remains unchanged), and the circuit becomes ______ (resistive / inductive / capacitive). According to Table 2.3.5, the power factor reaches its maximum value when the compensation capacitance is ______.`
5. `An old fluorescent-lamp circuit equipped with an inductive ballast(镇流器) and glow-starter(启辉器) is to be retrofitted into an LED lighting circuit. Answer the following questions:`
   `(1) Does an LED lighting circuit require a ballast or a glow-starter?`
   `(2) How should the original ballast and glow-starter be handled during retrofitting? What extra component is required?`

> ⚠ **册上只有 5 问，与教材 §2.3.6 的 6 问不同**：没有"用数据验证相量关系"那一问（它变成 II-2 的独立设计实验）；第 5 问 **LED 改造教材完全没有**，只能自己作答。

### 仍缺的页

- **`I. Preliminary Work`（实验3 预习页）未拍到。** 实验2 的对应页是 p04（读 Section 2.1 + 画图 + 准备表格 + 答 4 问）；实验3 应有一页同构内容，直接决定预习分与"无预习报告不得做实验"的门槛。

---

## 与今天（实验1）的关系

- **p04–p08 属于"2. DC Circuit Experiment"＝实验2（2026-10-13，15:30–17:45，117）**，**不是今天的内容**。
  但它们是**实验2 的预习任务**（Preliminary Work 四问 + 画图 + 设计等效变换方案），可提前准备。
- **今天（实验1，Multisim 仿真）**用的是电子版 docx（见 `../INDEX.md` 第三节），纸质册只提供：
  成绩栏 + "电子报告打印后与册子一同提交"这句提示 + 通用规则（上课须知）。
- **[待确认]** 册子里 `1. Multisim Simulation Experiment` 一节的位置与页数；以及它是否另要求"预习报告"格式。
