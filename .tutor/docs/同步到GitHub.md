# 同步到 GitHub

> 建立：2026-10-14。仓库：`https://github.com/chaojinaolizhe-6/111学习助手`（**私有**）。

目标：让本工作区成为**可移植的 AI 工作环境**——任何一台机器、任何一个 AI 客户端
（Claude Code 认 `CLAUDE.md`，Codex / Cursor 等认 `AGENTS.md`）拉下仓库就能按同一套规则干活。

---

## 一、分层：什么进仓库，什么不进

判断标准不是「是不是文本」，而是**「另一个 AI 少了它就干不了活」**。

| 层 | 内容 | 体积 | 归属 |
|---|---|---|---|
| ① 规则层 | `AGENTS.md`、`CLAUDE.md`、`.tutor/core/`、`.tutor/config/`、`.tutor/docs/`、`.dsh/skills/`、`tools/` | ~1 MB | 普通 git |
| ② 事实层 | `learning/`、`state/`、`plan/`、`subjects/**/*.md`、`obsidian/obsidian知识库/`、`.tutor/cache/materials/`、`mock/`、`eval/` | ~26 MB | 普通 git |
| ③ 原始资料 | 教材与课件 PDF、TED 音频、作业照片、教材解构配图 | ~1.28 GB | **Git LFS** |
| ④ 本地专属 | `_scratch/`、`_package-portable/`、`backups/`、`_tmp_pdf/`、`.tutor/cache/_inspect/`、根目录 `_tmp_*` 与 `tmp-*` | ~1 GB | 忽略 |

合计入库：**2 556 个文件**，其中普通对象约 26 MB、LFS 约 1.28 GB。

**关于 ③ 的取舍**：另一个 AI 若与本机同盘运行，其实直接读本地 PDF 即可，LFS 是「换机器/云端也能开工」才需要的保险。
代价是**每次完整克隆消耗约 1.28 GB 流量**，免费额度 10 GB/月 ≈ 每月 7 次完整克隆。多端频繁拉取要留意。

---

## 二、日常用法

```powershell
# 看状态（零写操作，随时可跑）
python -B tools/git-sync.py --status

# 看这次会提交什么，但不提交
python -B tools/git-sync.py --check

# 正式同步：拉取 → 提交 → 推送
python -B tools/git-sync.py

# 只本地提交，不推
python -B tools/git-sync.py --no-push
```

退出码：`0` 成功或无变化 ／ `1` 失败 ／ `2` 冲突需人工处置。

### 多客户端闭环

1. AI 开工 → `--status`（落后则 `git pull --rebase`）
2. AI 干活
3. `python -B tools/session-close.py`（**收尾唯一入口**，十步全过）
4. `python -B tools/git-sync.py` 推送

第 1 步与第 4 步已写入 `AGENTS.md` / `CLAUDE.md`，因此**任何认这两个文件的客户端都会自动照做**，
不需要为每个客户端单独配置。

---

## 三、冲突处置（最重要的一节）

### 禁止手工合并「派生文件」

以下文件是 `session-close.py` 的**生成物**，手工合并必然产生静默不一致
（计数说一套、事实源说另一套，而第 10 步的一致性核对本来是专门防这个的）：

- `state/current.md`
- `learning/learner-state.json`
- `learning/coverage.md`
- `learning/curriculum-coverage.md`
- `plan/handoff-CURRENT.md`
- `plan/schedule.md`
- `AGENTS.md` / `CLAUDE.md` 里的 `TUTOR-STATUS` 块

**正确处置**：解决非派生文件的冲突后，**重新运行 `python -B tools/session-close.py`** 让它整体重算。
`git-sync.py` 检测到 rebase 冲突时会自动中止并打印这份清单，不会自作聪明地合并。

### 并发写入

两个 AI 同时干活会冲突，尤其 `learning/attempts.jsonl`（追加型，但同行区域仍可能冲突）。
`git-sync.py` 用 `.git/dsh-git-sync.lock` 做**跨客户端互斥**，僵死锁（>10 分钟）自动接管。
即便如此，**同一时间只让一个 AI 写工作区**仍是最稳的做法。

---

## 四、技术要点：为什么必须关掉行尾转换

`.gitattributes` 第一行是 `* -text`——**禁止任何 LF↔CRLF 转换**。这不是洁癖，是硬约束：

`tools/session-close.py` 第 10 步会比对 `learning/attempts.jsonl` 的 sha256 指纹。
而实测（2026-10-14）三个事实源的行尾**互不相同**：

| 文件 | CRLF | 纯 LF |
|---|---|---|
| `learning/attempts.jsonl` | 30 | 19 |
| `learning/corrections.jsonl` | 0 | 55 |
| `learning/hurdles.jsonl` | 3 | 0 |

一旦 git 做归一化，三个文件字节同时改变，指纹立刻失配 → **每次收尾都会 FAIL**，
且历史事件无法重算。因此：

- `.gitattributes`：`* -text`（排在最前）
- `.git/config`：`core.autocrlf = false`
- `.git/config`：`core.quotePath = false`（否则中文路径在输出里显示为八进制转义）

**验证方法**：克隆到别处，比对指纹是否与本地一致。

---

## 五、首次配置（换机器时照做）

```powershell
git clone https://github.com/chaojinaolizhe-6/111学习助手.git
cd 111学习助手
python -B tools/git-sync.py --init     # git init（若尚未）+ LFS 钩子 + autocrlf=false + 身份检查
```

凭据：本机使用 **HTTPS + Personal Access Token**。创建地址：

<https://github.com/settings/personal-access-tokens/new>

- Repository access：**Only select repositories** → 只勾 `111学习助手`
- Permissions → Repository permissions → **Contents: Read and write**
- 其余权限一律不勾

令牌由 Windows 凭据管理器保存，**不要写进任何文件**。

---

## 六、成本与额度（2026-10 核实）

GitHub Free 对**私有仓库不限数量、不限协作者**，LFS 含 **10 GB 存储 + 10 GB/月流量**。

本仓库占用约 1.28 GB → **完全在免费额度内，无需付费**。
LFS 的预付费数据包已取消，改为按量计费 + 预算上限；
即使超出，只要把预算设为 $0，就是**停止 LFS 使用**而不是扣费。

参考：[产品额度说明](https://docs.github.com/en/billing/reference/product-usage-included) ·
[LFS 计费](https://docs.github.com/en/billing/concepts/product-billing/git-lfs)

---

## 七、已知风险

1. **版权**：`obsidian/教材库/` 含第三方版权教材（部分标注 Z-Library 来源）。
   私有仓库风险可控；**若改为公开仓库**，请取消 `.gitignore` 末行注释把教材库移出版本控制。
2. **隐私**：`eval/` 与 `learning/` 含完整会话原文、学习者画像、作答与卡点记录。
   仓库必须保持**私有**。提交邮箱为真实 QQ 邮箱，会出现在每条提交元数据里。
3. **上游许可**：`upstream/tutor/` 是 [TonyRainforest 的 tutor](https://github.com/YusenZhang0601/tutor)（MIT）。
   本仓库 `LICENSE` 目前是其原始版权声明。**若公开分享**，须保留原署名并补一行衍生说明。
4. **嵌套仓库已解除**：`upstream/tutor/.git` 原为独立仓库，会阻止其内容入库，
   已于 2026-10-14 移至 `backups/upstream-tutor-dotgit-2026-10-14/`（保留历史，本地专属）。
   `upstream/PROVENANCE.md` 记录的 commit hash 足以随时重新克隆。
