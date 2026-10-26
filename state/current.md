# 当前状态事实卡（state/current.md）

> **本文件由 `python -B tools/current_state.py` 生成，勿手工编辑**（派生视图）。
> 这是**跨窗口续学的唯一事实来源**：`AGENTS.md` / `CLAUDE.md` 的 STATUS 与
> `plan/handoff-CURRENT.md` 都**引用**它，不再各写一份叙述。
> 生成于 **2026-10-26**（中国时间；系统英国日期 2026-10-26）。
> 事实源指纹：`attempts.jsonl` 52 条（sha256 `1388bfe3d536…`）＋ `corrections.jsonl` 55 条。
> 手写意图（下一步想做什么、为什么暂缓）不在这里：见 `.tutor/config/status-narrative.yml`、`plan/today-<日期>.md`、`plan/gaps.md`。

## ① 现在到哪了（按课程，全部由程序重算）

**06-电工电子技术** — 独立求解电工电子技术 交流电路（Chapter Two）计算题（`ee-ac-circuits`，状态 active，里程碑 2026-10-24）

| 目标 | 覆盖 | 等级 | 独立通过 | 未解决困难 |
|---|---|---|---|---|
| `ee.ac.phasor-impedance` | 已独立通过·待延迟复测 | 曾独立完成 | 2026-09-28 | — |
| `ee.ac.reactance` | 已独立通过·待延迟复测 | 延迟通过 | 2026-09-28、2026-09-30 | — |
| `ee.ac.resonance` | 已独立通过·待延迟复测 | 曾独立完成 | 2026-09-28 | — |
| `ee.ac.series-rlc` | 已独立通过·待延迟复测 | 曾独立完成 | 2026-09-28 | — |

**01-理论力学** — 独立求解理论力学 Topic 4 守恒定律问题（`tm-t4-conservation-laws`，状态 active，里程碑 2026-10-23）

| 目标 | 覆盖 | 等级 | 独立通过 | 未解决困难 |
|---|---|---|---|---|
| `tm.t3.lagrangian-construction` | 已安排·未作答 | 未测 | — | — |
| `tm.t4.angular-momentum-integral` | 已作答·需补练 | 需支持 | — | — |
| `tm.t4.cyclic-momentum` | 已作答·需补练 | 需支持 | — | — |
| `tm.t4.direct-check` | 已独立通过·待延迟复测 | 曾独立完成 | 2026-09-28 | — |
| `tm.t4.energy-criteria` | 已作答·需补练 | 需支持 | — | hurdle-1 |
| `tm.t4.energy-integral` | 已独立通过·待延迟复测 | 曾独立完成 | 2026-09-28 | — |
| `tm.t4.mechanical-similarity` | 已安排·未作答 | 未测 | — | — |
| `tm.t5.central-motion-types` | 已作答·需补练 | 需支持 | — | hurdle-4 |
| `tm.t5.effective-potential` | 已作答·需补练 | 需支持 | — | hurdle-4 |
| `tm.t5.law-of-motion` | 已作答·需补练 | 需支持 | — | — |
| `tm.t5.potential-analysis` | 已作答·需补练 | 需支持 | — | — |
| `tm.t5.turning-points` | 已作答·需补练 | 需支持 | — | — |

**03-微分方程** — 独立求解常系数线性系统 Y′ = AY（微分方程·方程组章）（`ode-systems-const-coeff`，状态 active，里程碑 2026-11-09）

| 目标 | 覆盖 | 等级 | 独立通过 | 未解决困难 |
|---|---|---|---|---|
| `ode.integrating-factor` | 已安排·未作答 | 未测 | — | — |
| `ode.sys.case-complex` | 已作答·需补练 | 需支持 | — | — |
| `ode.sys.case-repeated` | 已作答·需补练 | 需支持 | — | — |
| `ode.sys.eigen-basic` | 已作答·需补练 | 需支持 | — | — |
| `ode.sys.ivp` | 未安排（无题目） | 未测 | — | — |

**11-英语-雅思** — 雅思训练：听力 8.0 / 口语 7.0 / 写作冲高（均分 7.5 通路）（`ielts-english-75`，状态 active）

| 目标 | 覆盖 | 等级 | 独立通过 | 未解决困难 |
|---|---|---|---|---|
| `en.listen.decoding` | 未安排（无题目） | 未测 | — | — |
| `en.listen.structure` | 未安排（无题目） | 未测 | — | — |
| `en.read.timed` | 未安排（无题目） | 未测 | — | — |
| `en.speak.fc` | 未安排（无题目） | 未测 | — | — |
| `en.speak.gra` | 未安排（无题目） | 未测 | — | — |
| `en.speak.lr` | 未安排（无题目） | 未测 | — | — |
| `en.speak.pr` | 未安排（无题目） | 未测 | — | — |
| `en.write.cc` | 已作答·需补练 | 需支持 | — | — |
| `en.write.gra` | 已作答·需补练 | 需支持 | — | — |
| `en.write.lr` | 已作答·需补练 | 需支持 | — | — |
| `en.write.tr` | 已作答·需补练 | 需支持 | — | — |

