# -*- coding: utf-8 -*-
r"""round-02 成品文本与源文件的内容核对（查实际 PDF 文字，不只查编译成功）。

用法：python -B michelson/round-02/tools/content_check.py
核验重点：
  M03 最终 PDF 的 25% 与中英完整句确实可见、没有被 % 注释截断；
  M01/M02/M05/M07/M08/M09 的修订语句落在实际源文件中，旧错误句已不存在；
  M04 图 4 图注说明 z 从 M 量起、theta 顶点在 M；
  实验目的 7 项、仪器 14 件的双语落点仍在。
每条失败打印 [FAIL] 并以退出码 1 结束。
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import fitz

ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "handout.pdf"
TEX = ROOT / "handout.tex"
LOG = ROOT / "handout.log"

checks = 0
fails: list[str] = []


def ok(cond: bool, msg: str) -> None:
    global checks
    checks += 1
    if not cond:
        fails.append(msg)


def main() -> int:
    doc = fitz.open(PDF)
    pages = [p.get_text() for p in doc]
    full = re.sub(r"\s+", " ", "\n".join(pages))
    tex = TEX.read_text(encoding="utf-8")
    tex1 = re.sub(r"\s+", " ", tex)
    log = LOG.read_text(encoding="utf-8", errors="replace")

    # ---------- M03：百分号截断 ----------
    p16 = None
    for i, t in enumerate(pages, 1):
        if "附加(1)" in t and "Answer (English)" in t:
            p16 = i
            break
    ok(p16 is not None, "找不到附加 (1) 的成品页")
    if p16:
        pt = re.sub(r"\s+", " ", pages[p16 - 1])
        ok(re.search(r"暗纹的强度只有亮纹\s*的\s*25\s*%\s*，?\s*明暗对比变差", pt) is not None,
           f"p{p16} 中文 25% 后应紧接「明暗对比变差」（当前被截断）")
        ok(re.search(r"only\s*25\s*%\s*of the intensity of the bright ones", pt) is not None,
           f"p{p16} 英文 25% 后应紧接 of the intensity...")
        ok("数环容易数错" in pt, f"p{p16} 中文句末「数环容易数错」应可见")
        ok("so the rings are easily miscounted" in pt,
           f"p{p16} 英文句末 so the rings are easily miscounted 应可见")
        ok("25 选" not in pt, f"p{p16} 不应出现被截断后的「25 选」")
        ok("only 25 : 16" not in pt, f"p{p16} 不应出现被截断后的英文残片")
        bad = [ln for ln in pages[p16 - 1].splitlines() if re.search(r"25\s*$", ln)]
        ok(not bad, f"p{p16} 不应有以 25 结束的行（% 注释截断迹象）：{bad[:2]}")
    ok("25%" not in tex, "源文件不应再有未转义的 25%（应为 25\\%）")
    ok(tex.count("25\\%") >= 2, "源文件应有中文与英文两处 25\\%")

    # ---------- 问答完整性（实际 PDF 每页同时有中文答与英文答） ----------
    for qid in ("II-1", "II-2", "II-3", "II-6", "II-7", "II-8", "II-9", "附加(1)", "附加(2)"):
        page = None
        for i, t in enumerate(pages, 1):
            if re.search(r"(^|\n)" + re.escape(qid) + r"(\s|\n|$)", t):
                page = i
                break
        ok(page is not None, f"成品 PDF 找不到 {qid} 的标题页")
        if page:
            ok("答（中文）" in pages[page - 1], f"{qid} 页缺中文答案标记")
            ok("Answer (English)" in pages[page - 1], f"{qid} 页缺英文答案标记")

    # ---------- M05：相位约定 ----------
    ok("k-\\frac{\\delta_0}{2\\pi}" in tex.replace(" ", ""),
       "源文件应有含 δ0 的一般亮纹条件 (11-1')")
    ok("采用 $\\delta_0=0$ 的相位约定" in tex, "§3 应明确教学小例采用 δ0=0 约定")
    ok("中心亮纹条件就是 $2\\Dl=k_0\\lambda$" in tex,
       "例 3.2 应把中心亮纹条件落到自己的相位前提")
    ok("没有说 $0.01\\ \\mathrm{mm}$ 就是最小分度" in tex,
       "M07：应明确源资料未把 0.01 mm 定义为最小分度")

    # ---------- M07：最小分度只作假设 ----------
    ok("说明用假设" in tex, "M07：应把最小分度写成说明用假设")
    ok("并没有说 $0.01\\ \\mathrm{mm}$ 就是鼓轮的最小分度" in tex1.replace("  ", " "),
       "M07：§2.4 应说明 0.01 mm 不是已查明的最小分度")
    ok("按同一 $20:1$ 比例改算即可" in tex, "M07：应说明实际分度不同按 20:1 改算")

    # ---------- M08：G2 只补玻璃路程 ----------
    ok("补偿的是 I、II 两束光**穿过玻璃的那部分光程差**" in tex,
       "M08：应限定 G2 补偿的是玻璃部分")
    ok("不是两臂的总光程差" in tex, "M08：应明确不是两臂总光程差")
    ok("不消除两臂长度差产生的可调 $2\\Dl$" in tex,
       "M08：应说明 G2 不消除可调 2d")

    # ---------- M09：用词疑点不是数学冲突 ----------
    ok("是用词问题，不是可证明的公式冲突" in tex,
       "M09：§5.3 应把 thinner/denser 列为用词问题")
    ok("与公式相反" not in tex, "M09：不应再把源文整句判为与公式相反")
    ok("与该式相反" not in tex, "M09：II-6 不应再写与该式相反")
    ok("更疏／更密" in tex, "M09：应给出 thinner/denser 的读法")

    # ---------- M06：区分可见度、峰值与平均总强度 ----------
    ok("在入射总功率（即 $I_1+I_2$）保持不变的前提下" in tex,
       "M06：等分理由应写明 I1+I2 保持不变的条件")
    ok("一个周期内平均的总光强仍是 $I_1+I_2$" in tex,
       "M06：应说明平均总强度不因等分而增大")
    ok("if the total incident power $I_1+I_2$ is held fixed" in tex,
       "M06：英文也应写明固定总功率的条件")
    ok("更高的对比度" in tex and "higher contrast" in tex,
       "M06：中英应把等分的收益落到对比度")

    # ---------- M01：编号方向与符号 ----------
    ok("符号不能反" in tex, "M01：第四步应明确符号方向")
    ok("$r_{k-1}^2-r_k^2=\\frac{\\lambda z^2}{\\Dl}$" in tex
       or "r_{k-1}^2-r_k^2=\\frac{\\lambda z^2}{\\Dl}" in tex,
       "M01：应写较外减较内的正号方程")
    ok("$r_m^2-r_{m-1}^2=\\lambda z^2/\\Dl>0$" in tex,
       "M01：应给出环号差分正号")
    ok("$r_k^2-r_{k-1}^2=\\frac{\\lambda z^2}{\\Dl}$" not in tex,
       "M01：旧的正号错误式不应残留")
    ok("整数级次 $k$" in tex and "从中心数的环号 $m$" in tex,
       "M01：应把整数级次与环号分开命名")

    # ---------- M02：单位 ----------
    ok("6.328\\times10^{-4}\\ \\mathrm{mm}" in tex, "M02：应写出毫米单位中间结果")
    ok("10^{5}\\,\\Delta l[\\mathrm{mm}]" in tex, "M02：应给 nm 工作式")
    ok("不要直接把「读数差的毫米数除以 10 倍环数」当成波长的米数" in tex,
       "M02：应明确禁止旧口述操作")
    ok("就是波长的米数" not in tex, "M02：旧错误口述句不应残留")

    # ---------- M04：图 4 图注 ----------
    ok("尺寸线从 M 量到屏" in tex, "M04：图注应说明 z 从 M 量到屏")
    ok("M 是其中点" in tex, "M04：图注应说明 M 是中点")
    ok("$\\theta$ 的顶点在 M" in tex, "M04：图注应说明 theta 顶点在 M")
    ok("$\\Delta L\\equiv S_2'P-S_1P<0$" in tex,
       "M04：应保留有符号光程差约定")
    ok("光程差大小 $|\\Delta L|=2\\Dl\\cos\\theta$" in tex,
       "M04：应区分有符号差与大小")

    # ---------- 实验目的 7 项与仪器 14 件仍在 ----------
    objectives = [
        "Understand the structure of Michelson interferometer",
        "Adjust the non-localized interference fringe and measure the laser wavelength",
        "Adjust the localized fringe and measure the wavelength of the sodium laser",
        "Adjust white-light interference fringes",
        "Measure the refractive index of air",
        "Measure the refractive index of transparent sheet",
        "Observe multi-beam interference",
    ]
    for o in objectives:
        ok(o in tex, f"实验目的英文原文缺失：{o[:48]}")
    ok(tex.count("（选做") >= 4, "7 项目的中的 4 项 Optional 中文标注应保留")
    instruments = [
        "Helium-Neon laser (He-Ne laser)", "side plate", "beam expander",
        "fixed mirror M1", "light splitter G1", "compensation plate G2",
        "F-P fixed mirror P1", "F-P moving mirror P2", "presetting screw",
        "moving mirror M2", "micrometer screw", "moving mirror pallet",
        "frosted glass screen FG", "E, E$'$ observation position",
    ]
    for ins in instruments:
        ok(ins in tex, f"仪器英文名缺失：{ins}")

    # ---------- 日志硬性项 ----------
    ok("Overfull" not in log, "编译日志不应有 Overfull")
    ok("Underfull" not in log, "编译日志不应有 Underfull")
    ok("Missing character" not in log, "编译日志不应有 Missing character")
    ok("Undefined control sequence" not in log, "编译日志不应有未定义命令")
    ok("LaTeX Warning" not in log, "编译日志不应有 LaTeX Warning")

    print(f"内容检查 {checks} 条，失败 {len(fails)} 条；PDF 页数 {doc.page_count}")
    if fails:
        for f in fails:
            print("[FAIL]", f)
        return 1
    print("全部内容检查通过")
    return 0


if __name__ == "__main__":
    sys.exit(main())
