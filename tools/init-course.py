#!/usr/bin/env python3
"""生成一门课程的目录骨架：INDEX.md / progress.md / topics/INDEX.md / 课件/INDEX.md / 作业/INDEX.md。

用法（在工作区根目录运行）:
  python -B tools/init-course.py "NN-课程名" 类型

类型: 专业课 | 文科 | 其他
新增课程后记得同步 subjects/INDEX.md 与 .tutor/config/project.yml 的 subjects 段。
"""
from __future__ import annotations

import sys
from pathlib import Path

INDEX_TMPL = """# {name}（{cid}）

- 类型：{ctype}
- 教学进度：未知（尚未提供，不编造）
- 概念路径：未规划 —— 首次学习时先诊断（/plan），再按前置依赖生成路径

## 目录

- 课件：[课件/INDEX.md](课件/INDEX.md)
- 作业：[作业/INDEX.md](作业/INDEX.md)
- 主题：[topics/INDEX.md](topics/INDEX.md)
- 学习进度：[progress.md](progress.md)

## 三态标记（防"传了课件就以为会了"）

- 老师已讲：课堂讲过的部分
- 我已看过：自己翻看过课件
- 能独立完成：合上资料能独立做出对应题目

（三态均未登记：尚未放入课件，也未提供教学进度。）
"""

PROGRESS_TMPL = """# {name} 学习进度

> 会话记录由学习助手在每次学习/复习/测验后追加（rep + 反思 + 下一步）。

（暂无会话记录）
"""

TOPICS_TMPL = """# {name} 主题索引

（暂无主题；诊断后按概念路径建立主题与概念笔记）
"""

KEJIAN_TMPL = """# {name} 课件索引

> 把老师课件（PDF / PPT 转 PDF / 图片）直接放进本文件夹，放好后告诉学习助手，会读入并登记。
> 上传课件 ≠ 学会：三态由学习助手在辅导中核实，不因放入文件自动打勾。

## 课件登记

| 文件 | 老师已讲 | 我已看过 | 能独立完成 | 备注 |
|------|---------|---------|-----------|------|
| （暂无） | — | — | — | 等待放入课件 |
"""

ZUOYE_TMPL = """# {name} 作业索引

> 把作业题目照片（多张可以）直接放进本文件夹，告诉学习助手，会读图、登记、按截止日期纳入周计划。
{homework_note}
## 作业登记

| 编号 | 标题 | 截止日期 | 状态 | 材料 |
|------|------|---------|------|------|
| （暂无） | — | 未知 | 未知 | 等待放入题目 |

## 照片歧义标注约定

读题照片时，以下情况一律标 `[待确认]` 并向你确认，不自行猜测：
- 电路连接关系（哪根线接哪个节点）
- 公式上下标、指数、根号范围
- 手写数字/符号歧义（如 1 与 l、2 与 z、+ 与 t）
- 题目缺页、照片边缘被裁掉的部分
"""

HOMEWORK_NOTES = {
    "文科": "> 备注：目前没有课下作业。",
    "其他": "> 备注：目前没有课下作业。",
}


def main() -> int:
    if len(sys.argv) < 3:
        print("usage: python -B tools/init-course.py \"NN-课程名\" 类型", file=sys.stderr)
        return 2
    cid = sys.argv[1]
    ctype = sys.argv[2]
    name = cid.split("-", 1)[1] if "-" in cid else cid
    base = Path("subjects") / cid
    if base.exists():
        print(f"already exists, skip: {base}")
        return 1
    (base / "课件").mkdir(parents=True, exist_ok=True)
    (base / "作业").mkdir(parents=True, exist_ok=True)
    (base / "topics").mkdir(parents=True, exist_ok=True)
    hw_note = HOMEWORK_NOTES.get(ctype, "")
    files = {
        "INDEX.md": INDEX_TMPL.format(name=name, cid=cid, ctype=ctype),
        "progress.md": PROGRESS_TMPL.format(name=name),
        "topics/INDEX.md": TOPICS_TMPL.format(name=name),
        "课件/INDEX.md": KEJIAN_TMPL.format(name=name),
        "作业/INDEX.md": ZUOYE_TMPL.format(name=name, homework_note=hw_note),
    }
    for rel, content in files.items():
        (base / rel).write_text(content, encoding="utf-8")
    print(f"created {base} ({ctype})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
