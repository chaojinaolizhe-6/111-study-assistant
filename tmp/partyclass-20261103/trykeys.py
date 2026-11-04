import struct, subprocess, os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
FF1 = r"C:\Program Files (x86)\ACLOS\Cross\recorder-release\ffmpeg.exe"
FF2 = r"D:\Program Files\优酷转换器\ffmpeg.exe"
AES_KEY = b"893b57bf6f96b718"
dat = open(r"D:\aaa..D盘常用文件夹\xwechat_files\wxid_4g9cekhsy71c22_9d64\msg\attach\250ea1e712b1441663fd47be6fc3c833\2026-10\Img\24d9680778e11cf4218a87c1a5048f3d.dat","rb").read()
aes_size, xor_size = struct.unpack_from("<LL", dat, 6)
blk = 1040
pt = Cipher(algorithms.AES(AES_KEY), modes.ECB()).decryptor().update(dat[15:15+blk])
pad = pt[-1]
if 1 <= pad <= 16 and all(b==pad for b in pt[-pad:]): pt = pt[:-pad]
tail = dat[15+blk:]
outdir = r"D:\aaa_D_usual\DSH\111学习助手\tmp\partyclass-20261103\keys"
os.makedirs(outdir, exist_ok=True)
for key in (0x00,0x88,0x4C,0xFF,0x5A,0xC3):
    body = pt + bytes(b^key for b in tail)
    start = body.find(b"\x00\x00\x00\x01")
    p = os.path.join(outdir, "k%02X.hevc" % key)
    open(p,"wb").write(body[start:])
    for tag,FF in (("a",FF1),):
        o = os.path.join(outdir, "k%02X.jpg" % key)
        r = subprocess.run([FF,"-v","error","-y","-f","hevc","-i",p,"-frames:v","1","-c:v","mjpeg","-q:v","2","-update","1",o],capture_output=True,text=True)
        print(tag, hex(key), r.returncode, r.stderr.strip()[:150])
