# -*- coding: utf-8 -*-
"""马原口试 PPT · v2：七维每页加「机制链 + 判据 + 常见误读」，红金版式不变。"""
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
        T("tag", 620, 46, 284, 16, tag, 9.5, MUTED, align="right")
    R("rule", 56, 80, 848, 1, RULE)


def footer(page_no, src=""):
    if src:
        T("src", 56, 510, 760, 12, src, 7.5, MUTED)
    T("pageno", 844, 508, 60, 12, page_no, 8.5, MUTED, align="right")


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
     "封面。站定再翻页，不念标题。开口第一句直接报数字：2025 年，中国新能源汽车产量 1662.6 万辆。",
     page_type="cover")

# ================================================================ P2 三个数字
header("三个数字", "0:00 – 0:20")
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
    T(f"l{i}", x, 220, 250, 52, label, 11.5, SUB, lh=1.6)
R("note-rule", 56, 300, 848, 1, "EADCC6")
T("readout", 56, 314, 848, 40,
  "同一年：产得越多，单台利润越薄；出口越猛，被围堵得越狠。", 15, INK, bold=True)
T("readout2", 56, 352, 848, 30,
  "这不是两条新闻，是同一个矛盾的两面——下面用七个思维，把它拆开。", 11.5, SUB)
footer("02", "数据：中汽协 2026-01-14 发布；欧盟终裁 2024-10-29（新华网）。口播只报事实，不加评价。")
page("02.page", "bg-page.png",
     "二十五秒讲三件事，每件一句，不解释。最后一句要递到下一页去。")

# ================================================================ P3 两种读法
R("band", 0, 140, 960, 200, INK)
T("btag", 80, 168, 300, 16, "同一个事实", 10, GOLD)
T("q1", 80, 190, 820, 56, "看热闹的人得到情绪；", 26, "FBF3E2", bold=True)
T("q2", 80, 246, 820, 56, "看结构的人得到判断。", 26, "FBF3E2", bold=True)
T("kicker2", 56, 88, 720, 34, "同一件事，两种读法", 22, RED, bold=True)
T("after", 56, 372, 848, 24, "差别不在信息，在思维——把七个思维装成一台机器，才有结构。", 14, SUB)
footer("03", "")
page("03.page", "bg-page.png",
     "念这两句，中间停两秒。这是全场的转轴：从新闻转到方法。")

# ================================================================ P4 四层机器
header("不是七个筐，是一台机器", "0:32 – 0:50")
rows = [
    ("认识层", "引擎", ["辩证思维", "历史思维"], "转得动", "是什么矛盾 · 从哪来"),
    ("结构层", "骨架", ["系统思维", "战略思维"], "立得住", "连着谁 · 往哪压"),
    ("动力层", "动力", ["创新思维"], "走多远", "怎么变"),
    ("边界层", "护栏", ["法治思维", "底线思维"], "不翻车", "怎么固化 · 哪里停"),
]
for i, (layer, role, chips, cap, what) in enumerate(rows):
    y = 96 + i * 82
    R(f"row{i}", 56, y, 848, 70, CARD, BORDER, shape="roundRect")
    R(f"acc{i}", 56, y + 6, 4, 58, RED2 if i % 2 == 0 else GOLD)
    T(f"lay{i}", 76, y + 12, 110, 18, layer, 13, RED, bold=True)
    T(f"role{i}", 76, y + 34, 110, 14, role, 10, MUTED)
    T(f"what{i}", 76, y + 48, 130, 14, what, 7.5, MUTED)
    for j, c in enumerate(chips):
        x = 214 + j * 168
        R(f"chip{i}{j}", x, y + 17, 152, 36, SOFT, BORDER, shape="roundRect")
        T(f"chipt{i}{j}", x, y + 26, 152, 20, c, 13.5, INK, bold=True, align="center")
    T(f"cap{i}", 760, y + 25, 128, 18, cap, 11.5, SUB, align="right")
T("note4", 56, 440, 848, 20,
  "四个问题有先后：没有引擎转不动，没有骨架立不住，没有护栏会翻车。", 13, SUB)
T("note4b", 56, 462, 848, 18,
  "教材第一章原生五种；系统思维从第一章第二节调，法治思维从第三章、第六章调。", 9.5, MUTED)
