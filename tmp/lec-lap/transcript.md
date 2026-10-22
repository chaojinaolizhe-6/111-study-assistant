# 第六章 拉普拉斯变换 —— 课件逐页转写

> 来源：`subjects\04-数学物理方法1\课件\第六章+拉普拉斯变换+-+上传课件.pdf`（46 页，PowerPoint 导出）
> 转写方式：dpi=110 渲染成 PNG 后逐页多模态直读公式；中文措辞以文字层（`read_slides.py`）为底本核对。
> 符号约定：课件通篇用 $p$ 作拉氏变量（不用 $s$；$s$ 只在 p5 推导中作 $p=s-i\omega$ 的实部出现），角频率用 $\omega$，指数函数用 $e^{\alpha t}$ 记号。
> 另注：每页都带一条斜向水印「仅供学习…请勿上传任何网站」，非内容，下文不再重复。

---

## 全书结构

### 小节 → 页码区间

| 小节 | 页码区间 | 内容 |
| --- | --- | --- |
| 章封面 + 人物介绍 | p1–p2 | 章目录、拉普拉斯生平 |
| § 6.1 拉普拉斯变换的定义 | p3–p12 | 动机 → 推导 → 定义与存在条件 → 10 个基本变换 + 汇总表 |
| § 6.2 拉普拉斯变换的性质 | p13–p24 | 8 条定理（线性/导数 I/导数 II/积分/相似/位移/延迟/卷积）及配套例题 |
| 第六章作业（第 1 题） | p25 | 求三个函数的像函数 |
| § 6.3 拉普拉斯变换的反演 | p26–p34 | 反演三条思路 + 例 1–8 + 像函数积分定理 |
| § 6.4 拉普拉斯变换的应用 | p35–p45 | 1) 解微分方程与电路/振动（例 1–5，p35–p40）；2) 计算特殊积分（p41–p45，例 6–8） |
| 第六章作业（第 2、3 题） | p46 | 求反演 3 题 + 解常微分方程 4 题 |

### 逐页一句话摘要

- p1 → 第六章封面与四节目录（§6.1 定义 / §6.2 性质 / §6.3 反演 / §6.4 应用）。
- p2 → 拉普拉斯生平卡片（法国数学家，1749–1827，天体力学/拉氏变换/概率论）。
- p3 → §6.1 开篇：指出傅里叶变换「要求绝对可积」「要求 $(-\infty,\infty)$ 上分段光滑」两条局限，并提问「如何克服上述两个局限」。
- p4 → 给出两条改造手段：乘指数衰减函数 $e^{-st}(s>0)$ 压低增长，乘单位阶跃函数 $H(t)$ 把积分区间从 $[-\infty,\infty]$ 压到 $[0,\infty]$。
- p5 → 由傅里叶变换（乘 $e^{-st}$ 后）腾挪出拉普拉斯变换 $F(p)=\int_0^\infty f(t)e^{-pt}dt$ 与黎曼-梅林反演公式。
- p6 → 正式给出拉氏变换定义、原函数/像函数/核 $e^{-pt}$ 与 $p=s+i\sigma$，并列出两条存在条件。
- p7 → 例1 $f(t)=1\Rightarrow 1/p$；例2 $f(t)=e^{\alpha t}\Rightarrow 1/(p-\alpha)$（要求 $\mathrm{Re}\,p>\mathrm{Re}\,\alpha$）。
- p8 → 例3 $f(t)=t^n$：先用分部积分（方法1）、再用「对 $p$ 求导穿积分号」（方法2）算 $n=1,2$，类推得 $n!/p^{n+1}$。
- p9 → 例4 $f(t)=te^{\alpha t}$：与 $1/p^2$ 对比得 $1/(p-\alpha)^2$，类推 $t^n e^{\alpha t}$。
- p10 → 例5 用欧拉公式把 $\sin\omega t,\cos\omega t$ 拆成两支复指数，得 $\omega/(p^2+\omega^2)$ 与 $p/(p^2+\omega^2)$。
- p11 → 例6 用双曲函数定义把 $\sinh\omega t,\cosh\omega t$ 拆开，得 $\omega/(p^2-\omega^2)$ 与 $p/(p^2-\omega^2)$。
- p12 → 「常见函数的拉普拉斯变换」汇总表（幂函数 3 条、指数函数 3 条、三角函数 4 条）。
- p13 → §6.2 开篇：线性定理 + 例1 用线性定理由 $e^{i\omega t}$ 重新得到 $\sin\omega t$ 的像。
- p14 → 导数定理 I：$f^{(1)}(t)\rightleftharpoons pF(p)-f(0)$ 的分部积分证明，并「推广」到 $n$ 阶。
- p15 → 例2 用导数定理 I 解二阶方程 $f''+\omega^2f=0$，初值 $f(0)=1,f^{(1)}=0$，得 $f(t)=\cos\omega t$。
- p16 → 导数定理 II：$t^nf(t)\rightleftharpoons(-1)^n\dfrac{d^nF(p)}{dp^n}$ 的证明。
- p17 → 例3 用导数定理 II 三次求导得 $t^ne^{\alpha t}\rightleftharpoons n!/(p-\alpha)^{n+1}$。
- p18 → 积分定理：$\int_0^t f(\tau)d\tau\rightleftharpoons\dfrac{1}{p}F(p)$，借 $g(t)$ 与导数定理证明。
- p19 → 相似性定理：$f(at)\rightleftharpoons\dfrac{1}{a}F(p/a)$（$a>0$）的换元证明，并补写 $a<0$ 时的换限。
- p20 → 例4 先按定义证 $e^t\rightleftharpoons 1/(p-1)$，再用相似性定理得 $e^{\alpha t}\rightleftharpoons 1/(p-\alpha)$，与直接计算一致。
- p21 → 位移定理：$e^{-\lambda t}f(t)\rightleftharpoons F(p+\lambda)$，并给出乘 $e^{-\lambda t}$ 后的 $\sin/\cos$ 像。
- p22 → 延迟定理：$f(t-t_0)\rightleftharpoons e^{-pt_0}F(p)$ 的换元证明（要求 $t\ge t_0$）。
- p23 → 卷积定理：$f_1*f_2\rightleftharpoons F_1(p)F_2(p)$，写出二重积分并画出 $t$-$\tau$ 平面的积分区域。
- p24 → 卷积定理证明续：交换积分次序 + 令 $\zeta=t-\tau$，分离成两个单积分的乘积。
- p25 → 第六章作业第 1 题：求 $te^{-\omega t}$、$t\cos\omega t$、$\dfrac{1-\cos\omega t}{\omega}$ 的像函数。
- p26 → §6.3 开篇：说明「反演」的含义，并给出三条化归思路（拆和、拆积、其它数学操作）。
- p27 → 例1 $1/[(p^2+a^2)(p^2+b^2)]$ 的部分分式拆分与反演。
- p28 → 例2、例3 用位移定理由 $\sin/\cos$ 直接读出 $e^{-\lambda t}\sin\omega t$、$e^{-\lambda t}\cos\omega t$ 两类反演。
- p29 → 例4 $1/[p(p-1)^2]$ 反演：部分分式法得 $1-e^t+te^t$，卷积法得同一结果。
- p30 → 例5 $-1/[p^2(p-1)]$ 反演：两种方法均得 $t+1-e^t$。
- p31 → 例6 $\omega/[(p+\alpha)(p^2+\omega^2)]$ 用卷积定理做积分，一路化到 $\dfrac{1}{\omega^2+\alpha^2}(\alpha\sin\omega t-\omega\cos\omega t+\omega e^{-\alpha t})$。
- p32 → 例7 $p/(p^2+\omega^2)^2$ 反演：对 $\omega$ 求导法 + 对 $p$ 求导（导数定理 II）法，两法同得 $\dfrac{t\sin\omega t}{2\omega}$。
- p33 → 例8 $\omega/(p^2+\omega^2)^2$ 反演：对 $\omega$ 求导，得 $-\dfrac{1}{2}\left(\dfrac{t\cos\omega t}{\omega}-\dfrac{\sin\omega t}{\omega^2}\right)$。
- p34 → 像函数的积分定理 $\int_p^\infty F(q)dq\rightleftharpoons f(t)/t$，并示例算 $\int_0^\infty\dfrac{\sin t}{t}dt=\pi/2$。
- p35 → §6.4 例1：LR 回路接通直流电源，$i(t)=\dfrac{E}{R}\left(1-e^{-Rt/L}\right)$，并标出稳恒部分与暂态部分。
- p36 → 例2：LC 回路放电，解出振荡电流 $i(t)=\dfrac{q_0}{\sqrt{LC}}\sin\dfrac{t}{\sqrt{LC}}$。
- p37 → 例3：LR 回路接交流电源 $E_0\sin\omega t$，用卷积定理得暂态电流 + 强迫振荡电流之和。
- p38 → 例4：弹簧振子受 $f_0\sin\omega t$ 强迫振动（$\omega\ne\omega_0$），得两个正弦的叠加。
- p39 → 例4 续：共振情形 $\omega=\omega_0$，得含 $t\cos\omega t$ 的线性增长解。
- p40 → 例5：用拉氏变换把二元微分方程组化成线性代数方程组，解得 $y=e^{2t},z=3e^{2t}$。
- p41 → §6.4 第 2 类应用开场：引高斯型积分公式，两边取拉氏变换，左边化为 $\int_0^\infty\dfrac{\cos(bx)}{x^2+p}dx$。
- p42 → 用留数定理算出 $\dfrac{1}{\sqrt{p}}e^{-b\sqrt{p}}\rightleftharpoons\dfrac{1}{\sqrt{\pi t}}e^{-b^2/(4t)}$，另有 $e^{-b\sqrt p}$ 的形式，注明「将在第十章用到」。
- p43 → 例6：$\int_0^\infty\dfrac{\cos(tx)}{x^2+a^2}dx=\dfrac{\pi}{2a}e^{-at}$。
- p44 → 例7：$\int_0^\infty\dfrac{\sin(tx)}{x}dx=\dfrac{\pi}{2}$。
- p45 → 例8：$\int_0^\infty\dfrac{\sin^2(tx)}{x^2}dx=\dfrac{\pi}{2}t$，令 $t=1$ 得 $\pi/2$。
- p46 → 第六章作业第 2、3 题：三个像函数求反演 + 四个常微分方程用拉氏变换求解。

---

## p1 ｜ 章封面·目录（§6.1–§6.4 总览）
- 标题行：第六章　拉普拉斯变换
- 中文要点：章目录四项——§ 6.1 拉普拉斯变换的定义；§ 6.2 拉普拉斯变换的性质；§ 6.3 拉普拉斯变换的反演；§ 6.4 拉普拉斯变换的应用。
- 公式：无公式。
- 例题/作业：无。
- 图：无（仅斜向灰色水印「仅供学习……请勿上传任何网站」）。
- ⚠️存疑：无。

## p2 ｜ 章前人物介绍（拉普拉斯）
- 标题行：Pierre-Simon Laplace
- 中文要点：中文名：皮埃尔-西蒙·拉普拉斯；国籍：法国；出生日期：1749年3月23日；逝世日期：1827年3月5日；职业：数学家；主要成就：天体力学、拉普拉斯变换、概率论；代表作品：《宇宙系统论》，《天体力学》。
- 公式：无公式。
- 例题/作业：无。
- 图：左侧一张拉普拉斯半身彩色画像（历史油画，戴白色领巾、挂勋章），右侧为上述要点列表。
- ⚠️存疑：无。

## p3 ｜ §6.1 定义·1 傅里叶变换的两条局限
- 标题行：§ 6.1 拉普拉斯变换的定义
- 中文要点：傅里叶变换的局限：（1）原函数 $f(x)$ 绝对可积，但许多简单的常见函数（如单位阶跃函数、正弦函数、余弦函数以及线性函数等）都不满足这个条件。（2）原函数 $f(x)$ 在区间 $[-\infty,\ \infty]$ 上分段光滑，但在物理和无线电技术等实际应用中，许多以时间 $t$ 作为自变量的函数往往在 $t<0$ 时是无意义的或是不需要考虑的。——页末红字提问：如何克服上述两个局限。
- 公式：
  - 无独立公式，只有区间记号 $[-\infty,\ \infty]$ 与条件 $t<0$。
- 例题/作业：无（页末是设问，不是例题）。
- 图：右下角一张装饰插图（红色大问号 + 抱臂思考的白色小人），非数学图。
- ⚠️存疑：无。

## p4 ｜ §6.1 定义·2 两项改造手段（指数衰减因子、单位阶跃函数）
- 标题行：（本节标题页之后的续页，页面最上方即正文，无独立大标题）
- 中文要点：对于许多在区间 $[-\infty,\ \infty]$ 不绝对可积的函数，往往是因为当 $t\to\infty$ 时，其绝对值收敛太慢的缘故。因此，可以用指数衰减函数 $e^{-st}\ (s>0)$ 去乘以函数 $f(t)$。／引入单位阶跃函数 $H(t)$；用 $H(t)$ 乘以 $f(t)$，这样得到的 $H(t)f(t)$，在 $t<0$ 时就等于零，在 $t>0$ 时仍为 $f(t)$，就有可能使其积分区间由 $[-\infty,\ \infty]$ 变为 $[0,\ \infty]$。
- 公式：
  - 收敛性判断的前提（行内）：当 $t\to\infty$ 时绝对值收敛太慢，故乘 $e^{-st}\ (s>0)$。
  - 单位阶跃函数的定义（本页核心公式）：
    $$H(t)=\begin{cases}1,& t\ge 0\\[2pt] 0,& t<0\end{cases}$$
  - 截断后的积分区间（结论性说明，原文用文字表述）：$[-\infty,\infty]\ \longrightarrow\ [0,\infty]$。
- 例题/作业：无。
- 图：无（纯文字页）。
- ⚠️存疑：无。

