# -*- coding: utf-8 -*-
"""生成《党课心得体会怎么审》PDF 用 DOCX。"""
import os

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from docx.shared import Cm, Pt, RGBColor

OUT = r"D:\aaa_D_usual\DSH\111学习助手\入党\党课心得体会-审稿清单-20261105.docx"

doc = Document()
sec = doc.sections[0]
sec.page_width, sec.page_height = Cm(21.0), Cm(29.7)
sec.top_margin, sec.bottom_margin = Cm(2.2), Cm(2.0)
sec.left_margin, sec.right_margin = Cm(2.4), Cm(2.4)

st = doc.styles["Normal"]
st.font.name = "Times New Roman"
st.font.size = Pt(10.5)
st.element.rPr.rFonts.set(qn("w:eastAsia"), "宋体")


def rf(run, ea, size, bold=False, color=None):
    run.font.name = "Times New Roman"
    run.font.size = Pt(size)
    run.bold = bold
    if color:
        run.font.color.rgb = RGBColor(*color)
    rpr = run._element.get_or_add_rPr()
    fonts = rpr.find(qn("w:rFonts"))
    if fonts is None:
        fonts = rpr.makeelement(qn("w:rFonts"), {})
        rpr.append(fonts)
    fonts.set(qn("w:ascii"), "Times New Roman")
    fonts.set(qn("w:hAnsi"), "Times New Roman")
    fonts.set(qn("w:eastAsia"), ea)


def p(text, ea="宋体", size=10.5, bold=False, align=WD_ALIGN_PARAGRAPH.JUSTIFY,
      ls=1.4, sb=0, sa=3, indent=False, color=None):
    par = doc.add_paragraph()
    par.alignment = align
    par.paragraph_format.line_spacing = ls
    par.paragraph_format.space_before = Pt(sb)
    par.paragraph_format.space_after = Pt(sa)
    if indent:
        par.paragraph_format.first_line_indent = Pt(21)
    if ea == "黑体" and size >= 14:
        par.paragraph_format.keep_with_next = True
    rf(par.add_run(text), ea, size, bold, color)
    return par


def shade(cell, hexcolor):
    tcpr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hexcolor)
    tcpr.append(shd)


def table(headers, rows, widths, header_fill="8B1E1E", fs=9):
    t = doc.add_table(rows=1, cols=len(headers))
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False
    for i, h in enumerate(headers):
        c = t.rows[0].cells[i]
        c.text = ""
        par = c.paragraphs[0]
        par.paragraph_format.space_after = Pt(1)
        rf(par.add_run(h), "黑体", fs, True, (255, 255, 255))
        shade(c, header_fill)
    for row in rows:
        cells = t.add_row().cells
        for i, v in enumerate(row):
            cells[i].text = ""
            par = cells[i].paragraphs[0]
            par.paragraph_format.space_after = Pt(1)
            par.paragraph_format.line_spacing = 1.15
            rf(par.add_run(v), "宋体", fs)
    for i, w in enumerate(widths):
        t.columns[i].width = w
    trpr = t.rows[0]._tr.get_or_add_trPr()
    th = OxmlElement("w:tblHeader")
    th.set(qn("w:val"), "true")
    trpr.append(th)
    for row in t.rows:
        for i, w in enumerate(widths):
            row.cells[i].width = w
    p("", size=4, sa=0)
    return t


# ---------------- 封面区 ----------------
p("党课心得体会怎么审", "黑体", 22, True, WD_ALIGN_PARAGRAPH.CENTER, sa=4)
p("给审稿人的一份可执行清单 ｜ 2026-11-05 ｜ 配套：第36期入党积极分子培训",
  "楷体", 10, False, WD_ALIGN_PARAGRAPH.CENTER, sa=14, color=(0x66, 0x66, 0x66))

p("一句话：先看真假，再看对错，最后才看文采。提法错、事实错、换个人签名也能用——这三种，"
  "写得再漂亮都要退回。", "宋体", 10.5, False, indent=True, sa=8)

# ---------------- 一 ----------------
p("一、审什么：四个维度", "黑体", 14, True, WD_ALIGN_PARAGRAPH.LEFT, sb=6, sa=4)
table(
    ["维度", "具体看什么", "不合格的样子", "性质"],
    [["政治性", "提法、会议名称、表述顺序", "“被确立为积极分子”“从严治党”“建国以来”", "硬伤"],
     ["真实性", "有没有编造事迹、身份、数据", "写了本人没参加的活动、没担任的职务", "硬伤"],
     ["针对性", "有没有只有到场者才写得出的细节", "通篇道理，抽掉名字谁都能用", "硬伤"],
     ["规范性", "字数、结构、格式、落款", "四块缺一块、字数不够、字体行距乱", "硬伤/建议"]],
    [Cm(2.2), Cm(6.4), Cm(7.4), Cm(2.6)])

