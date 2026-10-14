#!/usr/bin/env python3
"""git-sync.py — 把本工作区同步到 GitHub（**独立脚本**，不接入 session-close.py）。

设计原则
--------
1. **只做同步，不碰学习数据**：本脚本不写任何 `learning/` `state/` `plan/` 文件，
   也不参与 `session-close.py` 的 10 步流水线。收尾仍以 session-close.py 为唯一入口。
2. **绝不自动解决冲突**。检测到 rebase 冲突立即中止并打印处置指引。
   原因：`state/current.md`、`AGENTS.md`/`CLAUDE.md` 的 STATUS 块、
   `learning/learner-state.json` 都是 session-close.py 的**派生产物**，
   手工合并必然产生"计数说一套、事实源说另一套"的静默不一致。
   正确处置是**重新运行 `python -B tools/session-close.py`** 让它整体重算。
3. **幂等**：无变化时不产生空提交。
4. **不伪装成功**：不是 git 仓库 / 没配 remote / 凭据缺失，都显式报出并返回非零，
   绝不打印"已同步"。

用法
----
    python -B tools/git-sync.py --status        # 只看状态，零写操作
    python -B tools/git-sync.py --check         # 汇报将提交什么，不提交
    python -B tools/git-sync.py                 # 拉取 → 提交 → 推送（默认）
    python -B tools/git-sync.py --no-push       # 只本地提交
    python -B tools/git-sync.py --message "..."  # 自定义提交信息
    python -B tools/git-sync.py --init          # 首次初始化仓库（配套 git init）

退出码：0 成功 / 无变化；1 失败；2 冲突需人工处置。
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

sys.path.insert(0, str(Path(__file__).resolve().parent))
from timebase import learning_today  # noqa: E402

LOCK_NAME = "dsh-git-sync.lock"
LOCK_STALE_SECONDS = 600  # 10 分钟：超过则认为上次同步僵死

# 派生文件清单：冲突时禁止手工合并，必须重跑 session-close.py
# ── 冲突分级 ────────────────────────────────────────────────────────────────
# 2026-10-14 依审查意见重做。原实现「一旦冲突就 rebase --abort 并让用户重跑
# session-close.py」是**错的**：rebase --abort 会退回拉取前状态，远端的提交
# 根本没进来，此时在本地重跑多少次 session-close.py 都无法把远端数据合进来
# ——跨设备真冲突下会彻底卡死。正确做法见 heal_conflicts()。

# 纯生成物：内容完全由 session-close.py 从事实源推出。
# 冲突时取任一侧都行——随后重跑 session-close.py 会整体重算，结果由事实源决定。
GENERATED = (
    "state/current.md",
    "learning/learner-state.json",
    "learning/coverage.md",
    "learning/curriculum-coverage.md",
    "learning/curriculum-coverage.json",
    "plan/handoff-CURRENT.md",
    "plan/schedule.md",
)

# 半生成物：既有手写正文，又有 session-close.py 生成的 TUTOR-STATUS 块。
# 冲突时保留**本地**一侧（护住手写正文），STATUS 块随后由 session-close.py 重算覆盖。
SEMI_GENERATED = ("AGENTS.md", "CLAUDE.md")

# 追加型事实源：由 .gitattributes 的 merge=union 自动拼接，正常不会冲突。
# 若仍冲突，说明出现了非追加式改写 → **必须人工介入**，绝不自动取舍。
FACT_SOURCES = (
    "learning/attempts.jsonl",
    "learning/corrections.jsonl",
    "learning/hurdles.jsonl",
    "learning/observations.jsonl",
)

# 大文件守卫：非 LFS 文件超过此阈值时拒绝提交。
# 对应审查意见对 upload/ 的担忧——但**不采用「忽略整个目录」**，
# 因为实测 upload/ 里有 17 个文件是孤本（subjects/ 下无副本），忽略会直接丢数据。
LARGE_FILE_MB = 50

# 供提示信息使用的合并清单
DERIVED = GENERATED + SEMI_GENERATED


class GitError(RuntimeError):
    pass


def run_git(args: list[str], root: Path, check: bool = True, timeout: int = 600,
            raw: bool = False) -> tuple[int, str, str]:
    """调用 git。GIT_TERMINAL_PROMPT=0 保证凭据缺失时**快速失败而非挂起**。

    raw=True：**不裁剪输出**。`git status --porcelain` 的状态码首位可能就是空格
    （` M` = 已修改未暂存）——对整个输出 strip 会吃掉它，导致解析出的路径
    被截掉第一个字符（实测：`AUDIT-…md` 被解析成 `UDIT-…md`）。
    """
    env = dict(os.environ)
    env["GIT_TERMINAL_PROMPT"] = "0"       # 禁止交互式要密码/令牌
    env["GCM_INTERACTIVE"] = "never"       # 禁止 Git Credential Manager 弹窗
    env["GIT_EDITOR"] = ":"                # 自动化场景绝不打开编辑器（rebase --continue 用）
    env["GIT_SEQUENCE_EDITOR"] = ":"
    env["LC_ALL"] = "C.UTF-8"
    proc = subprocess.run(
        ["git", *args],
        cwd=str(root),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=env,
        timeout=timeout,
    )
    out, err = proc.stdout or "", proc.stderr or ""
    if not raw:
        out, err = out.strip(), err.strip()
    if check and proc.returncode != 0:
        raise GitError(f"git {' '.join(args)} 失败（rc={proc.returncode}）：{err.strip() or out.strip()}")
    return proc.returncode, out, err


def list_changes(root: Path) -> list[tuple[str, str]]:
    """返回 [(两位状态码, 路径)]。

    用 `-z` 分隔而非换行：① 路径不做引号与八进制转义，中文路径原样返回；
    ② 首行的前导空格不会被破坏（这正是 strip 版实现出过的 bug）。
    """
    rc, out, _ = run_git(["status", "--porcelain", "-z"], root, check=False, raw=True)
    if rc != 0:
        return []
    fields = [f for f in out.split("\0") if f]
    entries: list[tuple[str, str]] = []
    i = 0
    while i < len(fields):
        entry = fields[i]
        if len(entry) < 4:
            i += 1
            continue
        code, path = entry[:2], entry[3:]
        # 重命名/复制：-z 格式下原路径是紧随其后的一个独立字段
        if "R" in code or "C" in code:
            i += 1
        entries.append((code, path))
        i += 1
    return entries


def is_repo(root: Path) -> bool:
    rc, out, _ = run_git(["rev-parse", "--is-inside-work-tree"], root, check=False)
    return rc == 0 and out.strip() == "true"


def current_branch(root: Path) -> str:
    rc, out, _ = run_git(["branch", "--show-current"], root, check=False)
    return out.strip() if rc == 0 and out.strip() else "main"


def remote_url(root: Path) -> str | None:
    rc, out, _ = run_git(["remote", "get-url", "origin"], root, check=False)
    return out.strip() if rc == 0 and out.strip() else None


def has_remote_branch(root: Path, branch: str) -> bool:
    rc, out, _ = run_git(["ls-remote", "--heads", "origin", branch], root, check=False, timeout=120)
    return rc == 0 and bool(out.strip())


def rebase_in_progress(root: Path) -> bool:
    git_dir = root / ".git"
    return (git_dir / "rebase-merge").exists() or (git_dir / "rebase-apply").exists()


def conflicted_files(root: Path) -> list[str]:
    """当前处于未合并（冲突）状态的路径。"""
    rc, out, _ = run_git(["diff", "--name-only", "--diff-filter=U"], root, check=False)
    return [l.strip() for l in out.splitlines() if l.strip()] if rc == 0 else []


def large_non_lfs_files(root: Path) -> list[tuple[str, float]]:
    """即将提交、未走 LFS、且超过阈值的文件。

    对应审查意见对 upload/ 的担忧：临时目录可能被塞入未匹配 LFS 规则的大二进制。
    与其一刀切忽略目录（实测会丢 17 个孤本文件），不如在提交前拦住并给出指引。
    """
    hits: list[tuple[str, float]] = []
    for _code, rel in list_changes(root):
        f = root / rel
        if not f.is_file():
            continue
        size_mb = f.stat().st_size / (1024 * 1024)
        if size_mb < LARGE_FILE_MB:
            continue
        rc, out, _ = run_git(["check-attr", "filter", "--", rel], root, check=False)
        if rc == 0 and "filter: lfs" in out:
            continue
        hits.append((rel, size_mb))
    return hits


def heal_conflicts(root: Path, max_rounds: int = 12) -> tuple[bool, str]:
    """尝试自动化解 rebase 冲突。返回 (是否化解, 说明)。

    分级策略（rebase 语义下 `--ours` = 远端基底，`--theirs` = 被重放的本地提交）：

      · 纯生成物 GENERATED      → 取本地一侧；随后 session-close.py 会整体重算，
                                  取哪一侧都不影响最终结果（结果由事实源决定）。
      · 半生成物 SEMI_GENERATED → 同样取本地一侧，以保住手写正文；
                                  TUTOR-STATUS 块会被重算覆盖。
      · 追加型事实源 FACT_SOURCES → 正常由 merge=union 自动合并，不会走到这里；
                                  若出现，说明是非追加式改写，**拒绝自动处理**。
      · 其它任何文件            → **拒绝自动处理**，交人工判断。

    这一点是审查意见里最关键的一条：原设计与它相反，会导致跨设备冲突死锁。
    """
    for _round in range(max_rounds):
        files = conflicted_files(root)
        if files:
            auto = [p for p in files if p in GENERATED or p in SEMI_GENERATED]
            manual = [p for p in files if p not in auto]
            if manual:
                kind = "追加型事实源（疑似被非追加式改写）" if any(
                    p in FACT_SOURCES for p in manual
                ) else "非派生文件"
                return False, f"{kind}冲突，需人工判断：" + "、".join(manual)

            for p in auto:
                run_git(["checkout", "--theirs", "--", p], root, check=False)
                run_git(["add", "--", p], root, check=False)
            print(f"      自动化解派生文件冲突 {len(auto)} 个：{'、'.join(auto)}")

        rc, out, err = run_git(["rebase", "--continue"], root, check=False)
        if not rebase_in_progress(root):
            return True, "rebase 已完成"
        if rc != 0 and not conflicted_files(root):
            return False, f"rebase --continue 失败：{err or out}"

    return False, f"冲突化解超过 {max_rounds} 轮仍未收敛"


def changed_between(root: Path, old: str, new: str, prefix: str) -> list[str]:
    """两个提交之间，路径以 prefix 开头的变更文件。"""
    rc, out, _ = run_git(["diff", "--name-only", old, new], root, check=False)
    return [l.strip() for l in out.splitlines() if l.strip().startswith(prefix)] if rc == 0 else []


def run_session_close(root: Path) -> tuple[bool, str]:
    """调用收尾唯一入口重算派生状态。返回 (是否全部通过, 摘要)。"""
    script = root / "tools" / "session-close.py"
    if not script.is_file():
        return False, "tools/session-close.py 不存在"
    proc = subprocess.run(
        [sys.executable, "-B", str(script), "--root", str(root)],
        cwd=str(root),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=900,
    )
    tail = [l for l in (proc.stdout or "").splitlines() if l.strip()][-1:] or [""]
    return proc.returncode == 0, tail[0]


# ---------------------------------------------------------------- 并发锁
class SyncLock:
    """跨客户端互斥。两个 AI 同时 push 会互相踩，这里用 .git 下的独占文件挡住。

    僵死锁（>10 分钟）自动接管，避免崩溃后永久卡住。
    """

    def __init__(self, root: Path) -> None:
        self.path = root / ".git" / LOCK_NAME
        self.acquired = False

    def __enter__(self) -> "SyncLock":
        import time

        if self.path.exists():
            age = time.time() - self.path.stat().st_mtime
            if age < LOCK_STALE_SECONDS:
                owner = self.path.read_text(encoding="utf-8", errors="replace").strip()
                raise GitError(
                    f"另一个同步正在进行中（{int(age)} 秒前由 PID {owner or '?'} 启动）。\n"
                    f"  若确认它已崩溃，删除 {self.path} 后重试。"
                )
            print(f"[WARN] 接管僵死锁（已存在 {int(age)} 秒）")
        try:
            fd = os.open(self.path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        except FileExistsError as exc:
            raise GitError(f"无法获取同步锁：{self.path}（可能是竞态，稍后重试）") from exc
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(str(os.getpid()))
        self.acquired = True
        return self

    def __exit__(self, *exc: object) -> None:
        if self.acquired:
            try:
                self.path.unlink()
            except OSError:
                pass


# ---------------------------------------------------------------- 报告
def summarize_changes(entries: list[tuple[str, str]]) -> str:
    """按顶层目录统计变更，生成人类可读的提交摘要。"""
    buckets: dict[str, int] = {}
    for _code, path in entries:
        top = path.split("/", 1)[0] if "/" in path else path
        buckets[top] = buckets.get(top, 0) + 1
    parts = [f"{k}×{v}" for k, v in sorted(buckets.items(), key=lambda kv: -kv[1])]
    return "、".join(parts[:8]) + ("…" if len(parts) > 8 else "")


def report_status(root: Path) -> int:
    branch = current_branch(root)
    url = remote_url(root)
    changes = list_changes(root)

    rc_lfs, lfs_out, _ = run_git(["lfs", "ls-files"], root, check=False)
    lfs_count = len(lfs_out.splitlines()) if rc_lfs == 0 and lfs_out else 0

    print("== 仓库状态 ==")
    print(f"  分支      : {branch}")
    print(f"  远端      : {url or '（未配置）'}")
    print(f"  未提交    : {len(changes)} 个文件")
    if changes:
        print(f"  分布      : {summarize_changes(changes)}")
    print(f"  LFS 跟踪  : {lfs_count} 个文件" + ("（LFS 可能未生效！）" if lfs_count == 0 else ""))

    rc_ahead, ahead, _ = run_git(["rev-list", "--count", f"origin/{branch}..HEAD"], root, check=False)
    if rc_ahead == 0 and ahead.isdigit():
        print(f"  领先远端  : {ahead} 个提交")
    return 0


# ---------------------------------------------------------------- 主流程
def do_sync(root: Path, message: str | None, push: bool, check_only: bool) -> int:
    if not is_repo(root):
        print("[FAIL] 当前目录不是 git 仓库。先运行：python -B tools/git-sync.py --init")
        return 1

    url = remote_url(root)
    if push and not url:
        print("[FAIL] 未配置远端 origin，无法推送。配置示例：")
        print("         git remote add origin https://github.com/<你的用户名>/111学习助手.git")
        return 1

    with SyncLock(root):
        branch = current_branch(root)

        # 1) 暂存
        run_git(["add", "-A"], root)
        staged = list_changes(root)

        if not staged:
            print("[OK  ] 无变化，无需提交。")
        else:
            print(f"== 待提交：{len(staged)} 个文件 ==")
            print(f"  分布：{summarize_changes(staged)}")
            if check_only:
                for code, path in staged[:40]:
                    print(f"    {code} {path}")
                if len(staged) > 40:
                    print(f"    …另有 {len(staged) - 40} 个")
                print("\n[CHECK] 未提交（--check 模式）。")
                return 0

            # 2a) 大文件守卫
            #     审查意见担心 upload/ 这类临时目录被塞入未匹配 LFS 规则的大二进制。
            #     解法不是忽略目录（实测会丢 17 个孤本），而是在提交前拦住。
            big = large_non_lfs_files(root)
            if big:
                print(f"[FAIL] 以下 {len(big)} 个文件超过 {LARGE_FILE_MB} MB 且未走 Git LFS，拒绝提交：")
                for rel, mb in sorted(big, key=lambda x: -x[1])[:10]:
                    print(f"         {mb:8.1f} MB  {rel}")
                print("       处置：把该扩展名加入 .gitattributes 的 LFS 规则，例如")
                print('         git lfs track "*.mp4"')
                print("       或确认无用后删除/加入 .gitignore。")
                return 1

            # 2b) 提交
            today = learning_today()
            dist = summarize_changes(staged)
            msg = message or f"{today} 学习会话同步（{len(staged)} 文件：{dist}）"
            name = run_git(["config", "user.name"], root, check=False)[1]
            email = run_git(["config", "user.email"], root, check=False)[1]
            if not name or not email:
                print("[FAIL] 未配置提交身份。请先执行：")
                print('         git config --local user.name  "你的名字"')
                print('         git config --local user.email "你的邮箱"')
                return 1
            run_git(["commit", "-m", msg], root)
            print(f"[OK  ] 已提交：{msg}")

        if not push:
            print("[OK  ] 本地提交完成（--no-push）。")
            return 0

        # 3) 拉取（rebase，保持线性历史）
        if has_remote_branch(root, branch):
            head_before = run_git(["rev-parse", "HEAD"], root, check=False)[1]
            rc, out, err = run_git(["pull", "--rebase", "--autostash", "origin", branch], root, check=False)
            healed = False

            if rc != 0:
                if not rebase_in_progress(root):
                    print(f"[FAIL] 拉取失败：{err or out}")
                    return 1
                print("[冲突] 拉取时发生冲突，尝试自动化解…")
                ok, why = heal_conflicts(root)
                if not ok:
                    run_git(["rebase", "--abort"], root, check=False)
                    print(f"[冲突] 无法自动化解：{why}")
                    print("       已中止 rebase（你的本地提交完好，未丢失）。")
                    print_derived_guidance(root)
                    return 2
                healed = True
                print(f"[OK  ] {why}；派生文件按本地侧保留，稍后重算")

            head_after = run_git(["rev-parse", "HEAD"], root, check=False)[1]
            print("[OK  ] 已拉取远端更新（rebase）")

            # 3b) 重算触发条件。两条都必须覆盖：
            #   ① 冲突被自动化解 —— 派生文件是按「本地侧」粗暴保留的，内容可能自相矛盾；
            #   ② 远端改动了 learning/ —— 本地派生状态是在**没有**这些新事件的情况下
            #      算出来的，直接推送会得到「计数与实际不符」的状态（正是 session-close
            #      第 10 步专门防的那种静默不一致）。
            learning_touched = bool(changed_between(root, head_before, head_after, "learning/"))
            if head_before != head_after and (healed or learning_touched):
                reason = "冲突化解后" if healed else "远端改动了 learning/"
                print(f"[INFO] {reason} → 重算派生状态…")
                ok, summary = run_session_close(root)
                print(f"[{'OK  ' if ok else 'FAIL'}] 重算：{summary}")
                if not ok:
                    print("[FAIL] 派生状态重算未全部通过 → **不推送**，避免上传不一致状态。")
                    print("       本地提交完好；请手工运行 python -B tools/session-close.py 排查。")
                    return 1
                run_git(["add", "-A"], root)
                rc_c, _, _ = run_git(
                    ["commit", "-m", f"{learning_today()} {reason}重算派生状态"], root, check=False
                )
                print("[OK  ] 已提交重算结果" if rc_c == 0 else "[INFO] 重算结果无变化")

        # 4) 推送
        rc, out, err = run_git(["push", "-u", "origin", branch], root, check=False, timeout=1800)
        if rc != 0:
            lowered = (err or out).lower()
            if "conflict" in lowered or "rejected" in lowered or "non-fast-forward" in lowered:
                print("[冲突] 推送被拒绝：远端有你的本地没有的提交。")
                print("       请重新运行本脚本（会先 rebase 再推），或手工 git pull --rebase。")
                return 2
            if "authentication" in lowered or "could not read username" in lowered or "403" in lowered:
                print("[FAIL] 认证失败。请配置 Personal Access Token：")
                print("         https://github.com/settings/personal-access-tokens/new")
                print("       权限：仅 Contents = Read and write；然后：")
                print("         git config --local credential.helper manager")
                print(f"       原始错误：{err or out}")
                return 1
            print(f"[FAIL] 推送失败：{err or out}")
            return 1
        print("[OK  ] 已推送到 GitHub")

        rc, lfs_out, _ = run_git(["lfs", "ls-files"], root, check=False)
        if rc == 0 and lfs_out:
            print(f"[INFO] LFS 跟踪 {len(lfs_out.splitlines())} 个文件；"
                  f"完整克隆约消耗 1.28 GB 月流量（免费额度 10 GB）")
        return 0


def print_derived_guidance(root: Path) -> None:
    print()
    print("       自动化解只覆盖**派生文件**（内容可由 session-close.py 重算）：")
    for p in GENERATED:
        print(f"           · {p}")
    for p in SEMI_GENERATED:
        print(f"           · {p}（仅 STATUS 块）")
    print("       人工冲突的处置顺序：")
    print("         1. 合并冲突文件本身。事实源 learning/*.jsonl 是追加型，")
    print("            保留**双方新增行**即可（.gitattributes 已配 merge=union，正常不会冲突）。")
    print("         2. 运行 python -B tools/session-close.py 重算派生状态。")
    print("         3. 重新运行本脚本完成推送。")
    print("       ⚠ 不要手工编辑派生文件：计数、镜像、指纹三者必须同源。")


def check_credentials(root: Path) -> bool:
    """检查 GitHub 凭据是否**已持久化**（非交互即可取到）。

    2026-10-14 加。原 --init 不检查凭据，是用户「一直被要求登录」的根源之一：
    Git 只在操作**成功之后**才调用 `credential approve` 存储凭据；
    若随后任何一步失败（例如远端仓库名写错导致 404），刚拿到的令牌会被
    **静默丢弃**，下次操作又要重新走一遍浏览器授权。
    这里用「禁止一切交互能否取到凭据」来判定是否真的落盘。
    """
    try:
        proc = subprocess.run(
            ["git", "credential", "fill"],
            cwd=str(root),
            input="protocol=https\nhost=github.com\n\n",
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            env={**os.environ, "GIT_TERMINAL_PROMPT": "0", "GCM_INTERACTIVE": "never"},
            timeout=60,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        print(f"[WARN] 凭据检查未能完成：{exc}")
        return False

    if "password=" in (proc.stdout or ""):
        print("[OK  ] GitHub 凭据已持久化（禁交互仍可取得，不会反复要求登录）")
        return True

    print("[WARN] GitHub 凭据**尚未持久化** —— 首次推送会要求授权一次。")
    print("       若授权后仍反复被要求登录，说明凭据被丢弃，用下面这条显式存储：")
    print("         python -B tools/git-sync.py --login")
    return False


def store_credential(root: Path, username: str, token: str) -> bool:
    """把已取得的凭据显式写入凭据管理器。

    绕开「git 只在操作成功后才 approve」这一行为，避免失败操作连带丢弃认证状态。
    """
    payload = (
        f"protocol=https\nhost=github.com\nusername={username}\npassword={token}\n\n"
    )
    proc = subprocess.run(
        ["git", "credential", "approve"],
        cwd=str(root),
        input=payload,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=60,
    )
    return proc.returncode == 0


def do_login(root: Path) -> int:
    """交互完成一次 GitHub 授权，并**显式持久化**凭据。

    存在理由（2026-10-14 实测）：git 只在操作**成功**后才调用 credential approve。
    本工作区曾因远端仓库名错误导致每次推送 404，于是每次辛苦取得的令牌都被
    静默丢弃，用户被迫反复在浏览器登录。把「授权」与「业务操作成败」解耦，
    是这件事的正解。
    """
    print("即将启动 GitHub 授权（会打开浏览器窗口，请完成登录并授权）…")
    env = {k: v for k, v in os.environ.items() if k not in ("GIT_TERMINAL_PROMPT", "GCM_INTERACTIVE")}
    try:
        proc = subprocess.run(
            ["git", "credential", "fill"],
            cwd=str(root),
            input="protocol=https\nhost=github.com\n\n",
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            env=env,
            timeout=900,
        )
    except subprocess.TimeoutExpired:
        print("[FAIL] 授权超时（900 秒）。请重试。")
        return 1

    out = proc.stdout or ""
    user = next((l.split("=", 1)[1] for l in out.splitlines() if l.startswith("username=")), "")
    token = next((l.split("=", 1)[1] for l in out.splitlines() if l.startswith("password=")), "")
    if not token:
        print("[FAIL] 未取得凭据，授权可能未完成或被取消。")
        print(f"       {(proc.stderr or '').strip()[:300]}")
        return 1

    print(f"[OK  ] 已取得凭据：用户={user}  令牌长度={len(token)}（内容不显示）")
    ok = store_credential(root, user, token)
    token = ""  # 尽早丢弃，避免残留在内存里
    print("[OK  ] 已显式写入凭据管理器" if ok else "[FAIL] 写入凭据管理器失败")
    if not ok:
        return 1
    print()
    return 0 if check_credentials(root) else 1


def do_init(root: Path) -> int:
    """首次初始化：git init + LFS + 身份检查，**不做提交**。"""
    if is_repo(root):
        print("[INFO] 已经是 git 仓库，跳过 init。")
    else:
        run_git(["init", "-b", "main"], root)
        print("[OK  ] 已初始化仓库（分支 main）")

    # LFS 必须显式安装钩子，否则大文件会被当成普通对象塞进仓库
    rc, out, err = run_git(["lfs", "install", "--local"], root, check=False)
    print(f"[{'OK  ' if rc == 0 else 'FAIL'}] git lfs install --local" + ("" if rc == 0 else f"：{err or out}"))

    # 防御性设置：即使 .gitattributes 丢失也不做行尾转换（保护 sha256 指纹）
    run_git(["config", "--local", "core.autocrlf", "false"], root, check=False)
    run_git(["config", "--local", "core.safecrlf", "false"], root, check=False)
    print("[OK  ] 已设置 core.autocrlf=false（保护事实源指纹）")

    # 忽略未来的 .git 内部变动对 diff 的干扰
    run_git(["config", "--local", "lfs.locksverify", "false"], root, check=False)

    name = run_git(["config", "user.name"], root, check=False)[1]
    email = run_git(["config", "user.email"], root, check=False)[1]
    if not name or not email:
        print("[WARN] 尚未配置提交身份，提交前必须执行：")
        print('         git config --local user.name  "你的名字"')
        print('         git config --local user.email "你的邮箱"')
    else:
        print(f"[OK  ] 提交身份：{name} <{email}>")

    print()
    check_credentials(root)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="同步工作区到 GitHub（独立脚本，不接入 session-close.py）")
    parser.add_argument("--root", default=".", help="工作区根目录，默认当前目录")
    parser.add_argument("--init", action="store_true", help="首次初始化（git init + LFS + 身份与凭据检查）")
    parser.add_argument("--login", action="store_true", help="交互完成 GitHub 授权并显式持久化凭据")
    parser.add_argument("--status", action="store_true", help="只报告状态，零写操作")
    parser.add_argument("--check", action="store_true", help="汇报将提交什么，不提交")
    parser.add_argument("--no-push", action="store_true", help="只本地提交，不推送")
    parser.add_argument("--message", default=None, help="自定义提交信息")
    args = parser.parse_args()

    root = Path(args.root).resolve()

    try:
        if args.login:
            return do_login(root)
        if args.init:
            return do_init(root)
        if args.status:
            if not is_repo(root):
                print("[FAIL] 不是 git 仓库。先运行 --init。")
                return 1
            return report_status(root)
        return do_sync(root, args.message, push=not args.no_push, check_only=args.check)
    except GitError as exc:
        print(f"[FAIL] {exc}")
        return 1
    except subprocess.TimeoutExpired:
        print("[FAIL] git 命令超时（网络过慢或凭据挂起）。")
        return 1
    except KeyboardInterrupt:
        print("\n[中断] 用户取消。")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
