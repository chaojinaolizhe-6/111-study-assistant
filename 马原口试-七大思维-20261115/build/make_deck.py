# -*- coding: utf-8 -*-
"""生成‘马原口试·七个思维一台机器’PPT 的 PPTD 工程（大工红金版式，v2 修订）。"""
import os

ROOT = r"D:\aaa_D_usual\DSH\111学习助手\马原口试-七大思维-20261115\deck"
PAGES = os.path.join(ROOT, "pages")
os.makedirs(PAGES, exist_ok=True)

RED = "C6252A"
RED2 = "D74023"
INK = "2D241E"
SUB = "6B5744"
MUTED = "9A8468"
GOLD = "C9A227"
RULE = "D9C3A3"
CARD = "FFFAF1"
BORDER = "E6D3B6"
SOFT = "F7E9D2"
TAN = "B08A5E"

FONT = "{latin: Microsoft YaHei, ea: Microsoft YaHei, mac: PingFang SC, win: Microsoft YaHei}"
SERIF = "{latin: Georgia, ea: Microsoft YaHei, mac: PingFang SC, win: Microsoft YaHei}"

els = []


def esc(s):
    return s.replace("\\", "\\\\").replace('"', '\\"')


def T(eid, x, y, w, h, text, size, color, bold=False, align="left", lh=1.25, font=None):
    a = f"[{align}, top]" if align in ("center", "right") else "left"
    s = f"""  - elementId: {eid}
    elementType: text
    bounds: [{x}, {y}, {w}, {h}]
    content:
      text: "{esc(text)}"
      fontFamily: {font or FONT}
      fontSize: {size}
"""
    if bold:
        s += "      bold: true\n"
    s += f"""      color: "#{color}"
      lineHeight: {lh}
      align: {a}
"""
    els.append(s)


def R(eid, x, y, w, h, fill=None, border=None, shape="rect", bw=1):
    s = f"""  - elementId: {eid}
    elementType: shape
    bounds: [{x}, {y}, {w}, {h}]
    shapeName: {shape}
"""
    if fill:
        s += f"    fill: {{type: solid, color: \"#{fill}\"}}\n"
    if border:
        s += f"    border: {{width: {bw}, color: \"#{border}\"}}\n"
    else:
        s += f"    border: {{width: 0, color: \"#{fill or 'FFFFFF'}\"}}\n"
    els.append(s)


def page(fname, bg, notes, page_type="content"):
    body = "".join(els)
    els.clear()
    txt = f"""pageType: {page_type}
background: {{type: solid, color: "#F7EFE0"}}
notes: "{esc(notes)}"
elements:
  - elementId: bg
    elementType: image
    bounds: [0, 0, 960, 540]
    src: media/{bg}
    fit: {{mode: fill}}
""" + body
    with open(os.path.join(PAGES, fname), "w", encoding="utf-8") as f:
        f.write(txt)


def header(title, tag=""):
    R("tbar", 56, 42, 5, 26, RED2)
    T("title", 72, 40, 600, 32, title, 24, RED, bold=True)
    if tag:
        T("tag", 640, 46, 264, 16, tag, 9.5, MUTED, align="right")
    R("rule", 56, 80, 848, 1, RULE)


def footer(page_no, src=""):
    if src:
        T("src", 56, 505, 740, 12, src, 7.5, MUTED)
    T("pageno", 844, 505, 60, 12, page_no, 8.5, MUTED, align="right")


def progress(active):
    for i in range(4):
        R(f"pg{i}", 56 + i * 212, 90, 210, 3.5, RED if i == active else "E8DAC2")


# ================================================================ P1 封面
R("cover-bar", 80, 96, 4, 40, RED2)
T("kicker", 98, 96, 520, 16, "马克思主义基本原理 · 免试口试", 12, "A8845F")
T("main", 80, 132, 760, 68, "七个思维，一台机器", 50, RED, bold=True, lh=1.1)
T("sub", 80, 214, 660, 22, "从一条新能源汽车新闻，看马克思主义的方法论", 17, SUB)
R("subline", 80, 250, 120, 2, GOLD)
R("tagbox", 80, 276, 396, 34, RED, shape="roundRect")
T("tagtxt", 94, 285, 368, 20, "看热闹的人得到情绪，看结构的人得到判断", 12, "FFFDF7")
T("who", 80, 460, 560, 16, "汇报人：马泽宇　｜　物理学院　｜　2026 年 11 月", 11, SUB)
T("foot", 80, 484, 720, 14, "教材依据：《马克思主义基本原理》（2023 年版）第一章第三节", 8, MUTED)
page("01.page", "bg-cover.png",
     "封面。上台站定再翻页，不要念标题。开口第一句直接报数字：2025 年，中国新能源汽车产量 1662.6 万辆。",
     page_type="cover")