**13-AI技术学习** — 独立完成 C00 编程与开发衔接（解释器/环境/容器/函数/文件/调试/Git/Notebook）（`ai-tech-c00`，状态 active）

| 目标 | 覆盖 | 等级 | 独立通过 | 未解决困难 |
|---|---|---|---|---|
| `ai-tech.c00-01` | 已安排·未作答 | 未测 | — | — |
| `ai-tech.c00-02` | 未安排（无题目） | 未测 | — | — |
| `ai-tech.c00-03` | 未安排（无题目） | 未测 | — | — |
| `ai-tech.c00-04` | 未安排（无题目） | 未测 | — | — |
| `ai-tech.c00-05` | 未安排（无题目） | 未测 | — | — |
| `ai-tech.c00-06` | 未安排（无题目） | 未测 | — | — |
| `ai-tech.c00-07` | 未安排（无题目） | 未测 | — | — |
| `ai-tech.c00-08` | 未安排（无题目） | 未测 | — | — |

**（未归入能力目标）**（未在 goals.yaml 归入能力目标）

| 目标 | 覆盖 | 等级 | 独立通过 |
|---|---|---|---|
| `ee.dc.kcl` | 已独立通过·待延迟复测 | 曾独立完成 | 2026-09-30 |
| `ee.dc.source-vs-load` | 已作答·需补练 | 需支持 | — |
| `ee.dc.steady-state` | 已作答·需补练 | 需支持 | — |
| `mp.delta-function` | 已安排·未作答 | 未测 | — |
| `mp.fourier-series` | 已安排·未作答 | 未测 | — |
| `mp.fourier-transform` | 已安排·未作答 | 未测 | — |
| `mp.isolated-singularity` | 已作答·需补练 | 需支持 | — |
| `mp.laplace-inverse` | 已安排·未作答 | 未测 | — |
| `mp.laplace-ode` | 已安排·未作答 | 未测 | — |
| `mp.laplace-transform` | 已安排·未作答 | 未测 | — |
| `mp.laurent-expansion` | 已作答·需补练 | 需支持 | — |
| `mp.power-series-radius` | 已独立通过·待延迟复测 | 曾独立完成 | 2026-10-03 |
| `mp.residue-applications` | 已作答·需补练 | 需支持 | — |
| `mp.residue-computation` | 已独立通过·待延迟复测 | 曾独立完成 | 2026-10-01 |
| `mp.residue-definition` | 已作答·需补练 | 需支持 | — |
| `mp.taylor-expansion` | 已独立通过·待延迟复测 | 曾独立完成 | 2026-10-03 |
| `ode.clairaut` | 已作答·需补练 | 需支持 | — |
| `ode.const-coeff-homogeneous` | 已作答·需补练 | 需支持 | — |
| `ode.exact-integ factor` | 已作答·开卷/受助通过 | 需支持 | — |
| `ode.first-order-linear` | 已作答·需补练 | 需支持 | — |
| `ode.homogeneous` | 已作答·需补练 | 需支持 | — |
| `ode.order-reduction` | 已作答·需补练 | 需支持 | — |
| `ode.riccati` | 已作答·需补练 | 需支持 | — |
| `ode.separable` | 已作答·需补练 | 需支持 | — |
| `ode.sys.cayley-hamilton` | 已安排·未作答 | 未测 | — |
| `ode.sys.matrix-exp` | 已安排·未作答 | 未测 | — |
| `ode.system-reduction` | 已作答·需补练 | 需支持 | — |
| `ode.undetermined-coefficients` | 已作答·需补练 | 需支持 | — |
| `ru.adj-agreement` | 已安排·未作答 | 未测 | — |
| `ru.noun-forms` | 已作答·需补练 | 需支持 | — |
| `ru.noun-gender` | 已作答·需补练 | 需支持 | — |
| `ru.qword-agreement` | 已独立通过·待延迟复测 | 曾独立完成 | 2026-09-30 |
| `ru.qword.kakoy-agreement` | 已安排·未作答 | 未测 | — |
| `ru.syntax.chto-clause` | 已安排·未作答 | 未测 | — |
| `ru.syntax.potomy-chto` | 已安排·未作答 | 未测 | — |
| `ru.verb.znat-dumat` | 已安排·未作答 | 未测 | — |

## ② 最近有效证据（最近 4 条作答事件）

| 事件 | 日期 | 题目 | 模式 | 提示 | 结果 | 曝光 | 目标 |
|---|---|---|---|---|---|---|---|
| `attempt-53` | 2026-10-19 | `tm-h5-02` | practice | H4 | partial | full@before_attempt | `tm.t5.effective-potential` |
| `attempt-52` | 2026-10-19 | `tm-t5-ueff-variant-01` | practice | H1 | partial | partial@before_attempt | `tm.t5.effective-potential` |
| `attempt-51` | 2026-10-14 | `de-gap-attack-01` | practice | H3 | partial | partial@before_attempt | `ode.homogeneous` |
| `attempt-49` | 2026-10-13 | `ode-l15-hw-01` | practice | H3 | correct | partial@before_attempt | `ode.sys.eigen-basic` |

