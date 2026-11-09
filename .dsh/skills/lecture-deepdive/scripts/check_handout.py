# -*- coding: utf-8 -*-
r"""讲义静态检查；不证明推导正确，也不代替 PDF 逐页检查。

用法：check_handout.py FILE.tex [--mode theory|appendix|lab] [--log FILE.log]
无文件参数时扫描 subjects/**/*.tex。默认 theory 兼容已有讲义。
appendix 模式区分正文 \practice 与附录 \answerstart/\answercontinue。
退出码：0 静态检查无问题；1 错误；2 仅有待人工复核的线索。
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import NamedTuple

HEAD_RE = re.compile(r"^\s*\\(?:subhdr|hdr)\{(.*)\}\s*$")
FIG_RE = re.compile(r"\\begin\{(?:figure|circuitikz|tikzpicture)\}|\\includegraphics")
DRAW_RE = re.compile(r"画图|作图|画出[^，。；]{0,6}(?:曲线|回线|图)|sketch|\bdraw\b", re.I)
ENG_TITLE_RE = re.compile(r"电路|桥式|整流|滤波|稳压|运放|放大|光路|受力|装置|接线|波形")
ENG_BODY_RE = re.compile(r"导通|截止|开关状态|电流方向|正半周|负半周")
PRACTICE_TITLE_RE = re.compile(r"作业|自测|练习|第\s*\d+\s*题")
QUESTION_RE = re.compile(r"Q\s*\d|第\s*\d+\s*题|例\s*\d+|Exercise|Problem", re.I)
STEM_MARKERS = (r"\qstem{", "题面", "题目", "已知", "求", "题：", "？", "?")
HINT_RE = re.compile(r"关键一步|解题提示|(?:答案|详解|提示)\s*(?:\}|：|:|为|是)")
DERIV_WORD_RE = re.compile(r"\\step\{|推导|证明|所以|代入|展开|合并|相减|两边|推出|因为|从而|可得")
EXAMPLE_WORD_RE = re.compile(r"数字例子|例如|举例|例子|试算|手动验算|取.{0,8}为例")
# theme-violet.tex 中这三项均由 \newcommand 定义，不能按环境调用。
THEME_COMMAND_ONLY = frozenset({"callout", "qstem", "warnbox"})


class Call(NamedTuple):
    name: str
    args: list[str]
    start: int
    end: int


def _blank(text: str) -> str:
    return re.sub(r"[^\n]", " ", text)


def _group(text: str, pos: int, opening: str = "{", closing: str = "}") -> tuple[str, int]:
    while pos < len(text) and text[pos].isspace():
        pos += 1
    if pos >= len(text) or text[pos] != opening:
        raise ValueError(f"缺少 {opening}{closing} 参数")
    start, depth = pos + 1, 1
    pos += 1
    while pos < len(text):
        if text[pos] == "\\":
            pos += 2
            continue
        if text[pos] == opening:
            depth += 1
        elif text[pos] == closing:
            depth -= 1
            if depth == 0:
                return text[start:pos], pos + 1
        pos += 1
    raise ValueError("花括号或方括号未闭合")


def _source(text: str) -> str:
    """保留行号，忽略注释、导言区与命令定义；定义不算真实调用。"""
    lines = []
    for line in text.splitlines(keepends=True):
        for i, char in enumerate(line):
            if char == "%":
                n = len(line[:i]) - len(line[:i].rstrip("\\"))
                if n % 2 == 0:
                    line = line[:i] + _blank(line[i:])
                    break
        lines.append(line)
    text = "".join(lines)
    begin = re.search(r"\\begin\s*\{document\}", text)
    if begin:
        text = _blank(text[:begin.end()]) + text[begin.end():]
    end = re.search(r"\\end\s*\{document\}", text)
    if end:
        text = text[:end.start()] + _blank(text[end.start():])
    definition = re.compile(r"\\(?:newcommand|renewcommand|providecommand|DeclareRobustCommand)\*?\s*")
    pos = 0
    while match := definition.search(text, pos):
        cursor = match.end()
        try:
            if cursor < len(text) and text[cursor] == "{":
                _, cursor = _group(text, cursor)
            else:
                name = re.match(r"\\[A-Za-z@]+", text[cursor:])
                if not name:
                    raise ValueError("命令定义缺少名称")
                cursor += name.end()
            while True:
                while cursor < len(text) and text[cursor].isspace():
                    cursor += 1
                if cursor >= len(text) or text[cursor] != "[":
                    break
                _, cursor = _group(text, cursor, "[", "]")
            _, cursor = _group(text, cursor)
        except ValueError:
            cursor = text.find("\n", match.start())
            if cursor < 0:
                cursor = len(text)
        text = text[:match.start()] + _blank(text[match.start():cursor]) + text[cursor:]
        pos = cursor
    return text


def _calls(text: str, signatures: dict[str, int]) -> tuple[list[Call], list[str]]:
    pattern = re.compile(r"\\(" + "|".join(map(re.escape, signatures)) + r")(?![A-Za-z@])")
    calls, errors = [], []
    pos = 0
    while match := pattern.search(text, pos):
        cursor, args = match.end(), []
        try:
            for _ in range(signatures[match.group(1)]):
                arg, cursor = _group(text, cursor)
                args.append(arg.strip())
            calls.append(Call(match.group(1), args, match.start(), cursor))
        except ValueError as exc:
            errors.append(f"第 {text.count(chr(10), 0, match.start()) + 1} 行 \\{match.group(1)}：{exc}")
            cursor = match.end()
        pos = cursor
    return calls, errors


def _appendix_start(text: str, calls: list[Call]) -> int | None:
    positions = [m.start() for m in re.finditer(r"\\appendix(?![A-Za-z@])", text)]
    positions.extend(c.start for c in calls if c.name in ("hdr", "subhdr")
                     and any(re.search(r"附录|\bAppendix\b", arg, re.I) for arg in c.args))
    return min(positions) if positions else None


def split_blocks(text: str) -> list[tuple[str, list[str]]]:
    """保留旧调用接口；同时支持 hdr 的两个参数与 subhdr 的一个参数。"""
    calls, _ = _calls(text, {"hdr": 2, "subhdr": 1})
    return [(" · ".join(c.args), text[c.start:calls[i+1].start if i+1 < len(calls) else len(text)].splitlines())
            for i, c in enumerate(calls)]


def check_boxes(lines: list[str]) -> list[str]:
    """只给人工复核线索；不判证明真假，也不规定例子与推导的顺序。"""
    warns = []
    for i, line in enumerate(lines):
        if r"\boxed" not in line:
            continue
        start = max(0, i - 60)
        for j in range(i - 1, start - 1, -1):
            if HEAD_RE.match(lines[j]):
                start = j
                break
        before = lines[start:i]
        examples = [j for j, s in enumerate(before) if EXAMPLE_WORD_RE.search(s)]
        if not examples:
            continue
        meaningful = [s.strip() for s in before if s.strip() and s.strip() not in (r"\[", r"\]")
                      and not s.strip().startswith((r"\begin{", r"\end{"))]
        if not meaningful:
            continue
        prev = meaningful[-1]
        if "=" in prev or DERIV_WORD_RE.search(prev) or re.search(r"定理|定义|命题|引理|推论|性质", prev):
            continue
        # 数字例前已有一般推导时，不因随后出现例子就重复报警。
        pre_example = "\n".join(before[:examples[0]])
        if DERIV_WORD_RE.search(pre_example) and len(re.findall(r"\\\[|\\begin\{(?:align\*?|equation\*?)\}", pre_example)) >= 2:
            continue
        warns.append(f"第 {i + 1} 行结论框邻近数值例子，且前一句未见一般推导依据；"
                     "仅为复核线索，请人工确认一般依据是否完整，不能据此判定证明错误或要求固定写作顺序")
    return warns


def check_file(path: Path, mode: str = "theory") -> tuple[list[str], list[str]]:
    errors, warns = [], []
    try:
        raw = path.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeError) as exc:
        return [f"无法读取输入：{path}：{exc}"], []
    text = _source(raw)
    if not text.strip():
        return ["输入为空，或没有可检查的正文（只有注释、导言区或命令定义）"], []
    environments, _ = _calls(text, {"begin": 1})
    for call in environments:
        name = call.args[0]
        if name in THEME_COMMAND_ONLY:
            line = text.count("\n", 0, call.start) + 1
            errors.append(f"第 {line} 行把主题命令 \\{name} 当作环境；"
                          f"请用 \\{name}{{...}}，不要用 \\begin{{{name}}}")
    calls, parse_errors = _calls(text, {"practice": 5, "answerstart": 3, "answercontinue": 2,
                                      "hdr": 2, "subhdr": 1, "qstem": 1, "label": 1})
    errors.extend(parse_errors)
    practices = [c for c in calls if c.name == "practice"]
    answers = [c for c in calls if c.name == "answerstart"]
    continuations = [c for c in calls if c.name == "answercontinue"]
    boundary = _appendix_start(text, calls)
    labels = [c.args[0] for c in calls if c.name == "label"] + ["ans:" + c.args[0] for c in answers]
    for label in set(labels):
        if labels.count(label) > 1:
            errors.append(f"重复标签：{label}")
    for kind, items in (("practice", practices), ("answerstart", answers)):
        ids = [c.args[0] for c in items]
        for item_id in set(ids):
            if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9:_.-]*", item_id):
                errors.append(f"{kind} 的 ID 应为非空字母/数字及 : _ . - ：{item_id!r}")
            if ids.count(item_id) > 1:
                errors.append(f"重复 {kind} ID：{item_id}")
    starts = {c.args[0]: c for c in answers}
    for call in practices:
        item_id, source, stem, target, ref = call.args
        if not all(call.args):
            errors.append(f"practice {item_id!r} 的 ID、来源、题干、考点和答案标签都必须填写")
        if HINT_RE.search(stem + "\n" + target):
            errors.append(f"正文练习 {item_id} 含明确的解题提示/关键一步/答案；请移入附录答案块")
        following = [c.start for c in calls if c.start > call.start and c.name in
                     ("hdr", "subhdr", "practice", "answerstart", "answercontinue")]
        end = min(following + ([boundary] if boundary is not None and boundary > call.start else []) + [len(text)])
        tail = re.sub(r"(?:详解|答案)\s*[：:]?\s*(?:见|在)附录[^\n]*", "", text[call.end:end])
        if HINT_RE.search(tail):
            errors.append(f"正文练习 {item_id} 后紧跟解题提示/答案，请移入附录或另设教学示例")
        if ref not in labels:
            errors.append(f"正文练习 {item_id} 的答案标签不存在：{ref}")
        if item_id not in starts:
            errors.append(f"正文练习 {item_id} 缺少同 ID 的 answerstart")
        elif ref != "ans:" + item_id:
            errors.append(f"正文练习 {item_id} 应指向自己的自动标签 ans:{item_id}，实际为 {ref}")
        if DRAW_RE.search(stem) and item_id in starts:
            answer = starts[item_id]
            answer_end = min([c.start for c in answers if c.start > answer.start] + [len(text)])
            if not FIG_RE.search(text[answer.end:answer_end]):
                warns.append(f"练习 {item_id} 要求作图，但对应附录解答未见图；请人工核对图是否完整且就近可读")
        if mode == "appendix" and (boundary is None or call.start >= boundary):
            errors.append(f"practice {item_id} 必须放在明确的附录边界之前")
    for call in answers:
        if not all(call.args):
            errors.append(f"answerstart {call.args[0]!r} 必须带来源和本题条件摘要")
        if mode == "appendix" and (boundary is None or call.start < boundary):
            errors.append(f"answerstart {call.args[0]} 必须放在 \\appendix 或附录标题之后")
    for call in continuations:
        prior = starts.get(call.args[0])
        if not all(call.args):
            errors.append("answercontinue 必须带 ID 和条件摘要")
        if prior is None or prior.start >= call.start:
            errors.append(f"answercontinue {call.args[0]} 前没有同 ID 的 answerstart")

    heads = [c for c in calls if c.name in ("hdr", "subhdr")]
    legacy_practices = 0
    for i, head in enumerate(heads):
        end = heads[i+1].start if i+1 < len(heads) else len(text)
        title, joined = " · ".join(head.args), text[head.end:end]
        block_calls = [c for c in calls if head.end <= c.start < end]
        stems = [c for c in block_calls if c.name == "qstem"]
        explicit = any(c.name in ("practice", "answerstart", "answercontinue") for c in block_calls)
        if QUESTION_RE.search(title) and not explicit and not any(mark in joined[:1800] for mark in STEM_MARKERS):
            errors.append(f"题块「{title}」开头看不到题干或明确条件")
        for stem in stems:
            if not re.search(r"(?:课件|教材|讲义|补例|自编|改编)|\bp\s*\d", stem.args[0], re.I):
                warns.append(f"题块「{title}」题干来源不明确，请人工补核页码或自编说明")
        is_legacy_practice = bool(stems and PRACTICE_TITLE_RE.search(title) and not explicit
                                  and (boundary is None or head.start < boundary))
        if is_legacy_practice:
            legacy_practices += len(stems)
            if mode == "appendix":
                clean = re.sub(r"(?:详解|答案)(?:\}|\s)*[：:]?\s*(?:见|在)?\s*附录[^\n]*", "", joined)
                if HINT_RE.search(clean):
                    errors.append(f"正文练习「{title}」含解题提示/答案，不符合 appendix 模式")
                if not re.search(r"\\(?:page)?ref\s*\{", joined):
                    errors.append(f"正文练习「{title}」缺少可解析的附录答案引用")
                warns.append(f"旧式练习「{title}」尚无显式 ID 配对，请人工核对题号与附录条件；建议迁移到 practice")
        if ENG_TITLE_RE.search(title) and ENG_BODY_RE.search(joined) and r"\begin{tabular}" in joined and not FIG_RE.search(joined):
            warns.append(f"器件小节「{title}」有状态表而未见图，请人工核对拓扑/路径是否可读")
        asks_drawing = (QUESTION_RE.search(title) and DRAW_RE.search(title)) or any(DRAW_RE.search(c.args[0]) for c in stems)
        if asks_drawing and not FIG_RE.search(joined) and not is_legacy_practice:
            warns.append(f"题块「{title}」要求作图但本块未见图；请按教学示例/实验问答的实际要求核对")
    if mode == "appendix" and not practices and not legacy_practices:
        errors.append("appendix 模式未发现真实的正文练习调用；命令定义不算练习")
    if mode == "appendix" and (practices or legacy_practices) and boundary is None:
        errors.append("appendix 模式缺少 \\appendix 或明确的附录标题")
    refs, ref_errors = _calls(text, {"ref": 1, "pageref": 1, "eqref": 1, "autoref": 1, "nameref": 1})
    errors.extend(ref_errors)
    for ref in refs:
        if ref.args[0] not in labels:
            errors.append(f"引用标签在本源文件中未定义：{ref.args[0]}（分文件内容需合并检查）")
    warns.extend(check_boxes(text.splitlines()))
    for no, line in enumerate(text.splitlines(), 1):
        for char, replacement in (("✓", r"$\checkmark$"), ("✗", r"$\times$")):
            if char in line:
                errors.append(f"第 {no} 行有裸 {char}，请改用 {replacement} 并检查 PDF 字形")
    return list(dict.fromkeys(errors)), list(dict.fromkeys(warns))


def check_log(path: Path) -> tuple[list[str], list[str]]:
    try:
        text = path.read_text(encoding="utf-8-sig", errors="replace")
    except OSError as exc:
        return [f"无法读取编译日志：{path}：{exc}"], []
    if not text.strip():
        return ["编译日志为空"], []
    errors = []
    patterns = {
        "LaTeX 编译错误": r"(?m)^!", "版面溢出": r"Overfull \\[hv]box",
        "缺失字符": r"Missing character:",
        "未解析引用": r"(?:undefined references|(?:Reference|Citation)[^\n]*undefined)",
        "交叉引用仍需重编译": r"Label\(s\) may have changed|Rerun to get cross-references right",
        "重复标签": r"multiply defined",
    }
    for name, pattern in patterns.items():
        count = len(re.findall(pattern, text, re.I))
        if count:
            errors.append(f"{name}：{count} 处（见 {path.name}）")
    if "Output written on" not in text:
        errors.append("日志没有成功生成 PDF 的结束记录")
    return errors, []


def main(argv: list[str] | None = None) -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("files", nargs="*")
    ap.add_argument("--mode", choices=("theory", "appendix", "lab"), default="theory")
    ap.add_argument("--log", type=Path, help="检查单个 TeX 对应的最终编译日志")
    if argv and Path(argv[0]).name == "check_handout.py":
        argv = argv[1:]
    args = ap.parse_args(argv)
    files = [Path(p) for p in args.files] or sorted(Path("subjects").rglob("*.tex"))
    if args.log and len(files) != 1:
        ap.error("--log 只支持同时检查一个 TeX 文件")
    if not files:
        print("[E] 没有找到 .tex 文件")
        return 1
    total_err = total_warn = 0
    for path in files:
        errors, warns = check_file(path, args.mode)
        if args.log:
            log_errors, log_warns = check_log(args.log)
            errors.extend(log_errors)
            warns.extend(log_warns)
        print(f"[检查] {path}")
        for message in errors:
            print(f"   [E] {message}")
        for message in warns:
            print(f"   [W] {message}")
        if not errors and not warns:
            print("   静态检查未发现问题；尚不代表数学正确或 PDF 页面已验收")
        total_err += len(errors)
        total_warn += len(warns)
    print(f"\n合计：错误 {total_err} 条，人工复核线索 {total_warn} 条")
    return 1 if total_err else (2 if total_warn else 0)


if __name__ == "__main__":
    sys.exit(main())
