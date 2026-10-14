#!/usr/bin/env python3
"""跨进程写入保护（workspace lock + 原子替换 + 读-改-写 CAS 重试）。

**为什么需要**（ISSUES D4 / B8，2026-09-30 实测）：两条学习会话线同时写同一套文件
（`learning/attempts.jsonl`、`learning/learner-state.json`、`AGENTS.md`、`plan/*`）。
原实现是"读全文件 → 改 → 重写全文件"，没有任何互斥：
  - 两个写者都读到同一份旧内容 → 后写者覆盖先写者的新增行（记录静默丢失）；
  - `learner-state.json` 可能被"较旧的一次派生结果"覆盖（等级与独立通过日期看起来倒退）；
  - 叙述行 STATUS 被并发编辑回退过一次。
"写入前再查一次"不够——两次查询之间仍有窗口。这里提供三件事：

1. `WorkspaceLock`：基于 `O_CREAT|O_EXCL` 的**原子**锁文件（跨进程，Windows/POSIX 通用）。
   - 带 owner 信息与超时（默认 60s）；进程崩溃留下的**过期锁**可被安全回收；
   - 锁内再校验"拿到锁时文件没被别人改过"（`expected_mtime`/`expected_size`）。
2. `atomic_write_text()`：写临时文件 → `os.replace` 原子替换，**永不出现半写文件**。
3. `locked_modify()`：锁 + 读 + 期望值校验 + 写 + 复核的**事务**；期望值不匹配 →
   释放锁、重读、重试（默认 5 次）。这解决"较旧快照覆盖较新状态"。

设计取舍：
- 锁只覆盖**本地工作区**（单机、多进程）；不假装能跨机器。
- 锁失败**不静默**：抛 `LockTimeout`，调用方必须显式报告，不能"只更新计数就说同步好了"。
- 所有写入都走 `atomic_write_text`，测试里可以注入"写到一半失败"来验证回滚。

用法:
  from workspace_lock import WorkspaceLock, locked_modify, atomic_write_text
  with WorkspaceLock(root / "learning", label="append_attempt") as lock:
      ...
"""
from __future__ import annotations

import errno
import json
import os
import socket
import time
import uuid
from contextlib import contextmanager
from pathlib import Path
from typing import Callable, Iterator

DEFAULT_TIMEOUT = 30.0
DEFAULT_STALE = 300.0
LOCK_NAME = ".write.lock"


class LockTimeout(RuntimeError):
    """在超时内没能拿到锁。调用方必须把失败报告出去，不得当作成功。"""


class ConcurrentModification(RuntimeError):
    """拿锁后发现目标文件已被别人修改（期望的快照过期）。"""


def _owner() -> dict:
    return {
        "pid": os.getpid(),
        "host": socket.gethostname(),
        "at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "monotonic": time.monotonic(),
    }


def _owner_alive(owner: dict) -> bool:
    """Unknown ownership is treated as live; never terminate a Windows process."""
    if owner.get('host') != socket.gethostname() or type(owner.get('pid')) is not int or owner['pid'] <= 0:
        return True
    pid=owner['pid']
    if os.name == 'nt':
        import ctypes
        from ctypes import wintypes
        kernel=ctypes.WinDLL('kernel32',use_last_error=True)
        kernel.OpenProcess.argtypes=[wintypes.DWORD,wintypes.BOOL,wintypes.DWORD]
        kernel.OpenProcess.restype=wintypes.HANDLE
        kernel.GetExitCodeProcess.argtypes=[wintypes.HANDLE,ctypes.POINTER(wintypes.DWORD)]
        kernel.GetExitCodeProcess.restype=wintypes.BOOL
        kernel.CloseHandle.argtypes=[wintypes.HANDLE]
        handle=kernel.OpenProcess(0x1000,False,pid)  # query-only access
        if not handle:
            return ctypes.get_last_error() != 87  # invalid process ID means gone
        try:
            code=wintypes.DWORD()
            return not kernel.GetExitCodeProcess(handle,ctypes.byref(code)) or code.value == 259
        finally:
            kernel.CloseHandle(handle)
    try:
        os.kill(pid,0)  # POSIX existence check only
        return True
    except ProcessLookupError:
        return False
    except PermissionError:
        return True


