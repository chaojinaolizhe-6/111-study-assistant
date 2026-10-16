# 电工电子技术 课件 · AI 可读层

> 生成方式：MinerU hybrid-engine（本地 GPU 版面解析）→ 本脚本组装　生成日期：2026-10-16
> 覆盖：12 册 / 547 页（物理页全覆盖）/ 401 处版面图区；504 页已附 AI 视觉通读图区描述
> 小节归属：533/547 页有小节号（其中 169 页是课件自己印了小节标题，其余按页序向前传播）
> 正文规模：≈45,788 tokens（整库）；含例题/习题标记的页 44 页

## 这是什么

老师的电工学课件是 PPT 导出的 PDF：**电路图、波形图、特性曲线全是位图**，
纯文字层取不到，而图恰恰是这门课的全部信息。这一层把每页拆成
「可检索正文（公式为 LaTeX）+ 图上标注 + 整页扫描图 + 图区 AI 视觉通读」，
让网页 AI 不必打开 PDF 就能读到页码级的内容，并能把每一句话回指到 `[课件-页码]`。

## 读取顺序（AI 用）

1. `index/INDEX.md`（本文件）→ 知道有哪些册、哪些页、怎么取。
2. `index/manifest.json` → 每册页数 / 源文件 sha256 / 统计（判断完整性）。
3. **按需取页**，不要整库读入：
   - 云端 AI：抓 `text/<deck>-p###.md` 单页（约 0.3–1 KB），或用
     `media.githubusercontent.com` 抓 `assets/<deck>/p###.jpg`（LFS）。
   - 本地 AI：直接 `grep` `index/pages.jsonl` 定位页码，再读对应 `text/*.md`
     和 `assets/*/p###.jpg`；需要整章上下文时读 `chapters/<deck>.md`。

## 页码引用规范

正文里写 `[C3-2 p14]` 就唯一指向 `Chapter Three-2-2026中白上传.pdf` 第 14 页。
物理页号 == PPT 页码 == `assets` 里的文件名编号，三者一致，不会有印刷页码偏移问题。

## 一行一页的机器可读索引

`index/pages.jsonl` 每行一个 JSON 对象，字段：

| 字段 | 含义 |
|---|---|
| `deck` / `page` | 课件 id（C1-1…C4-3）与物理页号 |
| `source` | 原始 PDF 路径（仓库内相对路径） |
| `section_no` / `section` | 该页命中的小节号与 running head 标题 |
| `title` | 页面标题（MinerU 标题层级或首个文本框） |
| `exercise` / `exercise_label` | 是否例题/习题页，及题号（如 E1） |
| `kinds` | 各类块计数：text / equation / image / table |
| `text` | 该页正文（含 LaTeX 公式，与 `text/*.md` 同源） |
| `noise` | 已剔除的母版噪声（水印、页码等） |
| `tokens_est` | 正文 token 估算，便于挑选阅读预算 |
| `page_image` | 整页扫描图（LFS，用 media URL 取） |
| `figures` | 该页 MinerU 判定的图区数量（0 表示纯文字页） |
| `figure_description` | 图区 AI 视觉通读（电路拓扑/波形/曲线读法），可能为空 |
| `md` | 对应的逐页 markdown |

## 目录结构

| 路径 | 内容 |
|---|---|
| `index/INDEX.md` | 本文件：导航与用法 |
| `index/manifest.json` | 构建元数据与统计 |
| `index/pages.jsonl` | 一行一页的机器可读索引 |
| `chapters/<deck>.md` | 整册串读全文（含目录表） |
| `text/<deck>-p###.md` | 逐页正文（最长被引用单元） |
| `assets/<deck>/p###.jpg` | 整页扫描图（150 dpi，版面事实的最终依据；**不另存图区裁切**） |

## 事实边界（重要）

- 这一层是**课件的忠实转写**，不是讲义、不是答案。图区描述里凡属推断的读法，
  写在「读图要点」中，供教学核对，**不能当作已经学会的证据**。
- 公式来自 MinerU 的版面识别；若与 `assets/<deck>/p###.jpg` 不一致，
  **以页面图为准**，并把差异记进 `subjects/06-电工电子技术/课件/INDEX.md`。
- 页码级覆盖 = 全部页；内容级理解仍需按页核对，课件上的手写补充、口头说明不在本层内。

---

## 分册一览