## p5 ｜ §6.1 定义·3 由傅里叶变换导出拉普拉斯变换（正变换 + 反演公式）
- 标题行：由傅里叶变换推导出拉普拉斯变换
- 中文要点：存在函数 $f(t)$，其中 $t\ge 0$；令 $g(t)=f(t)e^{-st}$，其中 $s>0$，且 $s$ 足够大，使得 $g(t)$ 绝对可积；先对 $g(t)$ 进行傅里叶变换；令 $p=s-i\omega$，且由于 $t\ge 0$，则……；令 $F(p)=2\pi G(\omega)$，则……；再进行逆变换；则……；由于 $dp=-i\,d\omega$，则……；右下红字标注「黎曼梅林反演公式」。
- 公式：
  1. 定义辅助函数（推导起点）：
     $$g(t)=f(t)e^{-st},\qquad s>0,\ t\ge 0$$
  2. 对 $g(t)$ 作傅里叶变换：
     $$G(\omega)=\frac{1}{2\pi}\int_{-\infty}^{\infty}g(t)e^{i\omega t}dt=\frac{1}{2\pi}\int_{-\infty}^{\infty}f(t)e^{-st}e^{i\omega t}dt$$
  3. 换元 $p=s-i\omega$，并利用 $t\ge 0$（已用 $H(t)$ 截断）：
     $$p=s-i\omega,\qquad G(\omega)=\frac{1}{2\pi}\int_{0}^{\infty}f(t)e^{-pt}dt$$
  4. **拉普拉斯变换（正变换）的定义式**（本页绿框，核心结论）：
     $$F(p)=2\pi G(\omega)\ \Longrightarrow\ \boxed{F(p)=\int_{0}^{\infty}f(t)e^{-pt}\,dt}$$
  5. 傅里叶逆变换（回代 $g(t)$）：
     $$g(t)=f(t)e^{-st}=\int_{-\infty}^{\infty}G(\omega)e^{-i\omega t}d\omega=\frac{1}{2\pi}\int_{-\infty}^{\infty}F(p)e^{-i\omega t}d\omega$$
  6. 两边乘 $e^{st}$：
     $$f(t)=\frac{1}{2\pi}\int_{-\infty}^{\infty}F(p)e^{st}e^{-i\omega t}d\omega=\frac{1}{2\pi}\int_{-\infty}^{\infty}F(p)e^{(s-i\omega)t}d\omega$$
  7. 换回 $p$（用 $dp=-i\,d\omega$，上下限随之互换）：
     $$f(t)=-\frac{1}{2\pi i}\int_{s+i\infty}^{s-i\infty}F(p)e^{pt}dp$$
  8. **黎曼-梅林反演公式**（右下绿框，核心结论，注意先把上下限翻正）：
     $$\boxed{f(t)=\frac{1}{2\pi i}\int_{s-i\infty}^{s+i\infty}F(p)e^{pt}\,dp}$$
- 例题/作业：无（纯推导页）。
- 图：无坐标图；两个绿框（正变换、反演公式）+ 一个蓝色箭头指向反演公式。
- ⚠️存疑：第 3 步「由于 $t\ge 0$」把 $\int_{-\infty}^{\infty}$ 换成 $\int_0^{\infty}$，图上确实写作 $\int_0^{\infty}$；但此步真正依据是 $f(t)=0\ (t<0)$，课件这一页没有写出来（见「跳步候选」）。

## p6 ｜ §6.1 定义·4 定义式、核、存在条件
- 标题行：拉普拉斯变换的定义为
- 中文要点：其中 $f(t)$ 是原函数，$F(p)$ 是像函数，$e^{-pt}$ 是积分变换的核，$p=s+i\sigma$ 为复数，且要求 $\mathrm{Re}\,p=s>0$。／说明（红字）：在上式的积分变换中，要求 $f(t)$ 在 $t<0$ 时刻的值为 $0$，即 $f(t)=0\ \ (t<0)$，这样才能保证上式的积分变换有意义。／拉普拉斯变换存在的条件：1）$f(t)$ 在区间 $0\le t<\infty$ 中是分段连续的，而且导数处处连续；2）存在正常数 $M>0$ 及 $s_0\ge 0$，使得对于任何 $t$ 值，有 $|f(t)|<Me^{s_0t}$ → $|g(t)|=\left|f(t)e^{-s_0t}\right|<M$ → $g(t)$ 绝对可积。
- 公式：
  1. 定义式（绿框，本页核心）：
     $$F(p)=\int_{0}^{\infty}f(t)e^{-pt}\,dt$$
  2. 核与复变量、收敛半平面：核 $=e^{-pt}$，$p=s+i\sigma$，要求 $\mathrm{Re}\,p=s>0$。
  3. 因果性要求：
     $$f(t)=0\quad (t<0)$$
  4. 存在条件（2）的增长限制（原页三个框用蓝箭头串成推理链）：
     $$|f(t)|<Me^{s_0t}\ \Longrightarrow\ |g(t)|=\left|f(t)e^{-s_0t}\right|<M\ \Longrightarrow\ g(t)\ \text{绝对可积}$$
- 例题/作业：无。
- 图：无坐标图；一条由三个绿框 + 两个蓝箭头构成的推理链。
- ⚠️存疑：本页写 $p=s+i\sigma$，而 p5 推导得 $p=s-i\omega$，两页不一致（$\sigma$ 与 $\omega$ 混用、$i$ 前符号相反）。图上字迹清晰，属课件内部不一致，不是渲染问题。另条件 1）写「导数处处连续」与「分段连续」并列，原文如此。

## p7 ｜ §6.1 定义·5 例1（$f=1$）与例2（$f=e^{\alpha t}$）
- 标题行：例1 求函数 $f(t)=1$ 的拉普拉斯变换
- 中文要点：解：按照拉普拉斯变换的定义，有……。／例2 求函数 $f(t)=e^{\alpha t}$ 的拉普拉斯变换；解：按照拉普拉斯变换的定义，有……，其中要求 $\mathrm{Re}\,p>\mathrm{Re}\,\alpha$。
- 公式：
  - 右上角贴的定义式（本页反复引用）：
    $$F(p)=\int_{0}^{\infty}f(t)e^{-pt}dt$$
  - 例1：
    $$F(p)=\int_{0}^{\infty}1\cdot e^{-pt}dt=-\frac{1}{p}\left.e^{-pt}\right|_{0}^{\infty}=\frac{1}{p}$$
    结论（绿框，蓝色箭头指入）：$1\rightleftharpoons\dfrac{1}{p}$
  - 例2：
    $$F(p)=\int_{0}^{\infty}e^{\alpha t}\cdot e^{-pt}dt=\int_{0}^{\infty}e^{-(p-\alpha)t}dt=\frac{1}{p-\alpha}$$
    收敛要求（右侧行内）：$\mathrm{Re}\,p>\mathrm{Re}\,\alpha$
    结论（绿框）：$e^{\alpha t}\rightleftharpoons\dfrac{1}{p-\alpha}$
- 例题/作业：例1、例2 均为「按定义计算」的示范题，页内已给完整解答（见上公式）。
- 图：无坐标图；两个绿结论框 + 蓝色箭头。
- ⚠️存疑：无。

## p8 ｜ §6.1 定义·6 例3（$f=t^n$，两种方法）
- 标题行：例3 求函数 $f(t)=t^n$ 的拉普拉斯变换
- 中文要点：解：按照拉普拉斯变换的定义……；当 $n=1$ 时，方法1……方法2……；当 $n=2$ 时，……；类推，有……。
- 公式：
  - 定义式（右上贴框）：$F(p)=\int_0^\infty f(t)e^{-pt}dt$
  - 起步式：$$F(p)=\int_{0}^{\infty}t^n\cdot e^{-pt}dt$$
  - $n=1$，方法1（分部积分，先凑 $de^{-pt}$）：
    $$F(p)=\int_{0}^{\infty}t\cdot e^{-pt}dt=-\frac{1}{p}\int_{0}^{\infty}t\,de^{-pt}=-\frac{1}{p}\left[\left.te^{-pt}\right|_{0}^{\infty}-\int_{0}^{\infty}e^{-pt}dt\right]=\frac{1}{p^{2}}$$
  - $n=1$，方法2（对参数 $p$ 求导穿过积分号）：
    $$F(p)=\int_{0}^{\infty}t\cdot e^{-pt}dt=-\frac{d}{dp}\int_{0}^{\infty}e^{-pt}dt=-\frac{d}{dp}\left(\frac{1}{p}\right)=\frac{1}{p^{2}}$$
    结论（绿框）：$t\rightleftharpoons\dfrac{1}{p^{2}}$
  - $n=2$（直接用方法2 的推广）：
    $$F(p)=\int_{0}^{\infty}t^{2}\cdot e^{-pt}dt=\frac{d^{2}}{dp^{2}}\int_{0}^{\infty}e^{-pt}dt=\frac{d^{2}}{dp^{2}}\left(\frac{1}{p}\right)=\frac{2}{p^{3}}$$
  - 类推的一般结论（绿框）：
    $$t^{n}\rightleftharpoons\frac{n!}{p^{\,n+1}}$$
- 例题/作业：例3 为示范题，页内给出两法完整解答（见上）。
- 图：无坐标图；两个绿结论框 + 蓝色箭头。
- ⚠️存疑：无。注意方法1 中 $-1/p$ 提到积分号外后，括号内第二项符号为 $-\int_0^{\infty}e^{-pt}dt$，图上清晰无误。

## p9 ｜ §6.1 定义·7 例4（$f=te^{\alpha t}$）
- 标题行：例4 求函数 $f(t)=te^{\alpha t}$ 的拉普拉斯变换
- 中文要点：解：按照拉普拉斯变换的定义……；对比 $\int_0^\infty t\cdot e^{-pt}dt=\dfrac{1}{p^2}$，则……；类推，有……。
- 公式：
  - 定义式（右上贴框）：$F(p)=\int_0^\infty f(t)e^{-pt}dt$
  - 主体计算（把 $\alpha$ 并入指数）：
    $$F(p)=\int_{0}^{\infty}te^{\alpha t}\cdot e^{-pt}dt=\int_{0}^{\infty}te^{-(p-\alpha)t}dt$$
  - 用于对比的已知结果：
    $$\int_{0}^{\infty}t\cdot e^{-pt}dt=\frac{1}{p^{2}}$$
  - 结论（本页核心）：
    $$F(p)=\int_{0}^{\infty}te^{-(p-\alpha)t}dt=\frac{1}{(p-\alpha)^{2}}$$
    绿框：$te^{\alpha t}\rightleftharpoons\dfrac{1}{(p-\alpha)^{2}}$
  - 类推的一般结论（绿框）：
    $$t^{n}e^{\alpha t}\rightleftharpoons\frac{n!}{(p-\alpha)^{n+1}}$$
- 例题/作业：例4 为示范题，页内给出解答（见上），关键手法是「把 $p-\alpha$ 整体当作 p8 里的 $p$」。
- 图：无坐标图；两个绿结论框 + 蓝色箭头。
- ⚠️存疑：无。

## p10 ｜ §6.1 定义·8 例5（$\sin\omega t$、$\cos\omega t$）
- 标题行：例5 求函数 $f(t)=\sin\omega t$，$\cos\omega t$ 的拉普拉斯变换
- 中文要点：解：按照拉普拉斯变换的定义，有……；类似地，有……。
- 公式：
  - 正弦（用 $\sin\omega t=\frac{1}{2i}(e^{i\omega t}-e^{-i\omega t})$ 拆两支）：
    $$\int_{0}^{\infty}\sin\omega t\,e^{-pt}dt=\frac{1}{2i}\int_{0}^{\infty}\left[e^{-(p-i\omega)t}-e^{-(p+i\omega)t}\right]dt=\frac{1}{2i}\left[\frac{1}{p-i\omega}-\frac{1}{p+i\omega}\right]=\frac{\omega}{p^{2}+\omega^{2}}$$
    绿框：$\sin\omega t\rightleftharpoons\dfrac{\omega}{p^{2}+\omega^{2}}$
  - 余弦（用 $\cos\omega t=\frac{1}{2}(e^{i\omega t}+e^{-i\omega t})$）：
    $$\int_{0}^{\infty}\cos\omega t\,e^{-pt}dt=\frac{1}{2}\int_{0}^{\infty}\left[e^{-(p-i\omega)t}+e^{-(p+i\omega)t}\right]dt=\frac{1}{2}\left[\frac{1}{p-i\omega}+\frac{1}{p+i\omega}\right]=\frac{p}{p^{2}+\omega^{2}}$$
    绿框：$\cos\omega t\rightleftharpoons\dfrac{p}{p^{2}+\omega^{2}}$
- 例题/作业：例5 为示范题，页内给出解答（见上）。
- 图：无坐标图；两个绿结论框 + 蓝色箭头。
- ⚠️存疑：无。

## p11 ｜ §6.1 定义·9 例6（$\sinh\omega t$、$\cosh\omega t$）
- 标题行：例6 求函数 $f(t)=\sinh\omega t$，$\cosh\omega t$ 的拉普拉斯变换
- 中文要点：解：根据 $\sinh\omega t=\frac{1}{2}\left(e^{\omega t}-e^{-\omega t}\right)$ 及 $\cosh\omega t=\frac{1}{2}\left(e^{\omega t}+e^{-\omega t}\right)$，按照拉普拉斯变换的定义，有……；类似地，有……。
- 公式：
  - 双曲正弦：
    $$\int_{0}^{\infty}\sinh\omega t\,e^{-pt}dt=\frac{1}{2}\int_{0}^{\infty}\left[e^{-(p-\omega)t}-e^{-(p+\omega)t}\right]dt=\frac{1}{2}\left[\frac{1}{p-\omega}-\frac{1}{p+\omega}\right]=\frac{\omega}{p^{2}-\omega^{2}}$$
    绿框：$\sinh\omega t\rightleftharpoons\dfrac{\omega}{p^{2}-\omega^{2}}$
  - 双曲余弦：
    $$\int_{0}^{\infty}\cosh\omega t\,e^{-pt}dt=\frac{1}{2}\int_{0}^{\infty}\left[e^{-(p-\omega)t}+e^{-(p+\omega)t}\right]dt=\frac{1}{2}\left[\frac{1}{p-\omega}+\frac{1}{p+\omega}\right]=\frac{p}{p^{2}-\omega^{2}}$$
    绿框：$\cosh\omega t\rightleftharpoons\dfrac{p}{p^{2}-\omega^{2}}$
