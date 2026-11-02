# A 股 AI 量化研究栈

一套可在个人电脑上完整跑通的量化研究框架：真实数据、可复现的回测、
以及严格的过拟合诊断。

配套讲义：`lectures/main.pdf`
配套报告：`reports/拟合精度报告.pdf`

---

## 一、这套东西包含什么

| 交付物 | 位置 | 说明 |
|---|---|---|
| 本地数据库 | `data/quant.db` | 全 A 股日线 1675 万行、28.5 万条 PIT 财报、47.7 万条估值快照、1950 条指数成分、指数与日历 |
| 因子库 | `aq/factors.py` | 39 个因子，每个都带公式、方向、回看期与注册表 |
| 研究框架 | `aq/*.py` | 面板、去极值/中性化、IC 评价、Purged CV/CPCV、DSR/PBO、回测 |
| 数据管道 | `scripts/00..05,09` | 增量更新、断点续抓、多源适配、数据质量巡检 |
| 研究流程 | `scripts/06..08` | 因子计算与评价、多协议重复测试、图表与报告 |
| 补充数据层 | `shm_*` 表 + `data/shm/` | 外部快照：真实成交额/换手率、四档资金流、日频估值、121 个财务指标（2020–2026） |
| 讲义 | `lectures/main.tex` | 13 章 + 8 个附录，可直接 `xelatex` 编译 |

## 二、环境

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Python 3.12 + pandas 3.x + LightGBM 4.x。数据库为 SQLite（无需额外安装）。

## 三、一键复现

```powershell
$py = ".\.venv\Scripts\python.exe"

# 日常增量更新（幂等，可随时中断）：只补缺口
& $py scripts\00_update.py

# 交付物自检（结构与数值回归检查；通过不等于研究有效）
& $py scripts\verify_delivery.py

# 或从头完整跑一遍：
& $py scripts\01_financials.py            # 财报（约 6 分钟）
& $py scripts\02_prices.py                 # 全市场日线（约 30 分钟，可 --resume 续抓）
& $py scripts\03_calendar.py               # 交易日历与指数
& $py scripts\04_valuation.py              # 月度估值快照
& $py scripts\05_finalize.py --save        # 上市/退市日 + 数据质量报告
& $py scripts\09_index_members.py          # 指数成分股（每跑一次积累一期快照）
& $py scripts\06_factors.py                # 因子计算与单因子评价（约 10 分钟）
& $py scripts\07_model.py                  # 多协议重复测试 + 过拟合诊断
& $py scripts\08_report.py                 # 仅重建报告；首次应先完成下方补充因子步骤

# 可选：接入外部数据快照（a_share_20260831）
& $py scripts\10_ingest_shm.py             # 导入四张 parquet
& $py scripts\11_flow_factors.py           # 资金流因子与换皮检验
& $py scripts\12_quality_factors.py        # 质量因子族（20 个）与有效样本诊断

# 严格化检验（t>3 门槛、剔除最小 30% 市值）
& $py scripts\13_universe_test.py          # 输出 universe_test.csv / factor_significance_t3.csv
& $py scripts\14_gen_strictness_tex.py     # 生成讲义表格
& $py scripts\13_refresh_documents.py      # 重建两份 PDF（保证与 CSV 一致）

# 指数增强（long-only）回测
& $py scripts\15_index_enhance.py          # 指数增强回测
& $py scripts\16_alpha_decomp.py           # alpha 多头/空头端分解与市值分组
& $py scripts\07_model.py --diagnostics-only # 复用预测与 IC，重算统计，不重训
& $py scripts\13_refresh_documents.py       # 同步表格、README、报告及讲义 PDF
```

编译讲义：

```powershell
cd lectures
xelatex -interaction=nonstopmode main.tex
xelatex -interaction=nonstopmode main.tex
```

## 四、数据源说明（重要）

2026-10-31 实测：东方财富 `push2his` 在约 50 次请求后被 IP 封锁；
腾讯 `fqkline` 在约 200 次后触发 WAF；baostock 并发即被限速；
**新浪 `CN_MarketData` 稳定可用**，本项目最终采用它。

免费接口随时可能变化。若某一步失败，请先读 `scripts/02_prices.py` 顶部的
「数据源决策记录」，那里列出了当时验证过的备选通道与失败方式。

### 补充数据层（外部快照 a_share_20260831）

2026 年 10 月接入的一份外部 A 股快照，覆盖 2020-01 至 2026-08，含四档资金流与
121 个财务指标。三项核验结论：

