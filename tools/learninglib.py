#!/usr/bin/env python3
"""learning/ 数据层共享工具（validate_attempts 与 derive_state 共用）。

约定：内容稳定（知识卡/题目），事件追加（attempts.jsonl），状态可重建（learner-state.json 是派生视图）。
"""
from __future__ import annotations

import json
import re
from pathlib import Path


def parse_frontmatter(text: str) -> dict[str, str]:
    """Safe YAML frontmatter, returning normalized strings for existing consumers."""
    match = re.match(r"^---\r?\n(.*?)\r?\n---(?:\r?\n|$)", text, re.S)
    if not match:
        return {}
    values = parse_yaml(match.group(1))
    def stringify(value):
        if value is None:
            return 'null'
        if isinstance(value, (bool, list, dict)):
            return json.dumps(value, ensure_ascii=False)
        return str(value)
    return {str(key): stringify(value) for key, value in values.items()}


def parse_list(value: str | None) -> list[str]:
    if not value:
        return []
    parsed = parse_yaml('items: '+value).get('items')
    if parsed is None:
        return []
    if not isinstance(parsed, list) or not all(isinstance(item, str) for item in parsed):
        raise ValueError('Expected a list of string IDs')
    return parsed


def parse_scalar(text: str):
    t = text.strip()
    if t.lower() == "null":
        return None
    if len(t) >= 2 and t[0] in {"'", '"'} and t[-1] == t[0]:
        return t[1:-1]
    if t.startswith("[") and t.endswith("]"):
        body = t[1:-1].strip()
        if not body:
            return []
        return [parse_scalar(item) for item in body.split(",") if item.strip()]
    if t.lower() == "true":
        return True
    if t.lower() == "false":
        return False
    try:
        return int(t)
    except ValueError:
        try:
            return float(t)
        except ValueError:
            return t


def parse_yaml(text: str) -> dict:
    """Standard safe YAML; preserve dates as strings and reject duplicate keys."""
    import copy
    try:
        import yaml
    except ImportError as exc:
        raise RuntimeError('PyYAML is required; install requirements.txt') from exc

    class Loader(yaml.SafeLoader):
        pass

    Loader.yaml_implicit_resolvers = copy.deepcopy(yaml.SafeLoader.yaml_implicit_resolvers)
    for key, entries in Loader.yaml_implicit_resolvers.items():
        Loader.yaml_implicit_resolvers[key] = [(tag, rx) for tag, rx in entries
                                               if tag != 'tag:yaml.org,2002:timestamp']

    def mapping(loader, node, deep=False):
        result = {}
        for key_node, value_node in node.value:
            key = loader.construct_object(key_node, deep=deep)
            if key in result:
                raise ValueError(f'Duplicate YAML key: {key}')
            result[key] = loader.construct_object(value_node, deep=deep)
        return result

    Loader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, mapping)
    try:
        value = yaml.load(text, Loader=Loader)
    except yaml.YAMLError as exc:
        raise ValueError(f'Invalid YAML: {exc}') from exc
    if value is None:
        return {}
    if not isinstance(value, dict):
        raise ValueError('YAML document must be a mapping')
    return value


def current_task_metadata(root: Path, path: Path) -> dict:
    fm = parse_frontmatter(path.read_text(encoding='utf-8'))
    windows = root/'learning/task-windows.json'
    if windows.exists():
        import hashlib
        data = json.loads(windows.read_text(encoding='utf-8'))
        if data.get('schema_version') != 1:
            raise ValueError('Unsupported task window schema')
        row = data.get('tasks',{}).get(fm.get('id'))
        if row:
            if hashlib.sha256(path.read_bytes()).hexdigest() != row.get('task_sha256') or not row.get('evidence_ref'):
                raise ValueError('Task window evidence is stale: '+str(fm.get('id')))
            for field in ('due','not_before'):
                if row.get(field):fm[field]=row[field]
    return fm