# ================================================================ P2 三个数字
header("三个数字", "0:00 – 0:30")
nums = [
    ("1662.6", "万辆 · 产量", "2025 年新能源汽车产量，连续 11 年全球第一", INK),
    ("50%", "国内销量占比", "每卖出两辆新车，就有一辆是新能源", INK),
    ("35.3%", "反补贴税最高档", "欧盟对华电动汽车加税，为期五年", RED2),
]
for i, (num, unit, label, color) in enumerate(nums):
    x = [56, 344, 632][i]
    T(f"n{i}", x, 140, 250, 48, num, 36, color, bold=True, lh=1.05)
    T(f"u{i}", x, 192, 250, 14, unit, 10, MUTED)
    R(f"nl{i}", x, 210, 56, 2, GOLD)
    T(f"l{i}", x, 220, 244, 52, label, 11.5, SUB, lh=1.6)
R("note-rule", 56, 316, 848, 1, "EADCC6")
T("readout", 56, 330, 848, 40,
  "同一年：产得越多，单台利润越薄；出口越猛，被围堵得越狠。", 15, INK, bold=True)
footer("02", "数据：中汽协 2026-01-14 发布；欧盟终裁 2024-10-29（新华网）。口播只报事实，不加评价。")
page("02.page", "bg-page.png",
     "三十秒讲三件事，每件一句，不解释。讲完停半拍再翻页，让数字落地。")

# ================================================================ P3 两种读法
R("band", 0, 148, 960, 214, INK)
T("btag", 80, 178, 300, 16, "同一个事实", 10, GOLD)
T("q1", 80, 200, 820, 56, "看热闹的人得到情绪；", 26, "FBF3E2", bold=True)
T("q2", 80, 258, 820, 56, "看结构的人得到判断。", 26, "FBF3E2", bold=True)
T("kicker2", 56, 92, 720, 34, "同一件事，两种读法", 22, RED, bold=True)
T("after", 56, 396, 848, 24, "差别不在信息，在思维——这就是为什么要把七个思维装成一台机器。", 14, SUB)
footer("03", "")
page("03.page", "bg-page.png",
     "念这两句，中间停两秒。这是全场的转轴：从新闻转到方法。")

# ================================================================ P4 四层机器
header("不是七个筐，是一台机器", "0:55 – 1:30")
rows = [
    ("认识层", "引擎", ["辩证思维", "历史思维"], "转得动"),
    ("结构层", "骨架", ["系统思维", "战略思维"], "立得住"),
    ("动力层", "动力", ["创新思维"], "走多远"),
    ("边界层", "护栏", ["法治思维", "底线思维"], "不翻车"),
]
for i, (layer, role, chips, cap) in enumerate(rows):
    y = 100 + i * 84
    R(f"row{i}", 56, y, 848, 72, CARD, BORDER, shape="roundRect")
    R(f"acc{i}", 56, y + 6, 4, 60, RED2 if i % 2 == 0 else GOLD)
    T(f"lay{i}", 78, y + 14, 110, 18, layer, 13, RED, bold=True)
    T(f"role{i}", 78, y + 36, 110, 16, role, 10, MUTED)
    for j, c in enumerate(chips):
        x = 196 + j * 168
        R(f"chip{i}{j}", x, y + 18, 152, 36, SOFT, BORDER, shape="roundRect")
        T(f"chipt{i}{j}", x, y + 27, 152, 20, c, 13.5, INK, bold=True, align="center")
    T(f"cap{i}", 760, y + 26, 128, 18, cap, 11.5, SUB, align="right")
T("note4", 56, 452, 848, 20,
  "四个问题有先后：没有引擎转不动，没有骨架立不住，没有护栏会翻车。", 13, SUB)
