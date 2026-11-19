# -*- coding: utf-8 -*-
"""第 6 章（临界点与稳定性）名词英文标注 + 章末对照表。"""
import os, sys

SRC = os.path.join('subjects', '03-微分方程', '讲义',
                   'ODE-期中之后-完整讲义-L13-L23-20261118.tex')

# ---------- 1) 逐条插入（原文 → 替换）----------
PAIRS = [
    # 导言宏
    (r'\newcommand{\cnum}[1]{\ding{\the\numexpr171+#1\relax}}',
     '\\newcommand{\\cnum}[1]{\\ding{\\the\\numexpr171+#1\\relax}}\n\n'
     '% ---- 名词英文标注：淡墨斜体，紧跟在中文名词后的括号里 ----\n'
     '\\newcommand{\\EN}[1]{{\\itshape\\color{inkgray}#1}}'),

    # 章题
    ('{相图、稳定性定义与第一近似}{',
     '{相图（phase portrait）、稳定性定义与第一近似（first approximation）}{'),

    # §0.2 三个词
    (r'\item \textbf{分析语言}：稳定、渐近稳定、不稳定，三个词各自的严格含义（§4）。',
     r'\item \textbf{分析语言}：稳定（\EN{stable}）、渐近稳定（\EN{asymptotically stable}）、不稳定（\EN{unstable}），三个词各自的严格含义（§4）。'),

    # §0.4 记号表
    (r'\subhdr{0.4 记号表（查表用，不要求先背）}',
     r'\subhdr{0.4 记号表（查表用，不要求先背；名词英文见 §13）}'),
    (r"$\X'=\F(\X)$ & 自治系统，$\F=(P,Q)^{\mathrm T}$ & §1.2\\",
     r"$\X'=\F(\X)$ & 自治系统（\EN{autonomous system}），$\F=(P,Q)^{\mathrm T}$ & §1.2\\"),
    (r'$\tau=\tr A$,\ $\Delta=\det A$ & 迹与行列式 & §2.2\\',
     r'$\tau=\tr A$,\ $\Delta=\det A$ & 迹（\EN{trace}）与行列式（\EN{determinant}） & §2.2\\'),
    (r'$D=\tau^{2}-4\Delta$ & 特征方程的判别式 & §2.2\\',
     r'$D=\tau^{2}-4\Delta$ & 特征方程的判别式（\EN{discriminant}） & §2.2\\'),
    (r'$\lambda_1,\ \lambda_2$ & 特征值（特征方程的根） & §2.2\\',
     r'$\lambda_1,\ \lambda_2$ & 特征值（\EN{eigenvalue}，特征方程的根） & §2.2\\'),
    (r'$V$ & 实特征向量；复情形记 $w=u+\mathrm{i}v$ & §2.3\\',
     r'$V$ & 实特征向量（\EN{eigenvector}）；复情形记 $w=u+\mathrm{i}v$ & §2.3\\'),
    (r'$\X^{*}$ & 临界点（平衡点） & §1.4\\',
     r'$\X^{*}$ & 临界点（\EN{critical point}，即平衡点） & §1.4\\'),
    (r'轨线、相图 & 解的像集；全部轨线的集合 & §1.3\\',
     r'轨线、相图 & 解的像集；全部轨线的集合（\EN{trajectory, phase portrait}） & §1.3\\'),
    (r'平凡解 & 零解 $\X(t)\equiv\mathbf{0}$ & §4.5\\',
     r'平凡解（\EN{trivial solution}） & 零解 $\X(t)\equiv\mathbf{0}$ & §4.5\\'),

    # §1
    (r'这张图叫\textbf{速度场}，§1.1 专门讲它。',
     r'这张图叫\textbf{速度场}（\EN{velocity field}），§1.1 专门讲它。'),
    (r'则称它为\textbf{自治系统}（autonomous system）。',
     r'则称它为\textbf{自治系统}（\EN{autonomous system}）。'),
    (r'称为一条\textbf{轨线}（trajectory，或称相轨线）；全部轨线（连同方向）的集合叫\textbf{相图}（phase portrait）。',
     r'称为一条\textbf{轨线}（\EN{trajectory}，也称\textbf{相轨线}、\EN{orbit}）；全部轨线（连同方向）的集合叫\textbf{相图}（\EN{phase portrait}），它画在\textbf{相平面}（\EN{phase plane}）上。'),
    (r'则称 $\X^{*}$ 为系统 (1.1) 的\textbf{临界点}（critical point），也称\textbf{平衡点}、\textbf{驻点}；有些教材叫\textbf{奇点}（singular point）。',
     r'则称 $\X^{*}$ 为系统 (1.1) 的\textbf{临界点}（\EN{critical point}），也称\textbf{平衡点}（\EN{equilibrium point}）、\textbf{驻点}（\EN{stationary point}）；有些教材叫\textbf{奇点}（\EN{singular point}）。'),
    (r'三步合起来，这张相图叫\textbf{中心}。',
     r'三步合起来，这张相图叫\textbf{中心}（\EN{center}）。'),
    (r'三步合起来，这张相图叫\textbf{结点}。',
     r'三步合起来，这张相图叫\textbf{结点}（\EN{node}）。'),
    (r'\item \textbf{解的唯一性}：从同一个状态出发，不能有两套不同的后续演化。',
     r'\item \textbf{解的唯一性}（\EN{uniqueness of solution}）：从同一个状态出发，不能有两套不同的后续演化。'),
    (r'若右端只是连续、不满足李普希茨条件（例如',
     r'若右端只是连续、不满足李普希茨（\EN{Lipschitz}）条件（例如'),

    # §2
    (r'下面所有结论都只依赖 $A$ 的\textbf{特征值}，与四个元素怎么排布无关。',
     r'下面所有结论都只依赖 $A$ 的\textbf{特征值}（\EN{eigenvalue}），与四个元素怎么排布无关。'),
    (r'\subhdr{2.2 特征方程}',
     r'\subhdr{2.2 特征方程（characteristic equation）}'),
    (r'于是 $V$ 是 $A$ 的特征向量，$\lambda$ 是特征值。要有非零解，必须',
     r'于是 $V$ 是 $A$ 的特征向量（\EN{eigenvector}），$\lambda$ 是特征值。要有非零解，必须'),
    (r'两根之和为 $\tau$，之积为 $\Delta$（韦达定理），判别式记',
     r'两根之和为 $\tau$，之积为 $\Delta$（韦达定理），判别式（\EN{discriminant}）记'),
    (r'若 $\lambda_1\neq\lambda_2$ 为实数，对应实特征向量 $V_1,V_2$，则通解为',
     r'若 $\lambda_1\neq\lambda_2$ 为实数，对应实特征向量 $V_1,V_2$，则通解（\EN{general solution}）为'),
    (r'把复解拆成实部与虚部：',
     r'把复解拆成实部（\EN{real part}）与虚部（\EN{imaginary part}）：'),
    (r'要分两种，区别在于\textbf{几何重数} $g$（线性无关特征向量的个数）：',
     r'要分两种，区别在于\textbf{几何重数}（\EN{geometric multiplicity}）$g$——它指线性无关（\EN{linearly independent}）特征向量的个数：'),
    (r'理由是\textbf{可逆线性变换保持相图结构}。',
     r'理由是\textbf{可逆线性变换}（\EN{invertible linear transformation}）\textbf{保持相图结构}。'),
    (r'而任意矩阵都可以化到若尔当标准形，其对角元正是特征值。',
     r'而任意矩阵都可以化到\textbf{若尔当标准形}（\EN{Jordan canonical form}），其对角元正是特征值。'),
    (r'所以 $A$ 与 $B$ 的相图\textbf{拓扑上一样}，类型名当然一样。',
     r'所以 $A$ 与 $B$ 的相图\textbf{拓扑等价}（\EN{topologically equivalent}），类型名当然一样。'),

    # §3
    (r'浅色为方向场，深色为轨线，虚线为特征方向。',
     r'浅色为方向场（\EN{direction field}），深色为轨线，虚线为特征方向（\EN{eigendirection}）。'),
    (r'\subhdr{（3）焦点（focus）}',
     r'\subhdr{（3）焦点（focus；课件作 spiral point）}'),
    (r'两者合起来就是对数螺线——每转一圈，半径乘同一个因子。',
     r'两者合起来就是对数螺线（\EN{logarithmic spiral}）——每转一圈，半径乘同一个因子。'),
    (r'这种叫\textbf{临界结点}（也译星形结点、proper node）。',
     r'这种叫\textbf{临界结点}（也译星形结点，\EN{proper node / star node}）。'),
    (r'叫\textbf{退化结点}（degenerate node）。',
     r'叫\textbf{退化结点}（\EN{improper node / degenerate node}）。'),
    (r'结点 & node（improper node） & $\Delta>0,\ D>0$ & 两条直线轨线，其余切于慢方向\\',
     r'结点 & node & $\Delta>0,\ D>0$ & 两条直线轨线，其余切于慢方向\\'),
    (r'焦点 & focus, spiral & $\Delta>0,\ D<0,\ \tau\neq0$ & 螺旋，无限多圈\\',
     r'焦点 & focus（spiral point） & $\Delta>0,\ D<0,\ \tau\neq0$ & 螺旋，无限多圈\\'),

    # §4
    (r'\textbf{定义 4.2（渐近稳定）}',
     r'\textbf{定义 4.2（渐近稳定，asymptotically stable）}'),
    (r'\textbf{定义 4.3（不稳定）}',
     r'\textbf{定义 4.3（不稳定，unstable）}'),
    (r'这个解叫\textbf{平凡解}（trivial solution）。',
     r'这个解叫\textbf{平凡解}（\EN{trivial solution}）。'),

    # §5
    (r'则零解\textbf{渐近稳定}（事实上是指数衰减：存在 $C,\gamma>0$ 使',
     r'则零解\textbf{渐近稳定}（事实上是指数衰减，\EN{exponential decay}：存在 $C,\gamma>0$ 使'),
    (r'代数重数 $=$ 几何重数',
     r'代数重数（\EN{algebraic multiplicity}）$=$ 几何重数'),
    (r'要看有没有 $t$ 因子（即若尔当块）。',
     r'要看有没有 $t$ 因子（即若尔当块，\EN{Jordan block}）。'),

    # §6
    (r'\subhdr{6.2 线性化就是一阶泰勒展开}',
     r'\subhdr{6.2 线性化（linearization）就是一阶泰勒展开}'),
    (r'其中 $\Jac(\X^{*})$ 叫\textbf{雅可比矩阵}（Jacobi matrix）。',
     r'其中 $\Jac(\X^{*})$ 叫\textbf{雅可比矩阵}（\EN{Jacobian matrix}，有的书写 Jacobi matrix）。'),
    (r'称为原系统在 $\X^{*}$ 处的\textbf{线性化系统}，$\Jac(\X^{*})$ 称为\textbf{线性部分}。',
     r'称为原系统在 $\X^{*}$ 处的\textbf{线性化系统}（\EN{linearized system}），$\Jac(\X^{*})$ 称为\textbf{线性部分}（\EN{linear part}）。'),
    (r'则称 $\X^{*}$ 为\textbf{双曲临界点}（hyperbolic critical point）。',
     r'则称 $\X^{*}$ 为\textbf{双曲临界点}（\EN{hyperbolic critical point}）。'),
    (r'特征值不落在虚轴上',
     r'特征值不落在\textbf{虚轴}（\EN{imaginary axis}）上'),
    (r'\textbf{定理 6.1（李雅普诺夫第一方法，稳定性部分）}',
     "\\textbf{定理 6.1（李雅普诺夫第一方法，Lyapunov's first method；稳定性部分）}"),
    (r'由格朗沃尔（Gronwall）不等式',
     r'由格朗沃尔（\EN{Gronwall}）不等式'),
    (r'\textbf{例 1}\ 无阻尼单摆（取 $g=\ell=1$）满足',
     r'\textbf{例 1}\ 无阻尼单摆（\EN{undamped pendulum}，取 $g=\ell=1$）满足'),
    (r'但要证明它需要另找守恒量 $E=',
     r'但要证明它需要另找守恒量（\EN{conserved quantity}）$E='),
    (r'鞍点的两条分界线把平面分成几个',
     r'鞍点的两条分界线（\EN{separatrix}）把平面分成几个'),
    (r'从\textbf{局部}看',
     r'从\textbf{局部}（\EN{local}）看'),
    (r'从\textbf{全局}看',
     r'从\textbf{全局}（\EN{global}）看'),

    # §7
    (r'称 $V$ \textbf{正定}；若 $V(\X)\ge0$，称\textbf{半正定}。',
     r'称 $V$ \textbf{正定}（\EN{positive definite}）；若 $V(\X)\ge0$，称\textbf{半正定}（\EN{positive semi-definite}）。'),
    (r'若 $U$ 上 $\dot V\le0$（半负定），则零解\textbf{稳定}；',
     r'若 $U$ 上 $\dot V\le0$（半负定，\EN{negative semi-definite}），则零解\textbf{稳定}；'),
    (r'上 $\dot V<0$（负定），则零解\textbf{渐近稳定}；',
     r'上 $\dot V<0$（负定，\EN{negative definite}），则零解\textbf{渐近稳定}；'),
    (r'（切塔耶夫条件）',
     r'（切塔耶夫条件，\EN{Chetaev condition}）'),
    (r'\subhdr{7.3 二次型怎么取}',
     r'\subhdr{7.3 二次型（quadratic form）怎么取}'),
    (r'它正定的充要条件（西尔维斯特判据）是',
     r"它正定的充要条件（西尔维斯特判据，\EN{Sylvester's criterion}）是"),

    # §12.4 对照表加一行
    (r'附录 A & 四道题的完整详解 & 第 1 题 (1)(2)(3)、第 2 题\\',
     r'§13 & 名词中英对照（考前查词） & 全章；题干原句的译法\\' + '\n' +
     r'附录 A & 四道题的完整详解 & 第 1 题 (1)(2)(3)、第 2 题\\'),

    # 附录
    (r'故 $\lambda=-1$ 是\textbf{二重}根。',
     r'故 $\lambda=-1$ 是\textbf{二重根}（\EN{double root}）。'),
    (r'（逻辑斯蒂方程），其解',
     r'（逻辑斯蒂方程，\EN{logistic equation}），其解'),
]