def load_tasks(root: Path) -> dict[str, dict]:
    """扫描 learning/tasks/*.md（下划线开头视为模板，跳过）。"""
    tasks: dict[str, dict] = {}
    base = root / "learning" / "tasks"
    if not base.is_dir():
        return tasks
    for path in sorted(base.glob("*.md")):
        if path.name.startswith("_"):
            continue
        fm = current_task_metadata(root,path)
        task_id = fm.get("id")
        if not task_id:
            continue
        tasks[task_id] = {
            "id": task_id,
            "subject": fm.get("subject", "（未标课程）"),
            "target_ids": parse_list(fm.get("target_ids")),
            "version": fm.get("version", "1"),
            "kind": fm.get("kind", "practice"),
            "status": fm.get("status", "open"),
            "device": fm.get("device", "any"),
            "est_minutes": fm.get("est_minutes", "30"),
            "due": fm.get("due", ""),
            # 2026-09-30 加：**最早开始日期**（窗口/门槛还没到就不能做）。
            # 例：`xz-2026f-course-selection` 的选课窗口 10-08 12:30 才开，
            # 只有 `due`（10-10）会被当成"今天就能做"，与事实不符。
            "not_before": fm.get("not_before", ""),
            "path": str(path.relative_to(root)),
        }
    return tasks


def load_attempts(root: Path) -> list[dict]:
    """读取 learning/attempts.jsonl；坏行标记 error，由校验器报告而不是崩溃。"""
    path = root / "learning" / "attempts.jsonl"
    if not path.is_file():
        return []
    rows = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            rows.append({"line": line_no, "data": json.loads(line)})
        except json.JSONDecodeError as exc:
            rows.append({"line": line_no, "data": None, "error": f"invalid json ({exc})"})
    return rows


def load_task_history(root: Path) -> dict[tuple[str, str], dict]:
    """读取 learning/tasks/history/*.md：题目历史版本的元数据（升版前保存的旧 frontmatter）。

    约定：升级题目版本时，把旧 frontmatter 存入
    learning/tasks/history/<task_id>.v<旧版本>.md（含 id/version/target_ids/kind）。
    """
    registry: dict[tuple[str, str], dict] = {}
    base = root / "learning" / "tasks" / "history"
    if not base.is_dir():
        return registry
    for path in sorted(base.glob("*.md")):
        if path.name.startswith("_"):
            continue
        fm = parse_frontmatter(path.read_text(encoding="utf-8"))
        task_id = fm.get("id")
        version = fm.get("version")
        if not task_id or not version:
            continue
        registry[(task_id, version)] = {
            "id": task_id,
            "version": version,
            "target_ids": parse_list(fm.get("target_ids")),
            "kind": fm.get("kind", "practice"),
            "path": str(path.relative_to(root)),
        }
    return registry


def resolve_task_meta(tasks: dict, history: dict, task_id: str, version: str | None) -> dict | None:
    """按 (task_id, version) 解析题目元数据：当前版本→tasks；历史版本→history；找不到→None。

    None 表示该版本元数据缺失：事件保留但不用于升级/目标校验（保守处理）。
    """
    if not version:
        return None
    current = tasks.get(task_id)
    if current is not None and current.get("version") == version:
        return current
    return history.get((task_id, version))


# ---------------------------------------------------------------------------
# 共享判定逻辑（validate_attempts / derive_state / plan-week 共用，避免规则漂移）
# 2026-09-27 加入：把"独立通过""答案曝光""提示是否已知""计时来源"集中到一处。
# ---------------------------------------------------------------------------

SOLUTION_EXPOSURE = ("none", "partial", "full")
# during_attempt（2026-09-28 加）：帮助发生在**作答进行中**（如学习者留空、导师代算）。
# 旧枚举只有 before/after，遇到"做到一半被代算"只能二选一，怎么写都与事实矛盾。
EXPOSURE_TIMING = ("before_attempt", "during_attempt", "after_attempt", "unknown")
TIME_SOURCES = ("actual", "self_reported", "estimated", "unknown")


def hint_value_known(hint) -> bool:
    """提示级别**值**是否已知：只有 0–4 的整数才算已知；null = 未知（不是无提示）。"""
    return isinstance(hint, int) and not isinstance(hint, bool) and 0 <= hint <= 4


def hint_level_known(attempt: dict) -> bool:
    """事件级提示级别是否已知（保留旧接口）。"""
    return hint_value_known(attempt.get("max_hint_level"))


