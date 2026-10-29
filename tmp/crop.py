from PIL import Image
src = r"C:\Users\M\AppData\Roaming\dsh-desktop\harness\attachments\v1\objects\e6\e65ecea419e78a7d6b27331048e0d90a0fc31c91dbb08161a0a0520fd3492287"
im = Image.open(src)
print(im.size)
w, h = im.size
# right column with equations, upper half and lower half
im.crop((int(w*0.55), int(h*0.05), w, int(h*0.30))).resize((int(w*0.45*1.6), int(h*0.25*1.6))).save(r"tmp\crop_eq_top.png")
im.crop((int(w*0.55), int(h*0.42), w, int(h*0.92))).resize((int(w*0.45*1.5), int(h*0.50*1.5))).save(r"tmp\crop_eq_bottom.png")
print("ok")