# ---------- 2) 整行替换（原行含 ASCII 引号，按行首匹配）----------
LINE_REPL = [
    ('注意英文的',
     '注意英文的 \\EN{proper node} 与 \\EN{star node} 是同一个东西（对应中文"临界结点"，$g=2$），'
     '而 \\EN{improper node} 与 \\EN{degenerate node} 是另一个东西（对应中文"退化结点"，$g=1$）；'
     '普通结点（$\\lambda_1\\neq\\lambda_2$，$\\Delta>0,D>0$）就叫 \\EN{node}。'
     '名字不同不要紧，条件与 $g$ 才是判据。'),
]

BRIDGE_ANCHOR = r'\subhdr{6.5 定理 6.1 为什么成立（证明思路）}'
BRIDGE = (
    '课件把用一次项判稳定性这件事叫\\textbf{第一近似}（\\EN{first approximation}）：'
    '\\textbf{第一近似系统}（\\EN{system in the first approximation}）就是 (6.4)，'
    '而第一近似判不出结论的情形就是 §6.6。答"由第一近似可知……"与答"由定理 6.1 可知……"是同一句话的两种说法，'
    '考试里两种都算对。\n\n'
)

GLOSS = r'''%=====================================================================
\hdr{§13}{名词中英对照（考前查用）}

\textbf{这一节解决什么问题。}课件与考卷都是英文，讲义是中文；考场上真正卡住的常常不是方法，而是题干里那个词。下面按用途分成五组，只做对照，不重复推导。正文里每个词在首次出现处也已用灰色斜体注过一次（例如"临界点（\EN{critical point}）"），两处可以互相印证。全书级的简表在 §0.5，那里每章只收一两个词；本节把第 6 章的名词收全。

\subhdr{13.1 相图与点型}

\begin{minipage}{\linewidth}
{\small
\tabtop
\begin{tabular}{@{}p{0.14\linewidth}p{0.31\linewidth}p{0.14\linewidth}p{0.31\linewidth}@{}}
\thead{中文} & \thead{英文} & \thead{中文} & \thead{英文}\\
\end{tabular}
\tabmid
\begin{tabular}{@{}p{0.14\linewidth}p{0.31\linewidth}p{0.14\linewidth}p{0.31\linewidth}@{}}
相图 & \EN{phase portrait} & 轨线 & \EN{trajectory (orbit)}\\
相平面 & \EN{phase plane} & 速度场 & \EN{velocity field}\\
方向场 & \EN{direction field} & 自治系统 & \EN{autonomous system}\\
临界点 & \EN{critical point} & 平衡点 & \EN{equilibrium point}\\
奇点 & \EN{singular point} & 驻点 & \EN{stationary point}\\
特征方向 & \EN{eigendirection} & 结点 & \EN{node}\\
鞍点 & \EN{saddle point} & 焦点 & \EN{focus (spiral point)}\\
中心 & \EN{center} & 临界结点 & \EN{proper node (star node)}\\
退化结点 & \EN{improper node (degenerate node)} & 分界线 & \EN{separatrix}\\
源 & \EN{source} & 汇 & \EN{sink}\\
\end{tabular}
\tabbot
}
\end{minipage}

{\small\color{inkgray}末两行的 \EN{source} 与 \EN{sink} 是课件讲结点时的叫法（$\tau>0$ 的叫 source，$\tau<0$ 的叫 sink）；本书正文写成"不稳定结点""稳定结点"，指的是同一件事。\par}

\subhdr{13.2 稳定性、线性化与方法}

\begin{minipage}{\linewidth}
{\small
\tabtop
\begin{tabular}{@{}p{0.14\linewidth}p{0.31\linewidth}p{0.14\linewidth}p{0.31\linewidth}@{}}
\thead{中文} & \thead{英文} & \thead{中文} & \thead{英文}\\
\end{tabular}
\tabmid
\begin{tabular}{@{}p{0.14\linewidth}p{0.31\linewidth}p{0.14\linewidth}p{0.31\linewidth}@{}}
稳定 & \EN{stable} & 渐近稳定 & \EN{asymptotically stable}\\
不稳定 & \EN{unstable} & 平凡解 & \EN{trivial solution}\\
指数衰减 & \EN{exponential decay} & 有界 & \EN{bounded}\\
雅可比矩阵 & \EN{Jacobian matrix} & 线性化 & \EN{linearization}\\
线性化系统 & \EN{linearized system} & 线性部分 & \EN{linear part}\\
第一近似 & \EN{first approximation} & 第一近似系统 & \EN{system in the first approximation}\\
双曲临界点 & \EN{hyperbolic critical point} & 虚轴 & \EN{imaginary axis}\\
拓扑等价 & \EN{topologically equivalent} & 邻域 & \EN{neighborhood}\\
李雅普诺夫第一方法 & \EN{Lyapunov's first method} & 李雅普诺夫第二方法 & \EN{Lyapunov's second method}\\
正定 & \EN{positive definite} & 负定 & \EN{negative definite}\\
半正定 & \EN{positive semi-definite} & 半负定 & \EN{negative semi-definite}\\
二次型 & \EN{quadratic form} & 西尔维斯特判据 & \EN{Sylvester's criterion}\\
守恒量 & \EN{conserved quantity} & 格朗沃尔不等式 & \EN{Gronwall's inequality}\\
局部 & \EN{local} & 全局 & \EN{global}\\
单摆 & \EN{pendulum} & 逻辑斯蒂方程 & \EN{logistic equation}\\
未扰解 & \EN{unperturbed solution} & 受扰解 & \EN{perturbed solution}\\
\end{tabular}
\tabbot
}
\end{minipage}

\subhdr{13.3 矩阵与判据}

\begin{minipage}{\linewidth}
{\small
\tabtop
\begin{tabular}{@{}p{0.14\linewidth}p{0.31\linewidth}p{0.14\linewidth}p{0.31\linewidth}@{}}
\thead{中文} & \thead{英文} & \thead{中文} & \thead{英文}\\
\end{tabular}
\tabmid
\begin{tabular}{@{}p{0.14\linewidth}p{0.31\linewidth}p{0.14\linewidth}p{0.31\linewidth}@{}}
特征值 & \EN{eigenvalue} & 特征向量 & \EN{eigenvector}\\
特征方程 & \EN{characteristic equation} & 迹 & \EN{trace}\\
行列式 & \EN{determinant} & 判别式 & \EN{discriminant}\\
几何重数 & \EN{geometric multiplicity} & 代数重数 & \EN{algebraic multiplicity}\\
若尔当标准形 & \EN{Jordan canonical form} & 若尔当块 & \EN{Jordan block}\\
通解 & \EN{general solution} & 线性无关 & \EN{linearly independent}\\
可逆线性变换 & \EN{invertible linear transformation} & 二重根 & \EN{double root}\\
初值 & \EN{initial value} & 唯一性 & \EN{uniqueness of solution}\\
\end{tabular}
\tabbot
}
\end{minipage}

\subhdr{13.4 五组容易混的词}

\begin{itemize}
\item \EN{stable}（稳定）与 \EN{asymptotically stable}（渐近稳定）：前者只要求不跑远，后者还要求回来（§4.3）。
\item \EN{proper node}（临界结点）与 \EN{improper node}（退化结点）：前者各方向都是特征方向（$g=2$），后者只有一个特征方向（$g=1$）。作业第 1 题 (2) 是前者。
\item \EN{node}（结点）与 \EN{saddle point}（鞍点）：两者靠 $\Delta$ 的符号分家，与 $\tau$ 的符号无关；$\tau$ 只管进出（§3.6）。
\item \EN{hyperbolic}（双曲）与 \EN{hyperbola}（双曲线）：前者是特征值实部不为零的条件，与双曲线没有关系（§6.3）。
\item \EN{local}（局部）与 \EN{global}（全局）：定理 6.1 只保证临界点附近的事，远处的行为可以完全不同（§6.8、§6.9）。
\end{itemize}

\subhdr{13.5 题干原句}

\qstem{\textbf{Determine the type of the critical point and study the stability.}}
译：判定临界点的类型，并研究其稳定性。\textbf{两件事都要写}：先给类型（结点/鞍点/焦点/中心/临界结点/退化结点），再给稳定性（稳定/渐近稳定/不稳定），最后补一句依据（哪条定理、哪个特征值）。第 1 题的三个小问都是这一句；课件把它写成 \EN{critical point(s)}，括号里的复数只是通用写法，$\Delta\neq0$ 时线性系统只有一个临界点（§1.5）。

\qstem{\textbf{Investigate the stability of the trivial solution.}}
译：研究平凡解的稳定性。关键词是 \EN{trivial solution}（平凡解，即 $\X\equiv\mathbf{0}$），不是一般解；第 2 题问的正是原点。

本讲义与考卷的英文标题：本章为 \EN{Critical Points and Stability}，两讲课件分别是 \EN{Phase Portrait}（相图）与 \EN{Linearization}（线性化）；课件里"第一近似下的稳定性"写作 \EN{stability in the first approximation}，与书中"线性化定理"是同一件事（§6.4）。
'''