def solution_exposure(attempt: dict) -> str:
    """答案曝光程度：显式 solution_exposure 优先；缺省回退旧字段 solution_seen（true→full，false→none）。"""
    exp = attempt.get("solution_exposure")
    if exp in SOLUTION_EXPOSURE:
        return exp
    return "full" if attempt.get("solution_seen") is True else "none"


# ---------------------------------------------------------------------------
# 逐目标判定（2026-09-28 加入）
#
# 背景：`target_results` 让"同一次作答里各目标表现不同"成为常态，而整条事件的
# 总评（final_result / max_hint_level / solution_exposure）是**汇总值**。
# 拿总评去逐目标升级，会同时造成两个方向的错判：
#   - 高估：总评 correct + H0，会把同事件中 `needs_verify` 的目标一起升级
#           （例：attempt-5 的判据二仍待核验；attempt-8 的 Q3(b) 相位待确认）；
#   - 低估：总评 partial + H3，会把同事件中已独立答对的目标一起压掉
#           （例：attempt-3 的 E 表达式与直接计算本为 H0 独立完成）。
# `plan-week.py` 早已按 (题目, 目标) 逐目标闭环；本组函数把同一口径补到
# derive_state，避免"同一规则两处实现"的漂移。
# ---------------------------------------------------------------------------

PER_TARGET_KEYS = (
    "initial", "hint_level", "final", "needs_verify", "note",
    "exposure", "exposure_timing",
)


def target_result(attempt: dict, tid: str | None) -> dict | None:
    """取某目标的分别记录 `target_results[tid]`；没有则 None（调用方回退事件级字段）。"""
    if not tid:
        return None
    tr = attempt.get("target_results")
    if isinstance(tr, dict):
        val = tr.get(tid)
        if isinstance(val, dict):
            return val
    return None


def _pick(tr: dict | None, key: str, attempt: dict, fallback: str):
    """目标级字段优先（显式给了就用），缺失回退事件级字段。"""
    if tr is not None and key in tr:
        return tr.get(key)
    return attempt.get(fallback)


def hint_level_of(attempt: dict, tid: str | None = None):
    """某目标的提示级别：`target_results[tid].hint_level` 优先，缺失回退事件级。"""
    return _pick(target_result(attempt, tid), "hint_level", attempt, "max_hint_level")


