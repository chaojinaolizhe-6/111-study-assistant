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
DERIVED = (
    "state/current.md",
    "learning/learner-state.json",
    "learning/coverage.md",
    "learning/curriculum-coverage.md",
    "plan/handoff-CURRENT.md",
    "plan/schedule.md",
    "AGENTS.md",
    "CLAUDE.md",
)


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

            # 2) 提交
            today = learning_today()
            msg = message or f"{today} 学习会话同步"
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
            rc, out, err = run_git(["pull", "--rebase", "--autostash", "origin", branch], root, check=False)
            if rc != 0:
                if rebase_in_progress(root):
                    run_git(["rebase", "--abort"], root, check=False)
                    print("[冲突] 拉取时发生冲突，已自动中止 rebase（未丢失你的提交）。")
                    print("       冲突文件：")
                    for line in (err or out).splitlines():
                        if "CONFLICT" in line or "both modified" in line:
                            print(f"         {line.strip()}")
                    print_derived_guidance(root)
                    return 2
                print(f"[FAIL] 拉取失败：{err or out}")
                return 1
            print("[OK  ] 已拉取远端更新（rebase）")

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
    present = [p for p in DERIVED if (root / p).exists()]
    print()
    print("       ⚠ 冲突文件若属于**派生产物**，禁止手工合并：")
    for p in present:
        print(f"           · {p}")
    print("         正确处置：解决非派生文件后，重新运行")
    print("           python -B tools/session-close.py")
    print("         让它整体重算（计数、镜像、指纹三者必须同源）。")


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
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="同步工作区到 GitHub（独立脚本，不接入 session-close.py）")
    parser.add_argument("--root", default=".", help="工作区根目录，默认当前目录")
    parser.add_argument("--init", action="store_true", help="首次初始化（git init + LFS + 身份检查）")
    parser.add_argument("--status", action="store_true", help="只报告状态，零写操作")
    parser.add_argument("--check", action="store_true", help="汇报将提交什么，不提交")
    parser.add_argument("--no-push", action="store_true", help="只本地提交，不推送")
    parser.add_argument("--message", default=None, help="自定义提交信息")
    args = parser.parse_args()

    root = Path(args.root).resolve()

    try:
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