class WorkspaceLock:
    """基于原子创建的互斥锁（同一目录内一个锁文件）。

    - `lock_dir` 必须存在（不存在则创建）；
    - 锁文件内容记录 owner，便于人读与排障；
    - `stale_after` 秒后视为残留锁（持锁进程已崩溃），可被回收；回收会打印告警。
    """

    def __init__(
        self,
        lock_dir: Path,
        label: str = "workspace",
        timeout: float = DEFAULT_TIMEOUT,
        stale_after: float = DEFAULT_STALE,
        verbose: bool = True,
    ) -> None:
        self.path = Path(lock_dir) / LOCK_NAME
        self.label = label
        self.timeout = timeout
        self.stale_after = stale_after
        self.verbose = verbose
        self._fd: int | None = None
        self._token = uuid.uuid4().hex

    # -- 内部 ---------------------------------------------------------------
    def _try_acquire(self) -> bool:
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            self._fd = os.open(self.path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        except FileExistsError:
            return False
        except OSError as exc:  # 目录不可写等
            raise LockTimeout(f"无法创建锁文件 {self.path}：{exc}") from exc
        payload = _owner() | {"label": self.label,"token":self._token}
        os.write(self._fd, json.dumps(payload, ensure_ascii=False).encode("utf-8"))
        os.close(self._fd)
        self._fd = None
        return True

    def _break_if_stale(self) -> bool:
        """残留锁回收：只有在锁文件**既未被更新、又超过 stale_after** 时才回收。"""
        try:
            age = time.time() - self.path.stat().st_mtime
        except FileNotFoundError:
            return True
        if age <= self.stale_after:
            return False
        try:
            owner=json.loads(self.path.read_text(encoding='utf-8'))
        except (ValueError,OSError):
            return False
        if not isinstance(owner,dict) or _owner_alive(owner):
            return False
        reclaim=self.path.with_name(self.path.name+'.reclaim')
        try:
            fd=os.open(reclaim,os.O_CREAT|os.O_EXCL|os.O_WRONLY)
        except FileExistsError:
            return False
        try:
            os.close(fd)
            if not self.path.exists():
                return True
            if json.loads(self.path.read_text(encoding='utf-8')) != owner:
                return False
            self.path.unlink()
            if self.verbose:
                print(f"WARN 已确认本机持锁进程退出，回收 {age:.0f}s 的残留锁 {self.path}")
        finally:
            reclaim.unlink(missing_ok=True)
        return True

    # -- 上下文管理 ---------------------------------------------------------
    def acquire(self) -> "WorkspaceLock":
        deadline = time.monotonic() + self.timeout
        while True:
            if self._try_acquire():
                return self
            if self._break_if_stale():
                continue
            if time.monotonic() >= deadline:
                holder = "?"
                try:
                    holder = self.path.read_text(encoding="utf-8")
                except OSError:
                    pass
                raise LockTimeout(
                    f"等锁超时（{self.timeout:.0f}s）：{self.path} 被占用，持锁者信息={holder}。"
                    "另一条会话线可能正在写入——**本次写入未执行**，请稍后重试，不要绕过锁直接改文件。"
                )
            time.sleep(0.05)

    def release(self) -> None:
        if self._fd is not None:
            try:
                os.close(self._fd)
            finally:
                self._fd = None
        try:
            owner=json.loads(self.path.read_text(encoding='utf-8'))
            if owner.get('token') == self._token:
                self.path.unlink()
        except FileNotFoundError:
            pass

    def __enter__(self) -> "WorkspaceLock":
        return self.acquire()

    def __exit__(self, *_exc) -> None:
        self.release()


@contextmanager
def atomic_write_text(path: Path, text: str, encoding: str = "utf-8") -> Iterator[None]:
    """原子替换写：先写同目录临时文件，再 `os.replace`（同分区上原子）。

    好处：读者永远看不到半写文件；写入过程崩溃 → 旧文件完好（天然回滚）。
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f".{path.name}.tmp{os.getpid()}")
    try:
        with open(tmp, "w", encoding=encoding, newline="\n") as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp, path)
    finally:
        if tmp.exists():
            try:
                tmp.unlink()
            except OSError:
                pass


def snapshot(path: Path) -> tuple[float, int] | None:
    """文件当前快照 (mtime_ns, size)；不存在返回 None。用于 CAS 期望值。"""
    try:
        st = Path(path).stat()
    except FileNotFoundError:
        return None
    return (st.st_mtime_ns, st.st_size)


def locked_modify(
    target: Path,
    mutate: Callable[[str], str | None],
    lock_dir: Path | None = None,
    label: str = "locked_modify",
    timeout: float = DEFAULT_TIMEOUT,
    retries: int = 5,
    verbose: bool = True,
) -> str:
    """事务化读-改-写：锁住 → 读 → 校验快照 → `mutate(旧内容)` → 原子写 → 复核。

    - `mutate` 返回 `None` 表示"无需修改"（不写文件）；
    - 拿锁后如果文件已与进入时不同（说明在等锁期间被别人改过）→ 重读重试，
      **而不是拿旧快照去覆盖**（这正是 D4 里"较旧快照覆盖较新派生状态"的修法）；
    - 重试耗尽 → 抛 `ConcurrentModification`，调用方必须显式报错。
    """
    target = Path(target)
    lock_dir = Path(lock_dir) if lock_dir else target.parent
    last: Exception | None = None

    for attempt in range(1, retries + 1):
        before = snapshot(target)
        try:
            with WorkspaceLock(lock_dir, label=label, timeout=timeout, verbose=verbose):
                after = snapshot(target)
                if before != after:
                    raise ConcurrentModification(
                        f"{target.name} 在等锁期间被其他会话修改（{before} → {after}）"
                    )
                old = target.read_text(encoding="utf-8") if target.is_file() else ""
                new = mutate(old)
                if new is None or new == old:
                    return old
                atomic_write_text(target, new)
                if verbose:
                    print(f"step 已原子写入 {target}（第 {attempt} 次尝试）")
                return new
        except ConcurrentModification as exc:
            last = exc
            if verbose:
                print(f"WARN {exc} → 重读重试（{attempt}/{retries}）")
            time.sleep(0.05 * attempt)
    raise ConcurrentModification(f"{target} 连续 {retries} 次被并发修改，本次未写入：{last}")


def next_counter(path: Path, prefix: str, minimum: int = 1) -> int:
    """机器可读的取号计数器（`learning/attempts/_ids.json`）。

    取号不再靠人读文本预留（ISSUES B8）——计数器与 attempts.jsonl 的实际最大号**同时**参与，
    取两者较大值 +1，因此即使计数器文件被人删掉也不会撞号。
    """
    data: dict = {}
    if path.is_file():
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            data = {}
    used = data.get(prefix)
    used = used if isinstance(used, int) and not isinstance(used, bool) else 0
    return max(used, minimum - 1) + 1


def bump_counter(path: Path, prefix: str, value: int) -> None:
    data: dict = {}
    if path.is_file():
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            data = {}
    previous = data.get(prefix)
    if isinstance(previous, int) and previous >= value:
        return
    data[prefix] = value
    data["_note"] = "机器可读取号计数器：append_attempt.py 在锁内预留并递增，勿手工编辑"
    atomic_write_text(path, json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def max_suffix_event_id(text: str, prefix: str = "attempt-") -> int:
    """扫描 jsonl 文本，取 `prefix<N>` 的最大 N（防"计数器丢了就撞号"）。"""
    best = 0
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            eid = json.loads(line).get("event_id", "")
        except json.JSONDecodeError:
            continue
        if isinstance(eid, str) and eid.startswith(prefix) and eid[len(prefix):].isdigit():
            best = max(best, int(eid[len(prefix):]))
    return best


__all__ = [
    "ConcurrentModification",
    "LockTimeout",
    "WorkspaceLock",
    "atomic_write_text",
    "bump_counter",
    "locked_modify",
    "max_suffix_event_id",
    "next_counter",
    "snapshot",
]