def independence_blockers(
    attempt: dict, tid: str | None = None, require_closed_book: bool = True
) -> list[str]:
    """逐目标判定"为什么不算独立通过"；返回空列表 = 本次对该目标构成独立通过。

    判定项（必须全部满足）：
      1. 非示例学习；按要求闭卷；
      2. 结果正确（目标级 `final` 优先）；
      3. 提示级别**明确为 0**（目标级 `hint_level` 优先；null=未知，不等于无提示）；
      4. `needs_verify` 不为真 —— **待核验的目标不得升级**，不只是统计；
      5. 答案未曝光：目标级 `exposure` 优先，回退事件级；
         `exposure_timing=after_attempt` 的曝光**不阻断**——反馈发生在作答之后，
         该目标此前是否独立，由它自己的提示级别与 needs_verify 反映
         （见 learning/README.md「反馈后的曝光不污染此前那次独立表现」）；
         `before_attempt` 与 `during_attempt`（做到一半被代算）**都阻断**。
    """
    blockers: list[str] = []
    tr = target_result(attempt, tid)

    if attempt.get("mode") == "worked-example":
        blockers.append("示例学习")
    if require_closed_book and attempt.get("closed_book") is not True:
        blockers.append("非闭卷")

    final = _pick(tr, "final", attempt, "final_result")
    if final != "correct":
        blockers.append(f"结果={final}")

    hint = _pick(tr, "hint_level", attempt, "max_hint_level")
    if not hint_value_known(hint):
        blockers.append("提示级别未知")
    elif hint != 0:
        blockers.append(f"提示H{hint}")

    if tr is not None and tr.get("needs_verify") is True:
        blockers.append("待核验")

    exposure = _pick(tr, "exposure", attempt, "solution_exposure")
    if exposure not in SOLUTION_EXPOSURE:
        if tr is not None and 'exposure' in tr:
            blockers.append('曝光程度未知')
            exposure = 'unknown'
        else:
            exposure = solution_exposure(attempt)
    timing = _pick(tr, "exposure_timing", attempt, "exposure_timing")
    # 2026-09-30（ISSUES B1，fail-closed）：曝光非 none 时，**时机缺失或 unknown 一律阻断**，
    # 不再"只看 after_attempt"——旧写法把独立性全押在一个可人手写错的字段上。
    if exposure != "none":
        if timing == "after_attempt":
            pass  # 反馈发生在作答之后：不污染此前那次独立表现（learning/README.md）
        elif timing in EXPOSURE_TIMING:
            blockers.append(f"曝光={exposure}@{timing}")
        else:
            blockers.append(f"曝光={exposure}@未知时机（默认阻断：未知不取最有利值）")

    # 2026-09-30（本次维护新增，fail-closed 交叉校验）：**声称的独立性必须留下可追溯依据**。
    # `independence_blockers` 只看手写字段；一条事件若声称"提示级别 0 + 无曝光 + 结果正确"
    # 却没有任何**逐目标的判定说明**，那么它无法被复查——而本次实测的误判（attempt-28）
    # 正是"测验中已针对第 4 题给过方法提示，却记成 H0 + 无曝光"。
    # 程序无法自动知道"当时到底提示没提示"，因此要求升级必须留下文字依据：
    # `target_results[tid].note`（写清判据）或 `artifact_ref`（作答照片/过程档）。
    if not blockers:
        tr_now = target_result(attempt, tid)
        note = (tr_now or {}).get("note")
        has_note = isinstance(note, str) and note.strip()
        if not has_note and not attempt.get("artifact_ref"):
            blockers.append("升级缺少可追溯依据（无 target_results[tid].note、无 artifact_ref）")

    return blockers


def is_independent_pass_for(
    attempt: dict, tid: str | None = None, require_closed_book: bool = True
) -> bool:
    """**逐目标**独立通过（推荐入口）；tid=None 时等价于事件级判定。"""
    return not independence_blockers(attempt, tid, require_closed_book)


def is_open_book_pass_for(attempt: dict, tid: str | None = None) -> bool:
    """逐目标开卷通过：闭卷标记不为 true，其余条件与独立通过相同（单独统计，不计等级）。"""
    if attempt.get("closed_book") is True:
        return False
    return not independence_blockers(attempt, tid, require_closed_book=False)


def is_independent_pass(attempt: dict, require_closed_book: bool = True) -> bool:
    """事件级独立通过（保留旧接口；逐目标场景请用 is_independent_pass_for）。

    与旧实现的区别：`max_hint_level=null`（未知）**不再**算作无提示，不用于升级。
    """
    return not independence_blockers(attempt, None, require_closed_book)


def is_open_book_pass(attempt: dict) -> bool:
    """事件级开卷通过（保留旧接口；逐目标场景请用 is_open_book_pass_for）。"""
    return is_open_book_pass_for(attempt, None)


# ---------------------------------------------------------------------------
# 帮助史一致性（2026-09-30 加）
#
# 为什么需要：`target_results[tid]` 是**判定值**（`independence_blockers` 目标级优先），
# 而事件级 `max_hint_level` / `solution_exposure` 是**汇总展示值**。两者一旦不一致，
# 记录看起来就像「无提示独立完成」，而判定其实按带提示处理——正是本次订正前
# `attempt-28` 的状态（事件级改成 H2 后，目标级还写着 H0，看表的窗口会被误导）。
#
# 只报**危险方向**：事件级声称零帮助，目标级却记着帮助。
# 反过来（事件级写得更保守）不报——那是保守，不是误导。
# ---------------------------------------------------------------------------
def help_record_inconsistencies(attempt: dict) -> list[str]:
    problems: list[str] = []
    event_claims_none = (attempt.get("max_hint_level") == 0) and (
        attempt.get("solution_exposure") in (None, "none")
    )
    if not event_claims_none:
        return problems
    for tid in attempt.get("target_ids") or []:
        tr = target_result(attempt, tid)
        if tr is None:
            continue
        tr_hint = tr.get("hint_level")
        tr_exp = tr.get("exposure")
        tr_has_help = (
            isinstance(tr_hint, int) and not isinstance(tr_hint, bool) and tr_hint > 0
        ) or (isinstance(tr_exp, str) and tr_exp not in ("none", ""))
        if tr_has_help:
            problems.append(
                f"目标 {tid}：事件级字段声称「H0 + 无曝光」，但目标级记录为 "
                f"hint_level={tr_hint!r} / exposure={tr_exp!r} → **展示与判定不一致**。"
                f"判定按目标级走，因此看起来无提示的记录实际按带提示算；"
                f"请用 tools/record_correction.py 把**目标级**字段一并订正。"
            )
    return problems


