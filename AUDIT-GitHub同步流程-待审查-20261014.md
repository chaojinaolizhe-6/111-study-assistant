# AUDIT — GitHub 同步流程 · 审查交接文档

> 生成：2026-10-14（中国时间 UTC+8）
> 用途：交给**另一个 AI** 独立审查本工作区「构建实时共享 GitHub 仓库」的整个流程
> **本文件自包含**，审查者无需其他上下文。建议先读第 7 节「待审查问题清单」，再回看前文取证。
> ⚠ 撰写者即本次执行者本人。第 7 节刻意列出**自己认为薄弱、未验证、可议之处**；

---

## 0. 审查任务

请核对以下四件事，并明确指出**显著问题**：

1. **方案选择是否正确**——用 GitHub + Git LFS 承载这个工作区，是不是解决用户真实需求的合理手段？
2. **分层边界是否恰当**——哪些文件进了仓库、哪些被排除，有没有放错的位置？
3. **是否存在会破坏现有系统的风险**——本工作区有一套带一致性校验的 tutor 流水线（`session-close.py`，10 步），git 的引入会不会破坏它？
4. **第 7 节列出的问题是否真实**——有没有被低估的、或反过来被夸大的？

---

## 1. 用户的目标（原话与推断）

### 用户原话（关键三句）

- 「我在思考我们现在本地空间的东西能不能上传到 github 上进行实时更新和共享」
- 「我想着是用其它 AI 也能同时用到这个仓库，然后想你一样处理任务，并且实时更新，但我不知道应该上传哪些。但是为了效果最佳，我可以购买会员，你给我相应网址就行」
- 「不能在每一次对话之后同步吗」

### 推断出的真实需求

不是「备份」，而是：**把工作区做成可移植的 AI 工作环境**——任何一台机器、任何一个 AI 客户端
（Claude Code 读 `CLAUDE.md`，Codex / Cursor 读 `AGENTS.md`）拉下仓库就能按同一套规则继续干活，
且在每次对话结束后把状态同步回去。**「共享」的对象是 AI 客户端，不是人。**

> 审查点：这个推断是否成立？如果用户其实只想备份，第 2 节的分层是否过度设计？

---

## 2. 环境事实（可复核）

| 项目 | 实测值 |
|---|---|
| 工作区根 | `D:\aaa_D_usual\DSH\111学习助手` |
| 原始规模 | 4 770 个文件 / 2 315 MB |
| git | `2.55.0.windows.5`，安装于 `D:\aaa_D_usual\DSH\tools\Git` |
| git-lfs | `3.7.1`（**已预装**，无需另装） |
| `gh` CLI | **不存在** |
| 远端 | `https://github.com/chaojinaolizhe-6/111学习助手.git` |
| 仓库可见性 | 私有 |
| 提交身份 | `chaojinaolizhe-6 <chaojinaolizhe@qq.com>`（用户明确选择真实 QQ 邮箱） |
| 凭据助手 | 系统级 `helper-selector`；**global 为空、`~/.gitconfig` 不存在 → 认证从未完成** |

工作区原有一套 tutor 系统：`AGENTS.md` / `CLAUDE.md`（强制镜像）、`tools/`（32 个 py）、
`learning/`（作答与订正事实源，jsonl）、`state/`、`plan/`、`subjects/`、`.tutor/`、`obsidian/`。

---

## 3. 执行过程（时间线，含确切命令）

1. **勘察**：统计体积、文件类型、最大文件、敏感信息。
   - 结论：PDF 1 222 MB、PNG 497 MB、MP3 261 MB、ZIP 188 MB；纯文本仅约 41 MB。
   - 全盘扫描 `.env` / `credentials.json` / `*.key` / `*.pem` / PAT 特征串 → **零命中**。
   - 发现 `upstream/tutor/.git` 是**嵌套 git 仓库**。
2. **解除嵌套**：`Move-Item upstream\tutor\.git → backups\upstream-tutor-dotgit-2026-10-14\.git`
   （**移动而非删除**，历史保留在已被忽略的目录里；`upstream/PROVENANCE.md` 已记录上游 commit hash）。
3. **写 `.gitignore`**（四层排除）与 **`.gitattributes`**（LFS 规则 + `* -text`）。
4. **写 `tools/git-sync.py`**（独立脚本，接入冲突保护与并发锁）。
5. **初始化**：`python -B tools/git-sync.py --init`
   → `git init -b main`、`git lfs install --local`、`core.autocrlf=false`、`core.quotePath=false`。
6. **改规则**：向 `AGENTS.md` 与 `CLAUDE.md` **写入逐字相同**的「跨设备同步」章节，并验证镜像规则仍成立。
7. **提交**：
   - `6387143` 初始提交，2 556 个文件
   - `a36e922` 同步脚本与规则，3 个文件
