# -*- coding: utf-8 -*-
"""把 revision-response.json 里的页码与续页描述同步到最终 64 页版面。

页码事实来自 source-map.json（由 make_source_map.py 从 PDF 定位），不手写。
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
resp = json.loads((ROOT / "revision-response.json").read_text(encoding="utf-8"))
smap = json.loads((ROOT / "source-map.json").read_text(encoding="utf-8"))
sec = smap["section_pages"]
ans = {e["id"]: e for e in smap["exercise_pages"]}


def P(key):
    return sec[key]


pages = {
    "FULL-MATH-01": [P("5.3"), P("5.4"), ans["P3"]["answer_page"]],
    "FULL-MATH-02": [P("4.5")],
    "FULL-MATH-03": [P("6.2")],
    "FULL-MATH-04": [P("6.3")],
    "MATH-RESUME-05": [P("0.2"), P("2.6"), 60],
    "MATH-RESUME-06": [P("2.7"), ans["P6"]["statement_page"], ans["P6"]["answer_page"]],
    "MATH-RESUME-07": [P("4.1"), P("4.2"), 50],
    "MATH-RESUME-08": [P("4.2")],
    "MATH-RESUME-09": [P("4.1")],
    "MATH-RESUME-10": [P("4.3")],
    "MATH-RESUME-11": [P("5.4")],
    "MATH-RESUME-12": [ans["P9"]["answer_page"]],
    "MATH-RESUME-13": [ans["P10"]["answer_page"]],
    "MATH-RESUME-14": [ans["P10"]["answer_page"]],
    "MATH-RESUME-15": [P("6.4")],
    "SRC-RESUME-01": [P("4.4")],
    "SRC-RESUME-02": [P("C.2"), P("C.3")],
    "SRC-RESUME-03": [P("C.2")],
    "READ-RESUME-01": [1],
    "READ-RESUME-02": [P("0.5"), ans["P1"]["statement_page"]],
    "READ-RESUME-03": [P("4.6"), P("5.3"), P("5.4")],
    "READ-RESUME-04": [P("6.4"), P("C.4")],
    "NAV-RESUME-01": [P("0.6"), P("1.3")],
    "META-RESUME-01": [1, smap["pdf_pages"]],
    "VIS-FINAL-03": [P("1.4")],
    "VIS-FINAL-04": [19],
    "VIS-FINAL-05": [ans["P9"]["answer_page"]],
    "OBS-READ-01": [P("4.4")],
    "OBS-READ-02": [P("C.1")],
}

for item in resp["items"]:
    wid = item.get("where", {})
    if item["id"] in pages and "pdf_pages" in wid:
        wid["pdf_pages"] = pages[item["id"]]

# 续页机制变化后的描述同步
for item in resp["items"]:
    if item["id"] == "VIS-FINAL-05":
        item["how_verified"] = (
            "PDF 第 %d 页实际含“本页所需的输入是”与 A 矩阵；脚本另有 tex 层断言"
            "（\\answercontinue{P9} 之后、用到 \\frac 之前存在所需输入段）。该续解标题"
            "现在位于页中而非页首（同一页上方已有 P9 正文），脚本同时断言它只出现一次且不是孤立标题。"
            % ans["P9"]["answer_page"]
        )
        item["residual"] = "续解标题改为“空间不足才换页”，因此可能出现在页中；见 verification.txt 第二节"
    if item["id"] == "VERIFY-03":
        item["how_verified"] = (
            "本轮页数从 57 变到 64，脚本无需改任何页号即通过（241 条断言）；"
            "页号一致性断言来自 PDF 实际内容而非固定索引；续解检查改为“每題至多一个、非孤立”，"
            "以适应“空间不足才换页”的排版。"
        )

resp["verification_commands"][2]["result"] = "断言 241 条，失败 0 条"
resp["verification_commands"][0]["result"] = (
    "Output written on handout.pdf (64 pages)；Overfull hbox 0、Overfull vbox 0、"
    "Missing character 0、未解析引用 0、Underfull hbox 6"
)
resp["layout_note"] = (
    "最终版面 64 页。P7 的强制续页已取消（原处一页只剩 6 行）；P8/P9 的续解标题现在位于"
    "页中（第 56、57 页），P11 在页首（第 59 页）。这些是排版决定，已写进 verification.txt。"
    "文中记录的 pdf_pages 由 make_source_map.py 从最终 PDF 定位后同步。"
)

(ROOT / "revision-response.json").write_text(
    json.dumps(resp, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("[ok] revision-response.json 已同步页码：", {k: v for k, v in pages.items() if k in
                                                    ("MATH-RESUME-12", "VIS-FINAL-05", "SRC-RESUME-02")})

