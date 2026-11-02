# -*- coding: utf-8 -*-
"""Build the companion XLSX checklist for the lecture note."""
import sys
from math import ceil
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table, TableStyleInfo

OUT = sys.argv[1]

HEADERS = ["编号", "层级", "技术 / 方法", "一句话核心", "关键公式或算法",
           "代表文献", "证据等级", "实盘普及度", "主要失效条件", "开源实现 / 工具", "学习优先级"]

ROWS = [
    # L0 数据
    ["D01", "L0 数据", "时点正确（PIT）数据", "用当时可得的数据，而不是事后重述版", "财报按公告日入库；保留原始值+修订标记", "López de Prado (2018) 第 2–4 章", "A", "全行业标配", "修订数据无标记、公告日错位", "自建 / Wind / Choice", "P0"],
    ["D02", "L0 数据", "幸存者偏差处理", "样本必须包含退市、ST、被并购股票", "全样本 + 退市日收益", "Banz (1981) 起的规模研究传统", "A", "全行业标配", "只用当前成分股", "CRSP / 交易所全量", "P0"],
    ["D03", "L0 数据", "复权与成分股历史", "前复权会引入未来信息", "后复权价格 + 复权因子；逐期成分股名单", "指数编制方案（中证/国证）", "A", "全行业标配", "用今日成分回测历史", "Tushare / 中证指数官网", "P0"],

    # L1 微观结构
    ["M01", "L1 微观结构", "订单流不平衡 OFI", "买卖挂单变化的净额驱动短期价格", "OFI = Σ买侧变化 − Σ卖侧变化", "Cont, Kukanov & Stoikov (2014)", "A", "HFT / 日内", "同步指标，不可直接预测", "自建（需逐笔数据）", "P2"],
    ["M02", "L1 微观结构", "VPIN 有毒流", "用成交量桶度量知情交易概率", "VPIN = |V_buy − V_sell| / (V_buy + V_sell)", "Easley, López de Prado & O'Hara (2012)", "B", "做市风控", "对桶大小与分类算法敏感", "自建", "P2"],
    ["M03", "L1 微观结构", "Avellaneda-Stoikov 做市", "保留价格随库存偏移，价差补偿库存风险", "r = s − qγσ²(T−t)；δ_a+δ_b = γσ²(T−t)+(2/γ)ln(1+γ/k)", "Avellaneda & Stoikov (2008)", "A", "做市商标准", "泊松到达、连续扩散、无博弈假设", "自建 / 加密做市框架", "P3"],
    ["M04", "L1 微观结构", "平方根冲击律", "冲击与下单量占成交量之比的平方根成正比", "E[ΔP] ≈ Y·σ·√(Q/V)，Y≈1", "Almgren et al. (2005)；Bouchaud 等", "A", "执行台与券商", "小单/极端行情下偏离", "自建", "P1"],
    ["M05", "L1 微观结构", "交易成本模型", "把佣金、税费、价差、冲击、机会成本逐项建模", "cost(order, market_state) 函数", "Frazzini, Israel & Moskowitz (2018)", "A", "全行业标配", "用固定 bp 代替逐笔成本", "自建", "P0"],

    # L2 统计套利
    ["S01", "L2 统计套利", "距离法配对交易", "标准化价格距离最小的股票对做均值回归", "z = (spread−μ)/σ；|z|>2 开仓，z→0 平仓", "Gatev, Goetzmann & Rouwenhorst (2006)", "B", "对冲基金基础策略", "拥挤、结构断裂、成本后利润消失", "statsmodels / 自建", "P2"],
    ["S02", "L2 统计套利", "协整与 O-U 半衰期", "价差平稳才可交易；半衰期决定持仓周期", "t_half = ln2/θ；θ 由 AR(1) 估计", "Engle & Granger (1987)", "A", "中频 stat arb", "协整关系会永久破裂", "statsmodels.tsa", "P2"],
    ["S03", "L2 统计套利", "PCA 残差套利", "剥离市场共同因子后交易残差", "s = (X−μ)/σ；±1.25 开仓", "Avellaneda & Lee (2010)", "B", "中频 stat arb", "2007 年后收益显著衰减", "自建 / sklearn PCA", "P3"],
    ["S04", "L2 统计套利", "卡尔曼滤波动态对冲比", "让对冲比率随时间自适应", "状态方程 β_t = β_{t−1} + w_t", "Chan (2013) 第 3 章", "B", "中频", "对结构断裂反应滞后", "pykalman", "P3"],

    # L3 因子
    ["F01", "L3 因子", "CAPM / FF3 / Carhart / FF5", "用少量共同因子解释横截面收益", "r−r_f = α + β_m·MKT + β_s·SMB + β_v·HML + …", "Sharpe (1964)；Fama-French (1993, 2015)；Carhart (1997)", "A", "工业标配", "作为纯 alpha 已高度拥挤", "statsmodels / linearmodels", "P0"],
    ["F02", "L3 因子", "价值因子 HML", "低估值长期跑赢高估值", "账面市值比排序，多空分组", "Fama & French (1992, 1993)", "A", "指数增强核心", "价值陷阱、可连续跑输十年", "Ken French 数据库", "P0"],
    ["F03", "L3 因子", "动量 MOM", "过去 12 个月赢家继续赢", "t−12 至 t−2 收益排序", "Jegadeesh & Titman (1993)", "A", "CTA / 多因子", "动量崩溃（2009、2020）", "自建", "P1"],
    ["F04", "L3 因子", "短期反转", "过去 1 个月输家短期反弹", "−r_{t−20,t}", "Jegadeesh (1990)；Lehmann (1990)", "A", "A 股尤其有效", "换手极高，成本吞噬", "自建", "P1"],
    ["F05", "L3 因子", "质量 / 盈利 RMW", "高盈利质量公司溢价", "毛利率、ROE、应计项目排序", "Novy-Marx (2013)；Fama-French (2015)", "A", "多因子", "财务造假、行业集中", "自建", "P1"],
    ["F06", "L3 因子", "低波 / BAB", "低 beta 股票风险调整后更优", "按 beta 排序，多低空高并加杠杆中性", "Frazzini & Pedersen (2014)", "A", "smart beta", "加息周期、拥挤", "自建", "P2"],
    ["F07", "L3 因子", "盈余漂移 PEAD", "盈余惊喜后价格持续漂移", "SUE = 盈余惊喜 / 标准差", "Bernard & Thomas (1989)", "B", "事件驱动", "信息效率提升后衰减", "自建", "P2"],
    ["F08", "L3 因子", "换手率情绪因子（A 股）", "高换手预示未来低收益", "换手率横截面排序，取负", "Liu, Stambaugh & Yuan (2019)", "B", "A 股指增常用", "牛市初期失效", "自建", "P1"],
    ["F09", "L3 因子", "因子中性化与正交化", "剥离行业、市值、风格后再比较", "对行业哑变量+对数市值回归取残差", "Grinold & Kahn (2000)", "A", "工业标配", "正交化顺序影响解释", "自建 / Alphalens", "P0"],
    ["F10", "L3 因子", "多重检验与因子动物园审查", "新因子需 t>3 或 DSR/PBO 才可信", "Harvey-Liu-Zhu 门槛；FDR 控制", "Harvey, Liu & Zhu (2016)；Hou, Xue & Zhang (2020)", "A", "严谨机构必备", "最常被跳过", "自建", "P0"],

    # L4 机器学习
    ["L01", "L4 机器学习", "线性正则化基线", "Ridge/Lasso 是判断非线性增量的唯一诚实基线", "min ‖y−Xw‖² + λ‖w‖₁ 或 λ‖w‖₂", "Gu, Kelly & Xiu (2020) 的基线设定", "A", "工业标配", "无法捕捉交互", "scikit-learn", "P0"],
    ["L02", "L4 机器学习", "梯度提升树 GBDT", "表格型特征的工业主力", "加法模型 + 二阶梯度 + 正则项", "Krauss, Do & Huck (2017)", "B+", "工业主力", "分布漂移、外推能力差", "LightGBM / XGBoost / CatBoost", "P0"],
    ["L03", "L4 机器学习", "MLP / LSTM / TCN", "序列与非线性组合", "门控循环 / 因果卷积", "Fischer & Krauss (2018)", "B", "作为组件", "样本少、易过拟合", "PyTorch", "P2"],
    ["L04", "L4 机器学习", "Transformer 类时序模型", "长序列与跨股票注意力", "PatchTST / iTransformer 分块注意力", "Zeng et al. (2023) 的警告；Gu-Kelly-Xiu (2020)", "C", "研究为主", "强噪声下不如线性模型", "PyTorch / GluonTS", "P3"],
    ["L05", "L4 机器学习", "图神经网络 GNN", "把供应链、行业、持仓关系变成特征", "GCN/GAT 邻居聚合", "Feng et al. (2019)", "C", "研究为主", "过平滑、伪边污染", "PyG / DGL", "P3"],
    ["L06", "L4 机器学习", "排序学习与 IC 损失", "优化排序而非均方误差", "ListNet / LambdaRank / IC loss", "Gu-Kelly-Xiu (2020)；实务经验", "B", "成熟机构常用", "实现复杂、易过拟合", "自建", "P2"],
    ["L07", "L4 机器学习", "三重障碍标签", "用路径而非终点定义标签", "上轨/下轨/时间上限三选一", "López de Prado (2018)", "B", "进阶", "样本不平衡、实现复杂", "mlfinlab", "P2"],
    ["L08", "L4 机器学习", "滚动重训与漂移监控", "模型必须随市场更新", "walk-forward + PSI/KS 监控", "实务标准", "A", "工业标配", "重训过频导致不稳定", "MLflow / 自建", "P0"],

    # L5 强化学习
    ["R01", "L5 强化学习", "RL 最优执行", "在冲击与风险间学习最优拆单", "MDP + 策略梯度 / Q-learning", "Nevmyvaka, Feng & Kearns (2006)", "B+", "券商算法交易", "模拟器与真实撮合差距", "FinRL / 自建", "P3"],
    ["R02", "L5 强化学习", "RL 做市报价", "在 A-S 解析解基础上微调报价", "状态=库存+订单簿；动作=价差", "Avellaneda & Stoikov (2008) 为基准", "B", "加密/期货做市", "对手博弈、延迟", "自建", "P4"],
    ["R03", "L5 强化学习", "端到端组合 RL", "直接输出仓位", "状态→权重", "Deng et al. (2016)；FinRL (2020)", "C", "少见成功案例", "样本效率、奖励黑客、种子方差", "FinRL", "P4"],
    ["R04", "L5 强化学习", "离线 RL / 模仿学习", "只从历史数据学习，避免在线试错", "CQL / IQL / BC", "近年离线 RL 文献", "C", "研究", "离线数据覆盖不足", "d3rlpy", "P4"],

    # L6 NLP
    ["N01", "L6 NLP", "金融情感词典", "领域词典优于通用词典", "LM 词典词频 → 情感分", "Loughran & McDonald (2011)", "B", "事件驱动辅助", "无法处理否定与语境", "自建 / pysentiment", "P2"],
    ["N02", "L6 NLP", "FinBERT 类模型", "上下文情感与句向量", "预训练 + 微调分类头", "Araci (2019)；Yang et al. (2020)", "B−", "辅助信号", "标注数据少、衰减快", "HuggingFace", "P3"],
    ["N03", "L6 NLP", "LLM 事件抽取", "从公告/新闻抽取结构化事件", "few-shot + 结构化输出", "Kim, Muhn & Nikolaev (2024)", "B−", "早期采用", "成本、幻觉、覆盖稀疏", "OpenAI / 本地模型", "P3"],
    ["N04", "L6 NLP", "LLM 直接选股", "让模型判断该买什么", "prompt → 打分 → 组合", "Lopez-Lira & Tang (2023, rev. 2025)", "C", "营销多、实盘少", "预训练记忆污染、不可交易", "—", "P4"],
    ["N05", "L6 NLP", "多智能体交易框架", "多角色辩论模拟投研流程", "分析师/研究员/风控/交易员 agent", "Xiao et al. (2024) TradingAgents", "C", "演示阶段", "回测短、成本缺失、不可复现", "TradingAgents", "P4"],
    ["N06", "L6 NLP", "另类数据", "卫星、卡数据、App、招聘", "覆盖率 × 领先期 × 历史长度", "供应商白皮书与实证研究", "B−", "大机构", "昂贵、样本偏差、合规", "Orbital / Consumer Edge 等", "P4"],

    # L7 组合
    ["P01", "L7 组合", "Markowitz 均值方差", "在收益与方差间求最优", "max wᵀμ − (λ/2)wᵀΣw", "Markowitz (1952)", "A", "标配（必须加约束）", "误差最大化器、权重爆炸", "PyPortfolioOpt / cvxpy", "P0"],
    ["P02", "L7 组合", "协方差收缩", "把样本协方差向结构化目标收缩", "Σ = (1−δ)S + δF", "Ledoit & Wolf (2004)", "A", "工业标配", "收缩强度选择", "scikit-learn / 自建", "P1"],
    ["P03", "L7 组合", "随机矩阵理论去噪", "压缩噪声特征值", "Marchenko-Pastur 边界内视为噪声", "López de Prado (2020)", "B", "进阶", "样本量不足时效果有限", "自建", "P3"],
    ["P04", "L7 组合", "Black-Litterman", "以市场均衡为先验融合观点", "μ_BL = [(τΣ)⁻¹+PᵀΩ⁻¹P]⁻¹[(τΣ)⁻¹Π+PᵀΩ⁻¹Q]", "Black & Litterman (1992)", "A", "机构资产配置", "观点不确定性设定主观", "PyPortfolioOpt", "P2"],
    ["P05", "L7 组合", "风险平价 / ERC", "每个资产风险贡献相等", "RC_i = w_i(Σw)_i/(wᵀΣw) = 1/N", "Roncalli (2013)", "A", "资管产品", "股债相关性转正时失效", "Riskfolio-Lib", "P2"],
    ["P06", "L7 组合", "层次风险平价 HRP", "聚类 + 递归二分，免求逆", "d_ij=√((1−ρ_ij)/2) → 聚类 → 二分", "López de Prado (2016)", "B", "逐步普及", "忽略预期收益、对 linkage 敏感", "Riskfolio-Lib", "P2"],
    ["P07", "L7 组合", "因子风险模型 Barra", "横截面回归分解因子收益与特质收益", "r_i = Σ X_ik·f_k + u_i（WLS）", "MSCI Barra 方法论", "A", "工业标配", "模型自建成本高", "自建 / 商业模型", "P2"],
    ["P08", "L7 组合", "凯利与分数凯利", "长期增长率最大的下注比例", "f* = μ/σ²；实操用 1/4–1/2 凯利", "Kelly (1956)；Thorp (2006)", "B", "仓位管理", "参数估计误差导致爆仓", "自建", "P2"],
    ["P09", "L7 组合", "波动率目标", "稳定风险暴露，改善复利", "w_t = target_vol / σ̂_t", "Moreira & Muir (2017)；Barroso & Santa-Clara (2015)", "A", "CTA / 多策略", "波动率估计滞后", "自建", "P1"],
    ["P10", "L7 组合", "CVaR 与回撤约束", "控制尾部而非仅方差", "min CVaR_α(w) s.t. 约束", "Rockafellar & Uryasev (2000)", "A", "机构风控", "历史模拟依赖样本", "cvxpy", "P2"],
    ["P11", "L7 组合", "成本感知优化", "把换手成本写进目标函数", "max wᵀμ − (λ/2)wᵀΣw − c‖w−w_prev‖₁", "实务标准", "A", "成熟机构", "c 的估计误差", "cvxpy", "P1"],

    # L8 回测
    ["B01", "L8 回测", "Purged K-Fold + Embargo", "剔除标签重叠样本，隔离测试集之后", "训练集标签区间不与测试集重叠 + embargo", "López de Prado (2018)", "A", "必须使用", "最常被跳过", "sklearn 改造 / mlfinlab", "P0"],
    ["B02", "L8 回测", "CPCV 组合清洗交叉验证", "给出多条回测路径的分布", "切 N 块取 k 块测试，遍历组合", "López de Prado (2018)", "A", "进阶机构", "计算量大", "自建", "P2"],
    ["B03", "L8 回测", "多重检验校正", "控制试了多少次带来的选择偏差", "Bonferroni / BHY-FDR / White Reality Check / Hansen SPA", "White (2000)；Hansen (2005)；Benjamini & Hochberg (1995)", "A", "严谨机构", "独立试验数难估计", "statsmodels / 自建", "P1"],
    ["B04", "L8 回测", "Deflated Sharpe Ratio", "扣除多次试验后的显著性", "DSR = Φ((SR̂−SR₀)√(T−1)/√(1−γ₃SR̂+((γ₄−1)/4)SR̂²))", "Bailey & López de Prado (2014)", "A", "必须使用", "N 与 V[SR] 的估计主观", "自建", "P0"],
    ["B05", "L8 回测", "PBO / CSCV", "训练集最优策略在测试集跌回中位数的概率", "PBO = P(ln(ω/(1−ω)) < 0)，S=16 时 12870 组", "Bailey, Borwein, López de Prado & Zhu (2017)", "A", "必须使用", "S 的选择影响结果", "自建", "P0"],
    ["B06", "L8 回测", "成本敏感性分析", "看夏普随成本上升的衰减速度", "SR vs 0–50bp 曲线", "Novy-Marx & Velikov (2016)", "A", "必须使用", "忽略容量", "自建", "P0"],
    ["B07", "L8 回测", "容量曲线", "资金放大后的收益衰减", "规模 → 冲击 → 净收益", "Frazzini, Israel & Moskowitz (2018)", "A", "机构必备", "冲击模型误差", "自建", "P1"],

    # L9 执行
    ["E01", "L9 执行", "Almgren-Chriss 最优执行", "在冲击与风险间求最优拆单轨迹", "x(t)=X·sinh(κ(T−t))/sinh(κT)，κ≈√(λσ²/η)", "Almgren & Chriss (2001)", "A", "券商算法交易", "线性冲击假设、参数误设", "自建", "P2"],
    ["E02", "L9 执行", "TWAP / VWAP / POV / IS", "按时间、成交量或实施差额执行", "四种基准与适用场景", "Cartea, Jaimungal & Penalva (2015)", "A", "工业标配", "轨迹可预测被抢跑", "自建 / 券商算法", "P1"],
    ["E03", "L9 执行", "冲击估计与预交易成本", "下单前先算这笔交易值不值", "impact_bp ≈ k·σ·√(Q/ADV)·10000", "Almgren et al. (2005)", "A", "执行台", "小单与极端行情偏离", "自建", "P1"],
    ["E04", "L9 执行", "反抢跑与随机化", "别让对手读出你的节奏", "时间/数量随机扰动、限价市价混用", "van Kervel & Menkveld (2019)", "B", "机构执行", "过度随机化增加跟踪误差", "自建", "P3"],

    # L10 工程
    ["G01", "L10 工程", "事件驱动回测", "逐笔模拟撮合与订单生命周期", "事件队列 + 撮合引擎", "NautilusTrader / LEAN 文档", "A", "终审必备", "慢、实现复杂", "NautilusTrader / backtrader", "P1"],
    ["G02", "L10 工程", "向量化回测", "快速粗筛大量因子", "矩阵运算 + 向量化持仓", "vectorbt 文档", "A", "研究阶段", "难以精确建模撮合", "vectorbt", "P1"],
    ["G03", "L10 工程", "实验与模型版本化", "不能复现的回测等于没有回测", "数据版本 + 参数 + 结果三元组", "MLOps 实践", "A", "成熟团队", "小团队常忽略", "MLflow / DVC", "P2"],
    ["G04", "L10 工程", "监控与归因", "每天回答赚的是 alpha 还是 beta", "滚动 IC、实施差额、暴露漂移", "实务标准", "A", "成熟团队", "指标过多反而失焦", "自建看板", "P2"],

    # 反清单
    ["X01", "反清单", "“AI 炒股软件”识别", "只展示曲线、不谈回撤与容量的都要警惕", "六红旗清单（见讲义 14.2）", "—", "—", "—", "无法验证实盘", "—", "P0"],
    ["X02", "反清单", "深度学习端到端预测股价", "回测漂亮、实盘罕见", "—", "见讲义第 6、14 章", "C", "少见", "非平稳 + 成本", "—", "P4"],
]

