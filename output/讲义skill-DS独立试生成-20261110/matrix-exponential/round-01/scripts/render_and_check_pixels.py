import fitz, sys, pathlib
import numpy as np
from PIL import Image
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
pdf=pathlib.Path(r"matrix-exponential/round-01/handout.pdf")
out=pathlib.Path(r"matrix-exponential/round-01/renders")
doc=fitz.open(pdf)
fails=[]
for i,page in enumerate(doc):
    pix=page.get_pixmap(dpi=120)
    png=out/f"handout-p{i+1:02d}.png"
    pix.save(png)
    im=Image.open(png).convert("L")
    a=np.asarray(im)
    ink=a<245
    frac=ink.mean()
    ys,xs=np.where(ink)
    if len(xs)==0:
        fails.append(f"p{i+1} 空白渲染"); print(f"p{i+1}: BLANK"); continue
    x0,x1,y0,y1=xs.min(),xs.max(),ys.min(),ys.max()
    h,w=a.shape
    border=ink[:6,:].any() or ink[-6:,:].any() or ink[:,:6].any() or ink[:,-6:].any()
    print(f"p{i+1}: ink={frac*100:.2f}% bbox=({x0},{y0})-({x1},{y1}) page={w}x{h} border={border}")
    if frac<0.005: fails.append(f"p{i+1} 墨迹过少 {frac*100:.2f}%")
    if border: fails.append(f"p{i+1} 墨迹触及页面边缘（可能裁切）")
print(f"\n渲染页数 {doc.page_count}, 像素检查失败 {len(fails)}")
if fails:
    print("\n".join(fails)); sys.exit(1)
print("PIXEL CHECKS PASSED")