- 例题/作业：例6 为示范题，页内给出解答（见上）。
- 图：无坐标图；两个绿结论框 + 蓝色箭头。
- ⚠️存疑：无。注意 $\sinh/\cosh$ 用的是 $p^2-\omega^2$（减号），与 p10 的 $\sin/\cos$ 用 $p^2+\omega^2$（加号）相对。

## p12 ｜ §6.1 定义·10 常见函数的拉普拉斯变换（汇总表）
- 标题行：常见函数的拉普拉斯变换
- 中文要点：分组标签三个：幂函数；指数函数；三角函数。
- 公式：按页内三组绿框逐条抄录——
  - 幂函数：
    $$1\rightleftharpoons\frac{1}{p},\qquad t\rightleftharpoons\frac{1}{p^{2}},\qquad t^{n}\rightleftharpoons\frac{n!}{p^{\,n+1}}$$
  - 指数函数：
    $$e^{\alpha t}\rightleftharpoons\frac{1}{p-\alpha},\qquad te^{\alpha t}\rightleftharpoons\frac{1}{(p-\alpha)^{2}},\qquad t^{n}e^{\alpha t}\rightleftharpoons\frac{n!}{(p-\alpha)^{n+1}}$$
  - 三角函数（含双曲）：
    $$\sin\omega t\rightleftharpoons\frac{\omega}{p^{2}+\omega^{2}},\qquad \cos\omega t\rightleftharpoons\frac{p}{p^{2}+\omega^{2}}$$
    $$\sinh\omega t\rightleftharpoons\frac{\omega}{p^{2}-\omega^{2}},\qquad \cosh\omega t\rightleftharpoons\frac{p}{p^{2}-\omega^{2}}$$
- 例题/作业：无（纯汇总表页，考试/查表直接用）。
- 图：无坐标图；11 个绿框排成三组。
- ⚠️存疑：无。此表未列 $\delta$ 函数（脉冲函数），与后续章节可能有关，本页确实没有。

## p13 ｜ §6.2 性质·1 线性定理
- 标题行：§ 6.2 拉普拉斯变换的性质　／　1、线性定理
- 中文要点：如果 $f_1(t)\rightleftharpoons F_1(p)$ 及 $f_2(t)\rightleftharpoons F_2(p)$，则有……，其中 $\alpha$ 和 $\beta$ 为常数。／例1 求函数 $\sin\omega t$ 的拉普拉斯变换；解：……，根据 $e^{\alpha t}\rightleftharpoons\dfrac{1}{p-\alpha}$，则……，则按照线性定理，有……。
- 公式：
  - **线性定理**（绿框，本页核心）：
    $$\alpha f_1(t)+\beta f_2(t)\rightleftharpoons\alpha F_1(P)+\beta F_2(p),\qquad \alpha,\beta\ \text{为常数}$$
    （框内第一个 $F_1(P)$ 是大写 $P$，与后面 $F_2(p)$ 不统一，原文如此）
  - 例1 的前置展开（用欧拉公式拆 $\sin$）：
    $$\sin\omega t=\frac{e^{i\omega t}-e^{-i\omega t}}{2i}=\frac{1}{2i}e^{i\omega t}-\frac{1}{2i}e^{-i\omega t}$$
  - 两支复指数的像（由 $e^{\alpha t}\rightleftharpoons\dfrac{1}{p-\alpha}$）：
    $$e^{i\omega t}\rightleftharpoons\frac{1}{p-i\omega},\qquad e^{-i\omega t}\rightleftharpoons\frac{1}{p+i\omega}$$
  - 按线性定理合成（例1 结论）：
    $$F(p)=\frac{1}{2i}F_1(p)-\frac{1}{2i}F_2(p)=\frac{1}{2i}\cdot\frac{1}{p-i\omega}-\frac{1}{2i}\cdot\frac{1}{p+i\omega}=\frac{\omega}{p^{2}+\omega^{2}}$$
- 例题/作业：例1 求 $\sin\omega t$ 的拉普拉斯变换——这是「线性定理」的第一个用例，与 p10 的按定义计算互为验证，页内解答完整（见上）。
- 图：无坐标图；一个绿定理框。
- ⚠️存疑：线性定理框内 $F_1(P)$ 的 $P$ 为大写字母（图上清晰），疑为笔误，应为 $F_1(p)$；另定理未写收敛域条件。

## p14 ｜ §6.2 性质·2 导数定理 I
- 标题行：2、导数定理I
- 中文要点：设 $f(t)$ 在 $t=0$ 时刻的值为 $f(0)$，则它的导数 $f^{(1)}(t)$ 的拉普拉斯变换为……。／证明：根据拉普拉斯变换的定义，有……。／推广到高阶导数 $f^{(n)}(t)$，则有……。／红字小结：通过拉普拉斯变换，把原函数的微商运算转化为像函数的乘法运算，而且还自动包括了原函数的初值。
- 公式：
  1. **导数定理 I**（绿框，本页核心结论）：
     $$f^{(1)}(t)\rightleftharpoons pF(p)-f(0)$$
  2. 证明（分部积分，先写成 $e^{-pt}df(t)$）：
     $$\int_{0}^{\infty}f^{(1)}(t)e^{-pt}dt=\int_{0}^{\infty}e^{-pt}df(t)=\left.e^{-pt}f(t)\right|_{0}^{\infty}-\int_{0}^{\infty}f(t)de^{-pt}$$
     $$=-f(0)-\int_{0}^{\infty}f(t)(-p)e^{-pt}dt$$
     $$=pF(p)-f(0)$$
  3. 高阶推广（蓝字）：
     $$f^{(n)}(t)\rightleftharpoons p^{n}F(p)-p^{n-1}f(0)-p^{n-2}f^{(1)}(0)-\cdots-f^{(n-1)}(0)$$
- 例题/作业：无（定理 + 证明页）。
- 图：无。
- ⚠️存疑：无。

## p15 ｜ §6.2 性质·2 例2（用导数定理 I 解二阶方程）
- 标题行：例2
- 中文要点：已知函数 $f(t)$ 满足如下二阶常微分方程 $\dfrac{d^2f(t)}{dt^2}+\omega^2f(t)=0$，其中 $\omega$ 为常数，初始条件为 $f(0)=1$，$f^{(1)}(t)=0$。试用拉普拉斯变换的导数定理 I 求解该方程。／解：根据导数定理 I，有……；整理得……；根据 $\cos\omega t\rightleftharpoons\dfrac{p}{p^2+\omega^2}$；则 $f(t)=\cos\omega t$。
- 公式：
  - 题面方程与初值：
    $$\frac{d^{2}f(t)}{dt^{2}}+\omega^{2}f(t)=0,\qquad f(0)=1,\quad f^{(1)}(t)=0$$
  - 右上贴的二阶导数定理（绿框，本页引用）：
    $$f^{(2)}(t)\rightleftharpoons p^{2}F(p)-pf(0)-f^{(1)}(0)$$
  - 代入后的代数方程：
    $$p^{2}F(p)-p+\omega^{2}F(p)=0$$
  - 解得像函数：
    $$F(p)=\frac{p}{p^{2}+\omega^{2}}$$
  - 反演（用 p12 的 $\cos$ 公式）：
    $$f(t)=\cos\omega t$$
- 例题/作业：例2 题面如上（方程、$\omega$ 为常数、$f(0)=1$、$f^{(1)}(t)=0$ 四项条件齐）；解答四步见上。
- 图：无。
- ⚠️存疑：题面把初值写成「$f^{(1)}(t)=0$」（含着 $t$ 的函数式），但按上下文与后文代入结果应为常数初值 $f^{(1)}(0)=0$——课件笔误，图上字面确实是 $f^{(1)}(t)=0$。另：$p^2F(p)-p+\omega^2F(p)=0$ 中的 $-p$ 来自 $-pf(0)=-p\cdot 1$，课件未写这步。

## p16 ｜ §6.2 性质·3 导数定理 II
- 标题行：3、导数定理II
- 中文要点：证明：根据拉普拉斯变换的定义……有……即……；红字小结：通过拉普拉斯变换，把像函数的微商运算转化为原函数的乘法运算。
- 公式：
  1. **导数定理 II**（绿框，本页核心结论）：
     $$t^{n}f(t)\rightleftharpoons(-1)^{n}\frac{d^{n}F(p)}{dp^{n}}$$
  2. 证明（对 $p$ 求导穿过积分号，每求一次导出一个 $(-t)$）：
     $$\frac{d^{n}F(p)}{dp^{n}}=\frac{d^{n}}{dp^{n}}\int_{0}^{\infty}f(t)e^{-pt}dt=\int_{0}^{\infty}f(t)(-t)^{n}e^{-pt}dt$$
  3. 中间形式（本页标「即」）：
     $$(-t)^{n}f(t)\rightleftharpoons\frac{d^{n}F(p)}{dp^{n}}$$
  4. 整理成标准形（蓝箭头指出的结论）：
     $$t^{n}f(t)\rightleftharpoons(-1)^{n}\frac{d^{n}F(p)}{dp^{n}}$$
- 例题/作业：无（定理 + 证明页）。
- 图：无；一个绿定理框 + 一个蓝箭头。
- ⚠️存疑：无。

## p17 ｜ §6.2 性质·3 例3（$t^ne^{\alpha t}$）
- 标题行：例3 利用导数定理II，求函数 $t^ne^{\alpha t}$ 的拉普拉斯变换。
- 中文要点：解：已知 $f(t)=e^{\alpha t}\rightleftharpoons\dfrac{1}{p-\alpha}$；当 $n=1$ 时，根据导数定理 II，得……；当 $n=2$ 时，根据导数定理 II，得……；类推，得……。
- 公式：
  - 右上贴的定理（绿框）：$t^{n}f(t)\rightleftharpoons(-1)^{n}\dfrac{d^{n}F(p)}{dp^{n}}$
  - 起点：$f(t)=e^{\alpha t}\rightleftharpoons\dfrac{1}{p-\alpha}$
  - $n=1$：
    $$tf(t)\rightleftharpoons-\frac{dF(p)}{dp}=-\frac{d}{dp}\left(\frac{1}{p-\alpha}\right)=\frac{1}{(p-\alpha)^{2}}$$
  - $n=2$：
    $$t^{2}f(t)\rightleftharpoons(-1)^{2}\frac{d^{2}F(p)}{dp^{2}}=\frac{d^{2}}{dp^{2}}\left(\frac{1}{p-\alpha}\right)=\frac{2}{(p-\alpha)^{3}}$$
  - 类推（本页最终结论）：
    $$t^{n}f(t)\rightleftharpoons(-1)^{n}\frac{d^{n}F(p)}{dp^{n}}=(-1)^{n}\frac{d^{n}}{dp^{n}}\left(\frac{1}{p-\alpha}\right)=\frac{n!}{(p-\alpha)^{n+1}}$$
- 例题/作业：例3 题面如上，解答三步见上（与 p9 的结论互相印证）。
- 图：无；一个绿定理框。
- ⚠️存疑：无。

## p18 ｜ §6.2 性质·4 积分定理
- 标题行：4、积分定理
- 中文要点：证明：令……则……；根据导数定理，有……；其中利用了 $g(0)=0$。；则 $F(p)=pG(p)$；红字小结：通过拉普拉斯变换，把原函数的积分运算转化为像函数的代数运算。
- 公式：
  1. **积分定理**（绿框，本页核心结论）：
     $$\int_{0}^{t}f(\tau)d\tau\rightleftharpoons\frac{1}{p}F(p)$$
  2. 引入辅助函数与其导数：
     $$g(t)=\int_{0}^{t}f(\tau)d\tau,\qquad g^{(1)}(t)=f(t)\rightleftharpoons F(p)$$
  3. 对 $g$ 用导数定理（初值 $g(0)=0$ 把 $-g(0)$ 消掉）：
     $$g^{(1)}(t)\rightleftharpoons pG(p)-g(0)=pG(p)$$
  4. 于是：$F(p)=pG(p)$
  5. 结论（蓝箭头）：$\displaystyle\int_{0}^{t}f(\tau)d\tau=g(t)\rightleftharpoons G(p)=\frac{1}{p}F(p)$
- 例题/作业：无（定理 + 证明页）。
- 图：无；一个绿定理框 + 一个蓝箭头。
- ⚠️存疑：无。

## p19 ｜ §6.2 性质·5 相似性定理
- 标题行：5、相似性定理
- 中文要点：证明：根据拉普拉斯变换的定义，有……；令 $y=at$，由于 $a>0$，则……；如果当 $a<0$ 时，则……。
- 公式：
  1. **相似性定理**（绿框，本页核心结论）：
     $$f(at)\rightleftharpoons\frac{1}{a}F(p/a),\qquad \text{其中 } a>0$$
  2. 证明第一步（把 $e^{-pt}$ 凑成 $e^{-\frac{p}{a}(at)}$）：
     $$\int_{0}^{\infty}f(at)e^{-pt}dt=\int_{0}^{\infty}f(at)e^{-\frac{p}{a}(at)}\frac{1}{a}d(at)$$
  3. 换元 $y=at$（$a>0$ 保序，限仍是 $0\to\infty$）：
     $$\int_{0}^{\infty}f(at)e^{-pt}dt=\frac{1}{a}\int_{0}^{\infty}f(y)e^{-\frac{p}{a}y}dy\rightleftharpoons\frac{1}{a}F\!\left(\frac{p}{a}\right)$$
  4. $a<0$ 的情形（本页只写到换限，未给最终结论）：
     $$\int_{0}^{\infty}f(at)e^{-pt}dt=\frac{1}{a}\int_{0}^{-\infty}f(y)e^{-\frac{p}{a}y}dy$$
- 例题/作业：无（定理 + 证明页）。
- 图：无；一个绿定理框。
- ⚠️存疑：$a<0$ 这一支的上限图上明确是 $-\infty$（$\int_0^{-\infty}$），字迹清晰；但课件到此为止，既没有翻正上下限，也没有写出 $a<0$ 时的最终公式。