footer("04", "教材：第一章第三节第二目「学习掌握唯物辩证法，不断增强思维能力」")
page("04.page", "bg-page.png",
     "二十秒：四个问题依次回答——什么矛盾、从哪来、连着谁、哪里停。最后一句点明教材只原生讲了五种，另两种是跨章调取的，这句话本身就是加分项。")

# ================================================================ P5–P11 七个思维
rows7 = [
    dict(no="01", name="辩证思维", layer="认识层 · 引擎", active=0, span="0:50 – 1:35",
         principle="对立统一规律：矛盾是事物发展的根本动力。",
         ask="“卖得好”和“被围堵”，是不是同一个矛盾的两面？",
         chain=["能力上升打破旧均衡", "对手存量被挤压", "反制成为必然"],
         criterion="看对立的两面，是否互为存在条件。",
         myth="只讲“有利有弊”，不讲“利怎么变成弊”。",
         src="教材：第一章第二节「对立统一规律」；案例：出口增长与反补贴税同期发生。",
         quote="教材原句：矛盾是事物发展的根本动力，要坚持两点论与重点论。",
         guard="防守：常识看到利弊并存，辩证法算的是优势向阻力的转化。",
         notes="十秒原理，二十秒机制，十五秒判据。"),
    dict(no="02", name="历史思维", layer="认识层 · 引擎", active=0, span="1:35 – 2:20",
         principle="社会存在决定社会意识，生产力决定生产关系。",
         ask="这条产业，现在走到第几阶段？",
         chain=["早期的技术选择", "形成路径锁定", "限定今天的选择空间"],
         criterion="看它是周期波动，还是不可逆的范式转移。",
         myth="把时间线当历史思维：列大事记不等于看规律。",
         src="教材：第三章第一节「社会存在与社会意识」；案例：市场换技术 → 合资跟随 → 换道超车。",
         quote="教材原句：社会存在决定社会意识，生产力决定生产关系。",
         guard="防守：复盘只讲过去成败，历史思维是给当下定坐标。",
         notes="三阶段各一句话带过；重点落在“周期还是拐点”这个判断上。"),
    dict(no="03", name="系统思维", layer="结构层 · 骨架", active=1, span="2:20 – 3:05",
         principle="联系的普遍性：要素、结构、功能、环境，缺一不可。",
         ask="动一个环节，别处哪里会疼？",
         chain=["结构先决定分工", "各方各求自身最优", "合成出来整体次优"],
         criterion="问成本最终落在谁身上：不落在你身上，就落在系统里。",
         myth="把“全面”当系统：面面俱到不等于找到结构。",
         src="教材：第一章第二节「联系的普遍性、整体与部分」；系统思维名称非教材原生，材料由本节调取。",
         quote="教材原句（非原生）：整体居于主导地位，统率部分并具备新功能。",
         guard="防守：全局观是凭经验拍脑袋，系统思维算的是结构与反馈。",
         notes="先讲整体大于部分之和，再讲动一环疼一片。判据那句是全页最值钱的。"),
    dict(no="04", name="战略思维", layer="结构层 · 骨架", active=1, span="3:05 – 3:50",
         principle="主要矛盾决定主攻方向；尊重规律与发挥能动性相统一。",
         ask="资源该压在哪一个方向上？",
         chain=["规律划定可能区间", "能动性选定主攻", "以取舍换主动"],
         criterion="看它敢放弃什么：不敢放弃的，不叫战略。",
         myth="把“看得远”当战略：战略是敢放弃，不是敢想象。",
         src="教材：第一章「主要矛盾」＋第二章「规律与能动性」；案例：换道超车。",
         quote="教材原句：抓主要矛盾；尊重客观规律与发挥主观能动性相统一。",
         guard="防守：战略不是豪赌，是顺应规律前提下的极限聚焦。",
         notes="战略思维不是看得远，是看得远之后敢把资源压上去。这句必须重读。"),
    dict(no="05", name="创新思维", layer="动力层 · 动力", active=2, span="3:50 – 4:35",
         principle="辩证否定观：新事物对旧事物的否定是扬弃。",
         ask="哪些要保留，哪些要否定？",
         chain=["旧路线逼近极限", "功能被保留", "路线被替换"],
         criterion="看它否定的是一条路线，还是一个功能。",
         myth="把“改良”当创新：打补丁和换心脏不是一回事。",
         src="教材：第一章「否定之否定」＋第二章第三节「理论与实践创新」；案例：磷酸铁锂 → 三元 → 固态。",
         quote="教材原句：辩证的否定是扬弃，是联系与发展的环节。",
         guard="防守：改良在旧框架打补丁，扬弃是保留外壳换掉心脏。",
         notes="这一条最容易被讲成“颠覆”。一定要说清“有保留的否定”，这是得分点。"),
    dict(no="06", name="法治思维", layer="边界层 · 护栏", active=3, span="4:35 – 5:20",
         principle="经济基础决定上层建筑，上层建筑反作用于经济基础。",
         ask="规则把竞争优势重新定义了一遍，这场仗你打不打？",
         chain=["竞争格局变化", "规则被重写", "成本结构随之改变"],
         criterion="看这条规则，改的是成本，还是资格。",
         myth="把“依法办事”当法治思维：那是守法，不是思维。",
         src="教材：第三章「上层建筑」＋第六章「社会主义法治」；案例：欧盟反补贴税五年期。",
         quote="教材原句（非原生）：经济基础决定上层建筑，上层建筑具有反作用。",
         guard="防守：谈判算眼前得失，法治思维算的是规则话语权。",
         notes="先纠偏：法治思维不等于“要依法办事”。锚点在上层建筑反作用。"),
    dict(no="07", name="底线思维", layer="边界层 · 护栏", active=3, span="5:20 – 6:05",
         principle="质量互变规律：过了度，性质就变了。",
         ask="最坏的情况，你算清了吗？",
         chain=["量在持续积累", "越过临界点", "性质改变且不可逆"],
         criterion="底线不是“最坏结果”，是“不可逆的那一步”。",
         myth="把底线当保守：守底线是为了敢前进，不是不敢动。",
         src="教材：第一章第二节「质量互变」；案例：关键环节、全行业亏损、电池与数据安全。",
         quote="教材原句：量变引起质变，度是保持事物质的量的界限。",
         guard="防守：居安思危是心态，底线思维是算清那个不可逆的点。",
         notes="底线思维不是悲观，是先把最坏情况摆上桌再决定走不走。收在这里最稳。"),
]

