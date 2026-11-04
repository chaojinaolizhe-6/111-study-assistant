import os, shutil, glob
src=r"D:\aaa_D_usual\DSH\111学习助手\tmp\partyclass-20261103\final"
dst=r"D:\aaa_D_usual\DSH\111学习助手\入党\党课现场照片-20261031"
os.makedirs(dst, exist_ok=True)
files={os.path.basename(p)[:8]: p for p in glob.glob(os.path.join(src,"*.jpg"))}
order = r"D:\aaa_D_usual\DSH\111学习助手\tmp\partyclass-20261103\image_order.txt"
n=0
for line in open(order,encoding="utf-8"):
    parts=line.split()
    if len(parts)<4: continue
    idx,t,md5,name=parts[0],parts[1],parts[2],parts[3]
    if name.endswith(".jpg") and md5 in files:
        new = "%s_%s.jpg" % (idx, t.replace(":",""))
        shutil.copyfile(files[md5], os.path.join(dst,new))
        n+=1
print(n, "copied")
print("\n".join(sorted(os.listdir(dst))))