- **价格一致性**：与本地库匹配 554 万行，收盘价相对误差 >0.1% 的比例为 0.000%
- **Point-in-Time**：通过（净利润变化日精确落在公告日）
- **覆盖偏差**：股票池只有全市场的 76%–83%，且各年比例不同——**只能作补充，不能替代全市场库**

结论详见讲义附录 F/G/H；因子结果见 `reports/flow_factor_eval.csv`、`reports/quality_factor_eval.csv`、
`reports/universe_test.csv`。

**规模因子已判定为不可用**：剔除最小 30% 市值后，其 IC 从 +0.0097 翻为 −0.0050（附录 H）。

**多空 alpha 不可变现**：把同一批样本外预测放进指数增强框架（long-only、行业中性、
2018–2025 共 383 期），跟踪误差从 0.1% 调到 4.0%，年化超额从 −0.9% 单调恶化到 −6.4%，
信息比率始终为负。

进一步分解（第 11.6 节）：价格差年化 +30.9%（t=6.67），**多头端与空头端都有 alpha**
（+10.7% / +18.5%）；但按市值分组后，多头端在小盘 +12.0%（t=5.53）、中盘 +10.3%（t=4.81）、
**大盘仅 +3.1%（t=1.27，不显著）**。市值加权基准由大盘股主导，这就是指增失败的原因。

<!-- AUDIT-RESULTS:START -->
修订后的两批因子均使用次日开盘到第六日开盘标签，原始/调整后 IC 从完整序列汇总：

- 资金流 `mfr` IC **-0.0108**；`mfr_pos_20` 增量 IC **+0.0246**，HAC t **5.41**。这是补充池的条件关联，尚未加入模型重训。
- 撤回质量因子“全部不显著”和“只有 14 个有效样本”的旧结论：旧表误将年度 t 的平均当全样本 t。现表包含 `n`、`nw_lags`、`n_eff` 和调整后有效样本量；`q_cfo_ni` 的方差等价样本量为 **371**（1609 个有值日期），依赖带宽选择。
- DSR 压力情景 **0.8220**（假定 603 个独立试验及零假设离散度下限）。603 是情景，完整搜索史未知，不能声称整个研究通过多重检验。
- PBO **0.107** 仅覆盖五候选、402 个共同有效日期；相关系数范围 0.716–0.994。缺失收益不再填零。
- `reports/dsr_sensitivity.csv` 和 `reports/ic_inference_sensitivity.csv` 保存完整敏感性结果；所有结果均属被反复查看过的历史数据内验证。
<!-- AUDIT-RESULTS:END -->

### 已知局限

1. **北交所缺失**：新浪无北交所接口，355 只未纳入（占比 6.4%，2021 年后才有该板块）。
2. **成交额为估算值**：由「成交量 × 当日均价」估算，误差通常 < 2%。
3. **历史股本为月度近似**：换手率用月度股本快照前向填充，送转后一个月内会有偏差。
4. **财务数据为最新披露值**：免费源不提供财报重述历史，存在轻微前视（已在讲义中讨论）。

5. **研究限制**：完整搜索日志缺失、无未见前瞻样本、PBO 仅五候选；未完成 long-only、事件驱动执行、成本分层或正式滚动稳定性检验。
6. **覆盖限制**：2010–2019 价格缺第二来源验证，退市股存在遗漏；补充库逐年变化且 2021 年缺失机制未知。
7. **工程限制**：外部数据路径仍需配置，基础 bar 表换手几乎为空；仅统计诊断增加了缓存重算，因子全流程尚无完整增量机制。

## 五、目录结构

```
ai-quant-2026/
├─ aq/                    框架
│  ├─ config.py           路径与股票池口径
│  ├─ http.py             双通道 HTTP（直连/代理交替）
│  ├─ sources.py          数据源适配
│  ├─ db.py / schema.sql  SQLite 读写与表结构
│  ├─ panel.py            研究面板（复权/PIT/TTM/可成交/标签）
│  ├─ factors.py          因子库（39 个 + 宽表引擎）
│  ├─ neutralize.py       去极值/标准化/行业市值中性化
│  ├─ metrics.py          IC/ICIR/分层/换手/衰减/相关性
│  ├─ cv.py               Purged K-Fold / CPCV / Walk-Forward
│  └─ stats.py            PSR / DSR / PBO / Reality Check / Bootstrap
├─ scripts/               00_update / 01..09 编号流水线 + check_db / repair
├─ data/                  quant.db、factors/*.parquet、ic_series.parquet
├─ reports/               评价表、诊断 JSON、图表、拟合精度报告 PDF
└─ lectures/              讲义源码与 PDF
```

## 六、这不是什么

不提供投资建议，不承诺任何策略能赚钱。
它提供的是一套判断"某个策略结论是否可信"的方法与工具。