> 「有效证据」= 能支持或推翻「独立掌握」的作答；
> **受助/曝光的作答也算证据**——它证明的是「当时需要帮助」，不是「已经会了」。

## 暂停与未完成题续学点

- `obs-4`（02-光学；来源 本会话 2026-10-08 学习者原话「我大概看懂了，但是现在精力有些不足，我晚上推导完给你」）：【暂停·2026-10-08 上午】学习者自述「大概看懂了，但现在精力有些不足，我晚上推导完给你」→ 会话暂停，晚上续。四要素：①【有效步骤】微分方程定位卷 A/B（11 题，题源＝老师课件 L1–11 的 Homework 页）**已做完**，照片待交（学习者在部分题下写了问题与当前理解）；光学第一课已讲完：为什么必须傍轴（严格关系式右边「−4r sin²(φ/2)[…]」就是非傍轴量）、傍轴条件两种写法、近轴物像公式「n/s + n′/s′ = (n′−n)/r」、焦点焦距「f′ = n′r/(n′−n)」、放大率「V = −s′n/(sn′)」，并示范 s=30 → s′=90、V=−2。②【卡点/障碍】精力不足（自述）；光学零基础起步；刚讲清「傍轴＝前提／物像公式＝结论」的区别（由学习者提问引发，补充见讲义 §5.1）。③【失败尝试】无（尚未作答，无错误可写）。④【下次首个动作】按序：(a) 交微分方程定位卷照片（含题下手写问题；读不准的只圈局部确认）；(b) 光学 (a) n=1、n′=1.5、r=10cm、s=60cm 求 s′、虚实、V；(c) 光学 (b) 傍轴判断三问（h=3cm：h/r、sin φ≈φ 的误差、是否还算傍轴）；(d) 今日 12:30 后形势与政策选课（窗口开，10-10 17:00 截止）。另有俄语线（先回补 УРОК 1–6 遗忘点再学 УРОК 7，10-13 前）与理论力学 H5.1（10-12 交），已排入 plan/today-2026-10-08.md。
- `tm-h5-02` / `attempt-53`：尚未完成；本题解答已于 2026-10-19 会话中完整给出（U_eff 与两端、驻点方程 αr² − βr + 3γ = 0、穿零轴 Δ = β² − 4αγ、五档草图）。学习者本次为誊写：自己重写 U_eff = −αr⁻¹ + βr⁻² − γr⁻³ = −r⁻³(αr² − βr + γ)，两个判别式与草图均与解答一致；过程中自行补出了用二次方程求根公式解驻点那一步。属受助后整理，不计独立证据。；第③问按骨架写成三档：A（β² < 3αγ）E<0 一个转向点、允许区 (0, r_a) 落向中心，E≥0 全 r 允许——两条都对；B（3αγ < β² < 4αγ）E≥0 全允许、(0,r_a)∪(r_b,r_c) 对应落向中心或环内有限运动——结构对，但分界标签有笔误（把 U_max 写成 U(r₂)，且「E < U(r₁)」那一行与上一行重复），E = U(r₂) 只写了落向中心、漏了稳定圆轨道。C（β² > 4αγ）只留了骨架（E > U(r₂)、E ∈ (U(r₁),U(r₂))、E < U(r₁)、E = U(r₁)/U(r₂)），未按零轴拆分 E 区间，尚未完成。
- `tm-t5-ueff-variant-01` / `attempt-52`：尚未完成；U_eff = ½kr² + L²/(2mr²) 写对；导数 kr − (L²/m)r⁻³ 与因式分解 r⁻³(kr⁴ − L²/m) 完全正确；两端极限与草图（单一口袋、两端 +∞）正确；「不用按参数分类」的结论正确但理由只写了半句。错误：驻点写成 r₀ = L/∜(mk)［分母 √[4]{mk} 已放大重读，分子是否为 √L 存疑，标「待确认」不据此改判］，按自己上一行的 kr⁴ = L²/m 应为 (L²/(mk))^(1/4)；最小能量写成 ½L²/m + ½k，量纲已不成立（k 为 N/m，非能量），正确为 L√(k/m) = k r₀²。；E ≥ U_min 的判据方向正确；E > U_min 判为 oscillation（环内有限运动）、并明确写「不会落向中心、不会无界运动，因为有限」——三处运动类型判断全对。缺口在临界点：纸上「E = E_min 静止」［手写放大后读作「静止」，若实为「圆轨道」则不成立，标「待确认」］；E = E_min 时应为半径 r₀ 的圆轨道（径向动能 0、φ̇ = L/(mr²) ≠ 0），即课件 p11『转向点不是停住点』。；E = U_eff 得 km r⁴ − 2mE r² + L² = 0，解出 r² = [E ± √(E² − kL²/m)]/k，再开平方得两个转向点——与标准答案一致；外侧多余的 ± 只是写法冗余（半径取正），不影响结论。这是全卷最好的一步。
- `tm-h5-01` / `attempt-47`：尚未完成；【H5.1 草稿·子任务 1】因式分解正确：U′ = −2Aα e^(−αx)(e^(−αx) − 1) ⟹ 唯一驻点 x = 0；U(0) = −A 为极小 ✓；已画草图（左端 → +∞、右端趋 0⁻、穿零在 −ln2/α）✓；并写出 E ≥ U_min = −A ✓。帮助史：导师当日先讲模块 A（能量积分/允许区/转向点）与「从表达式到草图的五步法」（示范用 U = x⁴/4 − x²/2），并在学习者自述会做后**确认了「驻点 x = 0、U_min = −A」这一行** ⟹ 本目标答案已部分曝光（before_attempt），不计独立。草图细节（右端是否贴 0⁻ 渐近）照片不易判定，故标待核验。；【子任务 2–3】令 u = e^(−αx) ⟹ A(u² − 2u) = E ⟹ u = 1 ± √(1 + E/A)（草稿写作 (A ± √(A² + AE))/A，等价）✓；x = −(1/α)·ln u ✓ **完全正确**。缺一句严谨性：**E > 0 时 u₋ < 0 无效**（只剩一个转向点）、**E = 0 时 u₋ = 0 对应 x → +∞**（不是有限转向点）——这两句正是「E ≥ 0 无限运动」的理由，应交作业时补上。帮助史：导师给过「令 u = e^(−αx) 会变成二次方程」这一关键替换提示（H2–H3）⟹ 不计独立。；【子任务 4｜**未完成**】草稿由 ẋ₀ > 0 取 + 支（ẋ = √(2(E−U)/m)），写出 **t = ±√(m/2)·∫(x₀ → x) dx/√(E−U)** —— **变上限积分的形式正确**（这是本目标的关键结构）；但**没有把积分做出来**，因此尚未得到 x(t)。运动类型分类正确：E = −A 静止（motionless）✓、−A < E < 0 有限振荡（finite motion, oscillation）✓、E ≥ 0 无限（infinite motion）✓（E = 0 的临界性未单独说明）。下一步（导师给到 H3）：配方 E − U = (E + A) − A(e^(−αx) − 1)²，换元 y = e^(−αx) − 1（dx = −dy/(α(y+1))），化为标准型 ∫dy/((y+1)√(a² − y²))，a² = 1 + E/A，积出后反解 y(t) → x(t)，并按 E 区间分段/延拓。
- `mp1-ch4-hw-01` / `attempt-46`：尚未完成；【§4.1／§4.2 复习】学习者自述「只学到留数定理，而且忘了」。复习从「a₋₁ 为什么特别」开始：她答『这一项的积分是多值的，不能用柯西积分定理直接化成零，自然就保留下来了』——**机制正确**（这正是 2026-10-01 `mp1-ch4-quiz-01` 留下的唯一缺口）。导师随后给出参数化推导 ∮(z−z₀)ⁿdz：n=−1 时 = 2πi（与 r 无关）、n≠−1 时 = 0。三条规则的适用条件讲清后，她能自行判出「cos z/z³ 不能用规则 II（分子非多项式）→ 改用洛朗展开」，并在下一轮主动说出「奇点在 0，阶数是 3，洛朗展开做」——三处全对。留数定理的公式、围道条件、求和范围 2026-10-01 已对，本次无新错。；【第 1 组 4 题】Q2（cos z/z³）：**独立**——自己判出三阶极点、自己用洛朗展开取 a₋₁ = −1/2；唯一错在誊写漏乘 2πi（导师指出后改 −πi）。Q3（1/(z sin z)）：**独立**——判二阶极点、用规则 III 得 Res=0、∮=0 ✓。Q4（e^(2z)/(z²+1)）：**独立**——规则 II 两次都用对（e^(2i)/(2i) 与 e^(−2i)/(−2i)）；缺口是**最后没收成实数形式**，导师展开复数指数后得 2πi sin 2。Q1（1/((z²+1)²(z−1))）：导师当模板逐步讲，学习者算出 Res(i) 时中途卡住，**最终未独立完成**（Σ Res 应为 0，她一度得 1/2）。⚠ 导师在本题上前后手算错误、判读矛盾多次，学习者的错误定位因此不可靠。；【§4.3 三类实积分，第 2／3／4 组】此前**完全未学**，本次从零建立。【类型 1 有理三角】三条换元式给出后，学习者**独立**做对 3 题：∫₀^{2π}dθ/(2+cos θ)=2√3π/3 ✓、∫₀^{2π}dθ/(1+sin²θ)=√2π ✓、∫₀^{2π}dθ/(1+cos²θ)=√2π ✓；第 2 题（1+εcos θ)² 在**通分处挂错 ε 的位置**（写成 ε 在分子），导师指出后当天补做正确，得 2π/(1−ε²)^(3/2)。【类型 2 有理函数无穷积分】模板给出后独立做对：π/3 ✓、√2π/(4a) ✓、π/(2a) ✓（中间在 z⁴+a⁴ 的根上**自加了一个不存在的「a>1/a<1」条件**把自己堵死；另在「−i³ = +i」处符号翻掉，导致 −π/(2a)）。【类型 3 约当引理】4(1) 独立得 π(2e^(−m)−e^(−2m))/6（含 z=2i 处漏写负号笔误）✓；4(2) 独立得 π/e ✓（错在把 e^(imz₀) 代成 e^(2imz₀)，改正后对）；4(3) **未完成**——求导式本身正确（含 im z² 项），但代 z₀=ai 化简时丢了 i、分母出 a³，得 m e^(−am)/(8a³)（应为 m e^(−am)/(4a)）。【共同卡点】复数代数的符号与 i 的幂：−i³、i³、(2ai)²、(2ai)³ 这几处反复出错；**数值代入自检（a=1、m=1）一次都没用过**。
- `de-midterm-diag-01` / `attempt-50`：尚未完成；A1 (e^v+1)cos u du + e^v(sin u+1)dv = 0：**分离变量与两边积分全对**（ln(sin u+1) = −ln(e^v+1)）；缺口＝①漏积分常数 C（自己写「不知要化成怎样」即卡在此）；②未写隐式解 (sin u+1)(e^v+1)=C；③未补除以 (sin u+1) 时丢掉的常数解 sin u = −1（u = −π/2 + 2kπ）。属收尾规范类缺口，不是方法不会。；A2 y′ = y/x + x³/y：**写「不会」**。识别失败：它不是普通齐次（y/x 与 x³/y 在 x→kx,y→ky 下缩放不同次），而是**准齐次**（x→kx、y→k²y 时两项同次）→ 令 u = y/x² 可分离；或看成 **Bernoulli**（y′ − y/x = x³y^{−1}，n=−1）令 v=y²。答案 y² = x⁴ + Cx²（未作答）。；A3 (Ax³y+y³)dx+(x⁴+3xy²)dy=0：**全对**——∂P/∂y = Ax³+3y²、∂Q/∂x = 4x³+3y² ⟹ **A=4**；再积分得 W = x⁴y + xy³ = C ✓。本块无缺口。；B1 cosθ dr + (r sinθ − cos⁴θ)dθ = 0：**化标准形、积分因子公式、r = (1/cosθ)(∫cos³θ dθ + C) 全对**；唯一卡点＝**不会积 ∫cos³θ dθ**（拆 cos³ = cosθ(1−sin²θ) → sinθ − sin³θ/3）。属积分技巧类缺口。；A4 x³y′ + 2x²y + 2x⁴y² = 18：化成 y′ + (2/x)y + 2xy² = 18/x³ 的方向对，但**找不到特解**（自述「找不到特解，也用不上洛卡蒂」）。缺口＝**观察法找特解**：试 y = c x^n（此处 y = c/x² 代入得 2c² = 18 ⟹ y₁ = ±3/x²，取 y₁ = 3/x²），再令 y = y₁ + 1/v 化线性。；B2 y = xy′ − y′²：先设 w = y′ = dy/dx 后**卡住**，自述「不会，这个课件里讲了吗？我可能还不会其它类似这样的更多知识点」。缺口＝Clairaut 标准动作：令 p = y′、对 x 求导 ⟹ (x − 2p)p′ = 0 ⟹ 通解 y = Cx − C² 与**奇解 y = x²/4**（奇解最常被漏）。；B3 y y″ − y′² = y² ln y（y>0, y′>0）：**设 w = y′、y″ = w·dw/dy 正确**，随后**卡住**（自述「不会了」）。缺口＝识别 y y″ − y′²)/y² = (y′/y)′，令 z = ln y ⟹ z″ = z ⟹ z = C₁e^x + C₂e^{−x} ⟹ y = exp(C₁e^x + C₂e^{−x})。；A6 y″ − 6y′ + 10y = 0：**全对**（γ = 3 ± i ⟹ y = e^{3x}(C₁cos x + C₂sin x)）。A5 y‴ + 9y″ + 27y′ + 27y = 0：特征方程与 (γ+3)³ = 0 正确，但解的第三项**疑似写成 x e^{−3x}**（三重根应为 C₁e^{−3x} + C₂x e^{−3x} + **C₃x²e^{−3x}**）→ **`[待确认]`（手写放大后仍只见 x，未见 x²；下一轮当面核）**。属「m 重根要给全 x^j, j=0…m−1」那一格。；A7 y″ − 2y′ − 3y = 3x³ − 2x：**全对**（λ = 3, −1；y_p = −x³ + 2x² − 4x + 4，经复核正确）。B4 y″ + 4y = 12x + 8cos2x：会拆成 y₁（→3x ✓）与 y₂，但**自述「我大致会解，但是为什么这样设没弄清楚」**（共振为何乘 x）；系数疑似写成 A = −2（正确为 **+2** ⟹ y₂ = 2x sin 2x）→ `[待确认]`；**初值 y(0)=0、y′(0)=5 未代入**。缺口＝共振的设法定理（x^s）+ IVP 收尾。
- `ru-level-check-01` / `attempt-43`：尚未完成；**俄语定位诊断·第一块「名词的性」（8 题）**：**对 3/8**。✅ `такси` 答「中」✓（上次当成复数的那个，**已修**）；`дедушка` 答「阳」✓（`-а` 结尾的例外**记住了**）；`окно́` 答「中」✓。❌ `тетра́дь` 答「阳」（应**阴**，与上次同一个错）；`ночь` 答「阳」（应**阴**：ж/ш/ч/щ 后带 ь）。❓ `слова́рь`（应阳）、`портфе́ль`（应阳）、`пло́щадь`（应阴）**均答「不知道」**——不是答错，而是没存储。【结论】`-ь` 词的性**几乎整块丢失**（3 个不知道 + 2 个错）；非 `-ь` 的规则（-а／-о 等）与 `такси` 类外来词**保持良好**。【后续】用她自己的卡 `topics/topic-01-名词的性和-ь结尾词.md` 的「可用的 5 条规律 ＋ 38 词成对记忆表」回补。；**俄语定位诊断·第四块「какой 与名词一致」（5 题）**：**对 4/5**。✅ 学习者按选项编号作答 1/2/3/4 ＝ `како́й`（阳）／`кака́я`（阴）／`како́е`（中）／`каки́е`（复）**四题全对**——**性数一致的机制完整保留**（与 2026-09-30 的结论一致：她的「性 → 疑问词」映射是通的）。❌ 第 5 题「这是新书」应填**形容词** `но́вая`，她仍填疑问词 `кака́я`（选项 2）→ **形容词词尾（УРОК 7 新内容）尚未上手**，只是把「阴性 → 第 2 个形式」的槽位套了过来。⚠ 本诊断是**定位基线**（`needs_verify=true`）→ **不计独立通过**。

