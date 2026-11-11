# round-04 阅读路径与版面检查记录

本文件记录 DSH 在 round-04 实际执行的 V8 单项分页返工、页面定位检查与渲染情况。它不是学习者试读报告，也不是外部目视验收结论。round-03 的完整记录保留在 `../round-03/reading-layout-check.md`；本文件保留其已通过结论，不覆盖、不回退。

## 1. 允许使用的基础（沿用，未变）

按 `learner-background.json` 与用户自述，本轮仍只采用：

- 会写矢量分量、做点乘与叉乘、做矩阵乘矢量、取转置；
- 知道“导数是改变量除以时间的极限”“积分是把物体切成小块再相加”这两句话；
- 不假定换基、线性映射、二次型、谱定理、张量、多重线性、并矢、微分方程解法或刚体动力学已熟练。

本轮没有新增前置、没有改写讲解，也没有因为返工而调整阅读门槛。

## 2. 本轮实际修改（只动 V8）

| 问题 | 原状 | 本轮处理 | 检查方式 |
|---|---|---|---|
| V8 | P11 在 p43 开始，p43 页底算完 SᵀS=1 并由 SSᵀ=1 确认正交性；p44 直接以“(c) 求导”开头，没有 P11 续页标识。旧续解标记落在 p43 中部，题设 φ=αt 与 c/s 记号留在前页。 | 删除 p43 中部的旧标记；在“同理 SSᵀ=1…”之后、“(c) 求导”之前放入新的 `\answercontinue{P11}`。续页首块为“P11 续解”，并重述：题设仍是绕 e₃ 转 φ=αt；上页已确认 SᵀS=SSᵀ=1；本页做 (c) 求导，记 c=cos αt、s=sin αt。 | `verify.py` 的 7 条 V8 页位/续页断言；PDF 文字层 p43/p44；`layout-report.txt`；`page-boundary-check.json` |

未改 READ-01/02、M2--M8、S1--S3、R2-READ02、R2-S3、R2-M3、V6、V7 的已通过内容；未改主题、题干、数字、图 1--8、推导与附录 A--C 的其余部分。`round03-vs-round04.diff.txt` 只有导言区主题路径 2.2.1→2.2.2（两份 theme 文件字节相同）与 P11 续解标记的删除/新增。

## 3. 保留的已通过结论（round-03 及以前）

- round-03 的数学报告与阅读内容经 `review-round03.json` 判定通过；本轮不重做整套验算，只保留既有数值/结构断言。
- V6：图 2 与两行关键图注同在 p15；V7：P4 续解在 p40 页首，重列 n、J、I(n)=145/18 与验证目标 ω·L=2K。两者在本轮最终 PDF 中未变。
- P9 仍在 p42 一页内完成，无续解标记；P1--P12 题干、考点与附录详解的配对未变。
- §8 速查与三句话总结、§6.4 均匀应力说明、P9 的 J′=mA 归一化说明保持 round-03 已通过措辞。

## 4. 主线阅读路径（未变）

主线顺序未变：§0.1 矢量 → §0.2 线性映射 → §0.3 矩阵账本 → §0.4 换基 → §0.5 迹/行列式/特征多项式 → §1 二次型/谱定理 → §2 张量与并矢 → §3 旋转算子 → §4 惯量张量 → §5 欧拉方程/对称陀螺 → §6 应力张量 → §7 P1--P12 → 附录 A。

本轮只需复查 P11 及其后的实际断页：

1. **p43 末尾**：P11 详解从 p43 中部开始；页底以“同理 SSᵀ=1，所以 S 是正交算子（§3.3）”结束。读者合上 p43 时已经完成 (b) 的正交性核验。
2. **p44 页首**：第一块是“P11 续解”，紧接着一行灰字重述题设 φ=αt、上页已确认 SᵀS=SSᵀ=1、本页做 (c) 求导，并重列 c=cos αt、s=sin αt。读者不翻回 p43 也能认出题号、题设、记号与当前步骤。
3. **p44 其余部分**：(c) 求导、Ω=αe₃ 与 P12 详解依次接排；P12 仍完整落在 p44，没有产生新的跨页详解，因此不需要额外的 P12 续解标记。
4. **p45/p46**：附录 B、附录 C 仍分别在 p45、p46 开始；P11 的改动没有把后文推后一页。

