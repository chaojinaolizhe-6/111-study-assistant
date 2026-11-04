from PIL import Image, ImageDraw
import os
src = r"D:\aaa_D_usual\DSH\111学习助手\tmp\partyclass-20261103\jpg"
order = [l.split() for l in open(r"D:\aaa_D_usual\DSH\111学习助手\tmp\partyclass-20261103\image_order.txt", encoding="utf-8") if l.strip()]
files = []
for parts in order:
    idx, t, md5, name = parts[0], parts[1], parts[2], parts[3]
    if name.endswith(".jpg"):
        files.append((idx, t, os.path.join(src, name)))
print("have", len(files))
CW, CH = 360, 640
per = 6
for page in range(0, len(files), per):
    chunk = files[page:page+per]
    cols = 3
    rows = (len(chunk) + cols - 1)//cols
    sheet = Image.new("RGB", (cols*CW, rows*(CH+26)), "white")
    d = ImageDraw.Draw(sheet)
    for i, (idx, t, p) in enumerate(chunk):
        im = Image.open(p).convert("RGB")
        im.thumbnail((CW, CH))
        x = (i % cols)*CW
        y = (i//cols)*(CH+26)
        sheet.paste(im, (x + (CW-im.width)//2, y+26))
        d.text((x+6, y+6), "#%s %s" % (idx, t), fill="black")
    out = r"D:\aaa_D_usual\DSH\111学习助手\tmp\partyclass-20261103\sheet_%d.jpg" % (page//per+1)
    sheet.save(out, quality=88)
    print(out, sheet.size)
