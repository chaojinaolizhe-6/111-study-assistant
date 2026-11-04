import struct, glob, os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from PIL import Image
AES=b"893b57bf6f96b718"
src=r"D:\aaa..D盘常用文件夹\xwechat_files\wxid_4g9cekhsy71c22_9d64\msg\attach\250ea1e712b1441663fd47be6fc3c833\2026-10\Img"
dst=r"D:\aaa_D_usual\DSH\111学习助手\tmp\partyclass-20261103\thumbs"
os.makedirs(dst, exist_ok=True)
for p in sorted(glob.glob(os.path.join(src,"*_t.dat"))):
    d=open(p,"rb").read()
    a,x=struct.unpack_from("<LL",d,6)
    blk=a+(16-a%16 if a%16 else 16)
    pt=Cipher(algorithms.AES(AES),modes.ECB()).decryptor().update(d[15:15+blk])
    pad=pt[-1]
    if 1<=pad<=16 and all(b==pad for b in pt[-pad:]): pt=pt[:-pad]
    body=pt+d[15+blk:]
    name=os.path.basename(p)[:-6]
    out=os.path.join(dst,name+".jpg")
    i=body.find(b"\xff\xd8\xff")
    open(out,"wb").write(body[i:])
    try:
        w,h=Image.open(out).size
    except Exception as e:
        w=h=0
    print(name[:8], len(body), w, h)
