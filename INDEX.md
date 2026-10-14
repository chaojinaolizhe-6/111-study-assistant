# 学习空间（根地图）

Status: 学习中；0 个概念待间隔复习。

## 目录

- 使用说明（先读）：[README-使用说明.md](README-使用说明.md)
- **学习法·重要原分析（2026-10-14 学习者提供）**：[学习法-细节失误的认知神经科学原理-20261014.pdf](学习法-细节失误的认知神经科学原理-20261014.pdf)（源 `.html` 同目录；内容＝EVC 控制期望价值 / ATS 图式捕获 / 前瞻记忆与 PCE / 自由能预测编码 四模型 + 物理破局策略对照表。**用途**：解释"简单细节反复出错、自查三遍看不出"，并指导防错动作——正交校验、外部 Checklist、串行解耦、抬升感知复杂度）
- 项目审查报告：[AUDIT-审查报告.md](AUDIT-审查报告.md)
- 课程：[subjects/INDEX.md](subjects/INDEX.md)
- 周计划输入：[plan/inputs.yml](plan/inputs.yml)；生成计划：`python -B tools/plan-week.py`
- 导师方法：[.tutor/core/protocol.md](.tutor/core/protocol.md)
- 学习者画像：[.tutor/config/learner-profile.md](.tutor/config/learner-profile.md)
- 掌握状态：`state/mastery.json` · 到期复习：`state/due.md` · 弱项：`state/mistakes.md`
- 刷新状态：`python -B .tutor/core/scripts/refresh-status.py --today <YYYY-MM-DD>`
- 校验：`python -B .tutor/core/scripts/validate-study.py --today <YYYY-MM-DD>`
- 复习顺序与题卡：`python -B .tutor/core/scripts/plan-review.py --today <YYYY-MM-DD> --cards`
- 会话收尾清单：[.tutor/docs/session-close-checklist.md](.tutor/docs/session-close-checklist.md)
- 上游项目（保留原样）：`upstream/tutor/`（来源与版本见 `upstream/PROVENANCE.md`）
- 模拟验证实例（全部为模拟数据）：`mock/`（说明见 `mock/README-模拟说明.md`）

## 续学

1. 读 `state/due.md` 与 `AGENTS.md` 的 STATUS 块，知道上次学到哪、今天复习什么。
2. 放新资料：对应课程的 `课件/` 或 `作业/` 文件夹。
3. `/plan <课程>` 建立路径；`/learn` 开始会话；`/review` 只复习。

For generated refresh compatibility: 先做 0 项到期复习.