WIDTHS = [7, 13, 24, 34, 42, 40, 9, 14, 30, 26, 10]

GRADE_FILL = {"A": "D9EAD3", "B+": "FFF2CC", "B": "FFF2CC", "B−": "FFF2CC",
              "C": "F4CCCC", "—": "EDEDED"}

thin = Side(style="thin", color="BFBFBF")
BORDER = Border(left=thin, right=thin, top=thin, bottom=thin)


def estimate_height(values):
    lines = 1
    for v, w in zip(values, WIDTHS):
        if v is None:
            continue
        text = str(v)
        # column width is measured in ASCII character units; a CJK glyph is ~2
        units = sum(2 if ord(ch) > 127 else 1 for ch in text)
        per_line = max(4, int(w * 1.0))
        lines = max(lines, ceil(units / per_line))
    return min(160, max(20, lines * 14 + 5))


def style_header(ws, row, ncol):
    for c in range(1, ncol + 1):
        cell = ws.cell(row=row, column=c)
        cell.font = Font(name="微软雅黑", size=10, bold=True, color="FFFFFF")
        cell.fill = PatternFill("solid", fgColor="1F3864")
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = BORDER


def main():
    wb = Workbook()

    # ---------- sheet 1 ----------
    ws = wb.active
    ws.title = "技术清单"
    ws.sheet_view.showGridLines = False

    ws["A1"] = "AI 炒股与量化交易：成熟技术清单"
    ws["A1"].font = Font(name="微软雅黑", size=16, bold=True, color="1F3864")
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=len(HEADERS))
    ws.row_dimensions[1].height = 30

    ws["A2"] = "证据等级：A=多市场多时期验证且扣成本后有效；B=有条件成熟，依赖执行与市场结构；C=研究前沿，证据薄弱。P0=必学，P4=了解即可。"
    ws["A2"].font = Font(name="微软雅黑", size=9, color="595959")
    ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=len(HEADERS))
    ws.row_dimensions[2].height = 20

    header_row = 3
    for i, h in enumerate(HEADERS, start=1):
        ws.cell(row=header_row, column=i, value=h)
    style_header(ws, header_row, len(HEADERS))
    ws.row_dimensions[header_row].height = 30

    for r, row in enumerate(ROWS, start=header_row + 1):
        for c, val in enumerate(row, start=1):
            cell = ws.cell(row=r, column=c, value=val)
            cell.font = Font(name="微软雅黑", size=9, color="1A1A1A")
            cell.alignment = Alignment(vertical="top", wrap_text=True,
                                       horizontal="center" if c in (1, 7, 8, 11) else "left")
            cell.border = BORDER
            if (r - header_row) % 2 == 0:
                cell.fill = PatternFill("solid", fgColor="F2F4F8")
        grade = row[6]
        if grade in GRADE_FILL:
            gc = ws.cell(row=r, column=7)
            gc.fill = PatternFill("solid", fgColor=GRADE_FILL[grade])
            gc.font = Font(name="微软雅黑", size=9, bold=True, color="1A1A1A")
        ws.row_dimensions[r].height = estimate_height(row)

    for i, w in enumerate(WIDTHS, start=1):
        ws.column_dimensions[get_column_letter(i)].width = w

    last_row = header_row + len(ROWS)
    ws.freeze_panes = f"A{header_row + 1}"
    ws.auto_filter.ref = f"A{header_row}:{get_column_letter(len(HEADERS))}{last_row}"
    ws.print_title_rows = f"{header_row}:{header_row}"
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True

    # ---------- sheet 2 ----------
    ws2 = wb.create_sheet("等级与读法")
    ws2.sheet_view.showGridLines = False
    ws2["A1"] = "证据等级定义与使用建议"
    ws2["A1"].font = Font(name="微软雅黑", size=14, bold=True, color="1F3864")
    ws2.merge_cells("A1:D1")

    head2 = ["等级", "定义", "典型技术", "使用建议"]
    for i, h in enumerate(head2, start=1):
        ws2.cell(row=3, column=i, value=h)
    style_header(ws2, 3, len(head2))

    data2 = [
        ["A", "多个市场、多个时期被独立重复验证；扣成本后仍有经济意义；机构工业标准流程的一部分",
         "因子模型、组合优化、最优执行、回测方法论、时间序列动量", "可以作为策略的地基"],
        ["B", "证据可靠，但高度依赖执行细节、市场结构或成本假设；换环境可能失效",
         "配对交易、GBDT 选股、文本情绪、HRP、风险平价", "可以用，但必须自己做成本与稳健性检验"],
        ["C", "主要在论文回测中成立，缺少独立复现，或计入真实成本后不成立",
         "端到端深度学习、RL 直接选股、LLM 选股、多智能体交易", "可以研究，不要作为主要收益来源"],
    ]
    for r, row in enumerate(data2, start=4):
        for c, val in enumerate(row, start=1):
            cell = ws2.cell(row=r, column=c, value=val)
            cell.font = Font(name="微软雅黑", size=9)
            cell.alignment = Alignment(vertical="top", wrap_text=True,
                                       horizontal="center" if c == 1 else "left")
            cell.border = BORDER
        ws2.cell(row=r, column=1).fill = PatternFill("solid", fgColor=GRADE_FILL[row[0]])
        ws2.row_dimensions[r].height = 52

    ws2["A9"] = "三种读法"
    ws2["A9"].font = Font(name="微软雅黑", size=12, bold=True, color="1F3864")

    data3 = [
        ["60 分钟速览", "读第 1、2、10、14 章 + 附录 C 自检清单；这四部分决定会不会亏钱"],
        ["一周入门", "加读第 3–6 章与第 9 章，配合第 15 周路径前 4 周"],
        ["一学期系统", "全书顺序读，把第 15 章的编程作业全部做一遍"],
    ]
    for r, row in enumerate(data3, start=10):
        ws2.cell(row=r, column=1, value=row[0]).font = Font(name="微软雅黑", size=9, bold=True)
        ws2.cell(row=r, column=2, value=row[1]).font = Font(name="微软雅黑", size=9)
        ws2.merge_cells(start_row=r, start_column=2, end_row=r, end_column=4)
        ws2.cell(row=r, column=2).alignment = Alignment(vertical="top", wrap_text=True)

    for i, w in enumerate([10, 62, 42, 34], start=1):
        ws2.column_dimensions[get_column_letter(i)].width = w

    ws2["A15"] = "说明：本表为教学材料，不构成投资建议；文献与数据以原始来源为准。"
    ws2["A15"].font = Font(name="微软雅黑", size=8, color="808080")

    wb.save(OUT)
    print("saved", OUT, "rows", len(ROWS))


if __name__ == "__main__":
    main()
