import struct
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
AES=b"893b57bf6f96b718"
def dec(p, xor=0xA9):
    d=open(p,"rb").read()
    a,x=struct.unpack_from("<LL",d,6)
    blk=a+(16-a%16 if a%16 else 16)
    pt=Cipher(algorithms.AES(AES),modes.ECB()).decryptor().update(d[15:15+blk])
    pad=pt[-1]
    if 1<=pad<=16 and all(b==pad for b in pt[-pad:]): pt=pt[:-pad]
    return pt+bytes(b^xor for b in d[15+blk:])
p=r"D:\aaa..D盘常用文件夹\xwechat_files\wxid_4g9cekhsy71c22_9d64\msg\attach\250ea1e712b1441663fd47be6fc3c833\2026-10\Img\5bcb153f7cc8fc39132f4ea8d055c101_t.dat"
pt=dec(p)
print(len(pt), pt[:32].hex())
for k in range(256):
    t=bytes(b^k for b in pt[:32])
    if t[:3]==b"\xff\xd8\xff": print("jpeg with key",hex(k)); break
print(pt[:64])
