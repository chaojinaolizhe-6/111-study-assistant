import glob, os, struct, subprocess
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
AES_KEY=b"893b57bf6f96b718"; XOR=0xA9
FF=r"C:\Program Files (x86)\ACLOS\Cross\recorder-release\ffmpeg.exe"
def dec(dat):
    if dat[:6]==b"\x07\x08\x56\x32\x08\x07":
        aes_size, xor_size = struct.unpack_from("<LL", dat, 6)
        blk = aes_size + (16 - aes_size%16 if aes_size%16 else 16)
        pt=Cipher(algorithms.AES(AES_KEY),modes.ECB()).decryptor().update(dat[15:15+blk])
        pad=pt[-1]
        if 1<=pad<=16 and all(b==pad for b in pt[-pad:]): pt=pt[:-pad]
        return pt+bytes(b^XOR for b in dat[15+blk:])
    return dat
def conv(src, tag):
    d=dec(open(src,"rb").read())
    i=d.find(b"\x00\x00\x00\x01\x40\x01")
    if i<0: i=d.find(b"\x00\x00\x00\x01")
    h=r"D:\aaa_D_usual\DSH\111学习助手\tmp\partyclass-20261103\%s.hevc"%tag
    open(h,"wb").write(d[i:])
    o=r"D:\aaa_D_usual\DSH\111学习助手\tmp\partyclass-20261103\%s.jpg"%tag
    r=subprocess.run([FF,"-v","error","-y","-f","hevc","-i",h,"-frames:v","1","-c:v","mjpeg","-q:v","2","-update","1",o],capture_output=True,text=True)
    print(tag, os.path.getsize(o) if os.path.exists(o) else 0, r.stderr.strip()[:80])
base=r"D:\aaa..D盘常用文件夹\xwechat_files\wxid_4g9cekhsy71c22_9d64"
conv(base+r"\cache\2026-10\Message\250ea1e712b1441663fd47be6fc3c833\Bubble\38b2ed83698f828714578f0b74145789_b.dat","bubble_38b2")
conv(base+r"\msg\attach\250ea1e712b1441663fd47be6fc3c833\2026-10\Img\5bcb153f7cc8fc39132f4ea8d055c101_t.dat","thumb_5bcb")