8. **验证**：LFS 属性匹配、LFS 指针内容、指纹往返一致、克隆副本比对。
9. **推送**：**未完成**——卡在认证（见第 8 节）。

---

## 4. 关键设计决策与理由

### 决策 1：按「另一个 AI 缺了它能否干活」分四层，而非按「是不是文本」

| 层 | 内容 | 体积 | 归属 |
|---|---|---|---|
| ① 规则层 | `AGENTS.md`、`CLAUDE.md`、`.tutor/core|config|docs`、`.dsh/skills`、`tools/` | ~1 MB | 普通 git |
| ② 事实层 | `learning/`、`state/`、`plan/`、`subjects/**/*.md`、`obsidian/obsidian知识库/`、`.tutor/cache/materials/`、`mock/`、`eval/`、`upload/` | ~26 MB | 普通 git |
| ③ 原始资料 | 教材与课件 PDF、TED 音频、作业照片 | ~1.18 GB | **Git LFS** |
| ④ 本地专属 | `_scratch/`、`_package-portable/`、`backups/`、`_tmp_pdf/`、`.tutor/cache/_inspect/`、根目录 `_tmp_*` 与 `tmp-*` | ~1 GB | 忽略 |

**关键发现**：`obsidian/obsidian知识库/` 已是教材解构成果（1 437 个 `.md`，15.5 MB），
`.tutor/cache/materials/` 已含 35 份课件解构 `extraction.json`（字段 `outline / pages / reading_claim`）。
**因此另一个 AI 读 md 即可，不必读 1.2 GB 扫描 PDF**——这是把 ③ 归为「可选保险」而非「必需」的依据。

> 审查点：既然解构成果够用，③ 是否根本不该上传？（用户明确选了全传。）

### 决策 2：大文件走 LFS（用户选择全传）