| 课件 id | 页数 | 源文件（原件不在仓库，见课件 INDEX） | 整册串读 |
|---|---|---|---|
| `C1-1` | 60 | `Chapter one -1-2026中白上传.pdf` | `chapters/C1-1.md` |
| `C1-2` | 45 | `Chapter One -2-2026中白上传.pdf` | `chapters/C1-2.md` |
| `C1-3` | 67 | `Chapter One -3-2026中白上传.pdf` | `chapters/C1-3.md` |
| `C1-4` | 45 | `Chapter One -4-2026中白上传.pdf` | `chapters/C1-4.md` |
| `C2-1` | 43 | `Chapter Two-1-2026中白上传.pdf` | `chapters/C2-1.md` |
| `C2-2` | 27 | `Chapter Two-2-2026中白上传.pdf` | `chapters/C2-2.md` |
| `C3-1` | 69 | `Chapter Three-1-2026中白上传.pdf` | `chapters/C3-1.md` |
| `C3-2` | 49 | `Chapter Three-2-2026中白上传.pdf` | `chapters/C3-2.md` |
| `C3-3` | 38 | `Chapter Three-3-2026中白上传.pdf` | `chapters/C3-3.md` |
| `C4-1` | 39 | `Chapter Four-1-2026中白上传.pdf` | `chapters/C4-1.md` |
| `C4-2` | 35 | `Chapter Four-2-2026中白上传.pdf` | `chapters/C4-2.md` |
| `C4-3` | 30 | `Chapter Four-3-2026中白上传.pdf` | `chapters/C4-3.md` |

## 逐页去向

| 课件 | 逐页正文 | 整页扫描图 |
|---|---|---|
| `C1-1` | `text/C1-1-p001.md` … `-p060.md` | `assets/C1-1/p001.jpg` … `p060.jpg` |
| `C1-2` | `text/C1-2-p001.md` … `-p045.md` | `assets/C1-2/p001.jpg` … `p045.jpg` |
| `C1-3` | `text/C1-3-p001.md` … `-p067.md` | `assets/C1-3/p001.jpg` … `p067.jpg` |
| `C1-4` | `text/C1-4-p001.md` … `-p045.md` | `assets/C1-4/p001.jpg` … `p045.jpg` |
| `C2-1` | `text/C2-1-p001.md` … `-p043.md` | `assets/C2-1/p001.jpg` … `p043.jpg` |
| `C2-2` | `text/C2-2-p001.md` … `-p027.md` | `assets/C2-2/p001.jpg` … `p027.jpg` |
| `C3-1` | `text/C3-1-p001.md` … `-p069.md` | `assets/C3-1/p001.jpg` … `p069.jpg` |
| `C3-2` | `text/C3-2-p001.md` … `-p049.md` | `assets/C3-2/p001.jpg` … `p049.jpg` |
| `C3-3` | `text/C3-3-p001.md` … `-p038.md` | `assets/C3-3/p001.jpg` … `p038.jpg` |
| `C4-1` | `text/C4-1-p001.md` … `-p039.md` | `assets/C4-1/p001.jpg` … `p039.jpg` |
| `C4-2` | `text/C4-2-p001.md` … `-p035.md` | `assets/C4-2/p001.jpg` … `p035.jpg` |
| `C4-3` | `text/C4-3-p001.md` … `-p030.md` | `assets/C4-3/p001.jpg` … `p030.jpg` |

## 页码 → 小节 快查（按课件分节）

### C1-1 第一章 直流电路（一）

| 小节 | 页范围 | 页数 |
|---|---|---|
| （未标注小节） | p1 | 1 |
| 1.1 1.1 Function and components | p2 | 1 |
| 1.1 1.1 Functions and Compositions | p3–p16 | 14 |
| 1.4 1.4 Reference point and reference direction | p17–p23 | 7 |
| 1.4.2 1.4.2 Reference direction | p24–p60 | 37 |

### C1-2 第一章 直流电路（二）

| 小节 | 页范围 | 页数 |
|---|---|---|
| （未标注小节） | p1–p13 | 13 |
| 1.6.1 1.6.1 Practical voltage source | p14–p16 | 3 |
| 1.6 1.6 Practical sources | p17–p45 | 29 |

### C1-3 第一章 直流电路（三）

| 小节 | 页范围 | 页数 |
|---|---|---|
| 1.6 1.6 Practical source | p1–p14 | 14 |
| 1.7 1.7 Kirchhoff’s Laws | p15–p67 | 53 |

### C1-4 第一章 直流电路（四）

| 小节 | 页范围 | 页数 |
|---|---|---|
| 1.9 1.9 Superposition theorem | p1–p21 | 21 |
| 1.10.1 1.10.1 Basic idea | p22–p23 | 2 |
| 1.10 1.10 Equivalent Source Theorem | p24–p45 | 22 |

### C2-1 第二章 正弦交流电路（一）