footer("04", "教材：第一章第三节「学习掌握唯物辩证法，不断增强思维能力」")
page("04.page", "bg-page.png",
     "先报四层名字，再讲元论证：认识一件事要依次回答四个问题——什么矛盾、从哪来、连着谁、哪里停。")

# ================================================================ P5–P11 七个思维
rows7 = [
    dict(no="01", name="辩证思维", layer="认识层 · 引擎", active=0,
         principle="对立统一规律：矛盾是事物发展的根本动力。",
         ask="“卖得好”和“被围堵”，是不是同一个矛盾的两面？",
         act="承认矛盾 → 分析矛盾 → 解决矛盾：先找主要矛盾，再压资源。",
         src="教材：第一章第二节「对立统一规律」；案例：出口增长与反补贴税同期发生。",
         notes="原理只念一句，立刻发问，停两秒。再给三步动作，不展开。"),
    dict(no="02", name="历史思维", layer="认识层 · 引擎", active=0,
         principle="社会存在决定社会意识，生产力决定生产关系。",
         ask="这条产业，现在走到第几阶段？",
         act="搞清阶段：别用第二阶段的办法，去打第三阶段的仗。",
         src="教材：第三章第一节「社会存在与社会意识」；案例：市场换技术 → 合资跟随 → 换道超车。",
         notes="三个阶段快速点名，重点落在“我在第几阶段”这个自问上。"),
    dict(no="03", name="系统思维", layer="结构层 · 骨架", active=1,
         principle="联系的普遍性：要素、结构、功能、环境，缺一不可。",
         ask="动一个环节，别处哪里会疼？",
         act="先画图，再动手：充电桩、电网、退役电池不是副作用，是系统的必然输出。",
         src="教材：第一章第二节「联系的普遍性、整体与部分」；系统思维名称非教材原生，材料由本节调取。",
         notes="先讲整体大于部分之和，再讲动一环疼一片。最后一句方法论：先画图，再动手。"),
    dict(no="04", name="战略思维", layer="结构层 · 骨架", active=1,
         principle="主要矛盾决定主攻方向；尊重规律与发挥能动性相统一。",
         ask="资源该压在哪一个方向上？",
         act="敢做取舍：放弃追了百年的内燃机，把资源压到刚起步的电池与电驱。",
         src="教材：第一章「主要矛盾」＋第二章「规律与能动性」；案例：换道超车。",
         notes="战略思维不是看得远，是看得远之后敢把资源压上去。这句必须重读。"),
    dict(no="05", name="创新思维", layer="动力层 · 动力", active=2,
         principle="辩证否定观：新事物对旧事物的否定是扬弃。",
         ask="哪些要保留，哪些要否定？",
         act="不是推倒重来：电动车保留汽车的全部功能，否定的是内燃机这条技术路线。",
         src="教材：第一章「否定之否定」＋第二章第三节「理论与实践创新」；案例：磷酸铁锂 → 三元 → 固态。",
         notes="这一条最容易被讲成“颠覆”。一定要说清“有保留的否定”，这是得分点。"),
    dict(no="06", name="法治思维", layer="边界层 · 护栏", active=3,
         principle="经济基础决定上层建筑，上层建筑反作用于经济基础。",
         ask="规则把竞争优势重新定义了一遍，这场仗你打不打？",
         act="应诉、举证、谈判、反制：规则不是背景，规则就是竞争力。",
         src="教材：第三章「上层建筑」＋第六章「社会主义法治」；案例：欧盟反补贴税五年期。",
         notes="先纠偏：法治思维不等于“要依法办事”。它的锚点在上层建筑反作用。"),
    dict(no="07", name="底线思维", layer="边界层 · 护栏", active=3,
         principle="质量互变规律：过了度，性质就变了。",
         ask="最坏的情况，你算清了吗？",
         act="三条线不能碰：技术底线、产能底线、安全底线。",
         src="教材：第一章第二节「质量互变」；案例：关键环节、全行业亏损、电池与数据安全。",
         notes="底线思维不是悲观，是先把最坏情况摆上桌再决定走不走。收在这里最稳。"),
]

PX, PW = 596, 308
CXI = PX + 22
CWD = PW - 44