## 5. 版面与页位检查（最终 48 页）

- PDF 共 **48 页**，与 round-03 相同；P11 续解移动没有造成页数变化。
- 章节标题页：§0 p1/p2，§1 p8，§2 p13，§3 p20，§4 p23，§5 p27，§6 p30，§7 p33，§8 p36，附录 A p38，附录 B p45，附录 C p46。
- 标题孤行检查：未发现“标题后同页正文不足 60 字”的章节标题。
- 练习与详解：P1 p38、P2/P3/P4 p39、P5/P6 p40、P7/P8 p41、P9 p42、P10 p43、P11 p43（续解 p44）、P12 p44。
- 续解页位：P4 p40 页首、P11 p44 页首；P2/P8/P10 仍在其详解同页中部（round-02 起已知，本轮未扩大改动）；P9 一页完成，无续解标记。
- 练习跳转：正文 12 条“详解见附录第 N 页”与附录实际页逐条一致（P1 38、P2 39、P3 39、P4 39、P5 40、P6 40、P7 41、P8 41、P9 42、P10 43、P11 44、P12 44），由两遍编译后的 `\pageref` 自动更新，`verify.py` 核对通过。
- 页边：`check_margins.py` 对 48 页 PNG 检查，flagged 0。
- 编译：两遍 `xelatex -halt-on-error -interaction=nonstopmode`，退出码 0；`handout.log` 中 Overfull=0、Underfull=0、Missing character=0、undefined=0、multiply defined=0。
- 静态检查：`check_handout.py --mode appendix --log handout.log`（2.2.2），错误 0、人工复核线索 0。
- 数值/结构：`verify.py` 通过 321 条、失败 0 条；其中 V8 的 7 条检查覆盖续解页、页首首块、φ=αt、c/s、当前步骤、旧标记移除、P12 与附录 B/C 页位。
- `page-boundary-check.json` 记录：p43 首“P10详解”、尾“同理 ST S=ˆ1，所以 S 是正交算子”；p44 首“P11续解”、尾 P12 的核对句；P11 续解页与详解页分别为 44/43。

### 5.1 分页变化

总页数 **48 → 48**，无顺延。唯一变化是 P11 续解块从 p43 中部移到 p44 页首；P12、附录 B、附录 C 的起始页均未变。未压缩字号、未删推导、未把长题强行压成一页。

## 6. 渲染与目视边界

- `render_pages.py` 用 PyMuPDF 以 150 dpi 渲染 **48 页**到 `render/page-01.png` … `render/page-48.png`，并生成 `render/contact-1.png` … `contact-4.png` 四张联系表。
- 当前模型 **不支持图像输入**（已确认，不再尝试调用看图工具）。因此没有目视检查字体、灰字对比、重叠、图内标号或 p44 页首的视觉留白；上述页面结论均来自 PDF 文字层、span/block bbox、坐标与页位检查。
- **尚未目视验收**：不能把编译通过、bbox 同页或页首断言称为“目视通过”。需要支持图像输入的审核者查看 `render/` 后再确认 P11 续页页首与 P12 页底。

## 7. 复现命令

```powershell
cd round-04
xelatex -halt-on-error -interaction=nonstopmode handout.tex   # compile-pass1.log
xelatex -halt-on-error -interaction=nonstopmode handout.tex   # compile-pass2.log
python -B build_source_map.py
python -B render_pages.py
python -B check_margins.py
python -B layout_check.py
python -B verify.py
python -B ..\rule-versions\2.2.2\lecture-deepdive\scripts\check_handout.py handout.tex --mode appendix --log handout.log
```

## 8. 未验证项

- 学习者实际试读尚未发生；本记录只说明“阅读支持已按 V8 复查”，不说明学习者已理解或已掌握。
- 外部目视审核尚未进行；`render/` 已保存，等待支持看图的审核者。
- P2/P8/P10 的续解标题仍在同页中部；本轮只按 V8 移动 P11，未扩大改动，也没有声称这三处已修复。
- 数学公式未改，未重做整套数值验算；`verify.py` 只新增 V8 页位检查，既有数值断言沿用 round-03。
- 图 2、图 6、图 8 的几何与视觉对应沿用 round-03 已通过的检查结果，本轮未重看图。
