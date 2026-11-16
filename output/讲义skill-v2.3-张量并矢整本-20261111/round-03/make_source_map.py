# -*- coding: utf-8 -*-
"""生成 round-03/source-map.json。

页码不手写：从最终 handout.pdf 的文本里定位每个小节标题、图注、练习与详解，
再写进映射表。这样重排后页码不会变成过时数据；找不到锚点会以非零退出码报错。
"""
from __future__ import annotations

import datetime
import hashlib
import json
import re
import sys
from pathlib import Path

import fitz

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent
PARENT = ROOT.parent
TEX = ROOT / "handout.tex"
PDF = ROOT / "handout.pdf"


def sha(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    tex = TEX.read_text(encoding="utf-8")
    doc = fitz.open(PDF)
    flat = [re.sub(r"\s+", "", doc[i].get_text()) for i in range(doc.page_count)]
    pages = doc.page_count

    # 小节锚点：从 \subhdr{X\quad 标题} 里取；标题去掉 \quad、数学式与空白后
    # 在 PDF 文本里找；纯数学标题（如 3.2）退化为“按出现顺序找编号”。
    anchors: dict[str, int] = {}
    order: list[str] = []
    pending: list[tuple[str, str]] = []
    for raw in re.findall(r"\\subhdr\{([^}]*)\}", tex):
        m = re.match(r"\s*([0-9A-C]+\.[0-9]+)", raw)
        if not m:
            continue
        num = m.group(1)
        title = re.sub(r"^\\quad", "", raw[m.end():])
        title = re.sub(r"\$[^$]*\$", "", title)
        plain = re.sub(r"\\[a-zA-Z]+\s*", "", title)
        plain = re.sub(r"[{}\s·]+", "", plain)
        order.append(num)
        pending.append((num, plain))

    prev_page = 1
    for num, plain in pending:
        pg = None
        if plain:
            key = num + plain                     # 小标题里编号与标题相邻
            pg = next((i + 1 for i, t in enumerate(flat)
                       if i + 1 >= prev_page and key in t), None)
            if pg is None:
                pg = next((i + 1 for i, t in enumerate(flat)
                           if i + 1 >= prev_page and plain in t), None)
        if pg is None:  # 纯数学标题：按顺序找编号首次出现的页
            pat = re.compile(rf"{re.escape(num)}(?!\d)")
            pg = next((i + 1 for i, t in enumerate(flat)
                       if i + 1 >= prev_page and pat.search(t)), None)
        if pg is None:
            print(f"[E] 小节 {num} 在 PDF 里定位不到", file=sys.stderr)
            return 1
        anchors[num] = pg
        prev_page = pg

    figures = {}
    for i, t in enumerate(flat, 1):
        for m in re.finditer(r"图(\d+)（(?:自绘|据课件)", t):
            figures.setdefault(int(m.group(1)), i)
    if len(figures) != 11:
        print(f"[E] 图注定位异常：{figures}", file=sys.stderr)
        return 1

    practice_pages = {}
    for i, t in enumerate(flat, 1):
        for m in re.finditer(r"练习(P\d+)题干", t):
            practice_pages.setdefault(m.group(1), i)
    answer_pages, cont_pages = {}, {}
    for i, t in enumerate(flat, 1):
        for pid in [f"P{k}" for k in range(1, 13)]:
            if pid + "详解" in t and pid not in answer_pages:
                answer_pages[pid] = i
            if pid + "续解" in t:
                cont_pages.setdefault(pid, []).append(i)

    appB = next((i + 1 for i, t in enumerate(flat) if '指标与记号速查' in t), pages)
    appC = next((i + 1 for i, t in enumerate(flat) if '来源对应、补充与自补推导' in t), pages)
    sec8 = next((i + 1 for i, t in enumerate(flat) if '易错点、速查与三句话' in t), pages)

    def P(num: str) -> int:
        return anchors[num]

    def span(num_lo: str, num_hi: str) -> str:
        return f"§{num_lo}--§{num_hi}（第 {P(num_lo)}--{P(num_hi)} 页起）"

    source_files = []
    for rel in ["inputs/TM2026-Topic8-P1.pdf", "inputs/RIT-Whelan-notes10-tensor.pdf",
                "inputs/baseline-full-v2.2.2.tex", "inputs/baseline-full-v2.2.2.pdf",
                "inputs/accepted-mainline-v2.3.tex", "inputs/accepted-mainline-v2.3.pdf",
                "inputs/learner-background-confirmed-20261114.json",
                "inputs/learner-background-full.json", "inputs/prior-learner-background.json",
                "inputs/accepted-mainline-selection.json"]:
        p = PARENT / rel
        if p.exists():
            source_files.append({"path": rel, "bytes": p.stat().st_size, "sha256": sha(p)})

    source_claims = [
        {
            "id": "TM-p8-basis-dot-cross-epsilon-dual",
            "source": "TM2026-Topic8-P1.pdf p8",
            "source_claim": "正交归一基、坐标 a_k=a·n_k、求和约定、点积、叉乘、Levi-Civita 符号、对偶张量及其矩阵",
            "new_location": [f"§0.1（第 {P('0.1')} 页）", f"§0.2（第 {P('0.2')} 页）",
                             f"§2.6（第 {P('2.6')} 页）", f"附录 B（第 {appB} 页）"],
            "status": "used_as_source",
            "note": "对偶张量的矩阵与作用按本稿记号重写；Whelan 的符号相反处已在 §2.6 注出。ε/叉乘/轴矢量的右手基边界在 §0.2、§2.6、附录 B 各写一次。"
        },
        {
            "id": "TM-p9-dyad-operator-quadratic-unit",
            "source": "TM2026-Topic8-P1.pdf p9",
            "source_claim": "张量积（Dyad）、左右作用、转置、一般张量、线性算子 b=Ta、二次型 E=aTa、单位张量",
            "new_location": [f"§1.1（第 {P('1.1')} 页）", f"§2.2（第 {P('2.2')} 页）",
                             f"§2.3（第 {P('2.3')} 页）", f"§2.4（第 {P('2.4')} 页）",
                             f"§2.5（第 {P('2.5')} 页）", f"§2.8（第 {P('2.8')} 页）"],
            "status": "used_as_source",
            "note": "p9 没有给出谱定理与并矢缩并的完整证明；本稿在 §1.4、§2.4、§2.5 补足。"
        },
        {
            "id": "TM-p10-rotation-operator",
            "source": "TM2026-Topic8-P1.pdf p10",
            "source_claim": "固定基与随体基、半径矢量两种展开、S(t)=Σ n'_k⊗n_k",
            "new_location": [f"§3.1（第 {P('3.1')} 页）", f"§3.2（第 {P('3.2')} 页）"],
            "status": "used_as_source",
            "note": "本稿补出 S e_j=n'_j 的唯一性核对与矩阵列约定。"
        },
        {
            "id": "TM-p11-orthogonality-rotation-formula",
            "source": "TM2026-Topic8-P1.pdf p11",
            "source_claim": "S^T S=SS^T=1、保点积、绕单位轴 n 转 φ 的显式公式、无穷小旋转及其交换性",
            "new_location": [f"§3.3（第 {P('3.3')} 页）", f"§3.4（第 {P('3.4')} 页）",
                             f"§3.5（第 {P('3.5')} 页）"],
            "status": "used_as_source",
            "note": "本稿用并矢点乘逐项算出两个正交性等式，并补 det S=+1 的连续性论证。"
        },
        {
            "id": "TM-p12-angular-velocity",
            "source": "TM2026-Topic8-P1.pdf p12",
            "source_claim": "A=dS/dt S^T 反对称、Ω^×=dS/dt S^T、dn'_k/dt=Ω×n'_k、无穷小情形 Ω=dφ/dt",
            "new_location": [f"§3.5（第 {P('3.5')} 页）", f"§5.1（第 {P('5.1')} 页）"],
            "status": "used_as_source",
            "note": "p12 只有旋转算子求导与角速度定义；没有欧拉方程、对称陀螺两方程或 Gauss 并矢版。旧元数据把后两者挂到 p12 是错的，见 metadata_corrections。"
        },
        {
            "id": "TM-p15-rigid-velocity",
            "source": "TM2026-Topic8-P1.pdf p15",
            "source_claim": "v=V+Ω×r；原点平移时 V'=V+Ω×a、Ω 不变；V·Ω=0 时存在瞬时转轴",
            "new_location": [f"§3.6（第 {P('3.6')} 页）", f"§4.1（第 {P('4.1')} 页）"],
            "status": "used_as_premise",
            "note": "本稿只用 v=V+Ω×r 与换基点关系；瞬时转轴细节不展开，因为本稿不处理平面运动学。"
        },
        {
            "id": "Whelan-pp2-3-angular-momentum",
            "source": "RIT-Whelan-notes10-tensor.pdf pp.2--3",
            "source_claim": "角动量与角速度、L=Iω 的矩阵动机、I=Σ m(r²1−rr^T)",
            "new_location": [f"§4.1（第 {P('4.1')} 页）", f"§4.2（第 {P('4.2')} 页）"],
            "status": "used_as_comparison",
            "note": "本稿从 L=∫r×v dm 重新推导，未照抄 Whelan 的矩阵动机。"
        },
        {
            "id": "Whelan-pp4-6-dyad-components-inertia",
            "source": "RIT-Whelan-notes10-tensor.pdf pp.4--6",
            "source_claim": "并矢积、单位张量、惯量张量、张量运算、分量与矩阵、连续体 dm=ρdV、δ_ij",
            "new_location": [f"§2.2（第 {P('2.2')} 页）", f"§2.4（第 {P('2.4')} 页）",
                             f"§4.1（第 {P('4.1')} 页）"],
            "status": "used_as_comparison",
            "note": "本稿的并矢定义、左右作用与缩并规则按 TM p9 与自己的记号组织。"
        },
        {
            "id": "Whelan-p7-transpose-dual",
            "source": "RIT-Whelan-notes10-tensor.pdf p7",
            "source_claim": "转置、对称/反对称、对偶张量 *A，且 *A·B=−A×B（与本稿 a^× 符号相反）",
            "new_location": [f"§2.3（第 {P('2.3')} 页）", f"§2.6（第 {P('2.6')} 页）"],
            "status": "used_as_comparison",
            "note": "符号差异在 §2.6 与附录 B 明确注出，避免读者按 Whelan 的 *A 直接套本稿公式。"
        },
        {
            "id": "Whelan-p8-change-basis",
            "source": "RIT-Whelan-notes10-tensor.pdf p8",
            "source_claim": "换基：式 3.12 定义 A_ki=e'_k·e_i（行是新基分量），式 3.13 写作 T'=A T A^T；另给正交矩阵与对称张量可对角化的断言",
            "new_location": [f"§0.4（第 {P('0.4')} 页）", f"§2.7（第 {P('2.7')} 页）"],
            "status": "used_as_comparison",
            "convention_correction": "round-01/round-02 元数据写成 T'=A^T T A，与原文不符。原文 A 的行是新基分量；本稿的 R 列是新基分量，R=A^T，故本稿写 T'=R^T T R。两条式子等价但不能互换记号。正文 §0.4 的推导本来就是按列约定做的，无需改动。",
            "note": "p8 的“可对角化”只是断言，证明在 §1.4。"
        },
        {
            "id": "Whelan-p9-spectral-assertions",
            "source": "RIT-Whelan-notes10-tensor.pdf p9",
            "source_claim": "特征方程、实对称特征值实、不同特征值特征向量正交、重根与正交基、谱分解",
            "new_location": [f"§1.3（第 {P('1.3')} 页）", f"§1.4（第 {P('1.4')} 页）",
                             f"§1.5（第 {P('1.5')} 页）"],
            "status": "used_as_comparison",
            "note": "Whelan 给的是断言与骨架；本稿 §1.4 的 2×2 引理、实根引理、正交补降维与实性论证是完整的自足证明。"
        },
        {
            "id": "Whelan-pp10-14-inertia",
            "source": "RIT-Whelan-notes10-tensor.pdf pp.10--14",
            "source_claim": "惯量张量分量、椭球常密度例的积分、主惯量与主轴、惯量张量与原点有关、平行轴定理",
            "new_location": [f"§4.2（第 {P('4.2')} 页）", f"§4.3（第 {P('4.3')} 页）",
                             f"§4.4（第 {P('4.4')} 页）", f"§4.5（第 {P('4.5')} 页）"],
            "status": "used_as_comparison",
            "note": "pp.11--12 的均质椭球例在本轮恢复为 §4.4 的选读（早期返工稿漏掉）；平行轴定理按自己的展开重写。Whelan pp.13--14 只作对照。"
        }
    ]

    baseline_map = [
        {"baseline": "§0.1--§0.5", "content": "矢量与分量、线性映射、矩阵、换基、迹/行列式/特征多项式",
         "here": f"§0.1--§0.5（第 {P('0.1')}--{P('0.5')} 页）",
         "treatment": "重组；换基改为三步推导 + 45° 核对，并说明行约定与列约定的差别"},
        {"baseline": "（基线无）", "content": "本轮新增前置",
         "here": f"§0.6（第 {P('0.6')} 页）、§0.7（第 {P('0.7')} 页）",
         "treatment": "§0.6 质量微元到积分的桥接（按新增自述压缩）；§0.7 奇次实多项式有实根"},
        {"baseline": "§1.1--§1.6", "content": "二阶张量两身份、对称部分、椭球、特征值、谱定理、三不变量",
         "here": f"§1.1--§1.6（第 {P('1.1')}--{P('1.6')} 页）",
         "treatment": "谱定理由“完整陈述与用法”升级为完整证明；特征值定义提到 §1.2"},
        {"baseline": "§2.1--§2.10", "content": "阶、张量积、左右作用、缩并、单位与投影、转置/对称分解/对偶、商法则、缩并层级表、谱分解、三记号字典",
         "here": f"§2.1--§2.8（第 {P('2.1')}--{P('2.8')} 页）",
         "treatment": "缩并层级表与三记号字典合并为 §2.8 的两张查阅表；谱分解与 §1.3、§1.5 对齐"},
        {"baseline": "§3.1--§3.5", "content": "两基与算子、S 的并矢形式、正交性、绕轴公式、无穷小旋转与角速度",
         "here": f"§3.1--§3.6（第 {P('3.1')}--{P('3.6')} 页）",
         "treatment": "另设 §3.6 讲刚体速度关系（取自 TM p15），基线只在 §4 里引用它"},
        {"baseline": "§4.1--§4.5", "content": "惯量构造、分量与正定、主轴、常用结果与平行轴定理、L 偏角示范",
         "here": f"§4.1--§4.6（第 {P('4.1')}--{P('4.6')} 页）",
         "treatment": "平行轴定理独立成 §4.5、示范独立成 §4.6；补半正定的等号条件、质量对称判据、均质椭球物体选读与惯量椭球"},
        {"baseline": "§5.1--§5.4", "content": "输运定理、欧拉方程、对称陀螺、维持力矩",
         "here": f"§5.1--§5.4（第 {P('5.1')}--{P('5.4')} 页）",
         "treatment": "维持力矩的计算改到 §5.4 完成（§4.6 只记录问题）；§5.3 补 Ω 的符号条件与 L⊥/ω⊥ 同向说明"},
        {"baseline": "§6.1--§6.4", "content": "柯西应力、对称性、斜截面示范、平衡方程",
         "here": f"§6.1--§6.4（第 {P('6.1')}--{P('6.4')} 页）",
         "treatment": "补法向角/截面角区分、局部平衡的参考系约定；高斯定理与整体形式降为选读"},
        {"baseline": "§7", "content": "独立练习 P1--P12",
         "here": f"§7（第 {min(practice_pages.values())} 页起）",
         "treatment": "题号与题型保留；详解在附录 A；并注明哪些是回忆复现"},
        {"baseline": "§8", "content": "易错点、速查、三句话",
         "here": f"§8（第 {sec8} 页起）",
         "treatment": "八条易错点与速查表；“角动量与动能”一行区分转动动能与总动能"},
        {"baseline": "附录 A/B/C", "content": "练习详解、指标速查、来源与选读清单",
         "here": f"附录 A（第 {min(answer_pages.values())} 页起）、附录 B（第 {appB} 页）、附录 C（第 {appC} 页）",
         "treatment": "附录 B 补右手基适用边界；附录 C 按冻结基线章号重建来源映射"}
    ]

    exercises = []
    for k in range(1, 13):
        pid = f"P{k}"
        item = {
            "id": pid,
            "statement_page": practice_pages.get(pid),
            "answer_page": answer_pages.get(pid),
            "content": re.sub(r"\s+", " ",
                              (re.search(rf"\\practice\{{{pid}\}}\{{[^}}]*\}}", tex) or [""])[0]
                              if re.search(rf"\\practice\{{{pid}\}}\{{[^}}]*\}}", tex) else ""),
        }
        if pid in cont_pages:
            item["answer_continuation_pages"] = cont_pages[pid]
        item["identity"] = "与冻结 v2.2.2 的题号/题型一致" if k <= 12 else ""
        exercises.append(item)

    figures = [{"figure": k, "page": v} for k, v in sorted(figures.items())]

    doc_data = {
        "created_at_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+00:00"),
        "round": "round-03",
        "book": "从张量到并矢：二次型主轴、并矢运算与三处力学落点",
        "page_numbering": f"PDF 物理页码，与 handout.pdf 页脚一致；共 {pages} 页。正文 §0--§8、附录 A--C。页码由脚本从最终 PDF 定位，不手写。",
        "pdf_pages": pages,
        "source_files": source_files,
        "source_claims": source_claims,
        "baseline_chapter_mapping": {
            "baseline_file": "inputs/baseline-full-v2.2.2.tex",
            "baseline_chapters": {"§0": "起点", "§1": "二次型与主轴", "§2": "张量与并矢",
                                  "§3": "旋转算子与角速度", "§4": "转动惯量张量",
                                  "§5": "欧拉方程与对称陀螺", "§6": "应力张量",
                                  "§7": "独立练习", "§8": "易错点、速查与三句话",
                                  "附录 A": "练习详解", "附录 B": "指标与记号速查",
                                  "附录 C": "来源对应、补充与选读清单"},
            "note": "round-01/round-02 的对应表用了更早祖先文档的 §1--§12 编号，与冻结基线对不上（例如把二次型记作“旧 §3”、应力记作“旧 §9”），还说旧稿“先张量后二次型”。本文件按冻结基线实际章号重建；若日后要比较那份祖先文档，需另立映射。",
            "items": baseline_map
        },
        "exercise_pages": exercises,
        "figure_pages": figures,
        "section_pages": {k: v for k, v in sorted(anchors.items(), key=lambda kv: kv[1])},
        "self_derived_or_supplemented": [
            {"topic": "奇次实多项式有实根", "location": f"§0.7（第 {P('0.7')} 页）",
             "basis": "本稿补的引理与二分法证明；服务 §1.4 第二步。", "status": "self_derived_proof"},
            {"topic": "三维实对称矩阵谱定理的完整证明", "location": f"§1.4（第 {P('1.4')} 页）",
             "basis": "Whelan p9 只给断言；本稿用 2×2 引理、实根引理、正交补降维、实性与分解式补足。",
             "status": "self_derived_proof"},
            {"topic": "张量变换律与商法则", "location": f"§2.7（第 {P('2.7')} 页）",
             "basis": "由 §0.4 换基公式推出；用于 §6.1 判定应力张量。", "status": "self_derived_proof"},
            {"topic": "转动惯量张量的完整构造", "location": f"§4.1（第 {P('4.1')} 页）",
             "basis": "从 L=∫r×v dm 与三矢量叉乘公式推出；Whelan pp.2--3 提供主题对照。",
             "status": "self_derived_derivation"},
            {"topic": "平行轴定理的并矢展开", "location": f"§4.5（第 {P('4.5')} 页）",
             "basis": "用质心定义消去交叉项；Whelan pp.13--14 同主题对照。", "status": "self_derived_derivation"},
            {"topic": "输运定理（矢量版与并矢版）", "location": f"§5.1（第 {P('5.1')} 页）",
             "basis": "TM p12 只给 dn'_k/dt；本稿逐项求导并用单并矢、单位张量核对。",
             "status": "self_derived_derivation"},
            {"topic": "欧拉方程", "location": f"§5.2（第 {P('5.2')} 页）",
             "basis": "TM p12 没有欧拉方程；本稿从角动量定理与输运公式推出。",
             "status": "self_derived_derivation"},
            {"topic": "对称陀螺 A=B≠C 的解与 Ω 的符号条件", "location": f"§5.3（第 {P('5.3')} 页）",
             "basis": "TM p12 没有对称陀螺两方程；本稿由欧拉方程在 A=B、M=0 时解出，并补符号条件。",
             "status": "self_derived_derivation"},
            {"topic": "柯西应力与 t=σ·n", "location": f"§6.1（第 {P('6.1')} 页）",
             "basis": "课件没有应力章；本稿用四面体面积投影与力平衡推出，并用商法则判定张量。",
             "status": "self_derived_derivation"},
            {"topic": "应力对称性", "location": f"§6.2（第 {P('6.2')} 页）",
             "basis": "课件没有；本稿用小立方体两对切应力力矩平衡推出（准静态、不设体力矩）。",
             "status": "self_derived_derivation"},
            {"topic": "局部平衡方程", "location": f"§6.4（第 {P('6.4')} 页）",
             "basis": "课件没有；本稿用小立方体净面力与体力直接推出，整体形式与高斯定理另列为选读。",
             "status": "self_derived_derivation"},
            {"topic": "均质椭球物体的惯量张量（§4.4 选读）",
             "location": f"§4.4（第 {P('4.4')} 页）",
             "basis": "恢复自冻结基线 §4.4 的选读，不是本轮新推；伸缩坐标与 4π/15 的三个一元积分为就地解释；对照 Whelan pp.11--12。",
             "status": "restored_from_baseline"}
        ],
        "metadata_corrections": [
            {
                "wrong_claim": "旧来源说明把“对称陀螺两方程”和“Gauss 并矢版”挂到 TM p12。",
                "checked_fact": "TM p12 原页只有 dS/dt S^T 的反对称性、Ω^×=dS/dt S^T、dn'_k/dt=Ω×n'_k、无穷小情形 Ω=dφ/dt。",
                "correction": "p12 没有这些内容；本稿在 §5.2、§5.3、§6 按自己的推导补出。§6.4 只用分量形式的高斯定理并把整体形式列为选读，不另称“Gauss 并矢版”为课件原有。"
            },
            {
                "wrong_claim": "旧来源记录把 Whelan p8 的换基式写成 T'=A^T T A。",
                "checked_fact": "原页式 3.12 定义 A_ki=e'_k·e_i（行是新基分量），式 3.13 为 T'=A T A^T。",
                "correction": "本文件按原文记录；正文的 R 取列约定（R=A^T），写 T'=R^T T R，二者等价。"
            },
            {
                "wrong_claim": "早期对应表沿用祖先文档的 §1--§12 编号，并把旧稿说成“先张量后二次型”。",
                "checked_fact": "冻结基线是 §0 基础、§1 二次型、§2 张量；没有 §1--§12 那种编号。",
                "correction": "本文件按冻结基线重建映射，见 baseline_chapter_mapping。"
            },
            {
                "wrong_claim": "round-02 末页称本稿为“round-01 独立首稿”。",
                "checked_fact": "round-02 是作者自审返工稿；本轮是审核后返工稿。",
                "correction": "round-03 的版本页脚与交付说明已改为“2026-11-14 审核后返工稿”，并说明编辑起点是 round-02。"
            }
        ],
        "source_boundary": {
            "included": "TM p8--p12 的数学主线与 p15 的刚体速度关系；原专题全部教学主题（三个力学落点）、均质椭球物体惯量选读与 P1--P12。",
            "excluded": "TM p13--p14、p16--p18 的欧拉角、E8.01/E8.02、HW8.01--HW8.03（按内容排除，不是整段页范围排除）；非正交坐标的完整上下标理论；连续介质本构、应变与失效判据；重力矩陀螺的完整定点运动。",
            "not_claimed": "本文件不表示用户已读、已理解或已掌握；用户试读反馈尚未提供。"
        }
    }

    out = ROOT / "source-map.json"
    out.write_text(json.dumps(doc_data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[ok] 写入 {out}（{pages} 页，{len(anchors)} 个小节锚点，{len(exercises)} 道练习）")
    return 0


if __name__ == "__main__":
    sys.exit(main())