## p20 ｜ §6.2 性质·5 例4（$e^t$ 与 $e^{\alpha t}$）
- 标题行：例4 
- 中文要点：证明 $e^{t}\rightleftharpoons\dfrac{1}{p-1}$，利用相似性定理，求函数 $e^{\alpha t}$ 的拉普拉斯变换。／解：根据拉普拉斯变换的定义，有……；根据相似性定理，有……；这和直接用拉普拉斯变换定义计算得到的结果一致。
- 公式：
  - 待证目标（题面行内）：$e^{t}\rightleftharpoons\dfrac{1}{p-1}$
  - 按定义计算：
    $$\int_{0}^{\infty}e^{t}e^{-pt}dt=\int_{0}^{\infty}e^{-(p-1)t}dt=-\frac{1}{p-1}\left.e^{-(p-1)t}\right|_{0}^{\infty}=\frac{1}{p-1}$$
    结论（蓝箭头 + 绿框）：$e^{t}\rightleftharpoons\dfrac{1}{p-1}$
  - 右上贴的相似性定理（绿框）：$f(at)\rightleftharpoons\dfrac{1}{a}F(p/a)$
  - 用相似性定理推 $e^{\alpha t}$：
    $$e^{\alpha t}\rightleftharpoons\frac{1}{a}\cdot\frac{1}{p/a-1}=\frac{1}{p-a}$$
- 例题/作业：例4 题面与解答见上；页末一句「这和直接用拉普拉斯变换定义计算得到的结果一致」。
- 图：无。
- ⚠️存疑：结论写成 $\dfrac{1}{p-a}$，与题面的 $\alpha$ 不是一个字母（课件把 $f(t)=e^t$ 中 $t\to at$ 得 $e^{at}$，故结果里是 $a$）。按上下文应理解为 $1/(p-\alpha)$，但图上字面确实是 $a$。

## p21 ｜ §6.2 性质·6 位移定理
- 标题行：6、位移定理
- 中文要点：证明：根据拉普拉斯变换的定义，有……；利用这个定理，就可以得到：……。
- 公式：
  1. **位移定理**（绿框，本页核心结论）：
     $$e^{-\lambda t}f(t)\rightleftharpoons F(p+\lambda)$$
  2. 证明（把两个指数合并成一个）：
     $$\int_{0}^{\infty}e^{-\lambda t}f(t)e^{-pt}dt=\int_{0}^{\infty}f(t)e^{-(p+\lambda)t}dt\rightleftharpoons F(p+\lambda)$$
  3. 直接推论（把 $p\to p+\lambda$ 代入 $\sin/\cos$ 的表）：
     $$e^{-\lambda t}\sin\omega t\rightleftharpoons\frac{\omega}{(p+\lambda)^{2}+\omega^{2}}$$
     $$e^{-\lambda t}\cos\omega t\rightleftharpoons\frac{p+\lambda}{(p+\lambda)^{2}+\omega^{2}}$$
- 例题/作业：无（定理 + 证明 + 推论页）。
- 图：无；一个绿定理框。
- ⚠️存疑：无。

## p22 ｜ §6.2 性质·7 延迟定理
- 标题行：7、延迟定理
- 中文要点：证明：为满足 $f(t-t_0)$ 有意义，要求 $t\ge t_0$；根据拉普拉斯变换的定义，并令 $\zeta=t-t_0$，则有……；即……。
- 公式：
  1. **延迟定理**（绿框，本页核心结论）：
     $$f(t-t_{0})\rightleftharpoons e^{-pt_{0}}F(p)$$
  2. 证明（区间从 $[0,\infty)$ 挪到 $[t_0,\infty)$，再换元 $\zeta=t-t_0$）：
     $$\int_{0}^{\infty}f(t-t_{0})e^{-pt}dt=\int_{t_{0}}^{\infty}f(t-t_{0})e^{-pt}dt=\int_{0}^{\infty}f(\zeta)e^{-p(\zeta+t_{0})}d\zeta$$
  3. 提出常数因子：
     $$\int_{0}^{\infty}f(t-t_{0})e^{-pt}dt=e^{-pt_{0}}\int_{0}^{\infty}f(\zeta)e^{-p\zeta}d\zeta=e^{-pt_{0}}F(p)$$
  4. 收尾行（蓝箭头）：$f(t-t_0)\ \square\ e^{-pt_0}F(p)$
- 例题/作业：无（定理 + 证明页）。
- 图：无；一个绿定理框 + 一个蓝箭头。
- ⚠️存疑：（a）证明中换元用的符号图像是 $\zeta$（zeta，草写体），也可能是 $\xi$，分辨率下不能百分百确认，按 $\zeta$ 记录。（b）最后一行蓝箭头右边的等价箭号在本页被渲染成一个空心方框「□」（字形缺失），按上下文应为 $\rightleftharpoons$。

## p23 ｜ §6.2 性质·8 卷积定理（引入 + 积分区域）
- 标题行：8、卷积定理
- 中文要点：设原函数 $f_1(t)$ 及 $f_2(t)$ 对应的像函数分别为 $F_1(p)$ 及 $F_2(p)$，则他们的卷积对应的拉普拉斯变换为……。／证明：根据拉普拉斯变换及卷积的定义，有……。／对于这个二重积分，积分顺序为：变量 $\tau$ 先从 $\tau=0$ 到 $\tau=t$ 进行积分，然后变量 $t$ 再从 $t=0$ 到 $t=\infty$ 进行积分。
- 公式：
  1. **卷积定理**（绿框，本页核心结论）：
     $$f_{1}(t)*f_{2}(t)\rightleftharpoons F_{1}(p)F_{2}(p)$$
  2. 证明起步（卷积的定义式藏在这里面：$f_1*f_2=\int_0^t f_1(t-\tau)f_2(\tau)d\tau$）：
     $$\int_{0}^{\infty}f_{1}(t)*f_{2}(t)e^{-pt}dt=\int_{0}^{\infty}\left[\int_{0}^{t}f_{1}(t-\tau)f_{2}(\tau)d\tau\right]e^{-pt}dt$$
- 例题/作业：无（定理 + 证明，本页只到写出二重积分为止）。
- 图：有一张 $t$-$\tau$ 平面示意图（灰底）：纵轴标 $t$、横轴标 $\tau$、原点标 $0$；一条从原点出发的 $45^\circ$ 斜线标 $t=\tau$；斜线与纵轴之间（即 $0\le\tau\le t$ 的三角区域）画了阴影；斜线上一点向右上方画箭头标 $t\to\infty$。整幅图说明「先对 $\tau$ 从 $0$ 积到 $t$，再对 $t$ 从 $0$ 积到 $\infty$」的积分区域。
- ⚠️存疑：无。卷积定义式本身（含 $\int_0^t$ 与 $t-\tau$）课件没有单独成行给出，只在证明的方括号里出现。

## p24 ｜ §6.2 性质·8 卷积定理（证明完成）
- 标题行：（接上页，无新标题）
- 中文要点：现在改变积分顺序，变量 $t$ 先从 $t=\tau$ 到 $t=\infty$ 进行积分，然后变量 $\tau$ 再从 $\tau=0$ 到 $\tau=\infty$ 进行积分；两种方法，积分区域相同，因此积分结果也相同；再进行变量代换，令 $\zeta=t-\tau$，则有……。／红字小结：两个原函数的卷积在拉普拉斯变换下变成了像函数的乘积。
- 公式：
  1. 交换积分次序（内层改 $t$，外层改 $\tau$）：
     $$\int_{0}^{\infty}\left[\int_{0}^{t}f_{1}(t-\tau)f_{2}(\tau)d\tau\right]e^{-pt}dt=\int_{0}^{\infty}\left[\int_{\tau}^{\infty}f_{1}(t-\tau)e^{-pt}dt\right]f_{2}(\tau)d\tau$$
  2. 换元 $\zeta=t-\tau$（此时 $t=\zeta+\tau$，$dt=d\zeta$）：
     $$\int_{0}^{\infty}\left[\int_{\tau}^{\infty}f_{1}(t-\tau)e^{-pt}dt\right]f_{2}(\tau)d\tau=\int_{0}^{\infty}\left[\int_{0}^{\infty}f_{1}(\zeta)e^{-p(\zeta+\tau)}d\zeta\right]f_{2}(\tau)d\tau$$
  3. 分离成两个单积分之积（本页最终结论）：
     $$=\int_{0}^{\infty}f_{1}(\zeta)e^{-p\zeta}d\zeta\int_{0}^{\infty}f_{2}(\tau)e^{-p\tau}d\tau=F_{1}(p)F_{2}(p)$$
- 例题/作业：无（证明续页）。
- 图：与 p23 同一张 $t$-$\tau$ 平面示意图（纵轴 $t$、横轴 $\tau$、斜线 $t=\tau$、阴影三角区、箭头标 $t\to\infty$），此处用来对照「两种积分次序对应同一块区域」。
- ⚠️存疑：换元符号与前页 p22 同为 $\zeta$（草写体，也可能读作 $\xi$）。

## p25 ｜ 第六章作业（第 1 题）
- 标题行：§ 第六章作业
- 中文要点：1.求下列函数的像函数。
- 公式：三道小题，逐题照抄——
  1) $te^{-\omega t}$
  2) $t\cos\omega t$
  3) $\dfrac{1-\cos\omega t}{\omega}$
- 例题/作业：**作业页，无解答**。题号与题面如上三项，一字不漏；答案未给。
- 图：无（大片空白，仅有水印）。
- ⚠️存疑：第 1 小题的指数是 $-\omega t$（希腊字母 $\omega$），图上字形与第 2、3 小题的 $\omega$ 完全一致，不是 $\alpha$、也不是 $a$。

## p26 ｜ §6.3 反演·1 反演的含义与三条思路
- 标题行：§ 6.3 拉普拉斯变换的反演
- 中文要点：在已知原函数的情况下，求出它对应的像函数，这叫拉普拉斯变换。反过来，若已知像函数，来求出它对应的原函数，这叫做拉普拉斯变换的反演。／1. 一个像函数可以分解成几个简单的像函数之和；2. 一个像函数可以分解成两个简单的像函数的乘积；3. 经过其它的数学操作，这个像函数可以用一些简单的像函数来表示。／这样就可以利用一些已知的简单原函数（如 $t^n,\sin\omega t,\cos\omega t,e^{\alpha t}$ 等）所对应的像函数及上节介绍的拉普拉斯变换的性质，来完成反演过程。
- 公式：无独立行间公式；页内出现的符号只有一组「已知的简单原函数」清单：
  $$t^{n},\quad \sin\omega t,\quad \cos\omega t,\quad e^{\alpha t}$$
- 例题/作业：无（方法总述页）。
- 图：无。
- ⚠️存疑：无。

## p27 ｜ §6.3 反演·2 例1（部分分式拆分）
- 标题行：例1 
- 中文要点：求像函数 $F(p)=\dfrac{1}{(p^2+a^2)(p^2+b^2)}$ 的反演；解：可以把这个像函数分解为……；根据 $\sin\omega t\rightleftharpoons\dfrac{\omega}{p^2+\omega^2}$，有……；则……。
- 公式：
  - 待反演的像函数：
    $$F(p)=\frac{1}{(p^{2}+a^{2})(p^{2}+b^{2})}$$
  - 第一步分解（裂项，产生 $1/(b^2-a^2)$ 的系数）：
    $$F(p)=\frac{1}{(p^{2}+a^{2})(p^{2}+b^{2})}=\frac{1}{b^{2}-a^{2}}\left(\frac{1}{p^{2}+a^{2}}-\frac{1}{p^{2}+b^{2}}\right)$$
  - 第二步（凑成 $\dfrac{\omega}{p^2+\omega^2}$ 的标准形，$\omega$ 分别取 $a$、$b$）：
    $$=\frac{1}{b^{2}-a^{2}}\left(\frac{1}{a}\cdot\frac{a}{p^{2}+a^{2}}-\frac{1}{b}\cdot\frac{b}{p^{2}+b^{2}}\right)$$
  - 查表：
    $$\frac{a}{p^{2}+a^{2}}\rightleftharpoons\sin at,\qquad \frac{b}{p^{2}+b^{2}}\rightleftharpoons\sin bt$$
  - 反演结果：
    $$F(p)\rightleftharpoons\frac{1}{b^{2}-a^{2}}\left(\frac{1}{a}\sin at-\frac{1}{b}\sin bt\right)$$
- 例题/作业：例1 题面 + 完整解答（见上）。
- 图：无。
- ⚠️存疑：无。

## p28 ｜ §6.3 反演·3 例2、例3（用位移定理读反演）
- 标题行：例2 
- 中文要点：求像函数 $F(p)=\dfrac{\omega}{(p+\lambda)^2+\omega^2}$ 的反演，其中 $\lambda$ 为复数；解：由 $\sin\omega t\rightleftharpoons\dfrac{\omega}{p^2+\omega^2}$ 及位移定理 $F(p+\lambda)\rightleftharpoons e^{-\lambda t}f(t)$，有 $F(p)\rightleftharpoons e^{-\lambda t}\sin\omega t$。／例3 求像函数 $F(p)=\dfrac{p}{(p+\lambda)^2+\omega^2}$ 的反演，其中 $\lambda$ 为复数；解：由 $\sin\omega t\rightleftharpoons\dfrac{\omega}{p^2+\omega^2}$，$\cos\omega t\rightleftharpoons\dfrac{p}{p^2+\omega^2}$ 及位移定理 $F(p+\lambda)\rightleftharpoons e^{-\lambda t}f(t)$，有……。
- 公式：
  - 例2 的像与结果：
    $$F(p)=\frac{\omega}{(p+\lambda)^{2}+\omega^{2}}\ \rightleftharpoons\ e^{-\lambda t}\sin\omega t$$
  - 例3 的像函数，先拆成「$\cos$ 型 + 常数/线性组合」：
    $$F(p)=\frac{p}{(p+\lambda)^{2}+\omega^{2}}=\frac{p+\lambda}{(p+\lambda)^{2}+\omega^{2}}-\frac{\lambda}{(p+\lambda)^{2}+\omega^{2}}=\frac{p+\lambda}{(p+\lambda)^{2}+\omega^{2}}-\frac{\lambda}{\omega}\cdot\frac{\omega}{(p+\lambda)^{2}+\omega^{2}}$$
  - 例3 的反演结果：
    $$F(p)\rightleftharpoons e^{-\lambda t}\cos\omega t-\frac{\lambda}{\omega}e^{-\lambda t}\sin\omega t$$
- 例题/作业：例2、例3 题面与解答见上（两题都用「位移定理 + 查表」，是本节的示范套路）。
- 图：无。
- ⚠️存疑：无。