# ---------------------------------------------------------------------------
# 结构化订正（learning/corrections.jsonl，2026-09-28 加入）
#
# 为什么需要：工作区约定"原始事件不改不删，订正写 corrections.md"。这条约定没错，
# 但 corrections.md 是给人读的自由文本，`validate_attempts` / `derive_state` /
# `plan-week` **都读不到它**——订正对能力判定实际上是零影响，同一件事在两个文件里
# 留下两种状态，而程序只认其中一种。
#
# 现在：`corrections.jsonl` 是**订正的唯一事实源**；三个消费者统一"先应用订正，
# 再在应用订正后的记录上判定"。`attempts.jsonl` 仍然只增不改。
# `corrections.md` 由 tools/render_corrections.py 生成，不再人工维护结论。
# ---------------------------------------------------------------------------

CORRECTION_SCOPES = ("event", "target")
CORRECTION_SOURCES = ("learner_statement", "photo_reread", "tutor_review", "record_audit")
ALLOWED_EVENT_FIELDS = (
    "initial_result", "final_result", "max_hint_level", "solution_exposure",
    "exposure_timing", "error_hypothesis", "diagnosis_status", "solution_seen",
    # 2026-09-30 新增（ISSUES B7 + 本次维护）：
    # - closed_book：由**学习者本人确认**（"我从来都是闭卷/那次是开卷"），性质与 solution_seen 同类；
    #   此前不可订正 → 记错就只能永远停在错值上，与"订正是订正的唯一事实源"矛盾。
    # - mode：**帮助强度的载体**。实测案例 attempt-28：记录为 quiz（测验）却被记成 H0，
    #   而事实上作答前导师已就该题给出方法提示。若只把 max_hint_level 改成 2，
    #   会立刻违反"quiz 模式只允许 H0"的校验——正确做法是把 mode 订正为 practice（有引导的练习），
    #   让"这次其实是带提示的练习，不是测验"这一事实**显式留在记录里**，而不是绕过校验。
    "closed_book", "mode",
)
# 订正后必须仍然成立的不变量（防止"为了让检查通过"而订正）：
# ① quiz 模式必须 H0（测验不得有提示，有提示就不是测验 → 应改 mode，不是把 hint 写回 0）
CORRECTION_INVARIANTS = (
    "quiz 模式的 max_hint_level 必须为 0（有提示的作答不是测验：请订正 mode 而不是把 hint 改回 0）",
)


def load_corrections(root: Path) -> list[dict]:
    """读取 learning/corrections.jsonl（追加式）。坏行带 error 返回，由校验器报告。"""
    path = root / "learning" / "corrections.jsonl"
    rows: list[dict] = []
    if not path.is_file():
        return rows
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            rows.append({"line": line_no, "data": json.loads(line), "error": None})
        except json.JSONDecodeError as exc:
            rows.append({"line": line_no, "data": None, "error": f"invalid json ({exc})"})
    return rows