## ③ 帮助史与曝光史（跨窗口保留，不因换窗口丢失）

共 **52** 条作答事件；其中 **36** 条记录了提示或答案曝光。

| 事件 | 提示 | 曝光 | 时机 | 说明（为何不计独立通过） |
|---|---|---|---|---|
| `attempt-52` | H1 | partial | before_attempt | 待核验 |
| `attempt-53` | H4 | full | before_attempt | 提示>0 |
| `attempt-51` | H3 | partial | before_attempt | 待核验 |
| `attempt-49` | H3 | partial | before_attempt | 提示>0 |
| `attempt-47` | H3 | partial | before_attempt | 待核验 |
| `attempt-48` | H3 | partial | before_attempt | 提示>0 |
| `attempt-46` | H2 | partial | before_attempt | 待核验 |
| `attempt-44` | H2 | partial | before_attempt | 待核验 |
| `attempt-45` | H2 | partial | before_attempt | 待核验 |
| `attempt-42` | H2 | partial | before_attempt | 待核验 |
| `attempt-40` | H3 | partial | before_attempt | 提示>0 |
| `attempt-23` | H4 | full | before_attempt | 待核验 |
| `attempt-27` | H1 | partial | before_attempt | 待核验 |
| `attempt-28` | H2 | partial | before_attempt | 提示>0 |
| `attempt-29` | H2 | partial | before_attempt | 待核验 |
| `attempt-31` | H3 | partial | before_attempt | 待核验 |
| `attempt-32` | H0 | partial | before_attempt | 待核验 |
| `attempt-33` | H2 | partial | before_attempt | 待核验 |
| `attempt-35` | H0 | none | — | — |
| `attempt-17` | H3 | partial | before_attempt | 待核验 |
| `attempt-18` | H3 | partial | before_attempt | 待核验 |
| `attempt-21` | H3 | partial | before_attempt | 提示>0 |
| `attempt-22` | H4 | full | before_attempt | 待核验 |
| `attempt-3` | H0 | partial | after_attempt | — |
| `attempt-4` | H0 | full | before_attempt | — |
| `attempt-5` | H0 | partial | before_attempt | 待核验 |
| `attempt-6` | H0 | partial | before_attempt | — |
| `attempt-7` | H0 | full | before_attempt | — |
| `attempt-9` | H0 | none | during_attempt | — |
| `attempt-10` | H4 | full | before_attempt | 待核验 |
| `attempt-11` | H2 | partial | before_attempt | 待核验 |
| `attempt-13` | H0 | partial | before_attempt | 待核验 |
| `attempt-14` | H2 | partial | during_attempt | 待核验 |
| `attempt-15` | H0 | full | before_attempt | 待核验 |
| `attempt-16` | H2 | none | before_attempt | 待核验 |
| `attempt-2` | H3 | partial | after_attempt | 提示>0 |