## p29 ｜ §6.3 反演·4 例4（$1/[p(p-1)^2]$，两种方法）
- 标题行：例4 
- 中文要点：求像函数 $F(p)=\dfrac{1}{p(p-1)^2}$ 的反演；解：方法一　可以把这个像函数分解；思路：……；则有……；利用 $\dfrac{1}{p}\rightleftharpoons 1$，$\dfrac{1}{p-\alpha}\rightleftharpoons e^{\alpha t}$ 及 $\dfrac{1}{(p-\alpha)^2}\rightleftharpoons te^{\alpha t}$，则 $f(t)=1-e^t+te^t$。／方法二……；由于 $\dfrac{1}{p}\rightleftharpoons 1$，$\dfrac{1}{(p-\alpha)^2}\rightleftharpoons te^{\alpha t}$，根据卷积定理，有……。
- 公式：
  - 待反演的像函数：
    $$F(p)=\frac{1}{p(p-1)^{2}}$$
  - 方法一「思路」两行（课件原样的试算草稿，等号两边是不同式子，非严格等式链）：
    $$\frac{1}{p}-\frac{1}{(p-1)^{2}}=\frac{p^{2}-3p+1}{p(p-1)^{2}},\qquad \frac{1}{p}+\frac{1}{(p-1)^{2}}=\frac{p^{2}-p+1}{p(p-1)^{2}}=\frac{1}{p(p-1)^{2}}+\frac{p^{2}-p}{p(p-1)^{2}}$$
  - 方法一 的分解结果：
    $$F(p)=\frac{1}{p}-\frac{1}{p-1}+\frac{1}{(p-1)^{2}}$$
  - 方法一 查表反演：
    $$\frac{1}{p}\rightleftharpoons 1,\qquad \frac{1}{p-\alpha}\rightleftharpoons e^{\alpha t},\qquad \frac{1}{(p-\alpha)^{2}}\rightleftharpoons te^{\alpha t}$$
    $$f(t)=1-e^{t}+te^{t}$$
  - 方法二（拆成两个像函数之积，用卷积定理）：
    $$F(p)=\frac{1}{p(p-1)^{2}}=\frac{1}{p}\cdot\frac{1}{(p-1)^{2}}$$
    $$f(t)=\int_{0}^{t}1\cdot\tau e^{\tau}d\tau=\int_{0}^{t}\tau\,de^{\tau}=\left.\tau e^{\tau}\right|_{0}^{t}-\int_{0}^{t}e^{\tau}d\tau=te^{t}-e^{t}+1$$
- 例题/作业：例4 题面 + 两条完整解法（见上）；两法结果一致（$1-e^t+te^t$）。
- 图：无。
- ⚠️存疑：「思路」两行是草稿式试算（左边是练习用的式子），课件没有说明它们怎么拼出 $F(p)$ 的分解，字面照录。

## p30 ｜ §6.3 反演·5 例5（$-1/[p^2(p-1)]$，两种方法）
- 标题行：例5 
- 中文要点：求像函数 $F(p)=-\dfrac{1}{p^2(p-1)}$ 的反演；解：方法一　可以把这个像函数分解；思路：……；则有……；利用 $\dfrac{1}{p}\rightleftharpoons 1$，$\dfrac{1}{p-1}\rightleftharpoons e^t$ 及 $\dfrac{1}{p^2}\rightleftharpoons t$，则 $f(t)=t-e^t+1$。／方法二……；由于 $\dfrac{1}{p^2}\rightleftharpoons t$，$\dfrac{1}{p-1}\rightleftharpoons e^t$，根据卷积定理，有……。
- 公式：
  - 待反演的像函数（注意前面有负号）：
    $$F(p)=-\frac{1}{p^{2}(p-1)}$$
  - 方法一「思路」两行（同样是试算草稿）：
    $$\frac{1}{p^{2}}+\frac{1}{p-1}=\frac{p-1+p^{2}}{p^{2}(p-1)},\qquad \frac{1}{p^{2}}-\frac{1}{p-1}=\frac{p-1-p^{2}}{p^{2}(p-1)}=-\frac{1}{p^{2}(p-1)}-\frac{p^{2}-p}{p^{2}(p-1)}$$
  - 方法一 的分解结果：
    $$F(p)=\frac{1}{p^{2}}-\frac{1}{p-1}+\frac{1}{p}$$
  - 方法一 反演：
    $$\frac{1}{p}\rightleftharpoons 1,\qquad \frac{1}{p-1}\rightleftharpoons e^{t},\qquad \frac{1}{p^{2}}\rightleftharpoons t$$
    $$f(t)=t-e^{t}+1$$
  - 方法二（卷积）：
    $$F(p)=-\frac{1}{p^{2}(p-1)}=-\frac{1}{p^{2}}\cdot\frac{1}{p-1}$$
    $$f(t)=-\int_{0}^{t}\tau e^{(t-\tau)}d\tau=-e^{t}\int_{0}^{t}\tau e^{-\tau}d\tau=e^{t}\int_{0}^{t}\tau\,de^{-\tau}=e^{t}\left[\left.\tau e^{-\tau}\right|_{0}^{t}-\int_{0}^{t}e^{-\tau}d\tau\right]=t+1-e^{t}$$
- 例题/作业：例5 题面 + 两条完整解法（见上）；两法同得 $t+1-e^t$。
- 图：无。
- ⚠️存疑：「思路」两行中第二行末尾的 $-\dfrac{1}{p^2(p-1)}-\dfrac{p^2-p}{p^2(p-1)}$ 是把 $-\frac{1}{p^2(p-1)}$ 拆成两项的草稿，原文如此。

## p31 ｜ §6.3 反演·6 例6（卷积定理 + 复指数积分化实）
- 标题行：例6 
- 中文要点：求像函数 $F(p)=\dfrac{\omega}{(p+\alpha)(p^2+\omega^2)}$ 的反演；解：由 $\dfrac{1}{p+\alpha}\rightleftharpoons e^{-\alpha t}$，$\dfrac{\omega}{p^2+\omega^2}\rightleftharpoons\sin\omega t$，及卷积定理，得到……。
- 公式：
  - 待反演像函数：
    $$F(p)=\frac{\omega}{(p+\alpha)(p^{2}+\omega^{2})}$$
  - 卷积积分（本页第一步）：
    $$\int_{0}^{t}e^{-\alpha(t-\tau)}\sin\omega\tau\,d\tau=\frac{1}{2i}\int_{0}^{t}e^{-\alpha(t-\tau)}\left[e^{i\omega\tau}-e^{-i\omega\tau}\right]d\tau$$
  - 提出 $e^{-\alpha t}$、合并指数：
    $$=\frac{1}{2i}e^{-\alpha t}\int_{0}^{t}\left[e^{(\alpha+i\omega)\tau}-e^{(\alpha-i\omega)\tau}\right]d\tau$$
  - 逐项积分：
    $$=\frac{1}{2i}e^{-\alpha t}\left[\frac{e^{(\alpha+i\omega)t}-1}{\alpha+i\omega}-\frac{e^{(\alpha-i\omega)t}-1}{\alpha-i\omega}\right]$$
  - 拆成「含 $t$ 的振荡项」与「含 $e^{-\alpha t}$ 的衰减项」：
    $$=\frac{1}{2i}\left[\frac{e^{i\omega t}}{\alpha+i\omega}-\frac{e^{-i\omega t}}{\alpha-i\omega}\right]-\frac{1}{2i}e^{-\alpha t}\left[\frac{1}{\alpha+i\omega}-\frac{1}{\alpha-i\omega}\right]$$
  - 最终化成实函数（本页结论）：
    $$=\frac{1}{\omega^{2}+\alpha^{2}}\left(\alpha\sin\omega t-\omega\cos\omega t+\omega e^{-\alpha t}\right)$$
- 例题/作业：例6 题面 + 完整解答（见上）。
- 图：无。
- ⚠️存疑：最后一步（从中括号两式化到实函数）跳得最大，中间的通分与复数整理全部省略；图上给出的实式符号依次为 $+\alpha\sin\omega t$、$-\omega\cos\omega t$、$+\omega e^{-\alpha t}$，前面整体为正号 $\frac{1}{\omega^2+\alpha^2}$。

## p32 ｜ §6.3 反演·7 例7（$p/(p^2+\omega^2)^2$，两法）
- 标题行：例7 
- 中文要点：求像函数 $F(p)=\dfrac{p}{(p^2+\omega^2)^2}$ 的反演；解：由于……，则……；根据 $\dfrac{p}{p^2+\omega^2}\rightleftharpoons\cos\omega t$，有……。／方法2：……；则……；根据导数定理 $tf(t)\rightleftharpoons(-1)\dfrac{dF(p)}{dp}$ 及 $\dfrac{\omega}{p^2+\omega^2}\rightleftharpoons\sin\omega t$，则……。
- 公式：
  - 待反演像函数：
    $$F(p)=\frac{p}{(p^{2}+\omega^{2})^{2}}$$
  - 方法一（对**参数 $\omega$** 求导，把分母的幂次降下来）：
    $$\frac{d}{d\omega}\frac{p}{p^{2}+\omega^{2}}=-\frac{2\omega p}{(p^{2}+\omega^{2})^{2}}$$
    $$F(p)=\frac{p}{(p^{2}+\omega^{2})^{2}}=-\frac{1}{2\omega}\frac{d}{d\omega}\frac{p}{p^{2}+\omega^{2}}$$
    $$-\frac{1}{2\omega}\frac{d}{d\omega}\frac{p}{p^{2}+\omega^{2}}\rightleftharpoons-\frac{1}{2\omega}\frac{d}{d\omega}\cos\omega t=\frac{t\sin\omega t}{2\omega}$$
  - 方法二（对**$p$** 求导，用导数定理 II）：
    $$\frac{d}{dp}\frac{1}{p^{2}+\omega^{2}}=-\frac{2p}{(p^{2}+\omega^{2})^{2}}$$
    $$F(p)=\frac{p}{(p^{2}+\omega^{2})^{2}}=-\frac{1}{2}\frac{d}{dp}\frac{1}{p^{2}+\omega^{2}}=-\frac{1}{2}\frac{d}{dp}\left(\frac{1}{\omega}\cdot\frac{\omega}{p^{2}+\omega^{2}}\right)$$
  - 引用的定理与表值（本页行内）：
    $$tf(t)\rightleftharpoons(-1)\frac{dF(p)}{dp},\qquad \frac{\omega}{p^{2}+\omega^{2}}\rightleftharpoons\sin\omega t$$
  - 方法二 结论：
    $$F(p)=-\frac{1}{2}\frac{d}{dp}\left(\frac{1}{\omega}\cdot\frac{\omega}{p^{2}+\omega^{2}}\right)\rightleftharpoons\frac{t\sin\omega t}{2\omega}$$
- 例题/作业：例7 题面 + 两种解法（见上），两法同得 $\dfrac{t\sin\omega t}{2\omega}$。
- 图：无。
- ⚠️存疑：方法一对 $\omega$ 求导属于「把参数当变量」的技巧，已讲的导数定理 II 是对 $p$ 求导，课件未说明这一步的合法性依据（见「跳步候选」）。

## p33 ｜ §6.3 反演·8 例8（$\omega/(p^2+\omega^2)^2$）
- 标题行：例8 
- 中文要点：求像函数 $F(p)=\dfrac{\omega}{(p^2+\omega^2)^2}$ 的反演；解：由于……，则……；根据 $\dfrac{\omega}{p^2+\omega^2}\rightleftharpoons\sin\omega t$，有……。
- 公式：
  - 待反演像函数：
    $$F(p)=\frac{\omega}{(p^{2}+\omega^{2})^{2}}$$
  - 前置求导（对 $\omega$）：
    $$\frac{d}{d\omega}\frac{1}{p^{2}+\omega^{2}}=-\frac{2\omega}{(p^{2}+\omega^{2})^{2}}$$
  - 把 $F(p)$ 写成导数形式（并刻意留一个 $\frac{1}{\omega}$ 配平）：
    $$F(p)=\frac{\omega}{(p^{2}+\omega^{2})^{2}}=-\frac{1}{2}\frac{d}{d\omega}\frac{1}{p^{2}+\omega^{2}}=-\frac{1}{2}\frac{d}{d\omega}\left(\frac{\omega}{p^{2}+\omega^{2}}\cdot\frac{1}{\omega}\right)$$
  - 反演（导数穿到已知表值上）：
    $$F(p)=-\frac{1}{2}\frac{d}{d\omega}\left(\frac{\omega}{p^{2}+\omega^{2}}\cdot\frac{1}{\omega}\right)\rightleftharpoons-\frac{1}{2}\frac{d}{d\omega}\left(\frac{\sin\omega t}{\omega}\right)=-\frac{1}{2}\left(\frac{t\cos\omega t}{\omega}-\frac{\sin\omega t}{\omega^{2}}\right)$$
- 例题/作业：例8 题面 + 解答（见上）。
- 图：无。
- ⚠️存疑：无。此式后续在 p39（共振解）被直接引用。

