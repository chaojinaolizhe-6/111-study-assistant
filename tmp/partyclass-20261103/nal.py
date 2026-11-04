import re, subprocess, os
p = r"D:\aaa..D盘常用文件夹\xwechat_files\wxid_4g9cekhsy71c22_9d64\cache\2026-10\Message\250ea1e712b1441663fd47be6fc3c833\ImageTemp\28_1793426482_mid_temp_convert"
d = open(p,"rb").read()
print("len", len(d), "head", d[:20].hex())
starts = [m.start() for m in re.finditer(b"\x00\x00\x00\x01", d)]
print("nal count", len(starts), "first", starts[:10])
for i, s in enumerate(starts[:12]):
    e = starts[i+1] if i+1 < len(starts) else len(d)
    hdr = d[s+4:s+6]
    typ = (hdr[0] >> 1) & 0x3F
    print(" nal", i, "off", s, "len", e-s, "type", typ)
ff = r"C:\Program Files (x86)\ACLOS\Cross\recorder-release\ffmpeg.exe"
out = r"D:\aaa_D_usual\DSH\111学习助手\tmp\partyclass-20261103\imgtemp.jpg"
r = subprocess.run([ff,"-v","error","-y","-f","hevc","-i",p,"-frames:v","1","-c:v","mjpeg","-q:v","2","-update","1",out],capture_output=True,text=True)
print("decode rc", r.returncode, r.stderr[:300])
print("jpg size", os.path.getsize(out) if os.path.exists(out) else None)