> ⚠ **未知不默认成最有利值**：曝光时机缺失/`unknown` 一律**阻断**独立通过（fail-closed）。
> ⚠ **反馈后的曝光**（`after_attempt`）不污染此前那次独立表现；**作答前/作答中**的曝光都阻断。

## ④ 当前卡点（未解决困难 + 未升级目标）

| 困难 | 状态 | 目标 | 观察到 | 证据 |
|---|---|---|---|---|
| `hurdle-2` | awaiting_retest | mp.taylor-expansion, mp.laurent-expansion | 2026-09-28 | 会话 2026-09-28（学习者原话：『我不会😭』）；相关任务 learning/tasks/mp1-ch3-hw-0 |
| `hurdle-3` | teaching | ru.qword-agreement | 2026-09-30 | 讲法见 subjects/07-俄语/topics/topic-02-疑问词какой在问什么.md；对照证据＝atte |
| `hurdle-4` | teaching | tm.t5.effective-potential, tm.t5.central-motion-types | 2026-10-19 | attempt-52（tm-t5-ueff-variant-01，partial）＋ 2026-10-19 会话内口头自 |

**已有独立通过、但延迟检验未满足**（下一步应做换题延迟复测）：`ee.ac.phasor-impedance`、`ee.ac.resonance`、`ee.ac.series-rlc`、`ee.dc.kcl`、`mp.power-series-radius`、`mp.residue-computation`、`mp.taylor-expansion`、`ru.qword-agreement`、`tm.t4.direct-check`、`tm.t4.energy-integral`

