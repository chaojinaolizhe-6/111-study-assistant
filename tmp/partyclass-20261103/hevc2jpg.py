import glob, os, subprocess, sys
ff = r"C:\Program Files (x86)\ACLOS\Cross\recorder-release\ffmpeg.exe"
src = r"D:\aaa_D_usual\DSH\111学习助手\tmp\partyclass-20261103\images"
dst = r"D:\aaa_D_usual\DSH\111学习助手\tmp\partyclass-20261103\jpg"
os.makedirs(dst, exist_ok=True)
for f in sorted(glob.glob(os.path.join(src, "*.bin"))):
    data = open(f, "rb").read()
    assert data[:4] == b"wxgf"
    h = os.path.join(dst, os.path.basename(f)[:-4] + ".hevc")
    open(h, "wb").write(data[16:])
    out = os.path.join(dst, os.path.basename(f)[:-4] + ".jpg")
    r = subprocess.run([ff, "-hide_banner", "-loglevel", "error", "-y", "-f", "hevc", "-i", h,
                        "-frames:v", "1", "-c:v", "mjpeg", "-q:v", "2", "-update", "1", out],
                       capture_output=True, text=True)
    print(os.path.basename(f), r.returncode, os.path.getsize(out) if os.path.exists(out) else 0, r.stderr.strip()[:120])