| 小节 | 页范围 | 页数 |
|---|---|---|
| 2.1 2.1 Basic concept | p1–p5 | 5 |
| 2.1.2 2.1.2 Expression of AC | p6 | 1 |
| 2.1 2.1 Basic concept | p7–p12 | 6 |
| 2.2 2.2 Phasor representation 2.2.1 Phasor representation of sine wave | p13 | 1 |
| 2.2.1 2.2.1 Phasor representation of sine wave | p14–p23 | 10 |
| 2.2 2.2 Phasor representation 2.2.2 Phasor representation of sinusoidal AC | p24 | 1 |
| 2.2.2 2.2.2 Phasor representation of sinusoidal AC | p25–p43 | 19 |

### C2-2 第二章 正弦交流电路（二）

| 小节 | 页范围 | 页数 |
|---|---|---|
| 2.4.1 2.4.1 Series RLC circuits | p1–p3 | 3 |
| 2.4 2.4 Series AC circuits | p4 | 1 |
| 2.4.1 2.4.1 Series RLC circuits | p5–p6 | 2 |
| 2.4 2.4 Series AC circuits | p7–p8 | 2 |
| 2.4.2 2.4.2 Series impedance circuit | p9–p12 | 4 |
| 2.5.1 2.5.1 Parallel RLC Circuit | p13–p14 | 2 |
| 2.5.2 2.5.2 Parallel impedance circuit | p15 | 1 |
| 2.5 2.5 Parallel AC circuits | p16 | 1 |
| 2.5.2 2.5.2 Parallel impedance circuit | p17–p27 | 11 |

### C3-1 第三章 直流稳压电源（一）

| 小节 | 页范围 | 页数 |
|---|---|---|
| 3.1 3.1 Basic Knowledge of Semiconductor | p1–p8 | 8 |
| 3.1.2 3.1.2 Intrinsic semiconductor | p9–p17 | 9 |
| 3.1.3 3.1.3 Extrinsic semiconductor | p18–p69 | 52 |

### C3-2 第三章 直流稳压电源（二）

| 小节 | 页范围 | 页数 |
|---|---|---|
| 3.3 3.3 DC Regulated Power Supply | p1–p8 | 8 |
| 3.3 3.3 DC Regulated Power Supply 3.3.2 Function of each part | p9–p12 | 4 |
| 3.4 3.4 Rectifier Circuit | p13–p49 | 37 |

### C3-3 第三章 直流稳压电源（三）