**已声明但一道题都没有（纸面目标）**：`ai-tech.c00-02`、`ai-tech.c00-03`、`ai-tech.c00-04`、`ai-tech.c00-05`、`ai-tech.c00-06`、`ai-tech.c00-07`、`ai-tech.c00-08`、`en.listen.decoding`、`en.listen.structure`、`en.read.timed`、`en.speak.fc`、`en.speak.gra`、`en.speak.lr`、`en.speak.pr`、`ode.sys.ivp`

> 没有题目**不等于**已掌握，也**不等于**没学过——它表示系统里没有任何证据。

## ⑤ 下一步（机械候选，不是最终安排）

| 最早开始 | 队列 | 任务 | 性质 | 为什么 |
|---|---|---|---|---|
| 2026-09-27 | 题目截止 | `tm-h4-01` | practice | 题目截止 2026-09-27（已逾期） |
| 2026-09-28 | 题目截止 | `mp1-ch3-quiz-01` | practice | 题目截止 2026-09-28（已逾期） |
| 2026-09-28 | 题目截止 | `tm-t4-criteria-03` | practice | 题目截止 2026-09-28（已逾期） |
| 2026-09-29 | 题目截止 | `ee-lab1-prep-01` | practice | 题目截止 2026-09-29（已逾期） |
| 2026-09-29 | 题目截止 | `tm-t4-criteria-04` | mixed | 题目截止 2026-09-29（已逾期） |
| 2026-09-30 | 能力再测 | `ee.ac.phasor-impedance` | 延迟检验 | 已有独立通过（2026-09-28）；已验证通过日期跨度 0d < 2d；最早 2026-09-30 可换题复测（等待本身不算通过） |
| 2026-09-30 | 能力再测 | `ee.ac.resonance` | 延迟检验 | 已有独立通过（2026-09-28）；已验证通过日期跨度 0d < 2d；最早 2026-09-30 可换题复测（等待本身不算通过） |
| 2026-09-30 | 能力再测 | `ee.ac.series-rlc` | 延迟检验 | 已有独立通过（2026-09-28）；已验证通过日期跨度 0d < 2d；最早 2026-09-30 可换题复测（等待本身不算通过） |
| 2026-09-30 | 能力再测 | `tm.t4.direct-check` | 延迟检验 | 已有独立通过（2026-09-28）；已验证通过日期跨度 0d < 2d；最早 2026-09-30 可换题复测（等待本身不算通过） |
| 2026-09-30 | 能力再测 | `tm.t4.energy-integral` | 延迟检验 | 已有独立通过（2026-09-28）；已验证通过日期跨度 0d < 2d；最早 2026-09-30 可换题复测（等待本身不算通过） |
| 2026-09-30 | 题目截止 | `ee-variant-01` | mixed | 题目截止 2026-09-30（已逾期） |
| 2026-09-30 | 题目截止 | `mp1-ch3-sing-01` | practice | 题目截止 2026-09-30（已逾期） |