PX, PW = 596, 308
CXI = PX + 22
CWD = PW - 44

for idx, d in enumerate(rows7):
    header(d["name"], f'{d["layer"]}　{d["span"]}')
    progress(d["active"])
    T("no", 56, 96, 60, 22, d["no"], 12, RED2, bold=True)

    T("plabel", 56, 124, 40, 12, "原理", 9.5, MUTED)
    T("principle", 56, 138, 512, 42, d["principle"], 15.5, INK, bold=True, lh=1.3)
    R("hr1", 56, 186, 512, 1, "EADCC6")

    T("asklabel", 56, 196, 40, 12, "问", 9.5, MUTED)
    T("ask", 56, 208, 512, 46, d["ask"], 15, RED, lh=1.35)
    R("hr2", 56, 256, 512, 1, "EADCC6")

    T("clabel", 56, 266, 40, 12, "判据", 9.5, MUTED)
    T("criterion", 56, 278, 512, 40, d["criterion"], 12, SUB, lh=1.5)

    T("mlabel", 56, 330, 120, 12, "常见误读", 9, MUTED)
    T("myth", 56, 344, 512, 34, d["myth"], 10.5, "8A7259", lh=1.4)

    # 右侧机制链
    R("panel", PX, 96, PW, 320, CARD, BORDER, shape="roundRect")
    T("chaintitle", CXI, 110, CWD, 16, "机制链：为什么必然如此", 9.5, MUTED)
    for k, node in enumerate(d["chain"]):
        y = 136 + k * 74
        fill = SOFT if k == 0 else CARD
        R(f"nd{k}", CXI, y, CWD, 52, fill, BORDER, shape="roundRect")
        T(f"ndt{k}", CXI, y + 15, CWD, 22, node, 11.5, INK, bold=(k == 2), align="center")
        if k < 2:
            R(f"cn{k}", CXI + CWD / 2 - 1, y + 52, 2, 22, RULE)
    T("chainroot", CXI, 368, CWD, 34, "机制不是同义反复：前一步必须是后一步的原因。", 8.5, MUTED, align="center", lh=1.4)

    footer(f"{idx + 5:02d}", d["src"])
    page(f"{idx + 5:02d}.page", "bg-page.png",
         f"{d['notes']}　{d['quote']}　{d['guard']}")