def check_corrections(rows: list[dict], attempts: list[dict]) -> list[str]:
    """校验订正本身：字段合法、事件与目标存在、`from` 与当前值一致（防悄悄漂移）。

    **顺序折叠**：校验在一个影子副本上逐条生效，每条都对照"此前订正后的值"。
    否则同一字段上的两条订正会互相掩盖——第二条 `from` 明明对不上，
    却因为拿原始值对照而通过校验，最后在 `apply_corrections` 里被静默跳过。
    """
    import copy as _copy

    errors: list[str] = []
    shadow = _copy.deepcopy(attempts)
    by_id = {a.get("event_id"): a for a in shadow}
    seen: set[str] = set()

    for row in rows:
        label = f"corrections line {row['line']}"
        data = row.get("data")
        if data is None:
            errors.append(f"{label}: {row.get('error')}")
            continue

        cid = data.get("correction_id")
        if not isinstance(cid, str) or not cid:
            errors.append(f"{label}: missing correction_id")
        elif cid in seen:
            errors.append(f"{label}: duplicate correction_id {cid!r}")
        else:
            seen.add(cid)

        # 叙述型条目：只带一段人读说明，不做字段修改（历史叙述的归档位）；
        # 不需要 event_id，也不参与 apply_corrections。
        if data.get("kind") == "narrative":
            if not data.get("text"):
                errors.append(f"{label}: narrative 条目必须带 text")
            continue

        event = by_id.get(data.get("event_id"))
        if event is None:
            errors.append(f"{label}: event_id {data.get('event_id')!r} 不在 attempts.jsonl 中")
            continue
        if data.get("source") not in CORRECTION_SOURCES:
            errors.append(f"{label}: bad source {data.get('source')!r}（应为 {CORRECTION_SOURCES}）")

        scope = data.get("scope")
        if scope not in CORRECTION_SCOPES:
            errors.append(f"{label}: bad scope {scope!r}（应为 {CORRECTION_SCOPES}）")
            continue
        field = data.get("field")
        if not isinstance(field, str) or not field:
            errors.append(f"{label}: missing field")
            continue
        if "from" not in data or "to" not in data:
            errors.append(f"{label}: 必须记录 from 与 to")
            continue
        if not data.get("reason"):
            errors.append(f"{label}: 必须写 reason")
        if not data.get("evidence_ref"):
            errors.append(f"{label}: 必须写 evidence_ref")

        if scope == "target":
            tid = data.get("target_id")
            tr = (event.get("target_results") or {}).get(tid) if isinstance(tid, str) else None
            if not isinstance(tr, dict):
                errors.append(f"{label}: target_results[{tid!r}] 不存在")
                continue
            if field not in PER_TARGET_KEYS:
                errors.append(f"{label}: 目标级字段 {field!r} 不在 {PER_TARGET_KEYS}")
                continue
            current = tr.get(field)
        else:
            if data.get("target_id"):
                errors.append(f"{label}: scope=event 不应带 target_id")
            if field not in ALLOWED_EVENT_FIELDS:
                errors.append(f"{label}: 事件级字段 {field!r} 不允许订正（仅 {ALLOWED_EVENT_FIELDS}）")
                continue
            tr = None
            current = event.get(field)

        if current == data["to"] and data["from"] == data["to"]:
            continue  # 合法的空操作（from==to）：幂等，不报错
        if current != data["from"]:
            # 2026-09-30 修（ISSUES B2）：旧写法在 `current == to` 时**无条件**短路，
            # 而本函数总是拿**原始记录**对照，"已应用"根本不可能出现 →
            # `from` 写错的订正会被静默接受（既不报错也不生效）。
            # 现在只有 from==to 才算合法空操作，其余一律按 from 不一致报错。
            errors.append(
                f"{label}: from 与当前值不一致（记录 {data['from']!r}，实际 {current!r}）——该条不会生效"
            )
            continue
        # 对照通过 → 在影子副本上生效，供后续条目对照
        if isinstance(tr, dict):
            tr[field] = data["to"]
        else:
            event[field] = data["to"]
        # 订正后不变量（防止"为了让检查通过"而订正）
        if event.get("mode") == "quiz" and event.get("max_hint_level") != 0:
            errors.append(
                f"{label}: 订正后违反不变量——quiz 模式的 max_hint_level={event.get('max_hint_level')!r}；"
                f"{CORRECTION_INVARIANTS[0]}"
            )
    return errors