完整排期（含'未来才开放、不得提前安排'的项）见 `plan/schedule.md`（`tools/schedule_reviews.py` 生成）。
**最终下一步以 `.tutor/config/status-narrative.yml` 的 `next` 行 + `plan/today-<日期>.md` 为准**（那是人工判断，不是机械候选）。

## ⑥ 最近订正（**摘要 + 指针**；纠错全过程不在这里）

共 **55** 条订正。最近 5 条：

| 订正 | 事件 | 字段 | from → to | 证据 |
|---|---|---|---|---|
| `corr-20261004-ielts-audit-08` | `attempt-42` | `en.write.cc.note` | `"**第 3 段重写 · CC**：段内顺序较基线清楚（角度 → 现象 → 收尾），但第 2、3 句照抄导致句首 `And` 仍出现一次；逗号粘连（`..., it's just a waste of time and our environment`）留存未改。"` → `'2026-10-04审查订正：新增开头和收尾，段内联系仍需说明；同段的逗号粘连留存。句首And出现一次本身不能作为扣分或不连贯依据。不对83词单段硬套完整作文四项分数。'` | subjects/11-英语-雅思/审查与修订-20261004.md；session-f5a649 |
| `corr-20261004-ielts-audit-09` | `attempt-42` | `en.write.lr.note` | `'**第 3 段重写 · LR**：新增搭配 `energy utilization efficiency`（可接受但偏术语，非学术写作常用块）；`take more bus and bicycle` **搭配错**；`less people`、`of no meaning and significance`（生硬）留存。**未使用结构讲义中点名的可复用搭配类型**。'` → `'2026-10-04审查订正：take more bus and bicycle不自然，可说use public transport more and cycle；less people在此用fewer people。energy utilization efficiency是否适合取决于实际表达，不强制使用讲义搭配；未用指定词块不是LR不通过理由。of no meaning and significance语义笼统。'` | subjects/11-英语-雅思/审查与修订-20261004.md；session-f5a649 |
| `corr-20261004-ielts-audit-10` | `attempt-42` | `en.write.gra.note` | `'**第 3 段重写 · GRA**：基线标出的三处错误**一处未修**——主谓一致 `pollution come out`（应为 comes）、`traffic jam occurs everyday and in every big cities`（every + 复数 cities；应为 in every big city 或 in all big cities）、逗号粘连。新增句本身语法无错。→ **「重写=改语言」这一步没有发生**，这是本次最值得记的一点。'` → `'2026-10-04审查订正：pollution come out、every big cities、逗号粘连仍需修正，这是文本中的语言事实。新增句没有明显结构错误不等于意思清楚；旧记录不能从这次未改语言确诊态度/认知问题，也不默认多项语法都是同一轮重写交付。'` | subjects/11-英语-雅思/审查与修订-20261004.md；session-f5a649 |
| `corr-20261004-ielts-audit-11` | `attempt-42` | `error_hypothesis` | `'**两个动作没做，一个是缺技能，一个是漏执行**：①**缺技能**——「把抽象主张具体化成一个场景」仍不会做（需要示范 + 单句练习），这是 TR 的根因；②**漏执行**——被明确点名的三处语法错误在「重写」时被原样保留，说明重写时只看结构、没通读语言。**判读提示**：不要把「照抄中间两句」理解为态度问题；更可能是他把「重写」理解成「在原有段落上加头加尾」。下一次指令要明确：**中间句必须改，或删掉重写**。'` → `'2026-10-04审查订正：旧诊断以已撤回的具体案例三件套为准，不能确诊缺技能或漏执行。可观察到新增开头/结尾但意思和因果联系仍不清楚，原稿若干语言错误留存。助手指令本身同时要求模板、案例、字数和三处语法，增加注意力负担。下一步只解释并改一句联系，不要求查政策、补案例或重复整段。'` | subjects/11-英语-雅思/审查与修订-20261004.md；session-f5a649 |
| `corr-20261004-ielts-audit-12` | `attempt-42` | `diagnosis_status` | `'confirmed'` → `'pending_probe'` | subjects/11-英语-雅思/审查与修订-20261004.md；session-f5a649 |