# ================================================================ P12 三个判断
header("三个判断", "6:05 – 6:40")
judg = [
    ("01", "趋势", "这是产业升级的必经关口，不是终点。", "回扣第一个数字：产量还在涨。"),
    ("02", "风险", "真正的风险不在关税，在利润与技术代差。", "回扣第三个数字：35.3% 只是症状。"),
    ("03", "抓手", "短期靠规则应诉，长期靠创新与系统配套。", "机器四层，每一层都要有动作。"),
]
for i, (no, name, line, why) in enumerate(judg):
    y = 104 + i * 112
    T(f"jn{i}", 56, y + 6, 60, 26, no, 15, RED2, bold=True)
    T(f"jt{i}", 116, y, 140, 30, name, 20, RED, bold=True)
    T(f"jl{i}", 116, y + 32, 660, 22, line, 13.5, INK)
    T(f"jw{i}", 116, y + 58, 660, 18, why, 10, MUTED)
    if i < 2:
        R(f"jr{i}", 56, y + 92, 848, 1, "EADCC6")
footer("12", "")
page("12.page", "bg-page.png",
     "三个判断一句话一个，中间留半拍。落点：同一件事，看热闹的人得到情绪，看结构的人得到判断。")

# ================================================================ P13 收束
T("l1", 56, 132, 848, 20, "世界观　→　方法论　→　思维能力", 13, MUTED, align="center")
T("big1", 56, 174, 848, 54, "机器转起来，", 34, RED, bold=True, align="center")
T("big2", 56, 222, 848, 54, "才叫思维能力。", 34, RED, bold=True, align="center")
R("cl", 400, 296, 160, 2, GOLD)
T("l2", 120, 318, 720, 28, "七个不是七选一，也不是七张并列的清单——", 12.5, SUB, align="center")
T("l3", 120, 346, 720, 28, "是一台有依赖关系的机器。", 12.5, SUB, align="center")
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
header("附录：七维 × 原理 × 判据 × 误读", "被追问时翻回")
for name, x, w in [("思维", 68, 70), ("原理锚点", 150, 268), ("可迁移判据", 430, 250), ("常见误读", 694, 210)]:
    T(f"h_{name}", x, 96, w, 14, name, 9, MUTED)
R("hrule", 56, 114, 848, 1, GOLD)
table = [
    ("辩证", "对立统一；两点论与重点论", "两面是否互为存在条件", "把“有利有弊”当分析"),
    ("历史", "社会存在决定社会意识", "周期波动还是范式转移", "把时间线当规律"),
    ("系统", "联系的普遍性；整体部分", "成本最终落在谁身上", "把“全面”当系统"),
    ("战略", "主要矛盾定主攻；规律与能动", "敢放弃什么", "把“看得远”当战略"),
    ("创新", "辩证否定＝扬弃", "否定的是路线还是功能", "把“改良”当创新"),
    ("法治", "上层建筑反作用于经济基础", "改的是成本还是资格", "把守法当法治思维"),
    ("底线", "质量互变；可能性与现实性", "哪一步不可逆", "把底线当保守"),
]
for i, (a, b, c, dd) in enumerate(table):
    y = 122 + i * 48
    if i % 2 == 0:
        R(f"zr{i}", 56, y, 848, 44, "FBF1E0")
    T(f"za{i}", 68, y + 12, 78, 20, a, 12, RED, bold=True)
    T(f"zb{i}", 150, y + 13, 276, 20, b, 9.5, INK)
    T(f"zc{i}", 430, y + 13, 256, 20, c, 9.5, SUB)
    T(f"zd{i}", 694, y + 13, 210, 20, dd, 9.5, "8A7259")
footer("15", "所有条目对应 2023 年版教材章节；口播时不报章节号，只说原理。")
page("15.page", "bg-page.png", "附录不计时。被追问“你凭什么这么判”时翻回来，指给对方看。")

lines = ["version: v2", "title: 马原口试·七个思维一台机器", "size: [960, 540]", "pages:"]
for i in range(1, 16):
    lines.append(f"  - pages/{i:02d}.page")
with open(os.path.join(ROOT, "deck.pptd"), "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")
print("pages written:", len(os.listdir(PAGES)))