免费额度实测为 **10 GB 存储 + 10 GB/月流量**（[产品额度文档](https://docs.github.com/en/billing/reference/product-usage-included)），
LFS 预付费数据包已取消、改为按量计费（[LFS 计费](https://docs.github.com/en/billing/concepts/product-billing/git-lfs)）。
本仓库 LFS 约 1.18 GB → **免费额度内，无需付费**。
代价：每次完整克隆消耗约 1.18 GB 流量 ≈ **每月约 8 次完整克隆**。

### 决策 3（最关键）：`.gitattributes` 首行 `* -text`，禁止任何行尾转换

**这不是洁癖，是硬约束。** `tools/session-close.py` 第 10 步会比对 `learning/attempts.jsonl` 的 sha256 指纹。
而实测三个事实源的行尾**互不相同**：

| 文件 | CRLF | 纯 LF |
|---|---|---|
| `learning/attempts.jsonl` | **30** | **19** |
| `learning/corrections.jsonl` | 0 | 55 |
| `learning/hurdles.jsonl` | 3 | 0 |

一旦 git 做 LF↔CRLF 归一化，三个文件字节同时改变 → 指纹失配 → **每次收尾必然 FAIL**，
且历史事件无法重算。故设置了双重保险：`.gitattributes` 的 `* -text` + `.git/config` 的 `core.autocrlf=false`。

> 审查点：`attempts.jsonl` 为何会有**混合行尾**？这是否暴露了写入路径不统一的数据质量问题？（第 7 节 B2）

### 决策 4：`git-sync.py` **不接入** `session-close.py`（用户选择）

理由：`session-close.py` 是「收尾唯一入口」，有 10 步一致性核对。
新功能以独立脚本 + `AGENTS.md` 规则的形式存在，对既有流水线**零改动**。
校验方式：改动 `AGENTS.md`/`CLAUDE.md` 后验证镜像规则仍成立。

### 决策 5：冲突时**禁止手工合并派生文件**

`state/current.md`、`learning/learner-state.json`、`AGENTS.md` 的 STATUS 块、`plan/handoff-CURRENT.md` 等
都是 `session-close.py` 的**生成物**。手工合并必然产生「计数说一套、事实源说另一套」的静默不一致。
`git-sync.py` 检测到 rebase 冲突时会 `rebase --abort` 并打印清单，指示**重跑 `session-close.py` 整体重算**。

---

## 5. 验证证据（已做的）

| # | 验证项 | 方法 | 结果 |
|---|---|---|---|
| 1 | 无敏感信息 | 全盘扫 `.env`/`credentials`/`*.key`/`*.pem`/PAT 特征串 | **零命中** |
| 2 | LFS 属性生效 | `git check-attr filter -- <pdf>` | `filter=lfs` ✓ |
| 3 | 行尾转换已关闭 | `git check-attr text -- <各文件>` | 全部 `text=unset` ✓ |
| 4 | LFS 实际生效 | `git show HEAD:<jpg>` | 输出标准 LFS 指针（`version`/`oid`/`size`）✓ |
| 5 | 文本未误入 LFS | 比对 `git lfs ls-files` | `learning/attempts.jsonl` 不在其中 ✓ |
| 6 | 排除规则无泄漏 | 检查待跟踪清单 | `_scratch`/`backups`/`*.pyc`/`*.part` 均未出现 ✓ |
| 7 | **指纹未被破坏** | 提交前后比对 `source_fingerprint` | **完全一致** ✓ |
| 8 | **往返一致性** | 克隆到临时目录后比对 | 指纹、事件计数（49/55）、镜像规则**全部一致** ✓ |
| 9 | 镜像规则 | `sync_status.mirrored_except_names()` | 修改 `AGENTS.md`/`CLAUDE.md` 后仍成立 ✓ |

第 7、8 项是最关键的：

```
提交前 / 克隆副本   attempts_sha256 = a588116da077cc60d89332c1f0fb87feb8a4014b3f98125e0c6c6be8d923c085
                    attempts_events = 49, corrections_events = 55
```

**该项目证明「换台机器拉下来就能按同一批事实继续工作」。**

---

## 6. 交付物清单

| 文件 | 作用 |
|---|---|
| `tools/git-sync.py` | 同步脚本（`--init` / `--status` / `--check` / `--no-push` / `--message`） |
| `.gitattributes` | LFS 规则 + `* -text`（保护指纹） |
| `.gitignore` | 四层排除规则 + 版权开关预留 |
| `.tutor/docs/同步到GitHub.md` | 完整使用说明 |
| `AGENTS.md` / `CLAUDE.md` | 新增「跨设备同步」章节（逐字镜像） |

---

## 7. 待审查问题清单 ★

### A. 阻断类 —— 已定位并解除（保留完整记录，因为这是本次最有价值的教训）

**A1 + A2【根因】GitHub 会把仓库名中的非 ASCII 字符替换为连字符。**
用户按约定创建名为 `111学习助手` 的仓库，GitHub 实际生成的是 **`111-`**。
于是本地 `origin` 指向 `https://github.com/chaojinaolizhe-6/111学习助手.git`，
而该 URL **永远不可能存在** → 推送恒报 `Repository not found`。

**这个故障之所以极难定位，是因为三层歧义叠加：**

1. GitHub 对未认证访问私有仓库返回 **404 掩码**（而非 401），
   因此「仓库不存在」与「无权限」报错**完全相同**。
   实测：`111学习助手` 与一个故意瞎编的仓库名 `this-repo-does-not-exist-xyz`，**报错逐字一致**。
2. 认证当时**确实未完成**（`~/.gitconfig` 不存在），所以两个原因同时成立、互相掩盖。
   实测确认：系统级 `credential.helper=helper-selector`，而选择结果写入了**系统级**配置
   （`system : !"...git-credential-manager.exe"`），并非用户级——只查 `~/.gitconfig` 会误判为「未保存」。
3. 中文名被静默转换，**GitHub 创建成功的页面不会提示这一点**。

**解除方式**：先用 `git credential fill` 强制完成 GCM 授权，拿到有效凭据；
再带令牌调 `GET /user/repos?affiliation=owner` 列出**含私有**的全部仓库——
`Repository not found` 从此不再有歧义（凭据有效仍 404 ⇒ 仓库确实不存在）。
结果查到实际名称 `111-`，随后 `git remote set-url` 更正并重新推送。

**审查点（仍然成立）**：
- 「认证」与「仓库存在性」共用一个 404，是本流程最脆弱的一环。**是否有更稳健的设计？**
  例如：初始化时用 API 校验仓库可达性，或在脚本中区分「认证失败」与「404」并给出不同指引。
- `tools/git-sync.py` 目前把 push 失败一律归为「认证失败」或「冲突」，**缺少「仓库不存在」这一分支**。
  这是脚本的真实缺陷，应当补上。

### B. 正确性风险

**B1. `attempts.jsonl` 的混合行尾（30 CRLF + 19 LF）被原样固化进了仓库。**
本次处理只是「防止它被改变」——**没有解决它本身**。同一文件为何有两种行尾？
若写入路径不统一，将来可能影响 sha256 的稳定性。
**审查点：这是否是一个应当独立修复的数据质量问题？**

**B2. `* -text` 的代价被低估。** 它保护了指纹，但让**所有**文本文件放弃 EOL 归一化。
若将来有协作者在 Windows 上编辑 `.py`，或用户用别的工具生成 CRLF 文件，仓库会积累混合行尾。
**审查点：是否应改为更精细的规则（例如只对 `learning/*.jsonl` 关闭转换，其余正常归一化）？**

**B3. `session-close.py` 的完整 10 步在改动 `AGENTS.md`/`CLAUDE.md` 后【未重跑】。**
只单独验证了镜像规则。**这是明确的验证缺口**，应当补跑一次确认一致性核对仍全过。

**B4. 冲突处理代码从未被实际触发。** `git-sync.py` 的 rebase 冲突分支是**未经测试的代码路径**。

**B5. 并发锁只在本机有效。** `.git/dsh-git-sync.lock` 是文件锁，**跨机器完全无效**。
两台机器同时推送仍会冲突。「多 AI 同时使用」场景下这是真实缺陷。

### C. 设计可议

**C1. 「实时」名不副实。** Git 是 commit 粒度，实际得到的是「每次对话后同步一次」。
用户说了两次「实时」，需确认这个粒度是否被真正接受。

**C2. 同步依赖软约束，无强制机制。** 完全靠 AI 遵守 `AGENTS.md`。
**AI 忘了执行就不同步，且不会有任何报错。** 没有计划任务或钩子兜底。

**C3. 收尾失败 → 不推送 → 恰恰在出问题时没有备份。**
`AGENTS.md` 规定「`session-close.py` 全部通过之后」才同步。这与备份目的存在张力。

**C4. `_scratch/` 被排除（582 MB），但用户的实验产物都在那里。**
若在 `_scratch/` 里做了重要工作，**不会被同步，也不会被发现**。

**C5. `upload/` 进了版本控制，但其语义像「临时上传区」**，长期可能无界膨胀。

**C6. `eval/` 含完整会话原文**（含系统提示词与工具 schema），是全仓库隐私敏感度最高、且会持续增长的部分。
**是否应该上传，值得重新审视。**

**C7. 提交信息固定为 `"YYYY-MM-DD 学习会话同步"`**，无法从历史看出某次提交到底改了什么学习内容。

**C8. 版权。** `obsidian/教材库/` 含标注 Z-Library 来源的教材。
私有仓库风险可控；`.gitignore` 末行预留了开关，但**该开关从未被测试**是否有效。

### D. 未验证清单（汇总）

- ❌ 推送至 GitHub（阻断于 A1）
- ❌ **全新克隆时 LFS 大文件能否正确拉取**——往返验证时用了 `GIT_LFS_SKIP_SMUDGE=1` **跳过了 LFS 下载**，
  所以「PDF 能否真正拉下来」**完全没有验证**。这是最实质的验证缺口。
- ❌ `session-close.py` 完整 10 步（B3）
- ❌ 冲突处理路径（B4）
- ❌ 跨机器并发（B5）
- ❌ `.gitignore` 的教材库开关（C8）
- ❌ LFS 对象在 GitHub 侧的完整性

---

## 8. 未完成事项与当前状态

1. **推送未完成**，阻断于 GitHub 认证。已执行 `git config --global credential.helper ""` +
   `--add manager` 清空继承的 `helper-selector`，并启动 `git credential-manager github login`（等待用户授权）。
2. **本地仓库完全就绪**：2 个提交、工作区干净、502 个文件走 LFS、指纹验证通过。
   **即使推送始终失败，本地仓库本身是可用且正确的。**

---

## 9. 给审查者的建议切入点

按优先级：

1. **B3 + D**：先补跑 `python -B tools/session-close.py`，确认十步全过——这是最便宜、最直接的风险排查。
2. **D 的 LFS 克隆**：做一次**真正带 LFS 下载**的克隆（不加 `GIT_LFS_SKIP_SMUDGE`），
   验证 PDF 完整性与耗时。这是验证「可移植」承诺的唯一方法。
3. **B2**：评估 `* -text` 是否过于粗暴，是否应改为按路径精细控制。
4. **B1**：判断混合行尾是历史遗留还是仍在发生的写入缺陷。
5. **C2 + C3**：判断「软约束 + 失败不推」的组合是否可接受，是否需要计划任务兜底。
6. **A1**：评估认证方案（GCM OAuth vs PAT）哪个更适合长期自动化场景。

---

## 附：复核用命令

```powershell
# 仓库状态
python -B tools/git-sync.py --status

# 指纹（应与提交前一致）
python -B -c "import sys; sys.path.insert(0,'tools'); from derive_state import source_fingerprint; from pathlib import Path; print(source_fingerprint(Path('.')))"

# 镜像规则
python -B -c "import sys; sys.path.insert(0,'tools'); import sync_status; from pathlib import Path; print(sync_status.mirrored_except_names(Path('AGENTS.md'), Path('CLAUDE.md')))"

# LFS 与属性
git lfs ls-files | Measure-Object -Line
git check-attr filter text -- learning/attempts.jsonl

# 完整收尾（验证 B3）
python -B tools/session-close.py

# 带 LFS 的真实克隆（验证可移植性）
git clone https://github.com/chaojinaolizhe-6/111学习助手.git <目标目录>
```
