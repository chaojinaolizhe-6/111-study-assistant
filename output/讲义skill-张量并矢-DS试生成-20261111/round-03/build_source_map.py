# -*- coding: utf-8 -*-
"""生成 source-map.json：来源、旧主题→新稿位置、必读/选读、缺口与旧稿勘误。"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

data = {
    "meta": {
        "title": "从张量到并矢：九个分量、一台机器、三处力学落点",
        "date": "2026-11-11",
        "round": "round-03",
        "skill": "lecture-deepdive 2.2.1",
        "old_version": "2026-11-05（用户指定旧稿，仅作范围与题目来源）",
        "authorship": "DSH 独立完成组织、推导、制图、写作、编译、自检与返工；外部协调器只改 skill、只读审核。",
        "learner_basis": "用户自述“只会简单线性代数”；按 learner-background.json 的工作假设安排必要回顾，未做逐项诊断，不声称任何细项已掌握。",
        "round02_basis": "依据 reviews/tensor-dyad-20261111/review-round01.json 的有效问题单（READ-01/02、M2-M8、S1-S3、V1/V4/V5、Q1）逐项核实并修改；首轮 round-01 冻结不改。",
        "round03_basis": "依据 review-round02.json 的有效项 R2-READ02、R2-S3、R2-M3、V6、V7 五项局部返工；round-02 及其已通过内容保持不改。最终重排使附录 B/C 后移一页（48 页），P9 不再跨页。",
        "outputs": ["handout.tex", "handout.pdf", "handout.log", "compile-pass1.log", "compile-pass2.log",
                    "source-map.json", "verification.txt", "issue-response.json", "layout-report.txt",
                    "reading-layout-check.md", "verify.py", "build_source_map.py", "layout_check.py",
                    "check_margins.py", "render_pages.py", "render/*.png"],
        "page_count": 48,
        "compile": "xelatex -halt-on-error -interaction=nonstopmode 两遍",
        "check_handout": "appendix 模式：0 errors, 0 warnings",
        "visual_review": "当前模型不支持图像输入；已保存 48 页 PNG，完成文字层、页边、坐标与图形数据检查。受改的图 2、P4 续页、P9 与练习跳转已做同页/页位检查；外部目视验收待审，未声称已目视通过。"
    },
    "sources": {
        "TM2026-Topic8-P1.pdf": {
            "role": "核心来源：张量代数、旋转算子与角速度",
            "pages_used": {
                "p8": "正交基、求和约定、点乘、叉乘、ε_ijk、对偶张量",
                "p9": "张量积（Dyad）、左右作用、转置、线性算子、二次型、单位张量",
                "p10": "固定基与随体基、S(t)=Σ n'_k⊗e_k",
                "p11": "S^T S=S S^T=1、绕轴转 φ 的公式、无穷小转动",
                "p12": "Ω^×=\\dot S S^T、dn'_k/dt=Ω×n'_k",
                "p15": "刚体速度 v=V+Ω×r；本稿只取绕定点/质心的 v=ω×r 作为 §4.1 的物理前提",
                "p13-p14": "欧拉角与欧拉运动学方程：属后续运动学，本稿未展开",
                "p16-p18": "E8.01、E8.02、HW8.01--HW8.03：运动学例题，本稿未重复"
            }
        },
        "RIT-Whelan-notes10-tensor.pdf": {
            "role": "原始参考：惯量张量、换基、谱定理、平行轴、椭球",
            "pages_used": {
                "pp.2--3": "L=Σ m_k r_k×(ω×r_k) 与矩阵形式，作为 §4.1 的对照",
                "pp.4--6": "并矢定义、分量、算子作用、惯量张量连续形式",
                "p.7": "转置、对称/反对称、对偶张量；注意其 ∗A·B=−A×B，与课件符号相反",
                "pp.8--9": "换基、谱定理与正交对角化",
                "pp.10--14": "惯量张量细节、椭球例子、平行轴定理"
            }
        },
        "inputs/old-handout.tex": {
            "role": "用户指定的 2026-11-05 旧稿：保留主题范围与原有题目，作为待核查材料；不沿用其章节顺序、例子、图或说法",
            "sections_used": ["§0", "§1--§12", "附录 A", "附录 B", "三句话总结"]
        },
        "learner-background.json": {
            "role": "本次学习者基础声明与工作假设；未进行闭卷诊断，不写能力事实"
        }
    },
    "coverage": [
        {"old": "旧 §0 路线图", "new": "封面路线图与 §0 开头", "status": "合并", "note": "三个坎改为：矩阵是账本、二次型与主轴、并矢与三处落点；最短路径只跳过选读，不跳过教学示范"},
        {"old": "旧 §1.1--§1.4（线性映射、矩阵、换基、不变量）", "new": "§0.2--§0.5", "status": "必读", "note": "重组；新增 3×3 行列式展开与 R 的列约定说明；换基保留三步推导"},
        {"old": "旧 §2.1--§2.3（迹、行列式、特征多项式）", "new": "§0.5", "status": "必读", "note": "并入 §0.5；保留迹的循环性证明与三个不变量"},
        {"old": "旧 §3.1--§3.6（二次型、对称部分、椭球、特征值、谱定理、不变量）", "new": "§1.1--§1.6", "status": "必读", "note": "重写 45° 例；谱定理完整陈述在正文，Lagrange 证明标为选读"},
        {"old": "旧 §4.1--§4.6（阶、张量积、指标、变换律、商法则、上下标）", "new": "§2.1、§2.2、§2.7、§2.10", "status": "必读（上下标为选读）", "note": "商法则与变换律统一 R 的约定；上下标移入 §2.10 选读"},
        {"old": "旧 §5.1--§5.7（并矢、左右作用、点积/双点积、单位/投影、转置/对称/对偶、缩并表、谱分解）", "new": "§2.2--§2.9", "status": "必读（缩并表为查阅）", "note": "左右作用、投影并矢、对偶张量、缩并表、谱分解均保留并补例"},
        {"old": "旧 §6 三记号字典", "new": "§2.10", "status": "查阅", "note": "保留并补“并矢不是矩阵”的说明；上下标作为选读"},
        {"old": "旧 §7.1--§7.5（惯量张量）", "new": "§4.1--§4.5", "status": "必读（椭球例为选读）", "note": "补正定性、三角形不等式、对称轴判断、平行轴推导；教学示范换用 m=12,a=1,b=2,c=3"},
        {"old": "旧 §8.1--§8.4（输运定理、欧拉方程、对称陀螺、力矩）", "new": "§5.1--§5.4", "status": "必读", "note": "补并矢版输运定理逐项推导与两个核对；对称陀螺教学示范换用 A=B=4,C=5,ω3=6"},
        {"old": "旧 §9.1--§9.4（应力张量）", "new": "§6.1--§6.4", "status": "必读（Gauss 说明为选读）", "note": "补四面体论证、指标顺序、30° 教学示范；最大剪应力留给 P10"},
        {"old": "旧 §10 例 1--例 4", "new": "独立练习 P1--P4", "status": "独立练习", "note": "题干进正文，详解进附录 A；教学示范另换数字，避免提前曝光"},
        {"old": "旧 §11 易错与速查", "new": "§8", "status": "必读（查阅）", "note": "八条易错（新增换基转置一条）+ 操作速查表 + 三句话"},
        {"old": "旧 §12 缺口清单", "new": "附录 C.3", "status": "交付说明", "note": "按“类型｜来源页与原短语｜缺什么｜补在哪”重写；不作为正文依赖"},
        {"old": "旧 附录 A 指标速查", "new": "附录 B", "status": "查阅", "note": "保留；补 ε_ijk 与 RIT 符号约定提示"},
        {"old": "旧 附录 B 自测六问", "new": "独立练习 P5--P10", "status": "独立练习", "note": "题干与考点进正文，答案进附录 A；P10 改为求最大剪应力与所在截面"},
        {"old": "旧 三句话总结", "new": "§8 末尾", "status": "必读", "note": "保留三句话，措辞与本稿记号一致"},
        {"old": "旧稿未单列：旋转算子（仅 §5.4/§8.1 片段）", "new": "§3.1--§3.5", "status": "必读", "note": "按课件 p10--p12 扩成独立一节：S 的定义、正交性、绕轴公式、无穷小转动、角速度；为 §5 输运定理提供前提"},
        {"old": "旧稿未列：P11 旋转算子、P12 欧拉方程一般情形", "new": "P11、P12", "status": "独立练习（新增）", "note": "补足 §3 与 §5.2 的练习覆盖，不替代原有题目"}
    ],
    "practice_map": [
        {"id": "P1", "old": "旧 §10 例 1", "topic": "并矢运算、不变量、主轴与谱分解", "answer": "附录 A P1"},
        {"id": "P2", "old": "旧 §10 例 2", "topic": "长方体惯量、薄板极限、垂直轴定理", "answer": "附录 A P2"},
        {"id": "P3", "old": "旧 §10 例 3", "topic": "对称陀螺 A=B、角速度与周期", "answer": "附录 A P3"},
        {"id": "P4", "old": "旧 §10 例 4", "topic": "方向惯量、角动量与动能", "answer": "附录 A P4"},
        {"id": "P5", "old": "旧 附录 B 第 1 问", "topic": "并矢右作用与两种“先点乘再乘矢量”", "answer": "附录 A P5"},
        {"id": "P6", "old": "旧 附录 B 第 2 问", "topic": "张量判定与位置矢量", "answer": "附录 A P6"},
        {"id": "P7", "old": "旧 附录 B 第 3 问", "topic": "迹的循环性与换基不变", "answer": "附录 A P7"},
        {"id": "P8", "old": "旧 附录 B 第 4 问", "topic": "二次型只取对称部分", "answer": "附录 A P8"},
        {"id": "P9", "old": "旧 附录 B 第 5 问", "topic": "惯量非对角元负号与物理意义", "answer": "附录 A P9"},
        {"id": "P10", "old": "旧 附录 B 第 6 问", "topic": "单轴拉伸最大剪应力", "answer": "附录 A P10"},
        {"id": "P11", "old": "新增（课件 p10--p12 的应用）", "topic": "旋转算子矩阵、正交性、角速度", "answer": "附录 A P11"},
        {"id": "P12", "old": "新增（课件未展开的欧拉方程应用）", "topic": "欧拉方程分量形式", "answer": "附录 A P12"}
    ],
    "readings": {
        "required": [
            "§0.1--§0.5 矢量、线性映射、矩阵账本、换基、迹/行列式/特征多项式",
            "§1.1--§1.6 二次型、对称部分、椭球、特征值、谱定理陈述与用法、不变量",
            "§2.1--§2.9 阶、张量积、左右作用、点乘/双点积、单位/投影、转置/对偶、商法则、缩并表、谱分解",
            "§3.1--§3.5 旋转算子与角速度（§3 的必读部分）",
            "§4.1--§4.5 惯量张量（§4.4 椭球为选读）",
            "§5.1--§5.4 输运定理、欧拉方程、对称陀螺、力矩",
            "§6.1--§6.4 应力张量（§6.4 Gauss 证明为选读）",
            "§7 独立练习与 §8 易错/速查",
            "附录 A 练习详解、附录 B 指标速查"
        ],
        "optional": [
            {"id": "opt-1", "location": "§1.5 末尾", "topic": "谱定理 (i)+(iii) 的拉格朗日乘子证明", "skip_to": "§1.6", "why": "回答“为什么一定存在三个正交主轴”；主线只需定理陈述与用法"},
            {"id": "opt-2", "location": "§2.10 末尾", "topic": "上下标、协变/逆变、度规", "skip_to": "§3", "why": "非正交基才需要；本稿后续全程正交基，只用下标"},
            {"id": "opt-3", "location": "§4.4 末尾", "topic": "椭球惯量张量", "skip_to": "§4.5", "why": "更复杂的几何例子；§4.5 与 P2/P4 不用它"},
            {"id": "opt-4", "location": "§6.4 末尾", "topic": "高斯定理为什么成立", "skip_to": "§7", "why": "只给图像与一维类比；平衡方程与 §7 练习不依赖该证明"}
        ],
        "skip_check": "遮住 opt-1..opt-4 后，§1.6 只用定理三条结论；§3 及以后只用下标；§4.5 不用椭球结果；§7 不用 Gauss 证明。四处末尾都写了“跳过后从哪里继续”。"
    },
    "gaps": [
        {"type": "机制缺口", "source": "TM2026 p9 “Tensor product (Dyad)”", "missing": "课件直接给并矢与分量表，未说明对象为什么存在、为何九个分量", "filled": "§2.2 双线性定义 + 基并矢展开 + 作用在基矢量对验证唯一性"},
        {"type": "压缩缺口", "source": "TM2026 p9 “Tensor as a quadratic form: E=aTa”", "missing": "为何只有对称部分起作用、等值面为何是椭球、主轴从哪来", "filled": "§1.2 对称化证明；§1.3 等值面与图 1"},
        {"type": "适用区间", "source": "TM2026 p9 同一行", "missing": "默认 T 对称、a 实；非对称时 E 只读出对称部分", "filled": "§1.2 说明；§4.2、§6.2 各给惯量与应力对称的理由"},
        {"type": "机制缺口", "source": "TM2026 p10--p11 “S^T S=Σ n_k⊗n_k=1”", "missing": "只给结果，未展示并矢点乘如何缩并", "filled": "§3.3 用 §2.8 的并矢点乘逐项算 S^T S 与 S S^T"},
        {"type": "拼接缺口", "source": "TM2026 p8 对偶张量与 p12 角速度", "missing": "两页之间没有把它们接起来", "filled": "§2.6 叉乘=反对称并矢；§3.5 Ω^×=\\dot S S^T；§2.6/§3.5 说明角速度为何是矢量"},
        {"type": "机制缺口", "source": "TM2026 p10--p12 输运定理", "missing": "课件没有给固定系与体坐标系的导数关系", "filled": "§5.1 矢量版与并矢版都推；并矢版保留 D_ij 系数，用 Ω^× 的普通矩阵乘法统一乘积求导、分量式与盒式，并用 D=1 和非对称并矢 e1⊗e2 两个核对"},
        {"type": "机制缺口", "source": "TM2026 p12 对称陀螺的两条一阶方程", "missing": "为何横向分量作匀速圆周运动、φ0 控制什么、怎样与初始横向矢量对上", "filled": "§5.3 用二维横向速度与位置垂直说明半径不变，再给显式解代回核验，并用初始条件定出 ω⊥ 与 φ0；不依赖‘简谐振子’背景"},
        {"type": "压缩缺口", "source": "TM2026 p12 高斯定理的并矢版", "missing": "偏导与散度的操作意义、应力随位置变化怎样产生净力", "filled": "§6.4 先用小盒差分说明 ∂j 与净面力的关系，再给线性应力例（σ11=σ0x1/L）和三个方向的展开式；严格 Gauss 证明留在选读"},
        {"type": "压缩缺口", "source": "TM2026 p12 由 S 的导数引出角速度", "missing": "未说明角速度为何是一个矢量而非九个分量", "filled": "§2.6 反对称张量只有三个独立分量；§3.5 定义 Ω^× 并读出 Ω"},
        {"type": "图缺/图替", "source": "TM2026 p8--p12 无图", "missing": "二次型等值面、并矢作用、投影并矢、旋转算子、固定系/体系、惯量主轴、对称陀螺、斜截面分解均靠脑补", "filled": "图 1--图 8 自绘；每张图与当前公式逐项对应"},
        {"type": "机制缺口", "source": "TM2026 p8 ε_ijk 定义", "missing": "只列偶/奇排列，未说明如何识别", "filled": "§2.6 给出六个排列查表与“两两交换次数”的读法"},
        {"type": "自造缺口（本稿自查）", "source": "本稿新增解释", "missing": "可能以例代证或引入未解释术语", "filled": "§0.4 换基由三步推导；§1.5 谱定理完整陈述；§4.4 平行轴展开推导；新增术语均在首次使用处解释"}
    ],
    "old_issues": [
        {
            "location": "旧 §3.3",
            "issue": "代入 x=(u+v)/√2, y=(−u+v)/√2 实际得 E=u²+3v²，旧稿写 3u²+v²；而图 1 的 u=(1,1)/√2 与 3u²+v² 对应，故旧稿的代入式符号与结论/图不一致。",
            "evidence": "把 x=(u+v)/√2,y=(−u+v)/√2 代入 2x²+2xy+2y² 得 u²+3v²；若改为 x=(u−v)/√2,y=(u+v)/√2 则得 3u²+v²。verify.py 复核图 1 端点。",
            "new_location": "§1.3",
            "status": "fixed"
        },
        {
            "location": "旧 §4.4",
            "issue": "δ'_ij=R_ki R_kj 写成 (R R^T)_ij，应为 (R^T R)_ij。",
            "evidence": "R_ki R_kj=Σ_k (R^T)_{ik}R_{kj}=(R^T R)_{ij}；两者都等于 δ_ij，结论不变，但记号错误。",
            "new_location": "§2.7",
            "status": "fixed"
        },
        {
            "location": "旧 §4.5",
            "issue": "商法则用 u'=R u，与旧 §1.3/§4.4 的 R（列是新基分量）不一致；按该 R，矢量新坐标是 R^T u。",
            "evidence": "§0.4 直接算 x'_i=n_i·x=Σ_k R_ki x_k=(R^T x)_i。旧稿用 R u 会与 T'=R^T T R 的约定冲突。",
            "new_location": "§2.7",
            "status": "fixed"
        },
        {
            "location": "旧 §9.4",
            "issue": "按旧稿自己的 σ_ij 定义（第一指标力方向、第二指标法向），面力 t_i=σ_ij n_j，散度应为 ∂_jσ_ij；旧稿写 (∇·σ)_k=∂_iσ_ik 并说“缩并第二个指标 ∂_jσ_ji”，与定义自相矛盾。",
            "evidence": "高斯定理 ∮σ_ij n_j dS=∫∂_jσ_ij dV；对称时 ∂_jσ_ij=∂_jσ_ji，数值相同，但非对称时会差符号。",
            "new_location": "§6.4",
            "status": "fixed"
        },
        {
            "location": "旧 §3.1",
            "issue": "E 的展开写成 +2T12a1a2，未先声明 T 对称；一般系数是 T12+T21。",
            "evidence": "Σ_{i,k}T_ik a_i a_k 的交叉项合并得 (T12+T21)a1a2；旧 §3.2 才说明只取对称部分，故后续对称前提下结果不变。",
            "new_location": "§1.1",
            "status": "fixed"
        },
        {
            "location": "旧 §7.3",
            "issue": "称“对称轴…绕该轴任意转动都保持刚体不变”；长方体的棱轴只有 180° 对称，不是任意角。",
            "evidence": "长方体绕棱轴转 90° 不回到自身；但 180° 对称足以推出该轴为特征方向。结论仍成立，理由需改。",
            "new_location": "§4.3",
            "status": "fixed"
        },
        {
            "location": "旧 §5.6",
            "issue": "第二个 bullet 说第七行“和第七行差在…”，应指第六行。",
            "evidence": "该段在解释第七行（矢量点并矢）与第六行（并矢点并矢）的缩并对象不同；文字自指第七行。",
            "new_location": "§2.8",
            "status": "fixed"
        },
        {
            "location": "旧 §11 第 4 条",
            "issue": "“固定系里还要补 ω×J·ω”表述不精确；应为 ω×L=ω×(Jω)。",
            "evidence": "输运公式：dL/dt|固定=dL/dt|体+ω×L；体坐标系里 J 常量时 dL/dt|体=J·ω̇。",
            "new_location": "§8 第 4 条",
            "status": "fixed"
        },
        {
            "location": "旧 §0 最短路径",
            "issue": "称“跳过所有例子”；理解所需的教学示范不应被建议跳过。",
            "evidence": "本稿把教学示范留在主线，只允许跳过标（选读）的段落。",
            "new_location": "封面路线图",
            "status": "fixed"
        },
        {
            "location": "旧 §10 开头",
            "issue": "称课件 E8.01、E8.02 与 HW8.01--HW8.03 已在另一份运动学讲义逐题处理；本稿未读该讲义，不能沿用此覆盖声明。",
            "evidence": "本稿只处理 p8--p12 的并矢主线；p13--p18 属运动学，明确标为未展开。",
            "new_location": "封面取材声明、附录 C.1",
            "status": "not_reused"
        },
        {
            "location": "旧 §3.4",
            "issue": "用“否则椭圆在这点歪了”说明主轴法向与径向平行，属直观断言，未给出可检验条件。",
            "evidence": "新稿用谱定理与 ∇E=2Tx：x 为主轴方向时 Tx∥x，故法向平行于 x；反之亦然。",
            "new_location": "§1.3、§1.5",
            "status": "improved"
        }
    ],
    "issue_fixes": [
        {"id": "READ-01", "priority": "2", "verified": True,
         "conclusion": "§5.3 不再用“简谐振子”名称充当理由；给出二维横向速度与位置垂直、显式解代回核验、初始条件定出 ω⊥ 与 φ0 的完整局部解释。",
         "changes": ["§5.3"], "evidence": "verify.py：三组初值的方程残差、初值配对、|w⊥| 不变；PDF 文字层含初始条件式"},
        {"id": "READ-02", "priority": "2", "verified": True,
         "conclusion": "§6.4 先解释偏导固定哪些坐标、小盒差值怎样给净面力，再用线性应力例 σ11=σ0x1/L 和三个方向展开落实操作意义；严格 Gauss 证明仍为选读。",
         "changes": ["§6.4"], "evidence": "verify.py：线性应力差分、小盒净力/体积、均匀应力零散度；PDF 文字层含三个展开式"},
        {"id": "M2", "priority": "必须修复", "verified": True,
         "conclusion": "§2.1 明确固定第二槽，§2.2 的右作用与之同槽；第一槽识别明确说成转置，并用 a=e1、b=e2、输入 e1 的非对称例给出 0 与 e2 两种结果。",
         "changes": ["§2.1", "§2.2"], "evidence": "verify.py：固定第二槽输入 e1 给 0、固定第一槽给 e2、两矩阵互为转置、双线性式与右作用一致"},
        {"id": "M3", "priority": "必须修复", "verified": True,
         "conclusion": "§2.3 的指标链改为 x_iD_ij=D_ijx_i=(D^T x)_j；对称条件写成对所有输入成立；‘a⊗b 不对称’限定为一般情形，并补 a∥b 时 n⊗n 对称。",
         "changes": ["§2.3"], "evidence": "verify.py：非对称 D 下 x_iD_ij 与 D_ji x_i 不同、x_iD_ij=(D^T x)_j、对称/非对称左右作用对照"},
        {"id": "M4", "priority": "必须修复", "verified": True,
         "conclusion": "§2.5 把迹 1/2 解释为保留方向数（P 保留 1、I-P 保留 2），不再说成投影掉的自由度。",
         "changes": ["§2.5"], "evidence": "verify.py：rank(P)=1、rank(I-P)=2、两者迹为 1/2"},
        {"id": "M5", "priority": "必须修复", "verified": True,
         "conclusion": "§5.1 并矢版保留 D_ij 系数；用 Ω^× 的普通矩阵乘法统一乘积求导、分量式、盒式和 D=1/非对称并矢两个核对，删去会差负号的 D×Ω 写法。",
         "changes": ["§5.1"], "evidence": "verify.py：e1⊗e2、Ω=e3 的 LHS=RHS=diag(-1,1,0)；ε 分量式与矩阵乘积一致；D=1 时为零"},
        {"id": "M6", "priority": "必须修复", "verified": True,
         "conclusion": "§4.5/P4 不再把 (1,1,1)/√3 称为体对角线，改为与三条棱等角的方向，并说明空间对角线是 (1,2,3)/√14；所有相关计算与 P4 重复题干同步。",
         "changes": ["§4.5", "P4 题干", "附录 A P4"], "evidence": "verify.py：三棱等角、与空间对角线不平行；TeX 不再含‘体对角线’"},
        {"id": "M7", "priority": "必须修复", "verified": True,
         "conclusion": "附录 A P1 的 λ=5 主轴步骤改为 (D-5I) 行方程 -x+y=0、z=0，给出 (1,1,0) 并代回核验；λ=3、λ=2 同步写清行方程。",
         "changes": ["附录 A P1"], "evidence": "verify.py：(D-5I)(1,1,0)=0、-e1+e2 不是零空间、(D-3I)(1,-1,0)=0、(D-2I)e3=0"},
        {"id": "M8", "priority": "必须修复", "verified": True,
         "conclusion": "附录 A P5 末句改为 c∥a（c=ka）时两式相等，并给出代入；不再说‘仍差一个因子’。",
         "changes": ["附录 A P5"], "evidence": "verify.py：随机 a,b 与 c=k a 时 (a⊗b)·c=(a·b)c"},
        {"id": "S1", "priority": "局部条件对齐", "verified": True,
         "conclusion": "§1.3 改为‘惯量张量通常正定、退化时有一个零主值’，并说明谱定理只需实对称、正定只保证等值面是椭球；§2.9 的应力椭球措辞同步。",
         "changes": ["§1.3", "§2.9"], "evidence": "verify.py：奇异对称张量仍可正交对角化、存在零主值；PDF 文本含新条件"},
        {"id": "S2", "priority": "局部措辞修正", "verified": True,
         "conclusion": "§6.4 提示框改为‘对称时两缩并相等；非对称时一般不同，不是简单差一个整体符号’，保留 t_i=σij n_j 与 ∂jσij 主线。",
         "changes": ["§6.4"], "evidence": "verify.py：非对称线性场的 ∂jσij 与 ∂jσji 不同且不互为相反数"},
        {"id": "S3", "priority": "例子与所解释错误对齐", "verified": True,
         "conclusion": "附录 A P9 改用 r=(1,1,1) 的点质量例子，让 J12 真正非零；只翻 J12 符号后主值 0,3m,3m 变成 m,m,4m，例子直接检验题干所述错误。round-03 因 P9 在最终分页上一页完成，删去原 answercontinue{P9} 标记。",
         "changes": ["附录 A P9"], "evidence": "verify.py：真实 J 与翻符号 J 的矩阵、特征值、特征多项式；仍对称；PDF 文字层 p42 含 r=(1,1,1) 与两个矩阵"},
        {"id": "V1", "priority": "must_fix", "verified": True,
         "conclusion": "图 8 右图 n 参考轴改为 30°、法向分量与角标一致；左端面力改为 -σ0e1，图注按 t(±e1)=±σ0e1 重写；切向仍与 n 垂直。",
         "changes": ["图 8"], "evidence": "verify.py：轴角、法向分量角、法向+切向=t、切向⊥n、两端标签与图注文本；PDF p32 渲染已保存"},
        {"id": "V4", "priority": "minor_fix", "verified": True,
         "conclusion": "章节标题 needspace 提高到 10 行；§5 标题与 §5.1 正文现在同页（p27）。",
         "changes": ["导言区 \\hdr", "§5"], "evidence": "layout_check.py：§5 标题后同页 771 字；verify.py PDF 文字层检查 §5 页含 5.1 与‘输运定理’"},
        {"id": "V5", "priority": "minor_fix", "verified": True,
         "conclusion": "图 6 右图 e1 轴标签移到正端并向外延伸，两条图注下移到 y=-1.70；PDF bbox 检查显示 e1 标签与‘体系’图注不重叠。",
         "changes": ["图 6"], "evidence": "verify.py：PDF bbox 不重叠；TeX 坐标检查；PDF p27 渲染已保存"},
        {"id": "R2-READ02", "priority": "局部修正", "verified": True,
         "conclusion": "§6.4 均匀应力不再用“σ0 不随 x1 变”解释线性场；改为明确换成另一个应力场 σ11≡σc（常数），均匀条件作用于整个分量，导数为零。",
         "changes": ["§6.4 线性应力例后的均匀场说明"],
         "evidence": "verify.py：线性场 ∂1σ11=σ0/L 与常数场 ∂1σ11=0 分别检查；TeX 检查“换成另一个应力场/整个应力分量处处相同”存在、旧句不存在"},
        {"id": "R2-S3", "priority": "局部修正", "verified": True,
         "conclusion": "P9 明确 J′=mA 的整体因子：A 的特征方程 (λ−1)^2(λ−4)=0 只属于 A，J′ 主值为 m,m,4m，并给出直接解 det(J′−λ1)=0 的等价说明。",
         "changes": ["附录 A P9"],
         "evidence": "verify.py：np.poly(A) 与 np.poly(J′) 分别按各自尺度检查，J′ 主值 = m×A 主值；TeX 含 J′=mA 与“整体因子只把特征值乘上 m”"},
        {"id": "R2-M3", "priority": "同类措辞同步", "verified": True,
         "conclusion": "§8 速查第 3 条与三句话总结同步到主节范围：左右作用作为算子一般不同，对所有 x 相同当且仅当 D 对称；特定输入仍可能碰巧相同。",
         "changes": ["§8 第 3 条", "§8 三句话总结第 2 条"],
         "evidence": "verify.py 文本检查：新措辞存在、旧句“D·x≠x·D，除非 D 对称”不存在"},
        {"id": "V6", "priority": "minor_readability_fix", "verified": True,
         "conclusion": "图 2 与两行图注放入同一不可分块；最终分页 p15 图、关键图注同页，§2.3 紧随其后。",
         "changes": ["图 2 与图注"],
         "evidence": "verify.py PDF 文字层：图内标签 b·x=0.4 与图注“图2（自绘）”同页且标签在图注上方；layout-report 图 2 p15"},
        {"id": "V7", "priority": "minor_readability_fix", "verified": True,
         "conclusion": "P4 续解移到实际续页 p40 页首，重列 n、J 与 I(n)=145/18，并标明本页验证 ω·L=2K；P9 因最终分页不再跨页，删去已落在同页中部的旧续解标记。",
         "changes": ["附录 A P4", "附录 A P9 续解标记"],
         "evidence": "verify.py PDF 文字层：P4 详解 p39，P4 续解 p40 且与“验证：取”及条件同页；P9 详解 p42 一页内完成"},
        {"id": "Q1", "priority": "moderate", "verified": True,
         "conclusion": "verify.py 删除‘覆盖至少 15 条/勘误至少 8 条’的无依据门槛；改为逐条字段完整、原题 P1-P10 与旧稿题号一一对应、P11/P12 标新增、勘误新位置可在 TeX 定位、无重复条目。",
         "changes": ["verify.py source-map 段"], "evidence": "verify.py 运行结果；source-map.json 的 coverage/practice_map/old_issues/issue_fixes"}
    ],
    "open_items": [
        "round-03 的外部目视审核尚未进行；当前模型不支持图像输入，render/ 下 48 页 PNG 待支持看图的审核者检查布局与几何。已用 PDF 文字层、bbox、同页/页位与坐标检查替代，但不声称目视通过。",
        "学习者实际试读尚未发生；本稿只做了阅读路径自查，不能声称学习者已理解或已掌握。",
        "旧稿 §10 提到的另一份运动学讲义未读；p13--p18 的运动学例题未在本稿重复，属于明确的范围外内容。",
        "check_handout 与 verify.py 只检查结构、数值、页位与日志，不证明数学推导的每一步都最优；外部审核仍可能提出新的讲解或布局问题。",
        "本轮只按 review-round02.json 的 R2-READ02、R2-S3、R2-M3、V6、V7 局部返工；未把外部审核通过当作学习效果已验证。",
        "P2/P8/P10/P11 的续解标题仍在同页中部（沿自 round-02 的已知排版小问题，本轮未扩大改动）；P4 续解已在实际续页 p40 页首，P9 在最终分页上一页完成并删去旧续解标记。"
    ]
}

out = HERE / "source-map.json"
out.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"wrote {out} ({out.stat().st_size} bytes)")
print(f"coverage {len(data['coverage'])}; practices {len(data['practice_map'])}; gaps {len(data['gaps'])}; old_issues {len(data['old_issues'])}")