# ---------------- 二 ----------------
p("二、五分钟快审：顺序不要反", "黑体", 14, True, WD_ALIGN_PARAGRAPH.LEFT, sb=6, sa=4)
p("先做排除法。五分钟能排掉八成问题，剩下的才值得细读。", indent=True, sa=4)
table(
    ["#", "动作", "看什么", "用时"],
    [["1", "看落款", "姓名、学院、学号、日期是否齐全；日期是否在截止前", "30 秒"],
     ["2", "扫提法", "对照《党的常用名词规范表》的 20 条易错，逐条比", "1 分钟"],
     ["3", "找细节", "能不能挑出三个具体名词：人名、日期、原话、教室号", "1 分钟"],
     ["4", "换人测试", "把作者名字换成别人，文章还成立吗？成立＝太虚", "1 分钟"],
     ["5", "查重复", "连续 13 字以上与公开范文一致、又没加引号的，标出来", "1 分钟"]],
    [Cm(1.0), Cm(2.6), Cm(11.0), Cm(2.2)])

# ---------------- 三 ----------------
p("三、硬伤清单（A 类：改完才能交）", "黑体", 14, True, WD_ALIGN_PARAGRAPH.LEFT, sb=6, sa=4)
table(
    ["编号", "检查项", "典型错误", "怎么改"],
    [["A1", "提法错", "“被确立为入党积极分子”“政治占位”“从严治党”“建国以来”", "按规范表替换；“确定”不是“确立”"],
     ["A2", "事实错", "时间、人名、亲属关系、引文、流程顺序有出入", "回到原始材料逐字对，不确定就删"],
     ["A3", "身份错", "写了本人没有的职务、活动、获奖、数据", "整段删除，不要换成别的身份"],
     ["A4", "结构缺", "理论、历史、程序、行动四块少一块", "补齐最短的那块，宁短勿凑"],
     ["A5", "字数", "少于 1900 或多于 2300（按 Word 字符数）", "删空话或补一个具体细节"],
     ["A6", "格式", "标题字体不对、行距不是 1.5、落款没右对齐", "按模板统一，导出 PDF 再看一遍"]],
    [Cm(1.4), Cm(2.8), Cm(8.2), Cm(6.2)])

# ---------------- 四 ----------------
p("四、建议清单（B 类：能改则改）", "黑体", 14, True, WD_ALIGN_PARAGRAPH.LEFT, sb=6, sa=4)
table(
    ["编号", "症状", "判据", "处理"],
    [["B1", "空转句", "“深刻认识到”“备受鼓舞”“精神洗礼”出现 3 处以上", "换成一件具体的事"],
     ["B2", "长句", "平均句长超过 45 字，或单句超过 90 字", "一句只放一件事"],
     ["B3", "堆词", "四字短语连用 6 个以上，读不出主语", "删一半，留一半"],
     ["B4", "结尾空", "只有“努力”“坚定”，没有可查的事", "写成“做什么、什么时候、凭什么叫人查”"],
     ["B5", "引文乱", "一次引超过一句，或没写是谁说的", "压到一句以内，注明出处"]],
    [Cm(1.4), Cm(2.6), Cm(8.6), Cm(6.0)])

