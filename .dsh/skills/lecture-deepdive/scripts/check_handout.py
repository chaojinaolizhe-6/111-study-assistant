# -*- coding: utf-8 -*-
r"""check_handout.py —— 讲义交付前的「一题一块」自动检查。

用法：
    python -B .dsh/skills/lecture-deepdive/scripts/check_handout.py [file.tex ...]
    不带参数时扫描 subjects/**/*.tex。

检查项（对应 SKILL.md 硬性约束 13 与步骤 5 清单）：
  1. 每个「第 N 题」详解块的开头若干行内必须有题干：`\qstem` 或「题面／题目／已知／求」；
  2. 每个「例 N」块同样要有题面（例题可以不用 \qstem，但题干不能缺席）；
  3. 出现「作业汇总／题面照抄」字样而全文没有「答案／详解」→ 作业只抄了题面，没有解；
  4. 正文出现裸 ✓ ✗（lmroman 缺字，应写 $\checkmark$）；
  5. 警告：\qstem 没写课件页码；\qstem 前没加 \qbreak（可能被跨页拆开）；
  6. 警告：器件级小节有表格但没有图（figure/circuitikz/tikzpicture/includegraphics），
     可能用表代替了拓扑图（对应 SKILL.md 硬性约束 15）；
  7. 题块要求作图（标题或 \qstem 里有「画图／作图／sketch／draw」）却没有图：
     读者被要求画图，答案块里却只有文字，只能去别处找图（对应「局部自足」与约束 15）。
     2026-10-31 加：3.8 磁滞回线讲义 §7 Q2「并画图」答案块无图，就是这个漏检。
     阻断口径只到 Q 编号题块（预习问题／课后思考题，答案要能直接抄）；
     其余块（作业、自测、小节标题）只提示——作业可能故意不给答案图。
  8. 警告：结论框（\boxed）前面看不到推导——窗口内既没有 \step／推理性连接词，
     也没有 ≥2 组行间公式；或窗口里最近的段落是「数字例子／例如」。
     这是「以例代证」的形状（对应 SKILL.md 硬性约束 16）。
     2026-11-04 加：《专题·从张量到并矢》§1.3 用 45° 例子顶替 T'=RᵀTR 的推导就是它。
     注意：这条只抓形状，真判据是「删例测试」——把例子整段遮住，还能不能走到结论。

退出码：0 全通过；1 有错误；2 只有警告。
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

HEAD_RE = re.compile(r"^\s*\\(?:subhdr|hdr)\{(.*)\}\s*$")
PROBLEM_RE = re.compile(r"第\s*\d+\s*题")
EXAMPLE_RE = re.compile(r"例\s*\d+")
STEM_MARKERS = (r"\qstem{", "题面", "题目", "已知", "求：", "求 ", "题：", "？", "?")
FIG_RE = re.compile(r"\\begin\{(?:figure|circuitikz|tikzpicture)\}|\\includegraphics")
ENG_TITLE_RE = re.compile(r"(电路|桥式|整流|滤波|稳压|运放|放大|光路|受力|装置|接线|波形)")
ENG_BODY_RE = re.compile(r"(导通|截止|开关状态|电流方向|正半周|负半周)")
DRAW_RE = re.compile(r"(画图|作图|画出[^，。；]{0,6}(曲线|回线|图)|示意图|sketch|Sketch|with sketches|\bdraw\b|\bDraw\b)")
QUESTION_HEAD_RE = re.compile(r"(Q\s*\d|第\s*[（(]?\d+[)）]?\s*[题问]|作业\s*\d|例\s*\d|Exercise|Problem)")
LOOKAHEAD = 12  # 标题后看几行

# 约束 16：结论框前面必须有推导，不能靠数值例子顶替
BOX_RE = re.compile(r"\\boxed\s*\{")
DERIV_WORD_RE = re.compile(
    r"(\\step\{|所以|于是|由此得|即得|代入|展开|合并|相减|两边|推出|注意到|因为|从而|可得)"
)
EXAMPLE_WORD_RE = re.compile(r"(数字例子|例如|举例|例子|试算|手动验算|取.{0,8}为例)")
BOX_WINDOW = 45  # 结论框往前看几行
# 这些记号说明这一行还在公式里（上一行行间公式的续行），不是散文断言
MATHISH = (r"\tag", r"\Longrightarrow", r"\Rightarrow", r"\qquad", r"\quad", r"\\",
           r"\sum", r"\frac", "^{", "_{", r"\cdot", r"\mathrm")


def split_blocks(text: str) -> list[tuple[str, list[str]]]:
    lines = text.splitlines()
    heads = [(i, m.group(1)) for i, line in enumerate(lines) if (m := HEAD_RE.match(line))]
    blocks: list[tuple[str, list[str]]] = []
    for k, (i, title) in enumerate(heads):
        j = heads[k + 1][0] if k + 1 < len(heads) else len(lines)
        blocks.append((title, lines[i:j]))
    return blocks


def has_stem(lines: list[str]) -> bool:
    head = "\n".join(lines[1 : 1 + LOOKAHEAD])
    return any(m in head for m in STEM_MARKERS)


def asks_for_drawing(title: str, body: list[str]) -> bool:
    r"""题面本身要求作图：标题里写了「画图／作图」，或 \qstem 里要求画。"""
    if DRAW_RE.search(title):
        return True
    return any("\\qstem{" in line and DRAW_RE.search(line) for line in body[1:])


def is_question_block(title: str, body: list[str]) -> bool:
    r"""是不是「题」块：Q1／第 3 题／作业 2／例 5，或带 \qstem 的块。"""
    if QUESTION_HEAD_RE.search(title):
        return True
    return any("\\qstem{" in line for line in body[1:])


def prev_meaningful(lines: list[str], i: int, n: int = 3) -> list[str]:
    r"""结论框往前的最后 n 行「有内容的行」，跳过空行与 \[ \] 之类的脚手架。"""
    out: list[str] = []
    for line in reversed(lines[max(0, i - 12):i]):
        s = line.strip()
        if not s or s in (r"\[", r"\]") or s.startswith(r"\end{") or s.startswith(r"\begin{"):
            continue
        out.append(s)
        if len(out) >= n:
            break
    return out


def check_boxes(lines: list[str]) -> list[str]:
    r"""约束 16：结论框是「算出来的」还是「举例举出来的」。

    只认一种形状（低误报）：**紧挨着结论框的那一行是散文断言**——
    不含公式、不含推导连接词、不是定理／定义的陈述句——
    而**同一小节里**（同一 \subhdr 之后）出现过「例子／例如／数字例子」。

    这正好是「算完 45° 例子 → 于是这条规则是 → 黑框」的走法：
    结论前面那行是「这条换算规则是」，而不是任何一行推导。

    不报的三种（有意放过）：
      ① 结论框前面紧挨着的是公式——那是推导链的末行；
      ② 结论框前面是 \step／所以／代入…——推理性连接词在；
      ③ 前面是「定理：…则」——定理陈述本来就不需要推导（约束 8 管它）。
    真判据仍是「删例测试」，这里只负责把可疑处指出来。
    """
    warns: list[str] = []
    for i, line in enumerate(lines):
        if not BOX_RE.search(line):
            continue

        prev = prev_meaningful(lines, i, n=1)
        if not prev:
            continue
        p = prev[0]
        if "=" in p or any(tok in p for tok in MATHISH):
            continue
        if DERIV_WORD_RE.search(p):
            continue
        if re.search(r"(定理|定义|命题|引理|推论|性质)", p):
            continue

        head = -1
        for k in range(i - 1, -1, -1):
            if HEAD_RE.match(lines[k]):
                head = k
                break

        ex = None
        for k in range(i - 1, max(head, i - BOX_WINDOW), -1):
            if EXAMPLE_WORD_RE.search(lines[k]):
                ex = k
                break
        if ex is None:
            continue  # 本小节里没有数值例子：不是这条要管的形状

        warns.append(
            f"第 {i + 1} 行的结论框，紧挨着的前一行是散文断言（「{p[:24]}…」），不是公式；"
            f"同小节第 {ex + 1} 行起在举数值例子——例子给完 {i - ex} 行就直接上结论。"
            "这是「以例代证」的形状（约束 16）：例子只算核对，推导要补在黑框之前，或按约束 1 给出课件页码"
        )
    return warns


def check_file(path: Path) -> tuple[list[str], list[str]]:
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    warns: list[str] = []

    for title, body in split_blocks(text):
        joined = "\n".join(body)

        if PROBLEM_RE.search(title) and not has_stem(body):
            errors.append(f"题块「{title}」开头看不到题干（既无 \\qstem，也无题面／题目／已知）")

        if r"\qstem" in joined:
            if not re.search(r"\\qstem\{\s*[（(]\s*课件", joined):
                warns.append(f"题块「{title}」的题干没写课件页码（应为「（课件 pXX 第 N 题）」开头）")
            start = text.index(joined)
            if not text[:start].rstrip().endswith(r"\qbreak"):
                warns.append(f"题块「{title}」的 \\qstem 前没有 \\qbreak，可能被跨页拆开")

        # 约束 15：器件级小节有表格、却没有拓扑图（警告，不阻断）
        if (ENG_TITLE_RE.search(title) and ENG_BODY_RE.search(joined)
                and "\\begin{tabular}" in joined and not FIG_RE.search(joined)):
            warns.append(f"器件级小节「{title}」只有表、没有图；检查是否用表代替了拓扑图（约束 15）")

        # 题面要求作图，答案块里就必须自带图
        if asks_for_drawing(title, body) and not FIG_RE.search(joined):
            msg = (f"题块「{title}」要求作图，但块内没有图"
                   "（figure/tikzpicture/includegraphics）；不能只让读者去看别处的「图 N」")
            if is_question_block(title, body) and QUESTION_HEAD_RE.search(title) and re.match(r"\s*Q\s*\d", title):
                errors.append(msg)
            else:
                warns.append(msg.replace("题块", "块") + "（非 Q 编号题块只提示，不阻断：作业／自测可能故意不给答案图）")

    if re.search(r"(作业汇总|题面照抄|题面成组)", text) and not re.search(r"(答案|详解)", text):
        errors.append("作业只有题面（「作业汇总／题面照抄」），全文没有答案或详解")

    warns.extend(check_boxes(text.splitlines()))

    for no, line in enumerate(text.splitlines(), 1):
        if "✓" in line:
            errors.append(f"第 {no} 行有裸 ✓（lmroman 缺字），改为 $\\checkmark$")
        if "✗" in line:
            errors.append(f"第 {no} 行有裸 ✗，改用文字或 $\\times$")

    return errors, warns


def main(argv: list[str]) -> int:
    files = [Path(p) for p in argv[1:]] or sorted(Path("subjects").rglob("*.tex"))
    if not files:
        print("没有找到 .tex 文件")
        return 2

    total_err = total_warn = 0
    for path in files:
        try:
            errors, warns = check_file(path)
        except (UnicodeDecodeError, OSError) as exc:
            print(f"[跳过] {path}：{exc}")
            continue
        if not errors and not warns:
            print(f"[通过] {path.name}")
            continue
        print(f"[检查] {path}")
        for e in errors:
            print(f"   [E] {e}")
        for w in warns:
            print(f"   [W] {w}")
        total_err += len(errors)
        total_warn += len(warns)

    print(f"\n合计：错误 {total_err} 条，警告 {total_warn} 条")
    if total_err:
        return 1
    return 2 if total_warn else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
