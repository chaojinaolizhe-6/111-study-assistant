# 第七—八章精讲合集（构建目录）

这是《数学物理方法（II）第七—八章 精讲讲义》的源文件目录。成品在这里：

- `main.pdf`（本目录，103 页）
- `../第七八章-精讲合集-20261117.pdf`（讲义目录顶层的副本，讲义台账扫描的是这一份）

## 文件

| 文件 | 内容 |
|---|---|
| `main.tex` | 主文件：`\documentclass` 与五个 `\input` |
| `preamble.tex` | 统一导言区：主题、宏、页眉、三级标题样式 |
| `front.tex` | 封面、怎么用、全书主线图（图 0-1）、共用记号、目录 |
| `ch7.tex` | 第七章：§7.1 波动方程、§7.2 输运、§7.3 泊松、§7.4 定解条件、§7.5 速查、§7.6 总结 |
| `ch8.tex` | 第八章：§8.1 直角坐标、§8.2 极坐标、§8.3 柱坐标与贝塞尔 |
| `quickref.tex` | 全书速查：三种坐标对照、四组边界、定解条件判据、课件页码对照 |
| `practice.tex` | 练习 P1--P20 的题干与考点 |
| `answers.tex` | 附录 A--E：P1--P20 详解 |

## 重建

在**仓库根**依次运行（`build/` 里的脚本从各分册 tex 抽取并重编号）：

```powershell
python -B subjects/05-数学物理方法2/讲义/合集-第七八章-20261117/build/build_ch7.py
python -B subjects/05-数学物理方法2/讲义/合集-第七八章-20261117/build/build_ch8.py
python -B subjects/05-数学物理方法2/讲义/合集-第七八章-20261117/build/build_answers.py
cd subjects/05-数学物理方法2/讲义/合集-第七八章-20261117
xelatex -halt-on-error -interaction=nonstopmode main.tex
xelatex -halt-on-error -interaction=nonstopmode main.tex
```

`front.tex`、`quickref.tex`、`practice.tex`、`preamble.tex` 是手写文件，不由脚本生成；重跑脚本不会覆盖它们。

## 合并规则（改稿时先读）

- 节号按最新课件：§7.1--§7.4、§8.1--§8.3。分册的旧节号在 `build_*.py` 的 `*_REFS` 表里映射。
- 三级标题 `\hdrsub`，四级 `\subhdr`，组标题 `\grp`。
- 图号 `图 7-x` / `图 8-x`，表号 `表 8-x`；分册原编号在脚本的 refs 表里改。
- 同一知识点只完整讲一次：§8.1 的方法总表（8.1.1--8.1.5）取代了合册 §4.1 与 §4.6；$n=0$ 一项在 8.1.9、8.1.20 讲。
- 练习与详解分离：题干在 `practice.tex`，详解在 `answers.tex`，题号 P1--P20 一一对应。

## 已知遗留

- 图 8-5（§8.3 主线图）底部两个节点在原 8.3 分册里就有轻微溢出，本合集沿用了原图，未重绘。
- 公式编号全书连续（1--约 120），未按节重编；正文没有硬编码「式 (n)」的引用，所以不影响阅读。