for idx, d in enumerate(rows7):
    header(d["name"], d["layer"])
    progress(d["active"])
    T("no", 56, 98, 60, 22, d["no"], 12, RED2, bold=True)
    T("plabel", 56, 128, 40, 12, "原理", 9.5, MUTED)
    T("principle", 96, 124, 466, 46, d["principle"], 16.5, INK, bold=True, lh=1.35)
    R("hr1", 56, 178, 506, 1, "EADCC6")
    T("asklabel", 56, 190, 40, 12, "问", 9.5, MUTED)
    T("ask", 96, 186, 466, 56, d["ask"], 16, RED, lh=1.4)
    R("hr2", 56, 250, 506, 1, "EADCC6")
    T("actlabel", 56, 262, 40, 12, "动", 9.5, MUTED)
    T("act", 96, 258, 466, 72, d["act"], 12.5, SUB, lh=1.65)

    R("panel", PX, 96, PW, 320, CARD, BORDER, shape="roundRect")

    if idx == 0:
        R("ca", CXI, 140, CWD, 42, SOFT, BORDER, shape="roundRect")
        T("cta", CXI, 150, CWD, 20, "卖得好　·　产能与价格优势", 11, INK, align="center")
        R("ln1", CXI + CWD / 2 - 1, 186, 2, 22, RULE)
        R("cc", CXI + 34, 210, CWD - 68, 52, RED, shape="roundRect")
        T("cct", CXI + 34, 226, CWD - 68, 22, "同一个矛盾", 12.5, "FFFDF7", bold=True, align="center")
        R("ln2", CXI + CWD / 2 - 1, 266, 2, 22, RULE)
        R("cb", CXI, 292, CWD, 42, SOFT, BORDER, shape="roundRect")
        T("ctb", CXI, 302, CWD, 20, "被围堵　·　反补贴税与壁垒", 11, INK, align="center")
        T("cap", CXI, 366, CWD, 40, "两面同时成立，才叫对立统一。", 10, SUB, align="center", lh=1.5)
    elif idx == 1:
        steps = [("换道超车", "第三阶段", 158), ("合资跟随", "第二阶段", 222), ("市场换技术", "第一阶段", 286)]
        for k, (name, lb, y) in enumerate(steps):
            R(f"st{k}", CXI, y, CWD, 48, SOFT if k == 0 else CARD, BORDER, shape="roundRect")
            if k == 0:
                R("stfill", CXI, y + 4, 5, 40, RED2)
            T(f"stt{k}", CXI + 18, y + 8, CWD - 36, 18, name, 12.5, INK, bold=True)
            T(f"stl{k}", CXI + 18, y + 27, CWD - 36, 14, lb, 8.5, MUTED)
        T("cap", CXI, 372, CWD, 24, "阶段搞错，方法就全错。", 10, SUB, align="center")
    elif idx == 2:
        chain = ["锂 · 钴 · 镍", "电池 · 电机 · 电控", "整车", "充电网络", "电网与回收"]
        for k, node in enumerate(chain):
            y = 116 + k * 52
            R(f"nd{k}", CXI, y, CWD, 42, SOFT if k in (0, 4) else CARD, BORDER, shape="roundRect")
            T(f"ndt{k}", CXI + 14, y + 12, CWD - 28, 18, node, 11, INK)
            if k < 4:
                R(f"cl{k}", CXI + 16, y + 44, 2, 16, RULE)
        T("cap", CXI, 388, CWD, 20, "动一环，别处会疼。", 10, SUB, align="center")
    elif idx == 3:
        R("ar1", CXI, 140, CWD, 46, CARD, BORDER, shape="roundRect")
        T("ar1t", CXI, 153, CWD, 20, "内燃机　←　收", 12, SUB, align="center")
        T("arrow", CXI, 192, CWD, 20, "↓", 12, GOLD, align="center")
        R("ar2", CXI, 216, CWD, 46, SOFT, BORDER, shape="roundRect")
        T("ar2t", CXI, 229, CWD, 20, "电池 · 电驱　→　放", 12, INK, bold=True, align="center")
        R("pill", CXI + 34, 292, CWD - 68, 40, RED, shape="roundRect")
        T("pillt", CXI + 34, 302, CWD - 68, 22, "取舍本身就是战略", 11, "FFFDF7", bold=True, align="center")
        T("cap", CXI, 356, CWD, 44, "放弃追了百年的曲线，压到刚起步的曲线。", 10, SUB, align="center", lh=1.5)
    elif idx == 4:
        R("sp1", CXI, 128, CWD, 44, CARD, BORDER, shape="roundRect")
        T("sp1t", CXI, 140, CWD, 18, "旧事物：内燃机路线", 11, SUB, align="center")
        T("spm", CXI, 178, CWD, 18, "↓　扬弃", 10, RED2, align="center")
        R("sp2", CXI, 204, CWD, 44, SOFT, BORDER, shape="roundRect")
        T("sp2t", CXI, 216, CWD, 18, "保留：交通工具的全部功能", 11, INK, align="center")
        R("sp3", CXI, 258, CWD, 44, CARD, BORDER, shape="roundRect")
        T("sp3t", CXI, 270, CWD, 18, "否定：技术路线与能源形式", 11, INK, align="center")
        T("cap", CXI, 366, CWD, 44, "不是推倒重来：保留合理的，抛弃过时的。", 10, SUB, align="center", lh=1.5)
    elif idx == 5:
        R("ra", CXI, 138, 118, 74, CARD, BORDER, shape="roundRect")
        T("rat", CXI, 160, 118, 24, "规则", 14, INK, bold=True, align="center")
        R("rb", CXI + CWD - 118, 138, 118, 74, CARD, BORDER, shape="roundRect")
        T("rbt", CXI + CWD - 118, 160, 118, 24, "竞争", 14, INK, bold=True, align="center")
        T("two", CXI + 118, 158, CWD - 236, 30, "⇄", 20, RED2, bold=True, align="center")
        T("capx", CXI, 228, CWD, 44, "法律把经济关系固定下来，\n竞争因此有了可预期的边界。", 10, SUB, align="center", lh=1.5)
        R("pill5", CXI + 34, 292, CWD - 68, 40, RED, shape="roundRect")
        T("pill5t", CXI + 34, 302, CWD - 68, 22, "规则就是竞争力", 11, "FFFDF7", bold=True, align="center")
        T("cap", CXI, 352, CWD, 40, "应诉、举证、谈判、反制：功夫全在规则里。", 9.5, SUB, align="center", lh=1.5)

    else:
        T("rlab", CXI, 160, CWD, 18, "三条线，一条都不能碰", 10, MUTED, align="center")
        for k, (lab, pos) in enumerate([("技术", 0.18), ("产能", 0.50), ("安全", 0.82)]):
            x = CXI + CWD * pos
            R(f"tk{k}", x - 1.5, 206, 3, 64, RED2)
            T(f"tkl{k}", x - 38, 184, 76, 18, lab, 11, RED2, bold=True, align="center")
            T(f"tkd{k}", x - 38, 280, 76, 16, "不能碰", 8.5, MUTED, align="center")
        R("ruler", CXI, 272, CWD, 3, TAN)
        T("rlab2", CXI, 310, CWD, 18, "度以内：量变　｜　过了度：质变", 9.5, MUTED, align="center")
        T("cap", CXI, 352, CWD, 40, "先把最坏情况摆上桌，再决定走不走。", 10, SUB, align="center", lh=1.5)

    footer(f"{idx + 5:02d}", d["src"])
    page(f"{idx + 5:02d}.page", "bg-page.png", d["notes"])