## p34 ｜ §6.3 反演·9 像函数的积分定理
- 标题行：像函数的积分的定理
- 中文要点：如果 $\int_p^\infty F(q)dq$ 存在，且当 $t\to 0$ 时，$|f(t)/t|$ 有界，则……。／证明：假设 $F(q)$ 所对应的原函数存在，则……；则……；即……；特殊的，当 $p=0$ 时，有……。／$\int_0^\infty\dfrac{f(t)}{t}dt$ 类型的积分可以通过 $f(t)$ 的像函数的积分来表示。／例如……。
- 公式：
  1. **像函数的积分定理**（右上绿框，本页核心结论）：
     $$\int_{p}^{\infty}F(q)dq\rightleftharpoons\frac{f(t)}{t}$$
     前置条件：$\int_p^\infty F(q)dq$ 存在，且当 $t\to 0$ 时 $\left|f(t)/t\right|$ 有界。
  2. 证明起点（把 $F(q)$ 按定义展开）：
     $$F(q)=\int_{0}^{\infty}f(t)e^{-qt}dt$$
  3. 交换积分次序（先对 $q$ 积，$\int_p^\infty e^{-qt}dq=e^{-pt}/t$）：
     $$\int_{p}^{\infty}F(q)dq=\int_{p}^{\infty}\left[\int_{0}^{\infty}f(t)e^{-qt}dt\right]dq=\int_{0}^{\infty}f(t)dt\int_{p}^{\infty}e^{-qt}dq$$
     $$=\int_{0}^{\infty}f(t)\frac{e^{-pt}}{t}dt=\int_{0}^{\infty}\frac{f(t)}{t}e^{-pt}dt$$
  4. 结论式（标「即」）：
     $$\int_{p}^{\infty}F(q)dq=\int_{0}^{\infty}\frac{f(t)}{t}e^{-pt}dt$$
  5. 特例 $p=0$（用于算定积分）：
     $$\int_{0}^{\infty}F(q)dq=\int_{0}^{\infty}\frac{f(t)}{t}dt$$
  6. 示范计算（$f(t)=\sin t$，$F(q)=1/(q^2+1)$，注意积分变量被写成 $p$）：
     $$\int_{0}^{\infty}\frac{\sin t}{t}dt=\int_{0}^{\infty}\frac{1}{p^{2}+1}dp=\left.\arctan p\right|_{0}^{\infty}=\frac{\pi}{2}$$
- 例题/作业：末行的 $\int_0^\infty\frac{\sin t}{t}dt=\frac{\pi}{2}$ 是定理的示范用例（不是编号例题）。
- 图：无。
- ⚠️存疑：特例与示范计算里积分变量记为 $p$（$\int_0^\infty\frac{1}{p^2+1}dp$），与定理中的哑变量 $q$ 混用，但值没错。

## p35 ｜ §6.4 应用·1 例1（LR 回路接直流电源）
- 标题行：§ 6.4 拉普拉斯变换的应用
- 中文要点：例1 对于电感-电阻串联回路，当开关 $K$ 合上之前，回路中没有电流流动，其中 $E$ 为直流电源的电动势，$R$ 为电阻，$L$ 为电感。求开关合上之后，电路中的电流 $i(t)$。／解：$i(t)$ 所满足的方程为……；根据拉普拉斯变换，有……；初始条件 $i(0)=0$，则……；结果下方用红字标注「稳恒部分」「暂态部分」分别指向两项。
- 公式：
  - 回路微分方程（题面）：
    $$L\frac{di(t)}{dt}+Ri(t)=E$$
  - 取拉氏变换（用导数定理 I）：
    $$L\left[pI(p)-i(0)\right]+RI(p)=\frac{E}{p}$$
  - 代入 $i(0)=0$ 并整理（部分分式）：
    $$I(p)=\frac{E}{p}\cdot\frac{1}{Lp+R}=\frac{E}{R}\left[\frac{1}{p}-\frac{L}{Lp+R}\right]=\frac{E}{R}\left[\frac{1}{p}-\frac{1}{p+R/L}\right]$$
  - 反演结果（蓝箭头指出的本页结论）：
    $$i(t)=\frac{E}{R}\left[1-e^{-Rt/L}\right]$$
    其中 $\dfrac{E}{R}$ 标「稳恒部分」，$-\dfrac{E}{R}e^{-Rt/L}$ 标「暂态部分」。
- 例题/作业：例1 题面：电感-电阻串联回路、开关 $K$ 合上前回路无电流、$E$ 为直流电动势、$R$ 为电阻、$L$ 为电感、求合上后 $i(t)$。解答四步见上。
- 图：右上角电路图——矩形回路：左边画直流电源（长/短横线电池符号）并标 $E$；上边画矩形电阻符号并标 $R$；右边画螺旋线圈（电感）标 $L$；下边画开关 $K$（带一个小黑点的斜刀开关）。四者串联。
- ⚠️存疑：无。

## p36 ｜ §6.4 应用·2 例2（LC 回路放电）
- 标题行：（接 §6.4，无新大标题）
- 中文要点：例2 对于电感-电容串联回路，电容器上初始电荷为 $\pm q_0$。当电容器进行放电时，电路中的电流 $i(t)$ 是多少？／解：设电容器进行放电时，它上面的瞬间电荷量为 $q(t)$，它与瞬时电流 $i(t)$ 的关系为……即……；对应的回路方程为……；代入 $q(t)$ 的表达式，则有……；根据导数定理，积分定理及初始电流 $i(0)=0$，有……；即……；红字标注「LC回路震荡电流」指向结果。
- 公式：
  - 电荷与电流的关系（放电取负号）：
    $$i(t)=-\frac{dq(t)}{dt}\qquad\Longrightarrow\qquad q(t)=-\int_{0}^{t}i(\tau)d\tau+q_{0}$$
  - 回路方程（电感两端电压 = 电容极板电压）：
    $$L\frac{di(t)}{dt}=\frac{q(t)}{C}$$
  - 代入 $q(t)$ 后的积分微分方程：
    $$L\frac{di(t)}{dt}+\frac{1}{C}\int_{0}^{t}i(\tau)d\tau=\frac{q_{0}}{C}$$
  - 取拉氏变换（导数定理 + 积分定理 + $i(0)=0$）：
    $$L\left[pI(p)-i(0)\right]+\frac{1}{C}\frac{I(p)}{p}=\frac{q_{0}}{C}\cdot\frac{1}{p}$$
  - 解得像函数并整理成标准形（$\omega=1/\sqrt{LC}$）：
    $$I(p)=\frac{q_{0}}{LCp^{2}+1}=\frac{q_{0}}{\sqrt{LC}}\cdot\frac{\sqrt{1/LC}}{p^{2}+1/LC}$$
  - 反演结果（本页结论，箭头指向、红字标「LC回路震荡电流」）：
    $$i(t)=\frac{q_{0}}{\sqrt{LC}}\sin\left(\frac{t}{\sqrt{LC}}\right)$$
- 例题/作业：例2 题面（初始电荷 $\pm q_0$、放电过程、求 $i(t)$）与完整解答见上。
- 图：右上角电路图——左边画电容器（两条平行板）并标 $C$，上极板标 $q_0$、下极板标 $-q_0$；右边画电感线圈标 $L$；两者用导线串联成闭合回路。
- ⚠️存疑：无。注意 $q(t)$ 表达式里积分限是 $\int_0^t$、常数项为 $+q_0$，图上清晰。

## p37 ｜ §6.4 应用·3 例3（LR 回路接交流电源）
- 标题行：（接 §6.4）
- 中文要点：例3 电感-电阻回路中，交变电源的电压为 $E(t)=E_0\sin\omega t$。当开关闭合时，求回路中的电流 $i(t)$。已知初始电流为 0，即 $i(0)=0$。／解：回路中电流满足的微分方程为……；根据拉普拉斯变换，则有……；由于……，并根据卷积定理得……；红字分别标注「暂态电流」与「外界电源引起的强迫震荡电流」。
- 公式：
  - 回路微分方程（题面）：
    $$L\frac{di}{dt}+Ri=E_{0}\sin\omega t$$
  - 取拉氏变换：
    $$L\left[pI(p)-i(0)\right]+RI(p)=E_{0}\frac{\omega}{p^{2}+\omega^{2}}$$
  - 解出像函数（蓝箭头指出的关键一步）：
    $$I(p)=\frac{E_{0}}{L}\cdot\frac{1}{p+R/L}\cdot\frac{\omega}{p^{2}+\omega^{2}}$$
  - 查表 + 卷积定理：
    $$\frac{1}{p+R/L}\rightleftharpoons e^{-Rt/L},\qquad \frac{\omega}{p^{2}+\omega^{2}}\rightleftharpoons\sin\omega t$$
    $$i(t)=\frac{E_{0}}{L}\int_{0}^{t}e^{-R(t-\tau)/L}\sin\omega\tau\,d\tau$$
  - 化成复指数积分：
    $$=\frac{E_{0}}{L}e^{-Rt/L}\cdot\frac{1}{2i}\int_{0}^{t}\left[e^{(R/L+i\omega)\tau}-e^{(R/L-i\omega)\tau}\right]d\tau$$
  - 最终结果（两段：暂态 + 强迫振荡）：
    $$=\frac{E_{0}L\omega}{R^{2}+L^{2}\omega^{2}}e^{-Rt/L}+\frac{E_{0}}{R^{2}+L^{2}\omega^{2}}\left[R\sin\omega t-L\omega\cos\omega t\right]$$
- 例题/作业：例3 题面（$E(t)=E_0\sin\omega t$、开关闭合、初值 $i(0)=0$、求 $i(t)$）与完整解答见上。
- 图：右上角电路图——左边画交流电源符号并标 $E(t)$；上边画电阻标 $R$；右边画电感线圈标 $L$；下边画开关，开关旁标 $K$。串联回路。
- ⚠️存疑：无。第一项（暂态）系数为 $\dfrac{E_0L\omega}{R^2+L^2\omega^2}$，第二项（强迫）系数为 $\dfrac{E_0}{R^2+L^2\omega^2}$，图上清晰，不要与 p35 的 $E/R$ 混。

## p38 ｜ §6.4 应用·4 例4（弹簧振子强迫振动，$\omega\ne\omega_0$）
- 标题行：（接 §6.4）
- 中文要点：例4 一个质量为 $m$、弹性系数为 $k$ 的弹簧振子在外界强迫力 $f(t)=f_0\sin\omega t$ 的作用下，其运动方程为……；初始位移及速度均为 0，即 $x(0)=0$，$x^{(1)}(0)=0$，求 $x(t)$。／解：对振子的运动方程进行拉普拉斯变换，则有……；令 $\omega_0=\sqrt{k/m}$；则……；假设 $\omega\ne\omega_0$（即不会发生强迫共振），则上式改写为……。
- 公式：
  - 运动方程（题面）：
    $$m\frac{d^{2}x}{dt^{2}}+kx=f_{0}\sin\omega t$$
  - 取拉氏变换（注意这里把二阶导写成 $mp^2\left[X(p)-px(0)-x^{(1)}(0)\right]$）：
    $$mp^{2}\left[X(p)-px(0)-x^{(1)}(0)\right]+kX(p)=f_{0}\frac{\omega}{p^{2}+\omega^{2}}$$
  - 固有频率记号：
    $$\omega_{0}=\sqrt{k/m}$$
  - 化成两个标准像函数之积：
    $$X(p)=\frac{1}{mp^{2}+k}\cdot\frac{f_{0}\omega}{p^{2}+\omega^{2}}=\frac{f_{0}\omega}{m}\cdot\frac{1}{p^{2}+\omega_{0}^{2}}\cdot\frac{1}{p^{2}+\omega^{2}}$$
  - 非共振情形的部分分式改写：
    $$X(p)=\frac{f_{0}}{m}\cdot\frac{\omega}{\omega^{2}-\omega_{0}^{2}}\left[\frac{1}{p^{2}+\omega_{0}^{2}}-\frac{1}{p^{2}+\omega^{2}}\right]$$
  - 反演结果（蓝箭头指出的本页结论）：
    $$x(t)=\frac{f_{0}}{m}\cdot\frac{\omega}{\omega^{2}-\omega_{0}^{2}}\left[\frac{1}{\omega_{0}}\sin\omega_{0}t-\frac{1}{\omega}\sin\omega t\right]$$
- 例题/作业：例4 题面（$m$、$k$、$f(t)=f_0\sin\omega t$、$x(0)=0$、$x^{(1)}(0)=0$、求 $x(t)$）与解答（分 $\omega\ne\omega_0$ 情形）见上。
- 图：无（纯公式页）。
- ⚠️存疑：无。

## p39 ｜ §6.4 应用·4 例4 续（共振情形 $\omega=\omega_0$）
- 标题行：（接上页，无新标题）
- 中文要点：假设 $\omega=\omega_0$（即发生强迫共振），则上式改写为……。
- 公式：
  - 复述上页的像函数（起衔接作用）：
    $$X(p)=\frac{1}{mp^{2}+k}\cdot\frac{f_{0}\omega}{p^{2}+\omega^{2}}=\frac{f_{0}\omega}{m}\cdot\frac{1}{p^{2}+\omega_{0}^{2}}\cdot\frac{1}{p^{2}+\omega^{2}}$$
  - 共振情形（$\omega=\omega_0$，两个因子相同，分母变成平方）：
    $$X(p)=\frac{f_{0}}{m}\cdot\frac{\omega}{\left(p^{2}+\omega^{2}\right)^{2}}$$
  - 引用的反演（即 p33 例8 的结果）：
    $$\frac{\omega}{\left(p^{2}+\omega^{2}\right)^{2}}\rightleftharpoons-\frac{1}{2}\left(\frac{t\cos\omega t}{\omega}-\frac{\sin\omega t}{\omega^{2}}\right)$$
  - 共振解（本页结论）：
    $$x(t)=\frac{f_{0}}{2m}\left(\frac{1}{\omega^{2}}\sin\omega t-\frac{1}{\omega}t\cos\omega t\right)$$
- 例题/作业：例4 的第二种情形（共振），是上页题面在 $\omega=\omega_0$ 下的解答。
- 图：无。
- ⚠️存疑：无。注意本页 $x(t)$ 的两项：$+\frac{1}{\omega^2}\sin\omega t$ 与 $-\frac{1}{\omega}t\cos\omega t$（后者带 $t$，是共振的增长项）。

## p40 ｜ §6.4 应用·5 例5（微分方程组）
- 标题行：（接 §6.4）
- 中文要点：例5 利用拉普拉斯变换方法求解如下微分方程组……，其中初始条件为 $y(0)=1$ 及 $z(0)=3$。／解：进行拉普拉斯变换，则变成如下线性代数方程组……。
- 公式：
  - 题面方程组（大括号给出）：
    $$\begin{cases}\dfrac{dy}{dt}+2y+2z=10e^{2t}\\[6pt] \dfrac{dz}{dt}+z-2y=7e^{2t}\end{cases}$$
    初始条件：$y(0)=1,\ z(0)=3$
  - 变换后得到的线性代数方程组（左大括号）：
    $$\begin{cases}(p+2)Y(p)+2Z(p)-1=\dfrac{10}{p-2}\\[6pt] (p+1)Z(p)-2Y(p)-3=\dfrac{7}{p-2}\end{cases}$$
  - 解出的像函数（蓝箭头指向的右大括号）：
    $$\begin{cases}Y(p)=\dfrac{1}{p-2}\\[6pt] Z(p)=\dfrac{3}{p-2}\end{cases}$$
  - 反演结果（蓝箭头）：
    $$\begin{cases}y(t)=e^{2t}\\ z(t)=3e^{2t}\end{cases}$$