# ---------------- 五 ----------------
p("五、这篇稿子的专属核对表（拿原件逐行对）", "黑体", 14, True, WD_ALIGN_PARAGRAPH.LEFT, sa=4)
p("下表是我核过的结果，审稿时照着复算一遍即可。对不上的，按 A2 处理。", indent=True, sa=4)
table(
    ["项目", "稿子里写的", "依据", "结论"],
    [["教室与场次", "综合教学一号楼 259 教室，五场报告＋开班仪式", "培训日程（259＝材料、建艺、中白）", "一致"],
     ["张灿 8:20", "中国式现代化；“现代化不等于西方化”", "现场幻灯片与笔记", "一致"],
     ["易耕 9:30", "三封复信：周辅仁—谭秀德；周玉麟—周芝麟；王基永—龙亦飞", "“02 不背原则，尽力帮助”幻灯片", "一致"],
     ["王基永引文", "“须与全国同类情形者同样办理……”55 字", "幻灯片原文", "逐字一致"],
     ["崔世彤 10:40", "1935.10.19 吴起镇；1937.1.13 进驻延安；1948.3.23 东渡黄河", "延安精神时间轴页", "一致"],
     ["黄克功案", "1937.10.10 致信雷经天", "“反贪污斗争”页（只写“作出批示”）", "史实无误，属推断"],
     ["徐迎华 13:30", "“严格把好政治标准这个首要关口”；“被确定为”", "“正确使用党言党语”对照表", "一致"],
     ["屈宏 14:40", "“半条被子”“一袋干粮”；“蓝图已绘就，奋进正当时”", "长征课件结课页", "一致"],
     ["本人信息", "2026-05-20 确定为积极分子；武恒、战兴媛", "入党介绍人分配表", "一致"],
     ["本人经历", "物理相关专业；读过《实践论》《论持久战》", "本人思想汇报", "一致"],
     ["视频学时", "两门必修、共 4 学时，已完成", "数字党校系统进度", "本人确认已看完"]],
    [Cm(3.0), Cm(8.4), Cm(5.6), Cm(2.0)], fs=8.5)

# ---------------- 六 ----------------
p("六、三个一票否决的测试", "黑体", 14, True, WD_ALIGN_PARAGRAPH.LEFT, sb=6, sa=4)
p("1. 换人测试。把署名换掉，文章仍然成立，说明写的是“通用感想”而不是“他的感想”。"
  "高校的评阅办法里写得明确：重点看是否结合个人实际、是否坦率交心。", indent=True, sa=3)
p("2. 三问测试。让他口头回答：这次课你学到哪一个具体观点？哪件事让你改了原来的看法？"
  "你身上哪个不足准备怎么改？三问答不上来，文章大概率不是他写的。", indent=True, sa=3)
p("3. 复述测试。随机指一段，让他讲讲这段背后的事。讲得出细节，是真的；只会重复原文，是拼的。",
  indent=True, sa=6)

# ---------------- 七 ----------------
p("七、查重与提交", "黑体", 14, True, WD_ALIGN_PARAGRAPH.LEFT, sb=6, sa=4)
table(
    ["事项", "做法"],
    [["查重 3 次怎么用", "初稿 1 次看标红；改后 1 次确认；终稿留 1 次，不要一次用完"],
     ["直引的尺度", "直接引用不超过全文 3%，且必须加引号、写明谁说的"],
     ["上传前 5 项", "字数达标／落款齐全／字体行距对／导出 PDF 预览无乱码／文件名规范"],
     ["提交之后", "把“提交成功”页面截图存档，学分核对时要用"]],
    [Cm(4.0), Cm(14.4)])

# ---------------- 八 ----------------
p("八、依据来源", "黑体", 14, True, WD_ALIGN_PARAGRAPH.LEFT, sb=6, sa=4)
p("· 《中国共产党发展党员工作细则》（2014，中办印发）——发展党员五个阶段、培养考察、预备期与党龄口径。",
  size=9, sa=1)
p("· 《中国共产党支部工作条例（试行）》——“三会一课”、组织生活会、民主评议党员的频次与要求。",
  size=9, sa=1)
p("· 党的二十届五中全会公报（2026-10-29）——习近平党建思想等最新提法。", size=9, sa=1)
p("· 江西农业大学计算机与信息工程学院《大学生入党积极分子思想汇报评阅办法（试行）》（2024）——"
  "评阅重点：是否结合个人实际、是否坦率交心。", size=9, sa=1)
p("· 中国大学生在线《同学们，思想汇报别网上照抄了！》（2026-06-27）——抄袭拼凑、内容雷同、空洞无物、"
  "字数敷衍、时间错乱五类常见问题，及“换个人也能用就是空”的判据。", size=9, sa=1)
p("· 包头市司法局转载《这些日常公文校核错情，你发现了吗？》（2026-07-03）——政治性差错的典型形态："
  "提法滞后（如“四史”应为“五史”）、表述越界。", size=9, sa=6)

p("本清单与《党的常用名词规范表》配套使用；规范表在 入党\\党的名词规范\\ 目录下，"
  "AI 引用版为其中的 AI-引用规则.md。", "楷体", 9, False, WD_ALIGN_PARAGRAPH.LEFT, sa=0,
  color=(0x66, 0x66, 0x66))

doc.save(OUT)
print("saved", OUT)


