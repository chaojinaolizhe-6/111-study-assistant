import fitz
for name in ["第三章 波动光学概念和描述.pdf", "第4章光波在界面的反射和折射规律.pdf"]:
    p = r"subjects\02-光学\课件\\" + name
    d = fitz.open(p)
    n = sum(1 for pg in d if len(pg.get_text("text").strip()) > 20)
    print(name, "pages", d.page_count, "with text", n)