全文：`learning/corrections.jsonl`（机器可读、唯一事实源）→ 人读视图 `learning/attempts/corrections.md`。
> 历史更正的**可追溯记录保留在那里**，冷启动入口只放这一条摘要。

## ⑦ 汇总（可数事实，唯一来源）

| 项 | 值 |
|---|---|
| 目标总数 | 76 |
| 　等级「迁移通过」 | 0 |
| 　等级「延迟通过」 | 1 |
| 　等级「曾独立完成」 | 10 |
| 　等级「需支持」 | 33 |
| 　等级「未测」 | 32 |
| 覆盖分布 | {"已安排·未作答": 17, "未安排（无题目）": 15, "已独立通过·待延迟复测": 11, "已作答·需补练": 32, "已作答·开卷/受助通过": 1} |
| 稳定证据（=迁移通过） | 0 |
| 未解决困难 | 3 |
| 作答事件 | 52 条 |
| 订正 | 55 条 |
| 题目 | 51 道 |
| 实测时长 / 估计时长 | 7.0 min / 1308.0 min（**单列，不混算**） |

> 本表是 STATUS 块里 `mastered` / `open_hurdles` / `attempts` 等字段的来源；
> **不允许**在其它文件再手写一份计数（避免「两处各写一份、对不上」）。