# ================================================================ P12 三个判断
header("三个判断", "6:20 – 7:00")
judg = [
    ("01", "趋势", "这是产业升级的必经关口，不是终点。", "回扣第一个数字：产量还在涨。"),
    ("02", "风险", "真正的风险不在关税，在利润与技术代差。", "回扣第三个数字：35.3% 只是症状。"),
    ("03", "抓手", "短期靠规则应诉，长期靠创新与系统配套。", "机器四层，每一层都要有动作。"),
]
for i, (no, name, line, why) in enumerate(judg):
    y = 108 + i * 118
    T(f"jn{i}", 56, y + 6, 60, 26, no, 15, RED2, bold=True)
    T(f"jt{i}", 116, y, 140, 30, name, 20, RED, bold=True)
    T(f"jl{i}", 116, y + 34, 660, 22, line, 13.5, INK)
    T(f"jw{i}", 116, y + 60, 660, 18, why, 10, MUTED)
    if i < 2:
        R(f"jr{i}", 56, y + 96, 848, 1, "EADCC6")
footer("12", "")
page("12.page", "bg-page.png",
     "三个判断一句话一个，中间留半拍。落点：同一件事，看热闹的人得到情绪，看结构的人得到判断。")

# ================================================================ P13 收束
T("l1", 56, 140, 848, 20, "世界观　→　方法论　→　思维能力", 13, MUTED, align="center")
T("big1", 56, 182, 848, 54, "机器转起来，", 34, RED, bold=True, align="center")
T("big2", 56, 230, 848, 54, "才叫思维能力。", 34, RED, bold=True, align="center")
R("cl", 400, 304, 160, 2, GOLD)
T("l2", 120, 326, 720, 48, "七个不是七选一，也不是七张并列的清单——\n是一台有依赖关系的机器。",
  13, SUB, align="center", lh=1.6)