- 例题/作业：例5 题面（两个方程 + 初值 $y(0)=1$、$z(0)=3$）与解答三步见上。
- 图：无（纯公式页，用两个大括号 + 蓝色箭头表示流程）。
- ⚠️存疑：无。

## p41 ｜ §6.4 应用·6 第 2 类应用（计算特殊积分的值）开端
- 标题行：2、计算特殊积分的值
- 中文要点：利用留数定理，曾得到……；如果令 $a=t$，则……；对上式两边进行拉普拉斯变换，有……；对上式左边的积分进行计算，有……。
- 公式：
  1. 引用的旧结论（来自留数定理，本课件不重推）：
     $$\int_{0}^{\infty}e^{-ax^{2}}\cos(bx)dx=\frac{1}{2}\sqrt{\frac{\pi}{a}}\,e^{-b^{2}/4a}$$
  2. 令 $a=t$ 并两边乘 $\frac{2}{\pi}$ 后的形式：
     $$\frac{2}{\pi}\int_{0}^{\infty}e^{-x^{2}t}\cos(bx)dx=\frac{1}{\sqrt{\pi t}}e^{-b^{2}/(4t)}$$
  3. 两边对 $t$ 取拉普拉斯变换：
     $$\int_{0}^{\infty}\left[\frac{2}{\pi}\int_{0}^{\infty}e^{-x^{2}t}\cos(bx)dx\right]e^{-pt}dt=\int_{0}^{\infty}\left[\frac{1}{\sqrt{\pi t}}e^{-b^{2}/(4t)}\right]e^{-pt}dt$$
  4. 计算左边（先对 $t$ 积分，$\int_0^\infty e^{-(p+x^2)t}dt=\frac{1}{x^2+p}$）：
     $$I(t)=\frac{2}{\pi}\int_{0}^{\infty}\cos(bx)dx\int_{0}^{\infty}e^{-(p+x^{2})t}dt=\frac{2}{\pi}\int_{0}^{\infty}\frac{\cos(bx)}{x^{2}+p}dx$$
- 例题/作业：无编号例题（本节是「特殊积分」总法，p43/p44/p45 才是例6/7/8）。
- 图：无。
- ⚠️存疑：（a）左端结果被记作 $I(t)$，但它其实是 $t$ 的拉氏变换（应是 $p$ 的函数），记号与 p42 重复使用，易混；（b）引用式中的 $a$ 与被代入的 $t$ 混用，两步之间还夹了一次乘 $2/\pi$ 的整理，课件没有写。

## p42 ｜ §6.4 应用·7 用留数定理算出 $(1/\sqrt p)e^{-b\sqrt p}$ 的反演
- 标题行：（接上页，无新标题）
- 中文要点：假设 $b>0$ 及 $z=i\sqrt{p}$ 位于上半平面，则由留数定理得……；即……；或……；红字小结：这是一个非常重要的拉普拉斯变换的公式，将在第十章用到。
- 公式：
  - 假设条件：$b>0$，$z=i\sqrt{p}$ 位于上半平面。
  - 用留数定理算出左边积分：
    $$I(t)=\frac{2}{\pi}\int_{0}^{\infty}\frac{\cos(bx)}{x^{2}+p}dx=\pi i\frac{2}{\pi}\mathrm{Res}\left[\frac{e^{ibz}}{z^{2}+p}\right]_{z=i\sqrt{p}}=\frac{1}{\sqrt{p}}e^{-b\sqrt{p}}$$
  - 与右边对齐：
    $$\frac{1}{\sqrt{p}}e^{-b\sqrt{p}}=\int_{0}^{\infty}\left[\frac{1}{\sqrt{\pi t}}e^{-b^{2}/(4t)}\right]e^{-pt}dt$$
  - **重要变换对**（绿框，蓝箭头，本页核心结论）：
    $$\frac{1}{\sqrt{p}}e^{-b\sqrt{p}}\ \rightleftharpoons\ \frac{1}{\sqrt{\pi t}}e^{-b^{2}/(4t)}$$
  - 另一形式（绿框，标「或」，先对 $b$ 求导造出 $e^{-b\sqrt p}$ 的像）：
    $$e^{-b\sqrt{p}}=-\frac{d}{db}\left(\frac{1}{\sqrt{p}}e^{-b\sqrt{p}}\right)\ \rightleftharpoons\ \frac{b}{2\sqrt{\pi}\,t^{3/2}}\,e^{-\frac{b^{2}}{4t}}$$
- 例题/作业：无编号例题（是 p41 的收尾）。
- 图：无；两个绿框 + 一个蓝箭头。
- ⚠️存疑：留数计算 $\mathrm{Res}\left[\frac{e^{ibz}}{z^{2}+p}\right]_{z=i\sqrt{p}}$ 的求值细节全部省略（应得 $\frac{e^{-b\sqrt p}}{2i\sqrt p}$，再乘 $\pi i\frac{2}{\pi}$ 得 $\frac{1}{\sqrt p}e^{-b\sqrt p}$），页面上只见结果。

## p43 ｜ §6.4 应用·8 例6（$\int_0^\infty\frac{\cos tx}{x^2+a^2}dx$）
- 标题行：例6
- 中文要点：利用拉普拉斯变换方法计算积分 $I(t)=\int_0^\infty\dfrac{\cos(tx)}{x^2+a^2}dx$，其中 $a>0$。／解：积分式两边分别做拉普拉斯变换，则有……；利用留数定理，可以得到……；然后再进行反演，可以得到……。
- 公式：
  - 题面积分：
    $$I(t)=\int_{0}^{\infty}\frac{\cos(tx)}{x^{2}+a^{2}}dx,\qquad a>0$$
  - 两边取拉氏变换（用 $\cos(tx)\rightleftharpoons\dfrac{p}{p^2+x^2}$）并裂项：
    $$I(p)=\int_{0}^{\infty}\frac{1}{x^{2}+a^{2}}\cdot\frac{p}{p^{2}+x^{2}}dx=\frac{p}{p^{2}-a^{2}}\int_{0}^{\infty}\left[\frac{1}{x^{2}+a^{2}}-\frac{1}{x^{2}+p^{2}}\right]dx$$
  - 用留数定理算定积分（$\int_0^\infty\frac{dx}{x^2+\alpha^2}=\frac{\pi}{2\alpha}$）：
    $$I(p)=\frac{p}{p^{2}-a^{2}}\pi i\left[\frac{1}{2ai}-\frac{1}{2pi}\right]=\frac{\pi}{2a}\cdot\frac{1}{p+a}$$
  - 反演（本页结论）：
    $$I(t)=\frac{\pi}{2a}e^{-at}$$
- 例题/作业：例6 题面（积分式 + 条件 $a>0$）与解答三步见上。
- 图：无。
- ⚠️存疑：中间「$\pi i\left[\frac{1}{2ai}-\frac{1}{2pi}\right]$」这一步的两个留数（$\frac{1}{2ai}$、$\frac{1}{2pi}$）是直接给出的，没有画围道、也没说清是乘 $\pi i$ 还是 $2\pi i\cdot\frac12$。

## p44 ｜ §6.4 应用·9 例7（$\int_0^\infty\frac{\sin tx}{x}dx$）
- 标题行：例7
- 中文要点：利用拉普拉斯变换方法计算积分 $I(t)=\int_0^\infty\dfrac{\sin(tx)}{x}dx$，其中 $t>0$。／解：利用拉普拉斯变换 $\sin(tx)\rightleftharpoons\dfrac{x}{p^2+x^2}$；则有……；利用留数定理，有……；然后再进行反演，可以得到……。
- 公式：
  - 题面积分：
    $$I(t)=\int_{0}^{\infty}\frac{\sin(tx)}{x}dx,\qquad t>0$$
  - 引用的变换对（注意这里 $t$ 是「参数」、$x$ 是「时间样」的变量）：
    $$\sin(tx)\rightleftharpoons\frac{x}{p^{2}+x^{2}}$$
  - 取拉氏变换（$1/x$ 约掉）：
    $$I(p)=\int_{0}^{\infty}\frac{1}{x}\cdot\frac{x}{x^{2}+p^{2}}dx=\int_{0}^{\infty}\frac{1}{x^{2}+p^{2}}dx$$
  - 留数定理：
    $$I(p)=\pi i\,\mathrm{Res}\left[\frac{1}{z^{2}+p^{2}}\right]_{z=pi}=\frac{\pi}{2p}$$
  - 反演（本页结论）：
    $$I(t)=\frac{\pi}{2}$$
- 例题/作业：例7 题面（积分式 + 条件 $t>0$）与解答三步见上。
- 图：无。
- ⚠️存疑：留数求值 $\mathrm{Res}\left[\frac{1}{z^2+p^2}\right]_{z=pi}=\frac{1}{2pi}$ 未写出，直接从 $\pi i\,\mathrm{Res}$ 跳到 $\frac{\pi}{2p}$。

## p45 ｜ §6.4 应用·10 例8（$\int_0^\infty\frac{\sin^2 tx}{x^2}dx$）
- 标题行：例8
- 中文要点：利用拉普拉斯变换方法计算积分 $I(t)=\int_0^\infty\dfrac{\sin^2(tx)}{x^2}dx$，其中 $t>0$。／解：首先进行降幂处理，则……；对上式两边进行拉普拉斯变换（关于 $t$），有……；再利用留数定理，有……；最后进行反演，则得到……；即……，如果令 $t=1$，则……。
- 公式：
  - 题面积分：
    $$I(t)=\int_{0}^{\infty}\frac{\sin^{2}(tx)}{x^{2}}dx,\qquad t>0$$
  - 降幂（$\sin^2=\frac{1-\cos 2}{2}$）：
    $$I(t)=\int_{0}^{\infty}\frac{1}{x^{2}}\cdot\frac{1-\cos(2tx)}{2}dx$$
  - 两边对 $t$ 取拉氏变换并逐步化简：
    $$I(p)=\int_{0}^{\infty}\frac{1}{2x^{2}}\left[\frac{1}{p}-\frac{p}{p^{2}+4x^{2}}\right]dx=\frac{2}{p}\int_{0}^{\infty}\frac{dx}{p^{2}+4x^{2}}=\frac{1}{2p}\int_{0}^{\infty}\frac{dx}{x^{2}+p^{2}/4}$$
  - 留数定理（极点在 $z=\frac{p}{2}i$）：
    $$I(p)=\frac{1}{2p}\pi i\,\mathrm{Res}\left[\frac{1}{z^{2}+p^{2}/4}\right]_{z=\frac{p}{2}i}=\frac{\pi}{2}\cdot\frac{1}{p^{2}}$$
  - 反演（本页结论）：
    $$I(t)=\frac{\pi}{2}t$$
  - 即：$\displaystyle\int_{0}^{\infty}\frac{\sin^{2}(tx)}{x^{2}}dx=\frac{\pi}{2}t$
  - 令 $t=1$（蓝箭头指向的特例）：
    $$\int_{0}^{\infty}\frac{\sin^{2}x}{x^{2}}dx=\frac{\pi}{2}$$
- 例题/作业：例8 题面（积分式 + 条件 $t>0$）与解答四步见上，末行附 $t=1$ 的特例。
- 图：无；一个蓝箭头指向「如果令 $t=1$」的结论。
- ⚠️存疑：中间那步 $\frac{1}{2x^2}\left[\frac1p-\frac{p}{p^2+4x^2}\right]=\frac{2}{p}\cdot\frac{1}{p^2+4x^2}$ 的通分与系数（含 $\frac{2}{p}$）未写过程；$\mathrm{Res}$ 的具体值同样未给。

## p46 ｜ 第六章作业（第 2、3 题）
- 标题行：§ 第六章作业
- 中文要点：2.求下列像函数的反演；3.利用拉普拉斯变换求解如下常微分方程。
- 公式：逐题照抄——
  - 第 2 题（三个像函数求反演）：
    1) $\dfrac{6}{(p+1)^{2}}$
    2) $\dfrac{3p}{p^{2}-1}$
    3) $\dfrac{p}{\left(p^{2}+\omega^{2}\right)^{2}}\quad(\omega>0)$
  - 第 3 题（四个常微分方程用拉氏变换求解）：
    1) $\begin{cases}\dfrac{dy}{dt}+y=1\\[6pt] y(0)=0\end{cases}$
    2) $\begin{cases}\dfrac{dy}{dt}-y=-3e^{-2t}\\[6pt] y(0)=2\end{cases}$
    3) $\begin{cases}\dfrac{d^{2}y}{dt^{2}}+4\dfrac{dy}{dt}+4y=\sin\omega t\\[6pt] y(0)=y_{0}\\[4pt] y'(0)=y_{1}\end{cases}$
    4) $\begin{cases}\dfrac{d^{2}T}{dt^{2}}+a^{2}\omega^{2}T=f(t)\\[6pt] T(0)=T'(0)=0\end{cases}$
- 例题/作业：**作业页，无解答**。第 2 题三小题 + 第 3 题四小题，题面（函数、系数、初值）全部照抄如上。
- 图：无。
- ⚠️存疑：（a）第 3 题第 4 小题写成「$T(0)=\mathrm{T}'(0)=0$」，其中第二个 $T$ 用的是正体大写 $\mathrm{T}$（与斜体 $T$ 混排），排除是别的字母。（b）第 3 题第 3 小题的初值用的是 $y'$ 记法（与前面 $y^{(1)}$ 记法不同），原文如此。

---

## 跳步候选

> 采集标准：课件「直接给结论」「省掉中间推导」「换了定理形式／换了对谁求导」的地方。格式：页码 | 课件原文短语（中文原文）| 缺了什么。

