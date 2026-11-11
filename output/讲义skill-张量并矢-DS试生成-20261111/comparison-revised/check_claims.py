# -*- coding: utf-8 -*-
"""Check the revised comparison's source quotations against the frozen PDFs.

Each entry is (source, page, required normalized substring, description).
The check is page-level: the crop rectangles are separately anchor-checked by
render_crops.py. This proves the quoted sentence still exists on the cited
source page; it does not prove the interpretation or readability.
"""
import fitz
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = {
    "old": os.path.join(ROOT, "inputs", "old-handout.pdf"),
    "new": os.path.join(ROOT, "round-04", "handout.pdf"),
}

CLAIMS = [
    # COMP-C1 / A1: the old draft does state the summation rule
    ("old", 11, "重复出现两次的指标自动求和", "旧 §4.3 写出求和规则本身"),
    ("old", 11, "本讲义正文照旧写求和号", "旧 §4.3 紧接着写求和号用法"),
    ("old", 28, "同一项里重复出现两次的指标自动求和", "旧附录 A 重复求和规则"),
    # CMP-MATH-01 / A2: the old side note already contains the A23 check
    ("old", 15, "用分量核一遍最省事", "旧 p15 旁注给分量核对"),
    ("old", 15, "与课件矩阵的(2,3)元一致", "旧 p15 旁注核对到 (2,3) 元"),
    # COMP-C2 / C2: old symmetric top relies on the standard oscillator name
    ("old", 20, "这是标准的", "旧 §8.3 用“标准”一词"),
    ("old", 20, "振子方程", "旧 §8.3 点名振子方程"),
    ("old", 21, "不是陀螺本身在进动", "旧 p21 只接解释与几何图像"),
    ("new", 29, "直接代回可以当场核对", "新 §5.3 给代回核对"),
    ("new", 29, "给定初始横向矢量", "新 §5.3 由初值定常数"),
    ("new", 29, "不需要预先学过", "新 §5.3 不依赖简谐振子课程"),
    # COMP-C2 / C3: old balance equation stops at the formula
    ("old", 22, "写得开就是", "旧 §9.4 到“写得开”一句"),
    ("old", 22, "三个方程", "旧 §9.4 只说对应三个方向"),
    ("new", 32, "偏导在做什么", "新 §6.4 解释偏导操作"),
    ("new", 32, "为什么它的和是净面力", "新 §6.4 接应力差与净力"),
    ("new", 32, "除以体积", "新 §6.4 除以体积得净面力"),
    ("new", 32, "均匀单轴拉伸", "新 §6.4 给均匀应力对照"),
    # COMP-C3: §1.4 omission is factual; §1.3 gives local Tn=lambda n
    ("new", 10, "若存在非零矢量", "新 §1.4 正式定义仍在"),
    ("new", 9, "Tn=λn", "新 §1.3 局部给出 Tn=λn（文字层近似）"),
    # COMP-C2 / D1: 瞬时轴 is introduced and defined by the new draft
    ("old", 17, "绕定点", "旧 §7.1 用定点/质心"),
    ("new", 23, "瞬时轴是某一瞬间", "新 §4.1 自己定义瞬时轴"),
    ("new", 23, "质心是质量加权平均位置", "新 §4.1 解释质心"),
    # COMP-C2: old §4.6 already gives skip/resume guidance
    ("old", 12, "本讲义正文不用", "旧 §4.6 段内已给跳过提示"),
    ("old", 12, "那时再回来补这半页即可", "旧 §4.6 段内已给回补指引"),
    ("new", 20, "选读（可跳过）：上下标", "新 p20 把可选写进标题"),
    # re-check the unchanged claims kept in the booklet
    ("old", 12, "正是§4.4 的变换律", "旧 §4.5 末句仍指向 §4.4"),
    ("old", 23, "前两块给出", "旧例 1 中间步仍在"),
    ("old", 17, "单位并矢的定义，§5.4", "旧 §7.1 仍引用 §5.4"),
]

# Claims about what the old page does NOT use. These guard against counting a
# new-draft term as an old omission.
ABSENT = [
    ("old", 17, "瞬时轴", "旧 §7.1 没有使用“瞬时轴”"),
]


def norm(s):
    return re.sub(r"\s+", "", s.replace("\x00", "").replace("\r", "").replace("\n", ""))


def main():
    docs = {k: fitz.open(v) for k, v in SRC.items()}
    passed = failed = 0
    for source, page, needle, desc in CLAIMS:
        page_text = norm(docs[source][page - 1].get_text())
        ok = norm(needle) in page_text
        passed += ok
        failed += (not ok)
        print(f"[{'PASS' if ok else 'FAIL'}] {source} p{page}: {desc} | {needle!r}")
    for source, page, needle, desc in ABSENT:
        page_text = norm(docs[source][page - 1].get_text())
        ok = norm(needle) not in page_text
        passed += ok
        failed += (not ok)
        print(f"[{'PASS' if ok else 'FAIL'}] {source} p{page}: {desc} | not {needle!r}")
    print(f"\nTOTAL: {passed} passed, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