| 小节 | 页范围 | 页数 |
|---|---|---|
| 12.5 2．Given that $I _ { \mathrm { { o } } } { = } 5 0 \mathrm { { m A } }$ , Find $I _ { \math | p1–p7 | 7 |
| 3.5 3.5 Filter Circuit | p8–p14 | 7 |
| 3.6 3.6 Voltage regulator circuits | p15–p20 | 6 |
| 4.5 U_{\mathrm{Z1}} = 4.5\mathrm{V} | p21 | 1 |
| 3.6 3.6 Voltage regulator circuits | p22–p23 | 2 |
| 3.6.1 3.6.1 zener voltage regulator | p24 | 1 |
| 3.6 3.6 Voltage regulator circuits | p25–p38 | 14 |

### C4-1 第四章 基本放大电路（一）

| 小节 | 页范围 | 页数 |
|---|---|---|
| 4.1 4.1 Bipolar Junction Transistor | p1 | 1 |
| 4.1 4.1 Bipolar Junction Transistor 4.1.1 Basic concept | p2–p3 | 2 |
| 4.1 4.1 Bipolar Junction Transistor | p4–p5 | 2 |
| 4.1 （此位置版面为图表：4.1 Bipolar Junction Transistor 4.1.1 Basic concept） | p6–p7 | 2 |
| 4.1 （此位置版面为图：4.1 Bipolar Junction Transistor 4.1.1 Basic concept） | p8 | 1 |
| 4.1 4.1 Bipolar Junction Transistor | p9–p19 | 11 |
| 8.6 I_{\mathrm{C}} = \beta I_{\mathrm{B}} = 100\times 8.6 = 0.86\mathrm{mA} | p20 | 1 |
| 8.6 I_{\mathrm{C}} = \beta I_{\mathrm{B}} = 100\times 86 = 8.6\mathrm{mA} | p21 | 1 |
| 4.1 4.1 Bipolar Junction Transistor | p22–p39 | 18 |

### C4-2 第四章 基本放大电路（二）

| 小节 | 页范围 | 页数 |
|---|---|---|
| 4.1 4.1 Bipolar Junction Transistor | p1 | 1 |
| 4.1 4.1 Bipolar Junction Transistor 4.1.3 Characteristic curves | p2–p7 | 6 |
| 4.1 4.1 Bipolar Junction Transistor 4.1.4 Main parameters | p8–p10 | 3 |
| 4.2 4.2 Principle of amplifier circuit | p11–p12 | 2 |
| 4.2 4.2 Principle of amplification circuit 4.2.1 Circuit development | p13 | 1 |
| 4.2 4.2 Principle of amplification circuit 4.2.2 Letter symbols | p14 | 1 |
| 4.2.3 4.2.3 Signal amplification process | p15–p20 | 6 |
| 4.3 4.3 Static analysis | p21–p23 | 3 |
| 4.3.2 4.3.2 Importance of static analysis | p24–p35 | 12 |

### C4-3 第四章 基本放大电路（三）

| 小节 | 页范围 | 页数 |
|---|---|---|
| 4.4 4.4 Dynamic analysis | p1–p5 | 5 |
| 4.4.1 4.4.1 Main performance indicators | p6–p11 | 6 |
| 4.4 4.4 Dynamic analysis | p12–p13 | 2 |
| 4.4.2 4.4.2 Small signal equivalent circuit | p14 | 1 |
| 4.4 4.4 Dynamic analysis | p15 | 1 |
| 4.4.2 4.4.2 Small signal equivalent circuit | p16–p19 | 4 |
| 4.4 4.4 Dynamic analysis | p20–p23 | 4 |
| 4.4.2 4.4.2 Small signal equivalent circuit | p24 | 1 |
| 4.4 4.4 Dynamic analysis | p25–p30 | 6 |

## 例题 / 习题页清单

共 44 页带例题或习题标记（`exercise: true`）。

| 课件 | 页 | 题号 | 标题 |
|---|---|---|---|
| `C1-1` | p9 |  | The circuit mainly consists of three parts: |
| `C1-1` | p23 |  | How to determine the reference direction? |
| `C1-1` | p24 |  | 1.4.2 Reference direction |
| `C1-1` | p25 |  | How to determine the reference direction? |
| `C1-2` | p2 |  | Potential |
| `C1-2` | p3 |  | Potential |
| `C1-2` | p22 | E1 |  |
| `C1-2` | p24 | E1 |  |
| `C1-3` | p24 | E2 | 1.7 Kirchhoff’s Laws |
| `C1-4` | p12 | E1 | 1.9 Superposition theorem |
| `C1-4` | p16 | E2 | 1.9 Superposition theorem |
| `C1-4` | p17 |  | 1.9 Superposition theorem |
| `C1-4` | p19 | E3 | E3 |
| `C1-4` | p20 | E4 | I 1Ω 1Ω 4Ω + + 18V -<sup>9V</sup> |
| `C1-4` | p21 | E5 | 1.9 Superposition theorem |
| `C2-1` | p23 | E1 | 2.2.1 Phasor representation of sine wave |
| `C2-2` | p7 | E1 | 2.4 Series AC circuits |
| `C2-2` | p8 | E2 | Examples |
| `C2-2` | p11 | E3 | E3 |
| `C2-2` | p14 |  | Example |
| `C2-2` | p17 | E1 | 2.5.2 Parallel impedance circuit |
| `C2-2` | p18 | E2 | E2 Judge how the voltmeter reading should change if $f _ { n |
| `C2-2` | p19 | E3 | E3 Judge how the brightness of the lamp changes if f ↑. |
| `C2-2` | p20 | E4 | Two methods: |
| `C2-2` | p21 | E4 | E4 Given that $U = 2 2 0 ~ \mathrm { V } , ~ R _ { 1 } = 2 0 |
| `C2-2` | p22 | E4 | E4 Given that $U = 2 2 0 ~ \mathrm { V } , ~ R _ { 1 } = 2 0 |
| `C2-2` | p23 |  | R1 Given that, $X _ { \mathrm { L } } { = } 1 6 \Omega , ／ \ |
| `C3-3` | p1 |  | 1．Find the maximum reverse voltage of the Diode（ ）. a． 0 b $ |
| `C3-3` | p8 | E1 | 3.5 Filter Circuit |
| `C3-3` | p9 | E1 | 3.5 Filter Circuit |
| `C3-3` | p10 | E1 | 大连理工大学 电气工程学院 |
| `C3-3` | p11 | E1 | 3.5 Filter Circuit |
| `C3-3` | p21 |  | 4. Example 1 |
| `C3-3` | p22 |  | 3.6 Voltage regulator circuits |
| `C3-3` | p23 |  | 3.6 Voltage regulator circuits |
| `C3-3` | p24 |  | 3.6.1 zener voltage regulator |
| `C3-3` | p25 |  | 3.6 Voltage regulator circuits |
| `C4-1` | p11 |  | 4.1 Bipolar Junction Transistor |
| `C4-1` | p20 | E1 | E1 |
| `C4-1` | p21 | E1 | E1 |
| `C4-1` | p23 | E2 | 4.1 Bipolar Junction Transistor |
| `C4-1` | p24 | E3 | 4.1 Bipolar Junction Transistor |
| `C4-1` | p25 | E4 | 4.1 Bipolar Junction Transistor |
| `C4-2` | p20 | E1 | 4.2.3 Signal amplification process |
