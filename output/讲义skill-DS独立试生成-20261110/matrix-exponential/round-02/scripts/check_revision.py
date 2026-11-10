#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""检查本轮返工的问题点是否在 TeX 源中真实落实（R1/R2/R3/R4/R5/R6/R8）。

这不是数学证明，也不代替 PDF 页面阅读；它只把问题单要求的可见改动变成可复核断言。
任一断言失败以非零退出码报告。
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parents[1]
TEX = ROOT / "handout.tex"
text = TEX.read_text(encoding="utf-8-sig")

checks = 0
failures: list[str] = []


def ok(name: str, condition: bool) -> None:
    global checks
    checks += 1
    if condition:
        print(f"[PASS] {name}")
    else:
        failures.append(name)
        print(f"[FAIL] {name}")


def require(name: str, needle: str) -> None:
    ok(name, needle in text)


def forbid(name: str, needle: str) -> None:
    ok(name, needle not in text)


# ---------- R1: 重根导数条件不再由点值等式直接求导 ----------
forbid("R1 不再写“把 e^λ=r(λ) 对 λ 求导”", "把等式 $e^{\\lambda}=r(\\lambda)$ 对 $\\lambda$ 求导")
require("R1 说明 r 是 Hermite 插值多项式", "Hermite 插值")
require("R1 用 f-r 的零点阶数解释导数条件", "阶零点")
require("R1 有 Jordan 块论证", "Jordan 块")
require("R1 说明块大小不超过代数重数", "块大小 $\\ell\\le m$")
require("R1 区分纯量矩阵块大小为 1", "纯量矩阵")
require("R1 Theorem 3.3 说明“特定的 r”", "结论是对这个特定的 $r$ 说的")
require("R1 定理前提含重数与次数", "次数 $\\le n-1$ 的多项式")

# ---------- R2: Cauchy 乘积指标范围 ----------
forbid("R2 去掉内层求和外的 t^k s^{n-k}", "\\right)t^ks^{n-k}")
require("R2 两个矩阵幂分式都在内层求和内",
        "\\frac{A^kt^k}{k!}\\,\\frac{A^{n-k}s^{n-k}}{(n-k)!}")

# ---------- R3: 特征多项式首一约定与解析函数除法范围 ----------
require("R3 记号表使用首一 det(sE-A)", "$\\det(sE-A)$")
require("R3 §4.5 明确使用首一 Δ", "首一特征多项式")
forbid("R3 不再说“幂级数的长除法总可以进行”", "幂级数的长除法总可以进行")
require("R3 说明不能把长除法无条件照搬", "不能把上面的长除法")
require("R3 说明先定 r 再验证整除", "先定 $r$，再验证整除")
require("R3 给出 f-r 被 Δ 整除", "f-r$ 被 $\\Delta_x$ 整除")

# ---------- R4: A 与 Ax 的特征值、x=0 适用域 ----------
require("R4 有独立的适用范围小节", "\\subhdr{4.5.1")
require("R4 说明 x=0 时特征值合并", "所有 $\\lambda_i(0)=0$ 合并成 $0$")
require("R4 例4 限定 x≠0", "故对 $x\\ne0$，$\\Ax$ 的特征值是 $\\lambda_1=4x$")
require("R4 例5 限定 x≠0", "对 $x\\ne0$，特征值 $\\lambda_1=\\ii x$")
require("R4 例8 限定 x≠0", "对 $x\\ne0$，$\\Ax$ 的特征值是 $\\lambda_1=0$")


# ---------- R5: 独立练习考点不泄露谱类型 ----------
def skip_space_comments(src: str, pos: int) -> int:
    while pos < len(src):
        if src[pos].isspace():
            pos += 1
        elif src[pos] == "%":
            nl = src.find("\n", pos)
            pos = len(src) if nl < 0 else nl + 1
        else:
            break
    return pos


def five_groups(src: str, pos: int) -> list[str]:
    out = []
    for _ in range(5):
        pos = skip_space_comments(src, pos)
        if pos >= len(src) or src[pos] != "{":
            raise ValueError("缺少花括号参数")
        depth, pos = 1, pos + 1
        start = pos
        while pos < len(src) and depth:
            if src[pos] == "\\":
                pos += 2
                continue
            if src[pos] == "{":
                depth += 1
            elif src[pos] == "}":
                depth -= 1
            pos += 1
        out.append(src[start:pos - 1])
    return out


practice_targets = []
for m in re.finditer(r"\\practice(?![A-Za-z@])", text):
    args = five_groups(text, m.end())
    practice_targets.append(args[3])

ok("R5 找到 3 道独立练习", len(practice_targets) == 3)
forbidden = re.compile(r"实特征值|复特征值|共轭|三个不同|谱类型|特征值类型|可对角化|Jordan")
for i, target in enumerate(practice_targets, 1):
    ok(f"R5 练习 H{i} 考点不含谱分类", not forbidden.search(target))
forbid("R5 导语不再说“特征值类型各不相同”", "特征值类型各不相同")
forbid("R5 练习页不再给出“实特征值”考点", "2×2 常系数系统；实特征值")
forbid("R5 练习页不再给出“共轭复特征值”考点", "共轭复特征值；实值通解")

# ---------- R6: 续页标记存在于源 ----------
for marker in ("例 1（续）", "例 4（续）", "例 5（续）", "例 6（补充，续）", "例 7（续）", "例 8（续）"):
    ok(f"R6 源中含续页标记 {marker}", marker in text)

# ---------- R8: 自检措辞与常数重命名 ----------
forbid("R8 去掉“几乎能抓住所有”", "几乎能抓住所有")
require("R8 说明局部检查不保证整体正确", "通过这两条并不保证整个矩阵函数正确")
require("R8 说明任意常数重命名是另一回事", "任意常数可以重新命名")

print(f"\n共执行 {checks} 条源级断言，失败 {len(failures)} 条。")
if failures:
    print("失败项：")
    for item in failures:
        print("  -", item)
    sys.exit(1)
print("REVISION SOURCE CHECKS PASSED")
