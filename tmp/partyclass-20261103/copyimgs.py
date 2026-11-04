import os, shutil
src=r"D:\aaa_D_usual\DSH\111学习助手\tmp\partyclass-20261103\final"
dst=r"D:\aaa_D_usual\DSH\111学习助手\入党\党课现场照片-20261031"
os.makedirs(dst, exist_ok=True)
mapping={}
for line in open(r"D:\aaa_D_usual\DSH\111学习助手\tmp\partyclass-20261103\image_order.txt",encoding="utf-8"):
    parts=line.split()
    if len(parts)<4: continue
    idx,t,md5,name=parts[0],parts[1],parts[2],parts[3]
    if name.endswith(".jpg"):
        mapping[name]= "%s_%s.jpg" % (idx, t.replace(":",""))
for f,new in mapping.items():
    shutil.copyfile(os.path.join(src,f), os.path.join(dst,new))
print(len(mapping), "copied")
for n in sorted(os.listdir(dst)): print(n)