def main():
    text = open(SRC, encoding='utf-8').read()

    bad = []
    for old, new in PAIRS:
        n = text.count(old)
        if n != 1:
            bad.append((n, old[:70]))
    if bad:
        print('!! 片段不唯一，未写入：')
        for n, o in bad:
            print('   count=%d  %s' % (n, o))
        sys.exit(2)

    for old, new in PAIRS:
        text = text.replace(old, new, 1)
    print('OK  正文插入 %d 处' % len(PAIRS))

    lines = text.split('\n')
    done = 0
    for prefix, newline in LINE_REPL:
        idx = [i for i, l in enumerate(lines) if l.startswith(prefix)]
        if len(idx) != 1:
            print('!! 行替换失败 count=%d: %s' % (len(idx), prefix))
            sys.exit(3)
        lines[idx[0]] = newline
        done += 1
    text = '\n'.join(lines)
    print('OK  整行替换 %d 处' % done)

    if text.count(BRIDGE_ANCHOR) != 1:
        print('!! 6.5 锚点不唯一')
        sys.exit(4)
    text = text.replace(BRIDGE_ANCHOR, BRIDGE + BRIDGE_ANCHOR, 1)
    print('OK  插入"第一近似"对照段')

    lines = text.split('\n')
    appA = [i for i, l in enumerate(lines) if l.startswith(r'\settags{附录 A')]
    if len(appA) != 1:
        print('!! 附录 A 锚点不唯一')
        sys.exit(5)
    j = appA[0]
    while j > 0 and not lines[j].startswith(r'\flowerrule'):
        j -= 1
    if not lines[j].startswith(r'\flowerrule'):
        print('!! 未找到附录 A 前的花饰线')
        sys.exit(6)
    lines[j:j] = GLOSS.rstrip('\n').split('\n') + ['']
    text = '\n'.join(lines)
    print('OK  插入 §13')

    open(SRC, 'w', encoding='utf-8', newline='\n').write(text)
    print('written %s  %d chars' % (SRC, len(text)))


if __name__ == '__main__':
    main()