def apply_corrections(attempts: list[dict], rows: list[dict]) -> list[dict]:
    """在**深拷贝**上应用订正，返回"应用订正后的记录"。

    - 不修改传入的 attempts（原始事件保持只增不改）；
    - `from` 不匹配则跳过该条（不硬改），由 `check_corrections` 报错；
    - **幂等**：重复运行结果一致（已应用过的条目因 `from` 不再匹配而跳过）。
    """
    import copy as _copy

    effective = _copy.deepcopy(attempts)
    by_id = {a.get("event_id"): a for a in effective}
    for row in rows:
        data = row.get("data")
        if not data or data.get("kind") == "narrative":
            continue
        event = by_id.get(data.get("event_id"))
        if event is None:
            continue
        if data.get("scope") == "target":
            tr = (event.get("target_results") or {}).get(data.get("target_id"))
            if isinstance(tr, dict) and data.get("field") in PER_TARGET_KEYS:
                if tr.get(data["field"]) == data.get("from"):
                    tr[data["field"]] = data.get("to")
        elif data.get("field") in ALLOWED_EVENT_FIELDS:
            if event.get(data["field"]) == data.get("from"):
                event[data["field"]] = data.get("to")
    return effective


def effective_time_source(attempt: dict) -> str:
    """计时来源：actual（实际计时）/ self_reported（自述）/ estimated（估计）/ unknown（未知）。"""
    src = attempt.get("time_source")
    return src if src in TIME_SOURCES else "unknown"


def measured_minutes(attempt: dict) -> float:
    """**实测**时长：只有 actual / self_reported 计入；估计与未知返回 0（另计，不混入实测）。"""
    if effective_time_source(attempt) not in ("actual", "self_reported"):
        return 0.0
    try:
        return float(attempt.get("active_minutes", 0) or 0)
    except (TypeError, ValueError):
        return 0.0


def estimated_minutes(attempt: dict) -> float:
    """**估计**时长：time_source=estimated 时计入估计桶。"""
    if effective_time_source(attempt) != "estimated":
        return 0.0
    try:
        return float(attempt.get("active_minutes", 0) or 0)
    except (TypeError, ValueError):
        return 0.0


def load_hurdles(root: Path) -> list[dict]:
    """读取 learning/hurdles.jsonl（"明确表示不会/不理解"等观察，不是作答事件）。

    与 attempts 的区别：hurdles 记录**没有作答**的困难观察，带来源与状态，
    不伪装成一道做错的题，也不产生分数。
    """
    path = root / "learning" / "hurdles.jsonl"
    if not path.is_file():
        return []
    rows = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            data = json.loads(line)
        except json.JSONDecodeError as exc:
            rows.append({"line": line_no, "data": None, "error": f"invalid json ({exc})"})
            continue
        rows.append({"line": line_no, "data": data})
    return rows


def effective_attempts(root: Path) -> list[dict]:
    rows=load_attempts(root)
    if any(not isinstance(r.get('data'),dict) for r in rows):
        raise ValueError('Invalid original attempt log')
    raw=[r['data'] for r in rows]
    corrections=load_corrections(root)
    errors=check_corrections(corrections,raw)
    if errors:
        raise ValueError('Invalid correction log: '+'; '.join(errors))
    return apply_corrections(raw,corrections)


def completed_task_ids(root: Path) -> set[str]:
    """Partial/abandoned answers are not completion; corrections and versions matter."""
    tasks=load_tasks(root)
    latest={}
    for event in effective_attempts(root):
        task=tasks.get(event.get('task_id'))
        if task and str(event.get('task_version')) == task['version']:
            latest[event['task_id']]=event
    completed={tid for tid,t in tasks.items() if t.get('status') == 'done'}
    for tid,event in latest.items():
        if event.get('task_completed') is True:
            completed.add(tid)
        elif event.get('task_completed') is False or event.get('mode') == 'worked-example':
            continue
        elif set(tasks[tid]['target_ids']) <= set(event.get('target_ids') or []) and all(
            _pick(target_result(event,t),'final',event,'final_result') in ('correct','incorrect')
            for t in tasks[tid]['target_ids']):
            completed.add(tid)
    return completed


def resumable_attempts(root: Path) -> list[dict]:
    latest={e['task_id']:e for e in effective_attempts(root)}
    completed=completed_task_ids(root)
    return [e for tid,e in latest.items() if tid not in completed and e.get('final_result') in ('partial','abandoned')]