1. p3 | 「如何克服上述两个局限」 | 只抛问题不答：为什么偏要乘**指数**衰减函数、为什么要求 $s>0$、单位阶跃函数与指数因子之间是什么关系，全留到 p4 才补，且 p4 也没有说明「为何指数函数能救绝对可积」的判据。
2. p5 | 「令 $p=s-i\omega$，且由于 $t\ge 0$，则 $G(\omega)=\frac{1}{2\pi}\int_0^\infty f(t)e^{-pt}dt$」 | 积分限从 $(-\infty,\infty)$ 缩到 $[0,\infty)$ 只用「$t\ge0$」一句带过，真正的依据是 $f(t)=0\,(t<0)$（p6 才补此说明）；另外 $F(p)=2\pi G(\omega)$ 里那个 $2\pi$ 归一因子从哪来也没交代。
3. p5 | 「由于 $dp=-id\omega$，则 $f(t)=-\frac{1}{2\pi i}\int_{s+i\infty}^{s-i\infty}F(p)e^{pt}dp$」 | 由 $p=s-i\omega$ 反解 $\omega$ 并代入 $e^{(s-i\omega)t}$、以及 $\omega:-\infty\to\infty$ 对应 $p:s+i\infty\to s-i\infty$ 的积分限换算被整段吞掉。
4. p6 | 「$p=s+i\sigma$ 为复数」 | 与 p5 刚推得的 $p=s-i\omega$ 符号相反且字母不同（$\sigma$ vs $\omega$），$\sigma$ 从未定义、也没说明 $\sigma$ 与虚部的关系。
5. p8 | 「方法2 $F(p)=\int_0^\infty t\cdot e^{-pt}dt=-\frac{d}{dp}\int_0^\infty e^{-pt}dt$」 | 求导号穿过积分号（莱布尼茨法则）需要的一致收敛条件没提，直接交换。
6. p10 | 「$=\frac{1}{2i}\left[\frac{1}{p-i\omega}-\frac{1}{p+i\omega}\right]$」 | 从 $\int_0^\infty e^{-(p-i\omega)t}dt$ 直接取成 $\frac{1}{p-i\omega}$，没有写「须 $\mathrm{Re}(p-i\omega)>0$ 才收敛」，收敛条件在例 2 提过一次，此处完全省略。
7. p13 | 「$\alpha F_1(P)+\beta F_2(p)$，其中 $\alpha$ 和 $\beta$ 为常数」 | 定理只给结论，没有收敛域要求；且 $F_1(P)$ 的 $P$ 为大写，与 $F_2(p)$ 不统一（疑笔误）。
8. p14 | 「推广到高阶导数 $f^{(n)}(t)$，则有 $f^{(n)}(t)\rightleftharpoons p^nF(p)-p^{n-1}f(0)-\cdots-f^{(n-1)}(0)$」 | 由 $n=1$ 一句「推广到」直接给出 $n$ 阶公式，既没有归纳法，也没有逐次分部积分展示中间项。
9. p15 | 「根据导数定理I，有 $p^2F(p)-p+\omega^2F(p)=0$」 | 省掉把 $f(0)=1$、$f^{(1)}(0)=0$ 代入 $p^2F(p)-pf(0)-f^{(1)}(0)$ 的那一步（$-p$ 从哪来没有写）；题面还把初值 $f^{(1)}(0)$ 误写成 $f^{(1)}(t)$。
10. p16 | 「即 $(-t)^n f(t)\rightleftharpoons \frac{d^nF(p)}{dp^n}$」→「$t^nf(t)\rightleftharpoons(-1)^n\frac{d^nF(p)}{dp^n}$」 | 从 $(-t)^n$ 换成 $t^n$ 需写明 $(-t)^n=(-1)^nt^n$ 并把 $(-1)^n$ 移项，这一步被压缩成一句「即」；$d^n/dp^n$ 与 $\int$ 交换次序同样未论证。
11. p18 | 「其中利用了 $g(0)=0$」 | 没有说明 $g(0)=\int_0^0f(\tau)d\tau=0$ 为何成立；「根据导数定理」也没指明是 p14 的 $n$ 阶一般式还是 $n=1$ 的形式。
12. p19 | 「如果当 $a<0$ 时，则 $\int_0^\infty f(at)e^{-pt}dt=\frac{1}{a}\int_0^{-\infty}f(y)e^{-\frac{p}{a}y}dy$」 | $a<0$ 一支只写到换限就断了，既没翻正上下限、也没给最终公式，而定理本身只声明 $a>0$——这个分支实际上没有结论。
13. p20 | 「根据相似性定理，有 $e^{\alpha t}\rightleftharpoons\frac{1}{a}\cdot\frac{1}{p/a-1}=\frac{1}{p-a}$」 | 把 $e^t$ 中的 $t$ 换成 $at$ 的字母替换过程省略（题面用 $\alpha$、结果用 $a$），也没说明相似性定理要求 $a>0$ 而 $\alpha$ 可以任意。
14. p21 | 「利用这个定理，就可以得到：$e^{-\lambda t}\sin\omega t\rightleftharpoons\frac{\omega}{(p+\lambda)^2+\omega^2}$」 | 只写「利用这个定理」，没有展示把 $F(p)=\frac{\omega}{p^2+\omega^2}$ 中的 $p$ 整体换成 $p+\lambda$ 的那一步。
15. p22 | 「为满足 $f(t-t_0)$ 有意义，要求 $t\ge t_0$」 | 用「有意义」代替了真正的条件：$t<t_0$ 时须 $f(t-t_0)=0$（因果性/截断），这也正是积分限从 $0$ 改成 $t_0$ 的依据；末行的等价箭号还渲染成方框「□」。
16. p23 | 「$f_1(t)*f_2(t)\rightleftharpoons F_1(p)F_2(p)$」 | 卷积的定义式 $f_1*f_2=\int_0^t f_1(t-\tau)f_2(\tau)d\tau$ 没有单独给出，只在证明的方括号里露一次；卷积的可交换性（为何可写成 $f_1(t-\tau)f_2(\tau)$ 而非 $f_1(\tau)f_2(t-\tau)$）也未提。
17. p24 | 「两种方法，积分区域相同，因此积分结果也相同」 | 交换二次积分次序的合法性（Fubini / 一致收敛）只用「区域相同」一句代替，没有给出区域不等式 $0\le\tau\le t<\infty$ 的完整描述。
18. p26 | 「1. …分解成几个简单的像函数之和；2. …分解成两个简单的像函数的乘积；3. 经过其它的数学操作…」 | 只给了三条「思路」，没有给手段：部分分式分解怎么做、待定系数怎么定、什么情形该用卷积、什么情形该对参数求导，全部不写。
19. p27 | 「$=\frac{1}{b^2-a^2}\left(\frac{1}{p^2+a^2}-\frac{1}{p^2+b^2}\right)$」 | 裂项的待定系数求解（设 $\frac{1}{(p^2+a^2)(p^2+b^2)}=\frac{A}{p^2+a^2}+\frac{B}{p^2+b^2}$ 解 $A,B$）完全省略，直接给分解结果。
20. p29 | 「思路：$\frac{1}{p}-\frac{1}{(p-1)^2}=\frac{p^2-3p+1}{p(p-1)^2}$，$\frac{1}{p}+\frac{1}{(p-1)^2}=\frac{p^2-p+1}{p(p-1)^2}=\frac{1}{p(p-1)^2}+\frac{p^2-p}{p(p-1)^2}$」 | 两行是「试算草稿」，从试算到 $F(p)=\frac1p-\frac{1}{p-1}+\frac{1}{(p-1)^2}$ 的拼接逻辑没有交代；读者无法从这两行唯一还原分解思路。
21. p30 | 「思路：$\frac{1}{p^2}+\frac{1}{p-1}=\frac{p-1+p^2}{p^2(p-1)}$，$\frac{1}{p^2}-\frac{1}{p-1}=\frac{p-1-p^2}{p^2(p-1)}=-\frac{1}{p^2(p-1)}-\frac{p^2-p}{p^2(p-1)}$」 | 同 p29：试算草稿直接跳到 $F(p)=\frac{1}{p^2}-\frac{1}{p-1}+\frac{1}{p}$，中间的「取负号凑出目标」这一步没有说明。
22. p31 | 「$=\frac{1}{\omega^2+\alpha^2}\left(\alpha\sin\omega t-\omega\cos\omega t+\omega e^{-\alpha t}\right)$」 | 从 $\frac{1}{2i}\left[\frac{e^{i\omega t}}{\alpha+i\omega}-\frac{e^{-i\omega t}}{\alpha-i\omega}\right]-\frac{1}{2i}e^{-\alpha t}\left[\frac{1}{\alpha+i\omega}-\frac{1}{\alpha-i\omega}\right]$ 化成实函数，中间的通分、取实部、合并同类项全部省略，是本页跨度最大的一步。
23. p32 | 「由于 $\frac{d}{d\omega}\frac{p}{p^2+\omega^2}=-\frac{2\omega p}{(p^2+\omega^2)^2}$」 | 这里对**参数 $\omega$** 求导来做反演，而课件已讲的只有对 **$p$** 求导的导数定理 II；「对参数求导还能否与拉氏反演交换」这一合法性依据完全没提。
24. p34 | 「如果 $\int_p^\infty F(q)dq$ 存在，且当 $t\to 0$ 时，$|f(t)/t|$ 有界，则…」 | 定理条件 $|f(t)/t|$ 有界是突然出现的，没有解释它对应换序/收敛的哪一环；随后示范计算里积分变量又从 $q$ 换成 $p$，两个哑变量混用。
25. p36 | 「即 $I(p)=\frac{q_0}{LCp^2+1}=\frac{q_0}{\sqrt{LC}}\cdot\frac{\sqrt{1/LC}}{p^2+1/LC}$」 | 从 $L[pI-i(0)]+\frac{1}{C}\frac{I}{p}=\frac{q_0}{C}\frac{1}{p}$ 解出 $I(p)$ 的代数整理（两边乘 $p$、提取 $LCp^2+1$）以及为凑标准形而同乘 $\sqrt{LC}$ 的技巧都没写。
26. p37 | 「$=\frac{E_0L\omega}{R^2+L^2\omega^2}e^{-Rt/L}+\frac{E_0}{R^2+L^2\omega^2}\left[R\sin\omega t-L\omega\cos\omega t\right]$」 | 从复指数积分 $\frac{E_0}{L}e^{-Rt/L}\frac{1}{2i}\int_0^t\left[e^{(R/L+i\omega)\tau}-e^{(R/L-i\omega)\tau}\right]d\tau$ 一步跳到最终实式，中间的复数除法、取实部、以及「哪一项算暂态、哪一项算强迫」的判据都是直接给的。
27. p38–p39 | 「假设 $\omega\ne\omega_0$（即不会发生强迫共振），则上式改写为…」／「假设 $\omega=\omega_0$（即发生强迫共振），则上式改写为…」 | 两种情形的部分分式改写（非共振时拆成 $\frac{1}{p^2+\omega_0^2}-\frac{1}{p^2+\omega^2}$ 并配 $\frac{\omega}{\omega^2-\omega_0^2}$；共振时分母合并成平方）都只给结果，拆分与配系数过程省略；共振解还直接引用了 p33 例8 的反演式。
28. p40 | 「解：进行拉普拉斯变换，则变成如下线性代数方程组 … （直接给出 $Y(p)=\frac{1}{p-2}$，$Z(p)=\frac{3}{p-2}$）」 | 二元一次方程组的消元/代入过程全被跳过；也没说明为什么解出来的 $Y,Z$ 分母恰好都只剩 $p-2$（分母 $(p-1)(p+2)$ 之类的约掉）。
29. p41 | 「利用留数定理，曾得到 $\int_0^\infty e^{-ax^2}\cos(bx)dx=\frac{1}{2}\sqrt{\frac{\pi}{a}}e^{-b^2/4a}$」 | 该公式本身来自复变/留数部分，课件只引用不推导；此外从它到「令 $a=t$ 后两边乘 $\frac{2}{\pi}$」的系数整理（$\frac{2}{\pi}\cdot\frac{1}{2}\sqrt{\pi}=\frac{1}{\sqrt{\pi}}$）也没写。
30. p42 | 「则由留数定理得 $I(t)=\frac{2}{\pi}\int_0^\infty\frac{\cos(bx)}{x^2+p}dx=\pi i\frac{2}{\pi}\mathrm{Res}\left[\frac{e^{ibz}}{z^2+p}\right]_{z=i\sqrt{p}}=\frac{1}{\sqrt{p}}e^{-b\sqrt{p}}$」 | 留数的实际求值（$\left.\frac{e^{ibz}}{2z}\right|_{z=i\sqrt p}=\frac{e^{-b\sqrt p}}{2i\sqrt p}$）与「为何是 $\pi i\cdot\frac{2}{\pi}$ 而不是 $2\pi i$」都没写；「将在第十章用到」只是预告，没有说明用途。
31. p43 | 「利用留数定理，可以得到 $I(p)=\frac{p}{p^2-a^2}\pi i\left[\frac{1}{2ai}-\frac{1}{2pi}\right]$」 | 两个定积分 $\int_0^\infty\frac{dx}{x^2+a^2}$、$\int_0^\infty\frac{dx}{x^2+p^2}$ 的留数值直接给出（应为 $\frac{\pi}{2a}$、$\frac{\pi}{2p}$），围道选择与「实轴积分 = $\pi i\times$ 上半平面留数」的依据也未说明。
32. p44 | 「利用留数定理，有 $I(p)=\pi i\mathrm{Res}\left[\frac{1}{z^2+p^2}\right]_{z=pi}=\frac{\pi}{2p}$」 | $\mathrm{Res}\left[\frac{1}{z^2+p^2}\right]_{z=pi}=\frac{1}{2pi}$ 这一步没写出，读者看到的是「留数 → $\frac{\pi}{2p}$」的直接跳跃。
33. p45 | 「$I(p)=\int_0^\infty\frac{1}{2x^2}\left[\frac{1}{p}-\frac{p}{p^2+4x^2}\right]dx=\frac{2}{p}\int_0^\infty\frac{dx}{p^2+4x^2}=\frac{1}{2p}\int_0^\infty\frac{dx}{x^2+p^2/4}$」 | 括号内通分得 $\frac{4x^2}{p(p^2+4x^2)}$、与前面的 $\frac{1}{2x^2}$ 约简为 $\frac{2}{p(p^2+4x^2)}$，再提出 $4$ 凑成 $\frac{p^2}{4}$ —— 三次系数整理合一，全部省略。