footer("13", "")
page("13.page", "bg-page.png", "这句说完就停。不要补话，不要解释，等老师示意。")

# ================================================================ P14 谢谢
T("end1", 80, 150, 560, 20, "总结与致谢", 12, "A8845F")
T("end2", 76, 184, 640, 80, "THANK YOU", 52, RED, bold=True, font=SERIF)
R("endbar", 80, 286, 420, 38, RED, shape="roundRect")
T("endbt", 96, 295, 388, 20, "看结构的人，得到判断", 14, "FFFDF7", bold=True)
T("end3", 80, 342, 640, 20, "七个思维，一台机器：从一条新闻，到一套方法。", 12.5, SUB)
T("who2", 80, 464, 560, 16, "汇报人：马泽宇　｜　物理学院　｜　2026 年 11 月", 10.5, SUB)
page("14.page", "bg-cover.png", "备用页。不讲话，等老师示意。", page_type="closing")

# ================================================================ P15 附录
header("附录：七个思维 × 原理锚点 × 案例镜头", "被追问时翻回")
for name, x, w in [("思维", 72, 130), ("原理锚点", 210, 350), ("案例镜头", 566, 330)]:
    T(f"h_{name}", x, 98, w, 16, name, 9.5, MUTED)
R("hrule", 56, 118, 848, 1, GOLD)
table = [
    ("辩证", "对立统一规律；两点论与重点论", "卖得好与被围堵是同一矛盾两面"),
    ("历史", "社会存在决定社会意识", "市场换技术 → 跟随 → 换道超车"),
    ("系统", "联系的普遍性；整体与部分", "锂钴镍—电池电控—整车—充电—回收"),
    ("战略", "主要矛盾定主攻；规律与能动性", "放弃内燃机追赶，压到电池电驱"),
    ("创新", "辩证否定＝扬弃", "磷酸铁锂、三元、固态的路线之争"),
    ("法治", "上层建筑反作用于经济基础", "欧盟反补贴税：规则重定义竞争"),
    ("底线", "质量互变；可能性与现实性", "技术、产能、安全三条线不能碰"),
]
for i, (a, b, c) in enumerate(table):
    y = 126 + i * 50
    if i % 2 == 0:
        R(f"zr{i}", 56, y, 848, 46, "FBF1E0")
    T(f"za{i}", 72, y + 12, 120, 20, a, 12.5, RED, bold=True)
    T(f"zb{i}", 210, y + 13, 340, 20, b, 10.5, INK)
    T(f"zc{i}", 566, y + 13, 330, 20, c, 10.5, SUB)
footer("15", "所有条目对应 2023 年版教材章节；口播时不报章节号，只说原理。")
page("15.page", "bg-page.png", "附录不计时。只在需要证明“七维齐、原理准”时翻回来。")

lines = ["version: v2", "title: 马原口试·七个思维一台机器", "size: [960, 540]", "pages:"]
for i in range(1, 16):
    lines.append(f"  - pages/{i:02d}.page")
with open(os.path.join(ROOT, "deck.pptd"), "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")
print("pages written:", len(os.listdir(PAGES)))




